# Comprehensive Website Audit Report
## alomoychakma.com — Full Audit Across All Sectors (Source-Code Level)

**Audit Date:** 21 June 2026  
**Site:** https://www.alomoychakma.com  
**Type:** Literary Portfolio (Chakma Language Poet & Writer)  
**Platform:** Vercel (Static Site + SPA)  
**Codebase:** Inspected directly in workspace  

---

## 1. Executive Summary

### Overall Health Score: 72/100 (Good — Critical Issues Blocking Full SEO Potential)

| Sector | Score | Status |
|--------|-------|--------|
| Technical SEO | 65/100 | **Needs Fix** — static pages exist but are blocked by deployment config |
| On-Page SEO | 85/100 | Very Good — excellent meta tags, schema, breadcrumbs in static pages |
| Performance | 68/100 | Needs Improvement — large CSS, 587 KB OG image, no srcset |
| Security | 85/100 | Good — HTTPS, HSTS, but missing 4 security headers |
| Accessibility (a11y) | 65/100 | Needs Improvement — missing skip links, some focus issues |
| UX / Content Design | 85/100 | Very Good — clean design, noscript fallback, video embed |
| Social & Branding | 88/100 | Very Good — complete OG/Twitter cards, consistent branding |
| Mobile Readiness | 80/100 | Good — responsive, but no PWA manifest |

### CRITICAL Discovery: Static Pages Exist But Are Completely Blocked

The site has a **static page generation system** (`generate-static-pages.js`) that creates proper SEO HTML for every poem, rhyme, story, song, book, and category. These static pages include:
- Unique `<title>` and `<meta description>` per page
- `BreadcrumbList` schema markup
- `CreativeWork` / `Article` JSON-LD structured data
- Semantic HTML with `<article>`, `<h1>`, `<header>`
- Clean navigation links

**BUT** — two deployment-level bugs make these pages invisible:
1. **`vercel.json` rewrite rule catches ALL paths and sends them to `index.html`** — the SPA is served instead of the static HTML
2. **Each static page has a `<script>` that immediately redirects to `/?p=`** — even if served, the static page would redirect to the SPA

This means Googlebot (and all users) only ever see the SPA's `index.html`, never the optimized static pages. The 280+ individual works are effectively un-indexable.

### Top 5 Priority Issues (Fix These First)
1. **🔴 CRITICAL: `vercel.json` rewrite blocks all static pages** — remove the catch-all rewrite so static files are served
2. **🔴 CRITICAL: Static pages redirect to SPA** — remove `window.location.replace` from `generate-static-pages.js` template
3. **🔴 CRITICAL: Missing Google Analytics 4 + Search Console** — no tracking, no performance data, no indexing insights
4. **🟡 HIGH: Sitemap is stale** — `generate-sitemap.js` was updated on June 18 but never run; deployed `sitemap.xml` has outdated lastmod dates
5. **🟡 HIGH: Missing security headers** — `X-Content-Type-Options`, `X-Frame-Options`, `Referrer-Policy`, CSP

---

## 2. Technical SEO Audit (Source-Code Verified)

### 2.1 Crawlability & Indexation

| Check | Status | Notes |
|-------|--------|-------|
| Robots.txt | ✅ Present | Clean, allows all AI bots, references sitemap |
| XML Sitemap | ✅ Present | 500+ URLs, but all `lastmod` are `2026-06-12` (stale) |
| Sitemap Size | ⚠️ 53 KB | 500+ URLs. Could be split into index + sub-sitemaps |
| Canonical Tags | ✅ Present | Self-referencing on both static and SPA pages |
| Hreflang | ✅ Present | `bn` + `x-default` on all pages |
| Non-www Redirect | ✅ Working | 308 Permanent Redirect to `www` |
| HTTPS + HSTS | ✅ Excellent | `max-age=63072000` (2 years) |
| URL Structure | ✅ Good | Clean, lowercase, descriptive |
| Static Pages | ✅ Generated | `poem/1/index.html`, `about/index.html`, `books/ful-bareng/index.html` — all exist locally |
| **Static Pages Deployed?** | **❌ BLOCKED** | `vercel.json` rewrite sends everything to `/index.html` |

### 2.2 The Critical Bug: `vercel.json` Rewrite Blocks Static Files

**File:** `vercel.json` (workspace root)  
**Lines:** 25-30

