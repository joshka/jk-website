#!/usr/bin/env python3
"""Copy complete, reviewed manual evidence into permanent website assets."""

import argparse
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import re
import shutil
import subprocess
import tempfile

SITE = Path(__file__).resolve().parent.parent
IDENTIFIER = re.compile(r"[a-z0-9][a-z0-9-]{0,39}")
CHECKSUM = re.compile(r"[0-9a-f]{64}")


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def relative_path(value):
    """Accept canonical relative artifact paths, including nested diagnostics and sources."""
    if not isinstance(value, str) or not value or "\\" in value or "\0" in value:
        raise ValueError(f"Invalid evidence path: {value!r}")
    path = PurePosixPath(value)
    if (
        path.is_absolute() or ".." in path.parts or ":" in value
        or str(path) != value or value == "."
    ):
        raise ValueError(f"Evidence path must stay inside its scenario: {value!r}")
    return path


def evidence_file(directory, name):
    """Reject symlinks and traversal even when an evidence manifest has been modified."""
    relative = relative_path(name)
    path = directory.resolve()
    for part in relative.parts:
        path = path / part
        if path.is_symlink():
            raise ValueError(f"Evidence path contains a symlink: {path}")
    if not path.is_file():
        raise ValueError(f"Missing evidence file: {path}")
    return path


def available_evidence(directories, reviews):
    """Find the exact reviewed capture, regardless of run age or evidence-root ordering."""
    available = {}
    for directory in directories:
        if not directory.is_dir():
            raise ValueError(f"Evidence directory does not exist: {directory}")
        for path in sorted(directory.rglob("capture-metadata.json")):
            safe = evidence_file(directory, path.relative_to(directory).as_posix())
            metadata = json.loads(safe.read_text())
            if metadata.get("status") != "passed":
                continue
            identifier = metadata["scenario"]["id"]
            if not IDENTIFIER.fullmatch(identifier):
                raise ValueError(f"Invalid scenario identifier: {identifier!r}")
            review = reviews.get(identifier)
            if review and sha256(safe) == review.get("metadata_sha256"):
                available.setdefault(identifier, (safe.parent, metadata))
    return available


def accepted_review(review, label):
    if review.get("status") != "reviewed" or not all(
        isinstance(review.get(key), str) and review[key].strip()
        for key in ("reviewer", "reviewed_at", "summary")
    ):
        raise ValueError(f"Review is incomplete: {label}")


def validate_review(review, metadata, record):
    identifier = record["id"]
    if review.get("status") != "ready":
        raise ValueError(f"Recording is not ready for publication: {identifier}")
    if (
        review.get("metadata_sha256") != record["metadata_sha256"]
        or review.get("source_tape_sha256") != metadata["source_tape_sha256"]
    ):
        raise ValueError(f"Review belongs to different evidence: {identifier}")
    binary = metadata["provenance"]["jk"]
    if any(review.get("binary", {}).get(key) != binary.get(key) for key in ("sha256", "version")):
        raise ValueError(f"Review belongs to a different jk binary: {identifier}")
    github = metadata["provenance"].get("github", {})
    if (
        review.get("source_commit") != github.get("GITHUB_SHA")
        or review.get("pr_head_commit") != github.get("JK_PR_HEAD_SHA")
    ):
        raise ValueError(f"Review source/PR-head commit mismatch: {identifier}")
    checkpoints = {checkpoint["id"]: checkpoint for checkpoint in review.get("checkpoints", [])}
    if len(checkpoints) != len(review.get("checkpoints", [])) or set(checkpoints) != {
        checkpoint["id"] for checkpoint in record["checkpoints"]
    }:
        raise ValueError(f"Review checkpoint coverage mismatch: {identifier}")
    for checkpoint in record["checkpoints"]:
        bound = checkpoints[checkpoint["id"]]
        if (
            bound.get("png_sha256") != metadata["files"][checkpoint["png"]]["sha256"]
            or bound.get("state_sha256") != metadata["files"][checkpoint["state"]]["sha256"]
        ):
            raise ValueError(f"Review checkpoint hash mismatch: {identifier}/{checkpoint['id']}")
        accepted_review(bound.get("pixel_review", {}), f"{checkpoint['id']} pixels")
        accepted_review(bound.get("text_style_review", {}), f"{checkpoint['id']} text/styles")
    video = review.get("video_review", {})
    accepted_review(video, f"{identifier} video")
    if video.get("sha256") != metadata["files"][record["video"]]["sha256"]:
        raise ValueError(f"Video review hash mismatch: {identifier}")


