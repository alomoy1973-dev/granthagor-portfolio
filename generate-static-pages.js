const fs = require('fs');
const path = require('path');

const SITE_URL = 'https://www.alomoychakma.com';
const ROOT = __dirname;
const TODAY = new Date().toISOString().slice(0, 10);

const writings = JSON.parse(fs.readFileSync(path.join(ROOT, 'writings.json'), 'utf8'));

const categoryMeta = {
  poem: {
    bn: 'কবিতা',
    en: 'Chakma Poems',
    intro: 'আলোময় চাকমার চাঙমা ভাষার কবিতা সংগ্রহ। পার্বত্য চট্টগ্রামের জীবন, প্রকৃতি, স্মৃতি ও অনুভব এই কবিতাগুলোর প্রধান সুর।',
    description: 'Alomoy Chakma poems in the Chakma language, collected as a digital poetry archive from the Chittagong Hill Tracts.'
  },
  rhyme: {
    bn: 'ছড়া',
    en: 'Chakma Rhymes',
    intro: 'শিশু-কিশোর পাঠক ও চাঙমা ছড়ার ঐতিহ্যকে সামনে রেখে আলোময় চাকমার ছড়া সংগ্রহ।',
    description: 'Chakma rhymes and children’s verse by Alomoy Chakma, preserved in a searchable online archive.'
  },
  story: {
    bn: 'ছোটগল্প',
    en: 'Short Stories',
    intro: 'চাঙমা জীবন, পাহাড়ি সমাজ ও মানুষের অভিজ্ঞতা নিয়ে আলোময় চাকমার ছোটগল্প সংগ্রহ।',
    description: 'Short stories by Alomoy Chakma about Chakma life, culture, and the Chittagong Hill Tracts.'
  },
  song: {
    bn: 'গান',
    en: 'Chakma Songs',
    intro: 'আলোময় চাকমার গান ও গীতিকবিতার সংগ্রহ, চাঙমা ভাষার সুর ও অনুভূতির নথি।',
    description: 'Chakma songs and lyrics by Alomoy Chakma in a digital literature collection.'
  }
};

const books = [
  {
    slug: 'ful-bareng',
    name: 'ফুল বারেঙ',
    englishName: 'Ful Bareng',
    type: 'কাব্যগ্রন্থ',
    genre: 'Poetry',
    year: '2015',
    publisher: 'কল্পতরু প্রকাশনী',
    place: 'রাঙ্গামাটি',
    image: '/ful-bareng-alomoy-chakma-chakma-poetry-book.webp',
    download: 'https://drive.google.com/uc?export=download&id=15aJ-m6oz1LqUeeUq0dhGNcvgwX0KJhsV'
  },
  {
    slug: 'hakkeng-hakkeng',
    name: 'হক্কেং হক্কেং',
    englishName: 'Hakkeng Hakkeng',
    type: 'ছড়াগ্রন্থ',
    genre: "Children's Rhymes",
    year: '2017',
    publisher: 'পরিবার প্রকাশনী',
    place: 'ঢাকা',
    image: '/hakkeng-hakkeng-alomoy-chakma-chakma-rhyme-book.webp',
    download: 'https://drive.google.com/uc?export=download&id=15bLPx-LkC4HCN4WdYaZPK4TQDJ-4pL9Z'
  },
  {
    slug: 'tinnomuri',
    name: 'তিন্নোমুরি',
    englishName: 'Tinnomuri',
    type: 'ছড়াগ্রন্থ',
    genre: "Children's Rhymes",
    year: '2018',
    publisher: 'পরিবার প্রকাশনী',
    place: 'ঢাকা',
    image: '/tinnomuri-alomoy-chakma-chakma-rhyme-book.webp',
    download: 'https://drive.google.com/uc?export=download&id=15PlXb7JW7LZgMfUnYJnNKhiSPPZJO1Hp'
  },
  {
    slug: 'monpudi',
    name: 'মনপুদি',
    englishName: 'Monpudi',
    type: 'কাব্যগ্রন্থ',
    genre: 'Poetry',
    year: '2019',
    publisher: 'পরিবার প্রকাশনী',
    place: 'ঢাকা',
    image: '/monpudi-alomoy-chakma-chakma-poetry-book.webp',
    download: 'https://drive.google.com/uc?export=download&id=15LZJvC3T0MFdR8SBqj4dMcN8YTzoys2j'
  },
  {
    slug: 'nauri',
    name: 'নাউরি',
    englishName: 'Nauri',
    type: 'ছড়াগ্রন্থ',
    genre: "Children's Rhymes",
    year: '2020',
    publisher: 'পরিবার প্রকাশনী',
    place: 'ঢাকা',
    image: '/nauri-alomoy-chakma-chakma-rhyme-book.webp',
    download: 'https://drive.google.com/uc?export=download&id=15_RxnUlgBZBHzMLFIqmDIml5NPVdAK9a'
  }
];

