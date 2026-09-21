import type { MarkdownInstance } from 'astro';

export interface ChapterFrontmatter {
  title: string;
  description: string;
  order: number;
}

const documents = import.meta.glob<MarkdownInstance<ChapterFrontmatter>>(
  '../content/manual/*.md',
  { eager: true },
);

export const chapters = Object.entries(documents)
  .map(([path, document]) => ({
    slug: path.split('/').pop()!.replace(/\.md$/, ''),
    ...document.frontmatter,
    document,
  }))
  .sort((a, b) => a.order - b.order);

export const base = `${import.meta.env.BASE_URL.replace(/\/$/, '')}/`;
export const manualLink = (slug = '') => `${base}manual/${slug ? `${slug}/` : ''}`;