def validate_recording(source, scenario, directory, metadata):
    identifier = scenario["id"]
    if not IDENTIFIER.fullmatch(identifier):
        raise ValueError(f"Invalid scenario identifier: {identifier!r}")
    tape = evidence_file(source, scenario["tape"])
    if sha256(tape) != metadata["source_tape_sha256"]:
        raise ValueError(f"Recording predates tape changes: {identifier}")
    record = metadata["scenario"]
    if record["id"] != identifier or record["tape"] != scenario["tape"]:
        raise ValueError(f"Recording scenario does not match coverage: {identifier}")
    if metadata.get("problems") or metadata.get("source_consistency", {}).get("passed") is not True:
        raise ValueError(f"Recording lacks a successful source consistency check: {identifier}")
    source_hashes = metadata["provenance"].get("sources", {})
    if not {"Cargo.toml", "Cargo.lock"}.issubset(source_hashes):
        raise ValueError(f"Recording lacks compiled-source provenance: {identifier}")
    for name, checksum in source_hashes.items():
        if name in ("Cargo.toml", "Cargo.lock") or name.startswith("crates/"):
            if sha256(evidence_file(source, name)) != checksum:
                raise ValueError(f"Recording predates compiled-source changes: {identifier}/{name}")
    files = metadata.get("files", {})
    required = {record["video"], "source.tape", "capture.tape", "fixture.json"}
    checkpoints = []
    for name in record["checkpoints"]:
        relative_path(name)
        png, state_name = f"{name}.png", f"{name}.json"
        state = json.loads(evidence_file(directory, state_name).read_text())
        if not state.get("viewport_text", "").strip() or not isinstance(state.get("styles"), list):
            raise ValueError(f"Checkpoint lacks terminal text/styles: {identifier}/{state_name}")
        required.update((png, state_name))
        checkpoints.append({"id": name, "png": png, "state": state_name, "text": state["viewport_text"]})
    logs = sorted(name for name in files if name.endswith(".log"))
    if not logs:
        raise ValueError(f"No local or CI logs recorded: {identifier}")
    assertions = sorted(name for name in files if name.endswith("-assertions.json"))
    if not assertions:
        raise ValueError(f"No repository assertions recorded: {identifier}")
    for name in assertions:
        outcome = json.loads(evidence_file(directory, name).read_text())
        if (
            outcome.get("scenario") != identifier or outcome.get("status") != "passed"
            or not outcome.get("assertions")
            or any(check.get("passed") is not True for check in outcome["assertions"])
        ):
            raise ValueError(f"Failed or incomplete outcome assertions: {identifier}/{name}")
    snapshots = metadata.get("source_snapshots", {})
    essential = {"scripts/manual-fixture.sh", "scripts/manual-assert.sh", "scripts/manual-recordings.py"}
    if not essential.issubset(snapshots):
        raise ValueError(f"Recording lacks original helper snapshots: {identifier}; rerun the scenario")
    for original, snapshot in snapshots.items():
        if not str(relative_path(original)).startswith("scripts/"):
            raise ValueError(f"Invalid source-script origin: {original}")
        if not str(relative_path(snapshot)).startswith("source-scripts/"):
            raise ValueError(f"Invalid source-script snapshot: {snapshot}")
        required.add(snapshot)
        if sha256(evidence_file(directory, snapshot)) != metadata["provenance"]["sources"][original]:
            raise ValueError(f"Original helper hash mismatch: {identifier}/{snapshot}")
    if required - files.keys():
        raise ValueError(f"Unhashed required evidence for {identifier}: {sorted(required - files.keys())}")
    artifacts = []
    for name, expected in sorted(files.items()):
        if name == "capture-metadata.json":
            raise ValueError("Capture metadata cannot include its own hash")
        path = evidence_file(directory, name)
        if (
            not CHECKSUM.fullmatch(expected.get("sha256", ""))
            or sha256(path) != expected["sha256"]
            or path.stat().st_size != expected.get("bytes")
        ):
            raise ValueError(f"Evidence hash or byte-count mismatch: {path}")
        artifacts.append({"path": name, "sha256": expected["sha256"], "bytes": expected["bytes"]})
    # Do not quietly omit logs or snapshots that arrived after metadata was finalized.
    for path in directory.rglob("*"):
        name = path.relative_to(directory).as_posix()
        if path.is_file() and (path.suffix == ".log" or name.startswith("source-scripts/")) and name not in files:
            raise ValueError(f"Unhashed log or source snapshot: {path}; finalize evidence before import")
    duration = float(subprocess.check_output([
        "ffprobe", "-v", "error", "-show_entries", "format=duration", "-of",
        "default=noprint_wrappers=1:nokey=1", str(evidence_file(directory, record["video"])),
    ], text=True).strip())
    if not math.isfinite(duration) or duration <= 0:
        raise ValueError(f"Recording has no playable duration: {identifier}")
    return {
        "id": identifier, "title": scenario["title"], "group": scenario["group"],
        "manual_slugs": scenario.get("manual_slugs", [scenario["manual_slug"]]),
        "video": record["video"], "checkpoints": checkpoints, "metadata": "capture-metadata.json",
        "metadata_sha256": sha256(evidence_file(directory, "capture-metadata.json")),
        "assertions": assertions, "logs": logs, "artifacts": artifacts, "duration": duration,
    }