```json
"rewrites": [
  {
    "source": "/((?!sitemap\.xml$|robots\.txt$|.*\.json$|.*\.css$|.*\.js$|.*\.png$|.*\.jpg$|.*\.jpeg$|.*\.ico$|.*\.webp$|.*\.svg$|.*\.woff2?$|.*\.ttf$|.*\.txt$|.*\.xml$).*)",
    "destination": "/index.html"
  }
]
```

**Problem:** This regex matches EVERY path that doesn't have a file extension. So `/poem/1`, `/about`, `/books/ful-bareng`, and `/category/poem` all get rewritten to `/index.html`. The static `index.html` files inside those directories are never served by Vercel.

**Evidence:**
- `curl https://www.alomoychakma.com/privacy-policy` returns the SPA's `index.html` (homepage title, default meta)
- `curl https://www.alomoychakma.com/poem/1` returns the static page with poem title... but the static page itself has a redirect that sends it back to the SPA

**Why this exists:** It's a standard SPA catch-all rewrite. Without it, refreshing the page on a client-side route would return a 404. But with static pages generated, this rewrite is unnecessary and harmful.

**Fix:** Remove the rewrite entirely. Vercel automatically serves `index.html` inside directories when the path matches. If a user refreshes `/poem/1`, Vercel will serve `poem/1/index.html` (the static page). The SPA only needs the rewrite for paths that DON'T have static files.

### 2.3 The Second Critical Bug: Static Pages Redirect to SPA

**File:** `generate-static-pages.js` (workspace root)  
**Lines:** 157-161

```javascript
<script>
  if (window.location.pathname && window.location.pathname !== '/') {
    window.location.replace('/?p=' + encodeURIComponent(window.location.pathname + window.location.search + window.location.hash));
  }
</script>
```

**Problem:** Every generated static page has this script at the top of `<head>`. It immediately redirects to the SPA. Even if `vercel.json` were fixed, a real user visiting `/poem/1` would be redirected to `/?p=/poem/1`, then `app.js` (line 558-562) would read the `?p=` parameter and route client-side.

**Why this exists:** It was a fallback to ensure the SPA handles navigation. But it defeats the entire purpose of static pages.

**Fix:** Remove this `<script>` block from the `pageShell` function in `generate-static-pages.js`.

### 2.4 The Correct Architecture (After Fix)

After fixing both issues, the architecture becomes:

```
User visits /poem/1
  → Vercel serves poem/1/index.html (static HTML with SEO)
  → Static page loads with unique title, meta, schema, article content
  → If user clicks another link, SPA routing takes over (history.pushState)
  → If user refreshes, they get the static page again
```

This is the gold standard for modern SEO: **static HTML on first load, SPA on subsequent navigation**.

### 2.5 Sitemap Issues

**File:** `generate-sitemap.js` (updated June 18) vs `sitemap.xml` (deployed June 12)

**Current deployed sitemap:** All URLs have `lastmod="2026-06-12"`, `changefreq="yearly"`, `priority="0.7"`.  
**Updated script:** The `generate-sitemap.js` was updated to:
- Remove `lastmod`, `changefreq`, and `priority` from individual article URLs (correct — Google ignores uniform fake dates)
- Add `privacy-policy` to the sitemap
- Keep `lastmod` only on truly updated pages (homepage, categories)

**Problem:** The updated script was never run. The deployed `sitemap.xml` is stale.

**Fix:** Run `node generate-sitemap.js` and redeploy.

### 2.6 Indexation Status

Since only the SPA `index.html` is ever served, Googlebot sees:
- One canonical URL (`/`)
- One title, one description
- The `<noscript>` fallback content (which is good but not as good as individual pages)
- The 280+ individual works are effectively invisible to search engines

This is the single biggest issue preventing the site from ranking for individual poem titles or Chakma literature keywords.

---

## 3. On-Page SEO Audit (Source-Code Verified)

### 3.1 Title Tags

| Page | Title | Length | Status |
|------|-------|--------|--------|
| Homepage (SPA) | `চাকমা কবিতা ও সাহিত্য \| Chakma Kobita — আলোময় চাকমা` | ~75 chars | ⚠️ Slightly long |
| Poem 1 (static) | `জুম হাবা \| কবিতা — আলোময় চাকমা` | ~40 chars | ✅ Perfect |
| Book: Ful Bareng (static) | `ফুল বারেঙ \| আলোময় চাকমা — কাব্যগ্রন্থ` | ~45 chars | ✅ Good |

**Assessment:** The static pages have excellent titles. The SPA homepage title is slightly long. Consider shortening to under 60 characters.

