/**
 * generate-sitemap.js
 * Run with: node generate-sitemap.js
 * Generates sitemap.xml from the writings array in app.js
 */
const fs = require('fs');
const path = require('path');

const SITE_URL = 'https://www.alomoychakma.com';
const TODAY = new Date().toISOString().slice(0, 10);
const books = [
  'ful-bareng',
  'hakkeng-hakkeng',
  'tinnomuri',
  'monpudi',
  'nauri'
];

// Read writings.json directly
let writings;
try {
  const writingsJsonRaw = fs.readFileSync(path.join(__dirname, 'writings.json'), 'utf8');
  writings = JSON.parse(writingsJsonRaw);
} catch (e) {
  console.error('Failed to read or parse writings.json:', e.message);
  process.exit(1);
}

// Group by category
const categories = ['poem', 'rhyme', 'story', 'song'];
const grouped = {};
categories.forEach(c => { grouped[c] = writings.filter(w => w.category === c); });

// Build sitemap XML
let urls = [];

// Static pages — include lastmod (built today) and priority/changefreq hints
urls.push({ loc: SITE_URL + '/', priority: '1.0', changefreq: 'weekly', lastmod: TODAY });
urls.push({ loc: SITE_URL + '/about', priority: '0.8', changefreq: 'monthly', lastmod: TODAY });
urls.push({ loc: SITE_URL + '/privacy-policy', priority: '0.3', changefreq: 'yearly', lastmod: TODAY });

// Book pages
books.forEach(slug => {
  urls.push({ loc: `${SITE_URL}/books/${slug}`, priority: '0.8', changefreq: 'monthly', lastmod: TODAY });
});

// Category pages
const catMeta = {
  poem:  { priority: '0.9', changefreq: 'weekly' },
  rhyme: { priority: '0.9', changefreq: 'weekly' },
  story: { priority: '0.9', changefreq: 'weekly' },
  song:  { priority: '0.9', changefreq: 'weekly' },
};
categories.forEach(cat => {
  urls.push({ loc: `${SITE_URL}/category/${cat}`, priority: catMeta[cat].priority, changefreq: catMeta[cat].changefreq, lastmod: TODAY });
});

// Individual article pages: /poem/1, /rhyme/2, etc.
// Omit lastmod for articles — Google ignores uniform fake dates and uses crawl date instead.
// Omit changefreq/priority for articles — Google ignores these; keeps sitemap clean.
categories.forEach(cat => {
  grouped[cat].forEach((writing, idx) => {
    urls.push({
      loc: `${SITE_URL}/${cat}/${idx + 1}`
      // No lastmod, changefreq, or priority — Google uses crawl signals for these.
    });
  });
});

// Generate XML — only include fields that exist on each URL
const urlsXml = urls.map(u => {
  let xml = `  <url>\r\n    <loc>${u.loc}</loc>`;
  if (u.lastmod) xml += `\r\n    <lastmod>${u.lastmod}</lastmod>`;
  if (u.changefreq) xml += `\r\n    <changefreq>${u.changefreq}</changefreq>`;
  if (u.priority) xml += `\r\n    <priority>${u.priority}</priority>`;
  xml += '\r\n  </url>';
  return xml;
}).join('\r\n');

const xml = `<?xml version="1.0" encoding="UTF-8"?>\r\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"\r\n        xmlns:xhtml="http://www.w3.org/1999/xhtml">\r\n${urlsXml}\r\n</urlset>`;

fs.writeFileSync(path.join(__dirname, 'sitemap.xml'), xml, 'utf8');

console.log(`✅ sitemap.xml generated with ${urls.length} URLs`);
console.log(`   Static pages: 3`);
console.log(`   Book pages: ${books.length}`);
console.log(`   Category pages: ${categories.length}`);
categories.forEach(cat => {
  console.log(`   ${cat}: ${grouped[cat].length} entries`);
});
