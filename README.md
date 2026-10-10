# jk website

This repository hosts the [`jk`](https://github.com/joshka/jk) project page and README media.

The site is deployed with GitHub Pages to:

<https://www.joshka.net/jk/>

Media assets are served from stable URLs under:

<https://www.joshka.net/jk/assets/>

## Development

```sh
pnpm install
pnpm dev
pnpm build
pnpm check:site
```

Requires Node 22.12 or newer.

## Manual

Task chapters live in `src/content/manual/`. The command reference, coverage map, and UX audit use
reviewed JSON from the companion `jk` source repository. The site supports the `/jk` production
base and the `/jk-website` pull-request build base.

During authoring, record the collection from a `jk` source workspace:

```sh
python3 scripts/manual-recordings.py run
```

For the website, download the complete CI evidence archives. They retain the exact compiled commit
and PR head used by the publication checks. Review their PNG pixels, styled terminal state, and
video pacing using the source repository's `prepare-manual-evidence.py` workflow. Save the accepted
index as `docs/manual-evidence-index.json` in that source workspace, then import from this repository:

```sh
python3 scripts/import-manual-evidence.py \
  --source ../jk/manual-audit \
  --evidence ../jk/manual-audit/target/manual-recordings/ci-RUN_ID \
  --review-index ../jk/manual-audit/docs/manual-evidence-index.json \
  --version v0.3.0-manual-20260921
pnpm build
pnpm check:site
```

The importer requires every registered scenario and its accepted review. It checks tape, binary,
checkpoint, and video hashes, then copies MP4s, PNG/terminal-state pairs, logs, assertions, original
helper scripts, and provenance into a fresh versioned asset directory.
It also updates the reference and audit data. `ffprobe` must be on `PATH`. Use repeated `--evidence`
arguments when accepted recordings span several runs. The review index selects the exact recording
by its metadata hash, regardless of argument order or recording date.

Use the same `--version` value as the source evidence builder's `--website-version` so the accepted
index and imported assets declare identical durable paths. The value must be a single directory name
using letters, digits, dots, underscores, or hyphens, starting with a letter or digit. Existing
destinations are rejected. Omit `--version` to generate a fresh name from the source version and UTC
timestamp when no path has been predeclared.

Automated repository assertions cannot judge whether a workflow is understandable. Reviews bind to
the exact recorded bytes; a changed tape or recording requires a fresh review. Keep the audit's
evidence status accurate when importing a new set of recordings.

The importer and local preview do not deploy the site. Publication remains a separate reviewed
change through the existing Pages workflow.

## Media Assets

- Store generated screenshots, GIFs, and videos under `public/assets/`.
- Keep image and video assets Git LFS-backed.
- Do not copy these assets into the main `jk` repository.
- Regenerate the homepage workflow GIF with `betamax run tapes/homepage.tape`.
- After publishing an asset, verify the served URL returns real media bytes rather than a Git LFS
  pointer file.