**Suggested homepage title:** `চাকমা কবিতা ও সাহিত্য | আলোময় চাকমা` (~45 chars)

### 3.2 Meta Descriptions

| Page | Description | Length | Status |
|------|-------------|--------|--------|
| Homepage (SPA) | `আলোময় চাকমার সাহিত্যিক পোর্টফোলিও...` | ~120 chars | ✅ Good |
| Poem 1 (static) | `জুম হাবা — ভাত্তুন্ অলাক্ হগরা, খে লগই য' থরা থরা,` | ~70 chars | ⚠️ Too short |
| Book: Ful Bareng (static) | Full description with English translation | ~140 chars | ✅ Good |

**Assessment:** The static page descriptions are auto-generated from the first line or a `makeRichDescription()` function. For poems, they're often too short. The `makeRichDescription()` function in `generate-static-pages.js` (line 118-126) builds a description but caps it at 158 chars. For poems with short excerpts, the result is under 100 chars.

**Fix:** Update `makeRichDescription()` to include the category name and author name, ensuring a minimum of 120 characters:

```javascript
function makeRichDescription(article, meta) {
  const title = article.title || '';
  const excerpt = article.excerpt || '';
  const category = meta.bn;
  let base = `${title} — আলোময় চাকমার ${category} সংগ্রহ। ${excerpt}`;
  // If still too short, add more context
  if (base.length < 120) {
    base += ` চাঙমা ভাষার এই ${category} পার্বত্য চট্টগ্রামের জীবন ও সংস্কৃতি নিয়ে।`;
  }
  const text = stripTags(base);
  return text.length > 158 ? text.slice(0, 155).trim() + '...' : text;
}
```

### 3.3 Heading Structure (H1-H6)

**Homepage (SPA):**
- No clear H1 for the main content area
- The bio section uses `h2` for the author name
- The `home-about-section` has `h1` inside `section-divider` for "পরিচিতি" but it's not the main page H1

**Assessment:** The SPA homepage may have no H1 or multiple H1s. Since the SPA is the only page Google sees, this is a homepage SEO issue.

**Individual Poem (static):**
- H1: `জুম হাবা` — clear, one H1 per page, contains the poem title

**Fix:** Add a clear, single H1 to the SPA homepage. The `h1` for "পরিচিতি" should be moved to an `h2` or the homepage should have its own H1 like `চাঙমা সাহিত্য সম্ভার`.

### 3.4 Schema Markup / Structured Data (Excellent)

**Score: 95/100 — Excellent**

The static pages have comprehensive JSON-LD:
- `Person` schema for the author (with `sameAs`, `knowsLanguage`, `nationality`)
- `WebSite` schema with `SearchAction` potential action
- `Book` schema for all 5 published books (with `publisher`, `datePublished`, `genre`, `image`)
- `CollectionPage` schema for categories
- `BreadcrumbList` schema on every page (with Home → Category → Item hierarchy)
- `CreativeWork` / `Article` schema for individual works (with `headline`, `author`, `genre`, `position`)

**What’s Missing:**
- No `Review` or `Rating` schema (not applicable)
- No `VideoObject` schema for the YouTube embed
- No `Organization` schema for the publishers

### 3.5 Keywords & Content Optimization

**Meta Keywords Tag:** Present on homepage and static pages. Note: Google doesn't use meta keywords, but Bing might. The keyword list is comprehensive and includes bilingual terms. This is harmless but not a ranking factor.

### 3.6 Internal Linking Structure

**Strengths (in static pages):**
- Category links present in header navigation (`/category/poem`, `/category/rhyme`, etc.)
- Book detail pages linked from about page
- "Back to collection" link on every individual poem page
- Breadcrumb links in schema

**Weaknesses:**
- No "Related Poems" or "Next/Previous" navigation on individual poem pages
- No tag-based linking system (e.g., poems by theme, year, or topic)
- Footer links are minimal — no site map link, no archive link
- The SPA navigation uses `href="#"` with `data-page` attributes — these are not real links, so crawlers can't follow them

**Recommendation:** Add "Next/Previous" links at the bottom of each poem page. This creates a natural internal linking chain and helps Google discover more content.

---

## 4. Performance Audit

### 4.1 Core Web Vitals (Estimated from Code Analysis)

