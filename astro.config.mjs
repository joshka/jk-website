// @ts-check
import { defineConfig } from 'astro/config';

import tailwindcss from '@tailwindcss/vite';

import sitemap from '@astrojs/sitemap';

const base = '/jk';

// https://astro.build/config
export default defineConfig({
  site: 'https://www.joshka.net',
  base,

  vite: {
    plugins: [tailwindcss()],
  },

  markdown: {
    shikiConfig: {
      // Single dark theme, matching the hero code panel
      // (see src/components/home/Hero.astro).
      theme: 'catppuccin-mocha',
    },
  },

  integrations: [sitemap()],
});
