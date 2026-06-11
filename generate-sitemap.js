/**
 * generate-sitemap.js
 * Run with: node generate-sitemap.js
 * Generates sitemap.xml from the writings array in app.js
 */
const fs = require('fs');
const path = require('path');

const SITE_URL = 'https://alomoychakma.com';
const TODAY = new Date().toISOString().slice(0, 10);

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

// Static pages
urls.push({ loc: SITE_URL + '/', priority: '1.0', changefreq: 'weekly' });
urls.push({ loc: SITE_URL + '/#about', priority: '0.8', changefreq: 'monthly' });

// Category pages
const catMeta = {
  poem:  { priority: '0.9', changefreq: 'weekly' },
  rhyme: { priority: '0.9', changefreq: 'weekly' },
  story: { priority: '0.9', changefreq: 'weekly' },
  song:  { priority: '0.9', changefreq: 'weekly' },
};
categories.forEach(cat => {
  urls.push({ loc: `${SITE_URL}/#category/${cat}`, priority: catMeta[cat].priority, changefreq: catMeta[cat].changefreq });
});

// Individual article pages: #poem/1, #rhyme/2, etc.
categories.forEach(cat => {
  grouped[cat].forEach((writing, idx) => {
    urls.push({
      loc: `${SITE_URL}/#${cat}/${idx + 1}`,
      priority: '0.7',
      changefreq: 'yearly',
      lastmod: TODAY
    });
  });
});

// Generate XML
const urlsXml = urls.map(u => `  <url>
    <loc>${u.loc}</loc>
    ${u.lastmod ? `<lastmod>${u.lastmod}</lastmod>` : `<lastmod>${TODAY}</lastmod>`}
    <changefreq>${u.changefreq}</changefreq>
    <priority>${u.priority}</priority>
  </url>`).join('\n');

const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
${urlsXml}
</urlset>`;

fs.writeFileSync(path.join(__dirname, 'sitemap.xml'), xml, 'utf8');

console.log(`✅ sitemap.xml generated with ${urls.length} URLs`);
console.log(`   Static pages: 2`);
console.log(`   Category pages: ${categories.length}`);
categories.forEach(cat => {
  console.log(`   ${cat}: ${grouped[cat].length} entries`);
});
