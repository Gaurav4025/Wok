import type { MetadataRoute } from 'next';

export default function sitemap(): MetadataRoute.Sitemap {
  const base = process.env.NEXT_PUBLIC_SITE_URL || 'http://localhost:3000';

  return ['/', '/menu', '/cart', '/checkout', '/dashboard'].map((path) => ({
    url: `${base}${path}`,
    lastModified: new Date(),
    priority: path === '/' ? 1 : 0.8
  }));
}