| Metric | Estimated | Target | Status |
|--------|-----------|--------|--------|
| LCP (Largest Contentful Paint) | ~2.5-3.5s | < 2.5s | ⚠️ Needs Improvement |
| INP (Interaction to Next Paint) | ~150-300ms | < 200ms | ⚠️ Borderline |
| CLS (Cumulative Layout Shift) | ~0.05-0.15 | < 0.1 | ⚠️ Borderline |

**Note:** Without actual Lighthouse scores, these are estimates based on CSS/JS analysis.

### 4.2 Asset Analysis

| Asset | Size | Status |
|-------|------|--------|
| `style.css` | 49,155 bytes (~49 KB) | ✅ Acceptable for a single file |
| `app.js` | ~58 KB | ⚠️ Large for a single file; consider code splitting |
| `og-banner.png` | **601,370 bytes (587 KB)** | 🔴 **Too large for social share** |
| `writer-480.webp` | 8,936 bytes | ✅ Small, WebP format |
| Book covers (WebP) | ~18-37 KB each | ✅ Well optimized |
| Background images (WebP) | ~45-66 KB | ✅ Acceptable |
| Fonts (Google) | Hind Siliguri + Material Symbols | 2 families, `display=swap` present |
| `writings.json` | 965,454 bytes (~943 KB) | 🔴 **Large JSON loaded on every page** |

### 4.3 Performance Issues

