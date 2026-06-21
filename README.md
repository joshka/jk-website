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
```

Requires Node 22.12 or newer.

## Media Assets

- Store generated screenshots, GIFs, and videos under `public/assets/`.
- Keep image and video assets Git LFS-backed.
- Do not copy these assets into the main `jk` repository.
- Regenerate the homepage workflow GIF with `betamax run tapes/homepage.tape`.
- After publishing an asset, verify the served URL returns real media bytes rather than a Git LFS
  pointer file.