function escapeHtml(value) {
  return String(value || '')
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function stripTags(value) {
  return String(value || '').replace(/<[^>]*>/g, '').replace(/\s+/g, ' ').trim();
}

function makeDescription(value, fallback) {
  const text = stripTags(value || fallback);
  return text.length > 158 ? text.slice(0, 155).trim() + '...' : text;
}

function makeRichDescription(article, meta) {
  const title = article.title || '';
  const excerpt = article.excerpt || '';
  const category = meta.bn;
  const enCategory = meta.en;
  const base = `${title} — আলোময় চাকমার ${category} সংগ্রহ। ${excerpt}`;
  const text = stripTags(base);
  return text.length > 158 ? text.slice(0, 155).trim() + '...' : text;
}

function getKeywords(category) {
  const common = 'আলোময় চাকমা, Alomoy Chakma, চাঙমা ভাষার সাহিত্য, Chakma language literature, পার্বত্য চট্টগ্রামের সাহিত্য, CHT literature, indigenous literature Bangladesh';
  const map = {
    poem: 'চাকমা কবিতা, chakma kobita, chakma poem, chakma poetry, চাঙমা ভাষার কবিতা, Chakma language poetry, Chakma poet Bangladesh, চাকমা কবি, chakma kobita alomoy, ফুল বারেঙ, মনপুদি',
    rhyme: 'চাকমা ছড়া, chakma rhyme, chakma chhora, Chakma children rhyme, indigenous poetry Bangladesh, হক্কেং হক্কেং, তিন্নোমুরি, নাউরি',
    story: 'চাকমা গল্প, chakma story, chakma golpo, Chakma short story, CHT literature, indigenous literature Bangladesh',
    song: 'চাকমা গান, chakma song, chakma gaan, Chakma lyrics, indigenous music Bangladesh'
  };
  return (map[category] || map.poem) + ', ' + common;
}

function ensureDir(dir) {
  fs.mkdirSync(dir, { recursive: true });
}

function writePage(route, html) {
  const dir = path.join(ROOT, route);
  ensureDir(dir);
  fs.writeFileSync(path.join(dir, 'index.html'), html, 'utf8');
}

function pageShell({ title, description, canonical, body, schema, keywords, bodyClass = '' }) {
  const schemaHtml = schema ? `<script type="application/ld+json">${JSON.stringify(schema, null, 2)}</script>` : '';
  const keywordsHtml = keywords ? `<meta name="keywords" content="${escapeHtml(keywords)}">` : '';
  return `<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <script>
    if (window.location.pathname && window.location.pathname !== '/') {
      window.location.replace('/?p=' + encodeURIComponent(window.location.pathname + window.location.search + window.location.hash));
    }
  </script>
  <title>${escapeHtml(title)}</title>
  <meta name="description" content="${escapeHtml(description)}">
  ${keywordsHtml}
  <meta name="robots" content="index, follow">
  <meta name="author" content="আলোময় চাকমা">
  <link rel="canonical" href="${escapeHtml(canonical)}">
  <link rel="alternate" hreflang="bn" href="${escapeHtml(canonical)}" />
  <link rel="alternate" hreflang="x-default" href="${escapeHtml(canonical)}" />
  <meta property="og:type" content="article">
  <meta property="og:site_name" content="গ্রন্থাগার — আলোময় চাকমা">
  <meta property="og:title" content="${escapeHtml(title)}">
  <meta property="og:description" content="${escapeHtml(description)}">
  <meta property="og:url" content="${escapeHtml(canonical)}">
  <meta property="og:image" content="${SITE_URL}/og-banner.png">
  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="${escapeHtml(title)}">
  <meta name="twitter:description" content="${escapeHtml(description)}">
  <meta name="twitter:image" content="${SITE_URL}/og-banner.png">
  <link rel="stylesheet" href="/style.css?v=2">
  <link rel="icon" type="image/png" href="/favicon-96.png">
  ${schemaHtml}
</head>
<body class="${escapeHtml(bodyClass)}">
  <header>
    <div class="container-max">
      <nav>
        <a href="/" class="logo" style="text-transform:none;">
          <div class="logo-img-wrapper"><img src="/logo-96.webp" alt="আলোময় চাকমা - Alomoy Chakma" class="logo-img" width="38" height="38" decoding="async"></div>
          <span>আলোময় চাকমা</span>
        </a>
        <div class="nav-links">
          <a href="/">হোম</a>
          <a href="/category/poem">কবিতা</a>
          <a href="/category/rhyme">ছড়া</a>
          <a href="/category/story">গল্প</a>
          <a href="/category/song">গান</a>
          <a href="/about">পরিচিতি</a>
        </div>
      </nav>
    </div>
  </header>
  <main class="container-max mt-stack-lg">${body}</main>
  <footer>
    <div class="container-max footer-content">
      <div class="footer-brand">
        <h4>আলোময় চাকমা</h4>
        <p class="label-sm text-secondary">© ২০২৬ আলোময় চাকমা। সর্বস্বত্ব সংরক্ষিত।</p>
      </div>
      <div class="footer-links">
        <a href="/books/ful-bareng" class="footer-link">PDF বই</a>
        <a href="mailto:alomoyc6@gmail.com" class="footer-link">ইমেইল</a>
        <a href="https://www.facebook.com/share/18bFgu3zzu/" class="footer-link" target="_blank" rel="noopener">ফেসবুক</a>
        <a href="https://fulbareng.blogspot.com/search/label/%E0%A6%95%E0%A6%AC%E0%A6%BF%E0%A6%A4%E0%A6%BE?m=1" class="footer-link" target="_blank" rel="noopener">ব্লগ</a>
        <a href="/privacy-policy" class="footer-link">গোপনীয়তা নীতি</a>
      </div>
    </div>
  </footer>
</body>
</html>`;
}

function personSchema() {
  return {
    '@context': 'https://schema.org',
    '@type': 'Person',
    '@id': `${SITE_URL}/#author`,
    name: 'আলোময় চাকমা',
    alternateName: 'Alomoy Chakma',
    description: 'চাঙমা ভাষার কবি ও কথাসাহিত্যিক। পার্বত্য চট্টগ্রামের জীবন ও প্রকৃতি নিয়ে রচিত কবিতা, ছড়া, গল্প ও গানের রচয়িতা।',
    email: 'alomoyc6@gmail.com',
    url: SITE_URL,
    image: `${SITE_URL}/writer-480.webp`,
    sameAs: [
      'https://www.facebook.com/share/18bFgu3zzu/',
      'https://fulbareng.blogspot.com/search/label/%E0%A6%95%E0%A6%AC%E0%A6%BF%E0%A6%A4%E0%A6%BE?m=1'
    ],
    knowsLanguage: ['bn', 'চাঙমা'],
    jobTitle: 'কবি ও কথাসাহিত্যিক',
    nationality: {
      '@type': 'Country',
      name: 'Bangladesh'
    }
  };
}

function breadcrumbListSchema(items) {
  return {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: items.map((item, idx) => ({
      '@type': 'ListItem',
      position: idx + 1,
      name: item.name,
      item: item.url
    }))
  };
}

function articleSchema(article, serial, canonical) {
  const typeMap = { story: 'Article', poem: 'CreativeWork', rhyme: 'CreativeWork', song: 'CreativeWork' };
  const genreMap = { story: 'Short Story', poem: 'Poetry', rhyme: 'Rhyme', song: 'Song' };
  // Build a text snippet from content (first 500 chars) for the schema
  const textSnippet = (article.content || [])
    .filter(line => line !== '__STANZA__')
    .join(' ')
    .slice(0, 500);
  const schema = {
    '@context': 'https://schema.org',
    '@type': typeMap[article.category],
    headline: article.title,
    name: article.title,
    author: { '@id': `${SITE_URL}/#author` },
    inLanguage: 'bn',
    genre: genreMap[article.category],
    url: canonical,
    description: makeDescription(article.excerpt, `${article.badge} by Alomoy Chakma`),
    position: serial,
    text: textSnippet
  };
  if (!schema.text) delete schema.text;
  return schema;
}

function bookSchema(book) {
  return {
    '@context': 'https://schema.org',
    '@type': 'Book',
    name: book.name,
    alternateName: book.englishName,
    author: { '@id': `${SITE_URL}/#author`, '@type': 'Person', name: 'Alomoy Chakma' },
    inLanguage: 'Chakma',
    datePublished: book.year,
    publisher: {
      '@type': 'Organization',
      name: book.publisher,
      address: `${book.place}, Bangladesh`
    },
    genre: book.genre,
    image: `${SITE_URL}${book.image}`
  };
}

function renderArticlePage(article, serial) {
  const meta = categoryMeta[article.category];
  const canonical = `${SITE_URL}/${article.category}/${serial}`;
  const title = `${article.title} | ${meta.bn} — আলোময় চাকমা`;
  const description = makeRichDescription(article, meta);
  const keywords = getKeywords(article.category);
  const lines = (article.content || []).map((line) => {
    if (line === '__STANZA__') return '<p class="poem-stanza-break"></p>';
    return `<p class="${article.category === 'story' ? '' : 'poem-line'}">${escapeHtml(line)}</p>`;
  }).join('\n');
  const body = `
    <article class="reader-view reading-well">
      <div class="reader-header">
        <span class="label-sm text-secondary uppercase tracking-widest block mb-2">${escapeHtml(article.badge)}</span>
        <h1 class="headline-lg">${escapeHtml(article.title)}</h1>
        <div class="reader-meta">
          <time>${escapeHtml(article.date || TODAY)}</time>
          <span style="margin:0 12px;">—</span>
          <span>${escapeHtml(article.readTime || '')}</span>
        </div>
      </div>
      <div class="reader-content">${lines}</div>
      <p class="mt-stack-md"><a class="link-editorial" href="/category/${article.category}">${escapeHtml(meta.bn)} সংগ্রহে ফিরে যান</a></p>
    </article>`;
  const schema = [
    articleSchema(article, serial, canonical),
    breadcrumbListSchema([
      { name: 'হোম', url: SITE_URL + '/' },
      { name: meta.bn, url: `${SITE_URL}/category/${article.category}` },
      { name: article.title, url: canonical }
    ])
  ];
  return pageShell({
    title,
    description,
    canonical,
    keywords,
    body,
    schema,
    bodyClass: `${article.category}-reader-active`
  });
}

function renderCategoryPage(category, items) {
  const meta = categoryMeta[category];
  const canonical = `${SITE_URL}/category/${category}`;
  const links = items.map((item, index) => `
    <article class="poetry-item">
      <div class="poetry-header">
        <h2 class="headline-sm poetry-title"><a href="/${category}/${index + 1}">${index + 1}. ${escapeHtml(item.title)}</a></h2>
        <span class="poetry-date">${escapeHtml(item.date || '')}</span>
      </div>
      <p class="body-md poetry-excerpt">${escapeHtml(item.excerpt || '')}</p>
      <a href="/${category}/${index + 1}" class="link-editorial">পড়ুন</a>
    </article>`).join('\n');
  const body = `
    <section class="reading-well mb-stack-lg">
      <div class="section-divider">
        <h1 class="headline-md">${escapeHtml(meta.bn)} / ${escapeHtml(meta.en)}</h1>
        <div class="section-line"></div>
      </div>
      <p class="body-lg text-secondary">${escapeHtml(meta.intro)}</p>
      <p class="body-md text-secondary">${items.length}টি লেখা এই বিভাগে সংরক্ষিত আছে।</p>
      <div class="poetry-list mt-stack-md">${links}</div>
    </section>`;
  const schema = [
    {
      '@context': 'https://schema.org',
      '@type': 'CollectionPage',
      name: `${meta.bn} সংগ্রহ`,
      url: canonical,
      description: meta.description,
      author: { '@id': `${SITE_URL}/#author` },
      inLanguage: 'bn'
    },
    breadcrumbListSchema([
      { name: 'হোম', url: SITE_URL + '/' },
      { name: meta.bn, url: canonical }
    ])
  ];
  return pageShell({
    title: `${meta.bn} সংগ্রহ | ${meta.en} — আলোময় চাকমা`,
    description: `${meta.intro} ${meta.description}`,
    canonical,
    keywords: getKeywords(category),
    body,
    schema
  });
}

function renderAboutPage() {
  const canonical = `${SITE_URL}/about`;
  const body = `
    <section class="reading-well mb-stack-lg">
      <div class="section-divider">
        <h1 class="headline-md">আলোময় চাকমা / Alomoy Chakma</h1>
        <div class="section-line"></div>
      </div>
      <div class="bio-layout">
        <div class="bio-image-wrapper">
          <img src="/writer-480.webp" alt="আলোময় চাকমা - Chakma poet and fiction writer from Bangladesh" class="bio-image" loading="lazy" decoding="async" width="480" height="415">
        </div>
        <div class="bio-text">
          <p class="body-lg text-secondary italic mb-stack-sm">কবি ও কথাসাহিত্যিক</p>
          <p class="body-md text-secondary">আলোময় চাকমা চাঙমা ভাষার কবি ও কথাসাহিত্যিক। তাঁর কবিতা, ছড়া, ছোটগল্প ও গান পার্বত্য চট্টগ্রামের জীবন, প্রকৃতি, স্মৃতি, ভাষা ও সংস্কৃতির সঙ্গে গভীরভাবে যুক্ত।</p>
          <p class="body-md text-secondary">Alomoy Chakma is a Chakma language poet and fiction writer from the Chittagong Hill Tracts of Bangladesh. This site preserves his poems, rhymes, short stories, songs, and published books as a digital Chakma literature archive.</p>
          <h2 class="headline-sm">প্রকাশিত বই</h2>
          <ul>${books.map(book => `<li><a href="/books/${book.slug}">${escapeHtml(book.name)}</a> — ${escapeHtml(book.type)}, ${escapeHtml(book.publisher)}, ${escapeHtml(book.year)}</li>`).join('')}</ul>
          <p>Contact: <a href="mailto:alomoyc6@gmail.com">alomoyc6@gmail.com</a></p>
        </div>
      </div>
    </section>`;
  const schema = [
    personSchema(),
    breadcrumbListSchema([
      { name: 'হোম', url: SITE_URL + '/' },
      { name: 'পরিচিতি', url: canonical }
    ])
  ];
  return pageShell({
    title: 'পরিচিতি | আলোময় চাকমা — Chakma Poet & Writer',
    description: 'আলোময় চাকমা — চাঙমা ভাষার কবি ও কথাসাহিত্যিক। পার্বত্য চট্টগ্রামের জীবন ও প্রকৃতি নিয়ে রচিত সাহিত্যের স্রষ্টার পরিচয়, প্রকাশিত বই ও যোগাযোগের তথ্য।',
    canonical,
    keywords: 'আলোময় চাকমা, Alomoy Chakma, চাকমা কবি, Chakma poet, চাঙমা ভাষার লেখক, Chakma writer, পার্বত্য চট্টগ্রাম, CHT, indigenous poet Bangladesh, Chakma literature, চাকমা সাহিত্যিক',
    body,
    schema
  });
}

function renderBookPage(book) {
  const canonical = `${SITE_URL}/books/${book.slug}`;
  const body = `
    <article class="reading-well mb-stack-lg">
      <div class="section-divider">
        <h1 class="headline-md">${escapeHtml(book.name)} / ${escapeHtml(book.englishName)}</h1>
        <div class="section-line"></div>
      </div>
      <div class="bio-layout">
        <div class="bio-image-wrapper">
          <img src="${book.image}" alt="${escapeHtml(book.englishName)} - Chakma ${escapeHtml(book.genre)} book by Alomoy Chakma, ${escapeHtml(book.year)}" class="bio-image" loading="lazy" decoding="async" width="235" height="360">
        </div>
        <div class="bio-text">
          <p class="body-lg text-secondary italic mb-stack-sm">${escapeHtml(book.type)}</p>
          <p class="body-md text-secondary">${escapeHtml(book.name)} আলোময় চাকমার প্রকাশিত ${escapeHtml(book.type)}। প্রকাশক ${escapeHtml(book.publisher)}, ${escapeHtml(book.place)}, ${escapeHtml(book.year)}।</p>
          <p class="body-md text-secondary">${escapeHtml(book.englishName)} is a Chakma ${escapeHtml(book.genre.toLowerCase())} book by Alomoy Chakma, published in Bangladesh.</p>
          <p><a class="btn btn-secondary pdf-download-btn" href="${escapeHtml(book.download)}" target="_blank" rel="noopener">PDF ডাউনলোড</a></p>
        </div>
      </div>
    </article>`;
  const schema = [
    bookSchema(book),
    breadcrumbListSchema([
      { name: 'হোম', url: SITE_URL + '/' },
      { name: book.name, url: canonical }
    ])
  ];
  return pageShell({
    title: `${book.name} | আলোময় চাকমা — ${book.type}`,
    description: `${book.englishName}, a Chakma ${book.genre.toLowerCase()} book by Alomoy Chakma, published by ${book.publisher} in ${book.year}. ${book.name} আলোময় চাকমার প্রকাশিত ${book.type}। PDF ডাউনলোড।`,
    canonical,
    keywords: `${book.name}, ${book.englishName}, আলোময় চাকমা, Alomoy Chakma, চাকমা বই, Chakma book, ${book.genre}, indigenous literature Bangladesh, ${book.publisher}, ${book.place}`,
    body,
    schema
  });
}

Object.keys(categoryMeta).forEach((category) => {
  const items = writings.filter((writing) => writing.category === category);
  writePage(path.join('category', category), renderCategoryPage(category, items));
  items.forEach((item, index) => {
    writePage(path.join(category, String(index + 1)), renderArticlePage(item, index + 1));
  });
});

writePage('about', renderAboutPage());
books.forEach((book) => writePage(path.join('books', book.slug), renderBookPage(book)));

console.log(`Generated static SEO pages for ${writings.length} writings, ${Object.keys(categoryMeta).length} categories, ${books.length} books, and about.`);

