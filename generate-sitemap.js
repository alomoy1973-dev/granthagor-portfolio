/**
 * generate-sitemap.js
 * Run with: node generate-sitemap.js
 * Generates sitemap.xml from the writings array in app.js
 */
const fs = require('fs');
const path = require('path');

const SITE_URL = 'https://alomoy.vercel.app';
const TODAY = new Date().toISOString().slice(0, 10);

// Read app.js and extract the writings array
const appJs = fs.readFileSync(path.join(__dirname, 'app.js'), 'utf8');

// Extract the writings array section (between "let writings = [" and the closing "];")
const startMarker = 'let writings = [';
const startIdx = appJs.indexOf(startMarker);
const endMarker = '\n];\n';
const endIdx = appJs.indexOf(endMarker, startIdx);

if (startIdx === -1 || endIdx === -1) {
  console.error('Could not find writings array in app.js');
  process.exit(1);
}

const writingsRaw = appJs.slice(startIdx + startMarker.length - 1, endIdx + 2);

// Use Function constructor to evaluate the array safely
let writings;
try {
  writings = Function('return ' + writingsRaw)();
} catch (e) {
  console.error('Failed to parse writings array:', e.message);
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