def import_evidence(source, directories, review_index_path=None, version=None):
    coverage = json.loads((source / "docs/manual-coverage.json").read_text())
    audit = json.loads((source / "docs/manual-ux-audit.json").read_text())
    review_index_path = review_index_path or source / "docs/manual-evidence-index.json"
    review_index_bytes = review_index_path.read_bytes()
    review_index = json.loads(review_index_bytes)
    review_index_sha256 = hashlib.sha256(review_index_bytes).hexdigest()
    reviews = {review["id"]: review for review in review_index["scenarios"]}
    if len(reviews) != len(review_index["scenarios"]):
        raise ValueError("Accepted review index contains duplicate scenarios")
    expected = {scenario["id"] for scenario in coverage["scenarios"]}
    missing_reviews = expected - reviews.keys()
    if missing_reviews:
        raise ValueError(f"No accepted review for: {', '.join(sorted(missing_reviews))}")
    for identifier in expected:
        if not CHECKSUM.fullmatch(reviews[identifier].get("metadata_sha256", "")):
            raise ValueError(f"Accepted review lacks a valid metadata hash: {identifier}")
    available = available_evidence(directories, reviews)
    missing = expected - available.keys()
    if missing:
        raise ValueError(
            "Missing passed evidence matching accepted review metadata hash: "
            + ", ".join(sorted(missing))
        )
    if not re.fullmatch(r"[0-9A-Za-z.+-]+", coverage["source_version"]):
        raise ValueError("Invalid source version")
    if version is None:
        version = f"v{coverage['source_version']}-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ")
    elif not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", version):
        raise ValueError("Asset version must be one directory name using letters, digits, '.', '_' or '-'")
    parent = SITE / "public/assets/manual"
    version_directory = parent / version
    if version_directory.exists() or version_directory.is_symlink():
        raise ValueError(f"Asset version already exists: {version_directory}; choose a fresh version")
    validated = []
    for scenario in coverage["scenarios"]:
        directory, metadata = available[scenario["id"]]
        record = validate_recording(source, scenario, directory, metadata)
        validate_review(reviews[scenario["id"]], metadata, record)
        validated.append((directory, record))
    parent.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".import-", dir=parent))
    records = []
    try:
        (staging / "review-index.json").write_bytes(review_index_bytes)
        for directory, record in validated:
            output = staging / record["id"]
            output.mkdir()
            for artifact in record["artifacts"]:
                destination = output / artifact["path"]
                destination.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(evidence_file(directory, artifact["path"]), destination)
                if sha256(destination) != artifact["sha256"]:
                    raise ValueError(f"Evidence changed during import: {directory / artifact['path']}")
            shutil.copyfile(evidence_file(directory, record["metadata"]), output / record["metadata"])
            if sha256(output / record["metadata"]) != record["metadata_sha256"]:
                raise ValueError(f"Metadata changed during import: {directory}")
            if "accepted-review.json" in {artifact["path"] for artifact in record["artifacts"]}:
                raise ValueError("Evidence uses the reserved accepted-review.json filename")
            review_path = output / "accepted-review.json"
            review_path.write_text(json.dumps({
                "schema_version": 1,
                "source_index": f"manual/{version}/review-index.json",
                "source_index_sha256": review_index_sha256,
                "review": reviews[record["id"]],
            }, indent=2) + "\n")
            record["review"] = "accepted-review.json"
            record["artifacts"].append({
                "path": record["review"], "sha256": sha256(review_path),
                "bytes": review_path.stat().st_size,
            })
            record["path"] = f"manual/{version}/{record['id']}"
            records.append(record)
        if version_directory.exists() or version_directory.is_symlink():
            raise ValueError(f"Asset version already exists: {version_directory}; choose a fresh version")
        staging.rename(version_directory)
    except Exception:
        shutil.rmtree(staging, ignore_errors=True)
        raise
    data = SITE / "src/data"
    data.mkdir(parents=True, exist_ok=True)
    for name, value in (("manual-coverage", coverage), ("manual-ux-audit", audit),
                        ("manual-media", {"version": version, "scenarios": records})):
        temporary = data / f".{name}.json.tmp"
        temporary.write_text(json.dumps(value, indent=2) + "\n")
        temporary.replace(data / f"{name}.json")
    return version_directory, records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", required=True, type=Path, help="jk source workspace")
    parser.add_argument("--evidence", required=True, action="append", type=Path,
                        help="Local collections or downloaded CI artifacts containing the exact accepted captures")
    parser.add_argument("--review-index", type=Path,
                        help="Accepted review index; defaults to source/docs/manual-evidence-index.json")
    parser.add_argument("--version", help="Fresh asset directory name; defaults to a version plus UTC timestamp")
    args = parser.parse_args()
    destination, records = import_evidence(args.source, args.evidence, args.review_index, args.version)
    print(f"Imported {len(records)} complete recordings into {destination}")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, subprocess.SubprocessError) as error:
        raise SystemExit(f"Manual evidence import: {error}") from error