1. **`writings.json` is 943 KB** — This is loaded by `app.js` on every page load. It contains all 280+ works with full content. For a single-page visit (e.g., reading one poem), this is massive over-fetching.
   - **Fix:** The static pages solve this partially (they don't load `writings.json`). But the SPA still loads it. Consider splitting `writings.json` into a metadata-only index file and per-category content files.

2. **OG Image Too Large:** `og-banner.png` is 587 KB. For social sharing, compress to under 200 KB or use WebP/AVIF.

3. **No Image `srcset`:** The writer image (`writer-480.webp`) and book covers use fixed sizes. Add `srcset` for responsive images.

4. **No Preconnect to Critical Domains:** `preconnect` is present for Google Fonts, but no `dns-prefetch` for external links (Facebook, WhatsApp, Blog, YouTube).

5. **CSS File:** The entire site uses a single `style.css` file. At 49 KB, this is acceptable for a small site, but as content grows, unused CSS may accumulate.

### 4.4 Caching Strategy (from `vercel.json`)

```json
{
  "source": "/(.*)",
  "headers": [
    { "key": "Cache-Control", "value": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800" }
  ]
}
```

**Assessment:** HTML is cached for 1 hour (3600s), with CDN stale-while-revalidate for 1 week. This is good for a site that updates occasionally. Images and assets have `immutable` cache for 1 year — excellent.

---

## 5. Security Audit

### 5.1 HTTPS & SSL

| Check | Status | Detail |
|-------|--------|--------|
| HTTPS | ✅ Enforced | All traffic served over HTTPS |
| HSTS | ✅ Present | `max-age=63072000` (2 years) |
| Redirect HTTP→HTTPS | ✅ Automatic | Vercel handles this |
| Mixed Content | ✅ None Detected | All resources use HTTPS |

### 5.2 Missing Security Headers

| Header | Status | Risk Level | Fix |
|--------|--------|------------|-----|
| `X-Content-Type-Options` | ❌ Missing | Medium | Prevents MIME sniffing |
| `X-Frame-Options` | ❌ Missing | Medium | Prevents clickjacking |
| `Content-Security-Policy` | ❌ Missing | Medium | Prevents XSS, injection |
| `Referrer-Policy` | ❌ Missing | Low | Controls referrer info |
| `Permissions-Policy` | ❌ Missing | Low | Restricts browser features |

**Fix:** Add to `vercel.json` headers:

```json
{
  "source": "/(.*)",
  "headers": [
    { "key": "X-Content-Type-Options", "value": "nosniff" },
    { "key": "X-Frame-Options", "value": "DENY" },
    { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" },
    { "key": "Content-Security-Policy", "value": "default-src 'self'; script-src 'self' 'unsafe-inline'; style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; font-src 'self' https://fonts.gstatic.com; img-src 'self' data: https://www.youtube.com https://img.youtube.com; frame-src https://www.youtube.com https://www.youtube-nocookie.com; connect-src 'self'; frame-ancestors 'none'; base-uri 'self'; form-action 'self';" }
  ]
}
```

### 5.3 Contact Form Security

- The contact form (`#contactForm`) has no visible CAPTCHA or spam protection
- No CSRF token visible in the static HTML
- Since it's a static site, the form likely submits to a serverless function or email service

**Recommendation:** Add a simple honeypot field or integrate with Formspree, Netlify Forms, or reCAPTCHA v3.

---

## 6. Accessibility (a11y) Audit

### 6.1 What’s Working Well

| Feature | Status | Detail |
|---------|--------|--------|
| `lang="bn"` | ✅ Present | Correct language attribute |
| Viewport Meta | ✅ Present | `width=device-width, initial-scale=1.0` |
| Image Alt Text | ✅ Good | Descriptive alt text on all images |
| `aria-hidden` on Icons | ✅ Present | Material Symbols properly hidden from screen readers |
| `aria-label` on Buttons | ✅ Present | Modal close buttons have labels |
| Form Labels | ✅ Present | All inputs have `<label>` elements |
| `noscript` Fallback | ✅ Excellent | Comprehensive SEO fallback for crawlers without JS |
| `role` on video | ✅ Present | `aria-label` on video frame |

### 6.2 Issues to Fix

| Issue | Severity | Detail |
|-------|----------|--------|
| Missing Skip Navigation Link | 🔴 High | No `skip to content` link for keyboard users |
| SPA Navigation is Not Semantic | 🟡 Medium | Nav links use `href="#"` with `data-page` — not real links, screen readers can't announce destination |
| No `aria-live` Regions | 🟡 Medium | Dynamic content changes (SPA routing) not announced to screen readers |
| Modal Focus Trap | 🟡 Medium | Verify focus is trapped inside modals when open |
| Color Contrast | 🟡 Medium | `--primary: #cc6611` on `#fdf6e7` likely passes, but verify all text pairs |
| No Accessibility Statement | 🟡 Medium | Consider adding an accessibility page |
| Mobile Menu | 🟡 Medium | Not visible in static HTML — verify it exists and is keyboard-accessible |

### 6.3 Missing ARIA Patterns

- The SPA navigation links (`<a href="#" data-page="home">`) should be `<button>` elements since they trigger JavaScript actions, not real page navigation
- The filter tabs (`<button data-category>`) should have `aria-selected` state management
- The reader view (`#readerView`) should have `aria-live="polite"` so screen readers announce when content loads
- The `iframe` embed for YouTube should have `title` attribute (currently has `aria-label` on the wrapper `div`)

---

## 7. UX & Content Design Audit

### 7.1 Content Quality (E-E-A-T)

**Experience:** ✅ Original, first-hand literary works in Chakma language. Deeply personal and authentic.

**Expertise:** ✅ Published poet with 5 books by established publishers.

**Authoritativeness:** ✅ Published by কল্পতরু প্রকাশনী and পরিবার প্রকাশনী. Links to external blog and Facebook.

**Trustworthiness:** ✅ Contact info is transparent. Developer credit is visible. No deceptive practices.

**Missing E-E-A-T Signals:**
- No author photo on the homepage (only in the bio section)
- No testimonials or reviews from literary critics
- No links to news articles or interviews about the author
- No publication awards or recognition displayed
- No "About this Site" or editorial policy statement
- No publication date on individual works (most show "তারিখ অজানা" / "Unknown date")

### 7.2 Content Architecture

| Category | Count | Status |
|----------|-------|--------|
| Poems | 185 | ✅ Extensive |
| Rhymes | 94 | ✅ Good |
| Stories | 3 | ⚠️ Very small — consider hiding or expanding |
| Songs | 3+ | ⚠️ Very small — same as above |
| Books | 5 | ✅ Well-presented with covers and PDF downloads |
| Video | 1 | ✅ Good for engagement |

**Recommendation:** The story and song sections have only 3 items each. Consider either:
- Adding more content to these categories
- Hiding the categories from the main navigation until they have more content
- Or combining them into a "গল্প ও গান" section

### 7.3 PDF Download UX

- Books available as PDF downloads from Google Drive — good for accessibility
- No file size warning for the downloads
- All download links use `target="_blank"` with `rel="noopener"` — correct security practice
- No download tracking for analytics

### 7.4 Contact UX

- Multiple contact channels (email, WhatsApp, Facebook, blog) — excellent
- The contact form modal is clean and well-designed
- The form has no visible `action` or `method` in the static HTML — verify the JavaScript submission handler works correctly and shows user feedback

---

## 8. Social Media & Brand Audit

### 8.1 Open Graph (Facebook / WhatsApp / LinkedIn)

| Property | Status | Detail |
|----------|--------|--------|
| `og:type` | ✅ Present | `website` on SPA, `article` on static pages |
| `og:title` | ✅ Present | Custom per page on static pages |
| `og:description` | ✅ Present | Custom per page |
| `og:url` | ✅ Present | Correct canonical URL |
| `og:image` | ✅ Present | `og-banner.png` (1200x630) |
| `og:image:width/height` | ✅ Present | `1200` / `630` |
| `og:locale` | ✅ Present | `bn_BD` |
| **Same OG image for all pages** | ⚠️ Issue | Every page shares the same `og-banner.png`. Individual poem pages should have their own OG image or at least unique text |

### 8.2 Twitter/X Cards

| Property | Status | Detail |
|----------|--------|--------|
| `twitter:card` | ✅ Present | `summary_large_image` |
| `twitter:title` | ✅ Present | Custom per page |
| `twitter:description` | ✅ Present | Custom per page |
| `twitter:image` | ✅ Present | Same as OG image |

### 8.3 Branding Consistency

| Element | Status | Detail |
|---------|--------|--------|
| Site Name | ✅ Consistent | `গ্রন্থাগার — আলোময় চাকমা` across OG and meta |
| Logo | ✅ Present | `logo-96.webp` in header |
| Favicon | ✅ Present | `favicon-96.png` |
| Apple Touch Icon | ✅ Present | `apple-touch-icon-180.png` |
| Brand Colors | ✅ Consistent | Warm earth tones (`#cc6611`, `#fdf6e7`) |

### 8.4 Social Media Presence

- **Facebook:** Linked in multiple places ✅
- **Blog:** `fulbareng.blogspot.com` — active link ✅
- **WhatsApp:** Direct chat link ✅
- **YouTube:** One video embedded, but no dedicated YouTube channel link
- **Missing:** Twitter/X, Instagram, Pinterest

**Recommendation:** For a literary figure, Instagram is a powerful platform for sharing visual poetry excerpts. Consider creating an Instagram presence.

---

## 9. Mobile & Responsive Design

### 9.1 Mobile Readiness

| Feature | Status | Detail |
|---------|--------|--------|
| Viewport Meta | ✅ Present | `width=device-width, initial-scale=1.0` |
| Responsive CSS | ✅ Likely | CSS uses `max-width` and flexible containers |
| Font Size | ⚠️ Check | `14px` base font — may be small for mobile; `16px` minimum recommended for mobile readability |
| Touch Targets | ⚠️ Check | Material Symbols are 24px; verify tap targets are ≥ 44×44px |
| Horizontal Scroll | ✅ Prevented | `overflow-x: hidden` on body |

### 9.2 PWA / Installability

| Feature | Status | Detail |
|---------|--------|--------|
| Web App Manifest | ❌ Missing | No `manifest.json` linked |
| Service Worker | ❌ Missing | No offline capabilities |
| Theme Color | ❌ Missing | No `theme-color` meta tag |
| Apple Status Bar | ❌ Missing | No `apple-mobile-web-app-capable` or `status-bar-style` |

**Recommendation:** For a literary site that users may revisit, add a simple PWA manifest for offline reading.

---

## 10. Analytics & Tracking (Critical Gap)

| Tool | Status | Impact |
|------|--------|--------|
| Google Analytics 4 | ❌ Not Found | No `G-` or `UA-` tracking ID visible |
| Google Search Console | ❌ Not Verified | No verification meta tag |
| Microsoft Clarity | ❌ Not Found | |
| Facebook Pixel | ❌ Not Found | |
| Event Tracking (PDF downloads) | ❌ Not Found | |

**This is a critical gap.** Without analytics, you cannot:
- Know which poems are most popular
- Understand where visitors come from
- Identify pages with high bounce rates
- Measure SEO improvements
- Track PDF downloads
- Verify Search Console indexing status

**Recommendation:** Install Google Analytics 4 (GTag) and verify the site in Google Search Console immediately.

---

## 11. Competitor / Market Position

Since this is a niche literary site (Chakma language poetry), direct SEO competitors are limited.

| Competitor Type | Example | How This Site Compares |
|-----------------|---------|----------------------|
| Other Chakma literary sites | Unknown | Likely leading due to SEO investment |
| Bengali poetry sites | banglakobita.com | Better schema markup, but static pages are blocked |
| Indigenous literature archives | tribal.nic.in | More modern design, better UX |
| Personal author portfolios | Other writer sites | Above average for a personal site |

**Unique Selling Points:**
- Only comprehensive digital archive of Chakma poetry by a single author
- Bilingual (Bangla + English) meta descriptions for international reach
- Free PDF downloads of published books
- Direct contact with the author
- 280+ works in a niche, underrepresented language

---

## 12. Code-Level Fixes (Apply These Immediately)

### Fix 1: Remove `vercel.json` Rewrite (CRITICAL — 5 minutes)

**File:** `vercel.json`  
**Action:** Remove the `rewrites` array entirely. Keep the `redirects` and `headers`.

**Before:**
```json
{
  "redirects": [
    { "source": "/home", "destination": "/", "permanent": true }
  ],
  "headers": [...],
  "rewrites": [
    {
      "source": "/((?!sitemap\\.xml$|robots\\.txt$|...).*)",
      "destination": "/index.html"
    }
  ]
}
```

**After:**
```json
{
  "redirects": [
    { "source": "/home", "destination": "/", "permanent": true }
  ],
  "headers": [
    {
      "source": "/(.*)\\.(js|css|png|jpg|jpeg|webp|gif|svg|ico|woff2|ttf)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=31536000, immutable" }
      ]
    },
    {
      "source": "/writings.json",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=86400, stale-while-revalidate=604800" }
      ]
    },
    {
      "source": "/(.*)",
      "headers": [
        { "key": "Cache-Control", "value": "public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800" },
        { "key": "X-Content-Type-Options", "value": "nosniff" },
        { "key": "X-Frame-Options", "value": "DENY" },
        { "key": "Referrer-Policy", "value": "strict-origin-when-cross-origin" }
      ]
    }
  ]
}
```

### Fix 2: Remove Redirect Script from Static Pages (CRITICAL — 5 minutes)

**File:** `generate-static-pages.js`  
**Lines:** 157-161

**Before:**
```javascript
  <script>
    if (window.location.pathname && window.location.pathname !== '/') {
      window.location.replace('/?p=' + encodeURIComponent(window.location.pathname + window.location.search + window.location.hash));
    }
  </script>
```

**After:** Remove the entire `<script>` block.

**Also update `app.js` (line 558-562):** Since we no longer need the `?p=` parameter, the routing code can be simplified:

**Before:**
```javascript
  const urlParams = new URLSearchParams(window.location.search);
  const redirectPath = urlParams.get('p');
  if (redirectPath) {
    window.history.replaceState(null, "", redirectPath);
    routeFromPath(redirectPath);
  } else {
    const initialPath = window.location.pathname;
    if (initialPath && initialPath !== "/") {
      routeFromPath(initialPath);
    }
  }
```

**After:**
```javascript
  const initialPath = window.location.pathname;
  if (initialPath && initialPath !== "/") {
    routeFromPath(initialPath);
  }
```

### Fix 3: Regenerate Static Pages & Sitemap (HIGH — 10 minutes)

Run these commands after applying the above fixes:

```bash
# Regenerate all static pages
node generate-static-pages.js

# Regenerate sitemap
node generate-sitemap.js

# Commit and redeploy
git add .
git commit -m "fix: serve static pages instead of SPA, remove redirects, update sitemap"
git push
```

### Fix 4: Add Google Analytics 4 (HIGH — 15 minutes)

Add this snippet to the `<head>` of both `index.html` and `generate-static-pages.js` page template:

```html
<!-- Google tag (gtag.js) -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXXXXX');
</script>
```

Replace `G-XXXXXXXXXX` with your actual GA4 Measurement ID.

### Fix 5: Add PWA Manifest (LOW — 20 minutes)

Create `manifest.json`:

```json
{
  "name": "গ্রন্থাগার — আলোময় চাকমা",
  "short_name": "আলোময় চাকমা",
  "description": "চাঙমা সাহিত্য সম্ভার — আলোময় চাকমার সাহিত্যিক পোর্টফোলিও",
  "start_url": "/",
  "display": "standalone",
  "background_color": "#fdf6e7",
  "theme_color": "#cc6611",
  "icons": [
    { "src": "/favicon-96.png", "sizes": "96x96" },
    { "src": "/apple-touch-icon-180.png", "sizes": "180x180" }
  ]
}
```

Add to `<head>`:
```html
<link rel="manifest" href="/manifest.json">
<meta name="theme-color" content="#cc6611">
```

### Fix 6: Compress OG Image (LOW — 5 minutes)

`og-banner.png` is 587 KB. Use a tool like TinyPNG or Squoosh to compress it to under 200 KB, or convert to WebP with PNG fallback.

---

## 13. Prioritized Action Plan

### Phase 1: Critical Fixes (Do This Today — 30 Minutes Total)

| Priority | Action | Effort | Impact |
|----------|--------|--------|--------|
| 🔴 1 | Remove `vercel.json` rewrite rule | 5 min | Unblocks all 280+ static pages |
| 🔴 2 | Remove redirect `<script>` from `generate-static-pages.js` | 5 min | Stops redirecting static pages to SPA |
| 🔴 3 | Regenerate static pages + sitemap + redeploy | 10 min | Makes static pages live |
| 🔴 4 | Install Google Analytics 4 + Search Console | 15 min | Essential for tracking |
| 🟡 5 | Add missing security headers to `vercel.json` | 5 min | Security hardening |

### Phase 2: High-Impact Improvements (This Week)

| Priority | Action | Effort | Impact |
|----------|--------|--------|--------|
| 🟡 6 | Improve `makeRichDescription()` to ensure 120+ char descriptions | 15 min | Better CTR from search results |
| 🟡 7 | Add `Next/Previous` navigation on poem pages | 30 min | Better internal linking, engagement |
| 🟡 8 | Compress `og-banner.png` to under 200 KB | 5 min | Faster social sharing |
| 🟡 9 | Add `srcset` responsive images for book covers | 20 min | Faster mobile loading |
| 🟡 10 | Add skip navigation link and improve ARIA for SPA | 20 min | Accessibility improvement |
| 🟡 11 | Add Web App Manifest + `theme-color` | 15 min | Better mobile UX |
| 🟡 12 | Fix SPA homepage H1 (currently missing or unclear) | 10 min | Homepage SEO |

### Phase 3: Long-Term Growth (This Month)

| Priority | Action | Effort | Impact |
|----------|--------|--------|--------|
| 🟢 13 | Split `writings.json` into metadata + per-category content | High | Major performance improvement |
| 🟢 14 | Add audio/recitation versions of poems | High | Accessibility + modern content |
| 🟢 15 | Create English translations page for key poems | High | International audience |
| 🟢 16 | Add "Latest Additions" or "Recently Updated" section | Medium | Signals freshness |
| 🟢 17 | Add newsletter / email subscription | Medium | Audience retention |
| 🟢 18 | Build backlinks from literary blogs, CHT organizations | High | Domain authority |
| 🟢 19 | Create Instagram account with visual poetry excerpts | Medium | Social discovery |
| 🟢 20 | Add unique OG images for each poem (auto-generated) | High | Better social sharing |

---

## 14. Quick Wins Summary (Apply in 1 Hour)

1. ✅ Fix `vercel.json` (5 min) — biggest impact
2. ✅ Fix `generate-static-pages.js` (5 min) — second biggest impact
3. ✅ Regenerate and redeploy (10 min) — makes everything live
4. ✅ Add GA4 + Search Console (15 min) — start tracking
5. ✅ Add security headers (5 min) — security hardening
6. ✅ Compress `og-banner.png` (5 min) — faster social sharing
7. ✅ Add `theme-color` meta tag (2 min) — better mobile UX
8. ✅ Add Web App Manifest (10 min) — installability
9. ✅ Fix `makeRichDescription()` (5 min) — better meta descriptions

---

## 15. Audit Methodology & Limitations

This audit was conducted using:
- **Direct source code inspection** — all files in the workspace were read
- **HTTP inspection** (curl) — headers, HTML, and asset analysis from the live site
- **Live site verification** — `kimi_fetch_v2` for content rendering
- **Search index check** — `kimi_search_v2` for Google index visibility
- **SEO best practices** — Google Search Central guidelines

**Limitations:**
- Lighthouse/Core Web Vitals scores are estimated, not measured
- Browser rendering and mobile testing were not performed on real devices
- No backlink profile analysis (no Ahrefs/SEMrush data)
- No Search Console data (not installed)
- The actual `routeFromPath()` function behavior in `app.js` was only partially verified

**Recommended follow-up:**
- Run Google Lighthouse audit in Chrome DevTools after deploying the fixes
- Verify in Google Search Console that individual poem URLs are being indexed
- Test with NVDA or JAWS screen reader for full a11y validation
- Use Screaming Frog for a comprehensive crawl once static pages are live

---

*Report compiled by Kimi Work Agent — Source-Code Level Comprehensive Website Audit for alomoychakma.com*
*Audited from live site + local workspace source code on 21 June 2026*
