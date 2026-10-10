"""Verify complete local/CI imports, review binding, and safe nested evidence paths."""

import importlib.util
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock

spec = importlib.util.spec_from_file_location(
    "manual_import", Path(__file__).with_name("import-manual-evidence.py")
)
importer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(importer)


def write_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2) + "\n")


class EvidenceImport(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.source = self.root / "source"
        self.site = self.root / "website"
        self.evidence = self.root / "downloaded-artifacts"
        self.site_patch = mock.patch.object(importer, "SITE", self.site)
        self.duration_patch = mock.patch.object(importer.subprocess, "check_output", return_value="62.4\n")
        self.site_patch.start()
        self.duration_patch.start()
        self.addCleanup(self.site_patch.stop)
        self.addCleanup(self.duration_patch.stop)
        self.addCleanup(self.temporary.cleanup)

    def fixture(self, ci=True):
        scenario = {
            "id": "example", "title": "Example workflow", "group": "changes",
            "tape": "tapes/manual/example.tape", "manual_slug": "changes",
        }
        tape = self.source / scenario["tape"]
        tape.parent.mkdir(parents=True)
        tape.write_text("Output example.mp4\n")
        self.source.joinpath("Cargo.toml").write_text("# source manifest\n")
        self.source.joinpath("Cargo.lock").write_text("# source lockfile\n")
        write_json(self.source / "docs/manual-coverage.json", {
            "source_version": "0.3.0", "scenarios": [scenario],
        })
        write_json(self.source / "docs/manual-ux-audit.json", {"findings": []})
        directory = self.evidence / "manual-evidence-example"
        directory.mkdir(parents=True)
        (directory / "example.mp4").write_bytes(b"example video bytes")
        (directory / "example-view.png").write_bytes(b"example PNG bytes")
        (directory / "source.tape").write_bytes(tape.read_bytes())
        (directory / "capture.tape").write_text("# prepared tape\n")
        write_json(directory / "example-view.json", {"viewport_text": "A revision", "styles": []})
        write_json(directory / "fixture.json", {"repository": "/disposable/repo"})
        write_json(directory / "completed-assertions.json", {
            "scenario": "example", "status": "passed",
            "assertions": [{"name": "operation completed", "passed": True}],
        })
        log_names = ["action-diagnostics/tape-1.log", "action-diagnostics/bin/dependencies.log"] if ci else ["render.log"]
        for name in log_names:
            path = directory / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(f"Preserved log: {name}\n")
        snapshots = {}
        sources = {name: importer.sha256(self.source / name) for name in ("Cargo.toml", "Cargo.lock")}
        for helper in ("manual-fixture.sh", "manual-assert.sh", "manual-recordings.py"):
            name = f"source-scripts/{helper}"
            path = directory / name
            path.parent.mkdir(exist_ok=True)
            path.write_text(f"# original {helper}\n")
            snapshots[f"scripts/{helper}"] = name
            sources[f"scripts/{helper}"] = importer.sha256(path)
        metadata = {
            "status": "passed", "finished_at": "2026-09-21T00:00:00Z", "problems": [],
            "scenario": {**scenario, "video": "example.mp4", "checkpoints": ["example-view"]},
            "source_tape_sha256": importer.sha256(tape), "source_consistency": {"passed": True},
            "source_snapshots": snapshots,
            "provenance": {
                "sources": sources, "jk": {"version": "jk 0.3.0", "sha256": "a" * 64},
                "github": {"GITHUB_SHA": "compiled-merge", "JK_PR_HEAD_SHA": "pr-head"} if ci else {},
            },
            "files": {
                path.relative_to(directory).as_posix(): {
                    "sha256": importer.sha256(path), "bytes": path.stat().st_size,
                }
                for path in directory.rglob("*") if path.is_file()
            },
        }
        write_json(directory / "capture-metadata.json", metadata)
        accepted = {
            "status": "reviewed", "reviewer": "Example reviewer",
            "reviewed_at": "2026-09-21T01:00:00Z", "summary": "Reviewed actual output.", "findings": [],
        }
        review = {
            "id": "example", "status": "ready",
            "metadata_sha256": importer.sha256(directory / "capture-metadata.json"),
            "source_tape_sha256": metadata["source_tape_sha256"],
            "source_commit": "compiled-merge" if ci else None,
            "pr_head_commit": "pr-head" if ci else None, "binary": metadata["provenance"]["jk"],
            "checkpoints": [{
                "id": "example-view", "png_sha256": metadata["files"]["example-view.png"]["sha256"],
                "state_sha256": metadata["files"]["example-view.json"]["sha256"],
                "pixel_review": accepted, "text_style_review": accepted,
            }],
            "video_review": {**accepted, "sha256": metadata["files"]["example.mp4"]["sha256"]},
        }
        write_json(self.source / "docs/manual-evidence-index.json", {"schema_version": 1, "scenarios": [review]})
        return directory, metadata, review

    def test_ci_import_preserves_nested_logs_snapshots_and_review(self):
        directory, metadata, _ = self.fixture()
        destination, records = importer.import_evidence(self.source, [self.evidence])
        output = destination / "example"
        for name in metadata["files"]:
            self.assertEqual((output / name).read_bytes(), (directory / name).read_bytes())
        self.assertFalse((output / "render.log").exists())
        self.assertEqual(len(records[0]["logs"]), 2)
        self.assertTrue((output / "accepted-review.json").is_file())
        self.assertTrue((destination / "review-index.json").is_file())
        copied = json.loads((output / "capture-metadata.json").read_text())
        self.assertEqual(copied["provenance"]["github"]["GITHUB_SHA"], "compiled-merge")
        self.assertEqual(copied["provenance"]["github"]["JK_PR_HEAD_SHA"], "pr-head")

    def test_local_import_preserves_render_log(self):
        self.fixture(ci=False)
        _, records = importer.import_evidence(self.source, [self.evidence])
        self.assertEqual(records[0]["logs"], ["render.log"])

    def test_modified_nested_evidence_is_rejected_before_public_assets_change(self):
        directory, _, _ = self.fixture()
        (directory / "action-diagnostics/tape-1.log").write_text("changed after review")
        with self.assertRaisesRegex(ValueError, "hash or byte-count mismatch"):
            importer.import_evidence(self.source, [self.evidence])
        self.assertFalse((self.site / "public/assets").exists())

    def test_video_review_must_be_completed_for_exact_media(self):
        _, _, review = self.fixture()
        review["video_review"]["status"] = "pending"
        write_json(self.source / "docs/manual-evidence-index.json", {"scenarios": [review]})
        with self.assertRaisesRegex(ValueError, "Review is incomplete: example video"):
            importer.import_evidence(self.source, [self.evidence])

    def test_new_capture_cannot_reuse_old_pixel_review(self):
        _, _, review = self.fixture()
        review["checkpoints"][0]["png_sha256"] = "0" * 64
        write_json(self.source / "docs/manual-evidence-index.json", {"scenarios": [review]})
        with self.assertRaisesRegex(ValueError, "Review checkpoint hash mismatch"):
            importer.import_evidence(self.source, [self.evidence])

    def test_source_merge_and_pr_head_are_not_interchangeable(self):
        _, _, review = self.fixture()
        review["source_commit"] = review["pr_head_commit"]
        write_json(self.source / "docs/manual-evidence-index.json", {"scenarios": [review]})
        with self.assertRaisesRegex(ValueError, "source/PR-head commit mismatch"):
            importer.import_evidence(self.source, [self.evidence])

    def test_unsafe_paths_and_symlinks_are_rejected(self):
        for name in ("../escape", "/absolute", "a/../escape", "a//b", "./file", "C:\\file"):
            with self.subTest(name=name), self.assertRaises(ValueError):
                importer.relative_path(name)
        directory, _, _ = self.fixture()
        (directory / "source-scripts/linked.sh").symlink_to(self.source / "Cargo.toml")
        with self.assertRaisesRegex(ValueError, "symlink"):
            importer.evidence_file(directory, "source-scripts/linked.sh")

    def test_unhashed_late_log_cannot_be_silently_dropped(self):
        directory, _, _ = self.fixture()
        (directory / "late.log").write_text("late diagnostic")
        with self.assertRaisesRegex(ValueError, "Unhashed log or source snapshot"):
            importer.import_evidence(self.source, [self.evidence])

    def newer_capture(self, original, metadata, root):
        directory = root / "newer-example"
        shutil.copytree(original, directory)
        newer = json.loads(json.dumps(metadata))
        newer["finished_at"] = "2026-09-22T00:00:00Z"
        video = directory / "example.mp4"
        video.write_bytes(b"newer unreviewed video bytes")
        newer["files"][video.name] = {"sha256": importer.sha256(video), "bytes": video.stat().st_size}
        write_json(directory / "capture-metadata.json", newer)
        return directory

    def test_older_reviewed_capture_wins_across_evidence_roots_in_either_order(self):
        original, metadata, review = self.fixture()
        newer_root = self.root / "newer-ci-artifacts"
        self.newer_capture(original, metadata, newer_root)
        for roots in ([self.evidence, newer_root], [newer_root, self.evidence]):
            with self.subTest(roots=roots):
                destination, records = importer.import_evidence(self.source, roots)
                self.assertEqual(records[0]["metadata_sha256"], review["metadata_sha256"])
                self.assertEqual(
                    (destination / "example/example.mp4").read_bytes(),
                    (original / "example.mp4").read_bytes(),
                )

    def test_newer_capture_in_same_collection_does_not_replace_reviewed_capture(self):
        original, metadata, review = self.fixture()
        self.newer_capture(original, metadata, self.evidence)
        destination, records = importer.import_evidence(self.source, [self.evidence])
        self.assertEqual(records[0]["metadata_sha256"], review["metadata_sha256"])
        self.assertEqual(
            importer.sha256(destination / "example/capture-metadata.json"), review["metadata_sha256"]
        )

    def test_missing_accepted_capture_is_rejected_without_falling_back_to_newer_run(self):
        original, metadata, _ = self.fixture()
        newer_root = self.root / "newer-ci-artifacts"
        self.newer_capture(original, metadata, newer_root)
        with self.assertRaisesRegex(ValueError, "Missing passed evidence matching accepted review metadata hash"):
            importer.import_evidence(self.source, [newer_root])
        self.assertFalse((self.site / "public/assets").exists())

    def test_explicit_version_validates_paths_and_never_overwrites_existing_assets(self):
        self.fixture()
        for version in ("", ".", "..", "nested/version", "/absolute", "nested\\version"):
            with self.subTest(version=version), self.assertRaisesRegex(ValueError, "one directory name"):
                importer.import_evidence(self.source, [self.evidence], version=version)
        self.assertFalse((self.site / "public/assets").exists())
        version = "v0.3.0-manual-20260921"
        destination, records = importer.import_evidence(self.source, [self.evidence], version=version)
        self.assertEqual(destination.name, version)
        self.assertEqual(records[0]["path"], f"manual/{version}/example")
        accepted = json.loads((destination / "example/accepted-review.json").read_text())
        self.assertEqual(accepted["source_index"], f"manual/{version}/review-index.json")
        index = self.site / "src/data/manual-media.json"
        original_index = index.read_bytes()
        original_video = (destination / "example/example.mp4").read_bytes()
        with self.assertRaisesRegex(ValueError, "Asset version already exists"):
            importer.import_evidence(self.source, [self.evidence], version=version)
        self.assertEqual(index.read_bytes(), original_index)
        self.assertEqual((destination / "example/example.mp4").read_bytes(), original_video)
        self.assertFalse(list(destination.parent.glob(".import-*")))


if __name__ == "__main__":
    unittest.main()
