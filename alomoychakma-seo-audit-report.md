# Full SEO Audit Report — alomoychakma.com

**Audit Date:** June 18, 2026
**Domain:** https://alomoychakma.com (redirects to www.alomoychakma.com)
**Platform:** Vercel (Static/SSR)
**Language:** Bengali (bn) + Chakma
**Total URLs in Sitemap:** 318

---

## Executive Summary

**Overall Health:** Good Foundation — Several Optimization Opportunities

The site has a solid technical foundation with HTTPS enforcement, proper canonicalization, comprehensive schema markup, and unique meta tags on every page. However, there are **critical SEO gaps** that are likely limiting organic reach and ranking potential, especially around URL structure, caching strategy, and content pagination.

### Top 5 Priority Issues

| Priority | Issue | Impact |
|----------|-------|--------|
| 🔴 **1** | Numeric IDs in URLs (`/poem/1`, `/rhyme/1`) instead of keyword slugs | **High** — Major ranking barrier |
| 🔴 **2** | No HTTP caching (`max-age=0`) on all pages | **High** — Speed & Core Web Vitals |
| 🟡 **3** | Category page loads 185 poems without pagination | **Medium** — Page size, crawlability |
| 🟡 **4** | Poem/story meta descriptions are too thin (just first line) | **Medium** — CTR & relevance signals |
| 🟡 **5** | Missing `BreadcrumbList` schema & `Article` schema for individual works | **Medium** — Rich results eligibility |

---

## 1. Technical SEO Findings

### ✅ Crawlability & Indexation — Mostly Good

| Check | Status | Evidence |
|-------|--------|----------|
| Robots.txt | **Good** | Clean, allows all, references sitemap correctly |
| XML Sitemap | **Present** | 318 URLs listed at `/sitemap.xml` |
| Canonical Tags | **Good** | All pages have self-referencing canonicals to `https://www.alomoychakma.com/...` |
| Non-www → www | **Good** | 308 Permanent Redirect with HSTS header (`max-age=63072000`) |
| HTTPS | **Good** | Enforced across entire site, no mixed content detected |
| robots meta | **Good** | `index, follow` on all checked pages |

#### ⚠️ Issues Found:

**Issue 1.1 — Sitemap `lastmod` values are not realistic**
- **Evidence:** Every single URL has `<lastmod>2026-06-12</lastmod>` — identical date for 318 pages.
- **Impact:** Google may ignore `lastmod` entirely when all dates are uniform. This reduces crawl efficiency signals.
- **Fix:** Set accurate `lastmod` dates per page (e.g., when the poem was actually published or last edited). Use the build timestamp only if the build process genuinely updates every page.

**Issue 1.2 — Sitemap `changefreq` and `priority` are uniform**
- **Evidence:** All 185 poem pages have `changefreq>yearly</changefreq>` and `priority>0.7</priority>`. Homepage is `weekly/1.0`, category pages are `weekly/0.9`.
- **Impact:** Google ignores `priority` and largely ignores `changefreq`. However, misalignment can confuse crawl budget allocation.
- **Fix:** For a poetry archive, `yearly` may be appropriate for older poems, but newer poems should be `monthly`. Category pages should remain `weekly`.

**Issue 1.3 — Sitemap size approaching limits**
- **Evidence:** 318 URLs in a single sitemap. While under the 50,000 URL / 50MB limit, this will grow as more content is added.
- **Fix:** Split into a sitemap index when approaching 500+ URLs: `sitemap-index.xml` containing `sitemap-poems.xml`, `sitemap-rhymes.xml`, etc.

---

### ⚠️ Site Speed & Core Web Vitals — Needs Attention

| Check | Status | Evidence |
|-------|--------|----------|
| Cache Headers | **Poor** | `Cache-Control: public, max-age=0, must-revalidate` on all pages |
| CDN | **Good** | Vercel Edge Network (X-Vercel-Cache: HIT) |
| Image Format | **Good** | WebP used (`logo-96.webp`, `writer-480.webp`) |
| Lazy Loading | **Good** | `loading="lazy"` on images |
| Mobile Viewport | **Good** | `width=device-width, initial-scale=1.0` |

#### 🔴 Critical Issue — No HTTP Caching

- **Issue:** `max-age=0` forces the browser to revalidate every request. Even though Vercel serves cached responses (`X-Vercel-Cache: HIT`), the browser still makes a conditional request.
- **Impact:** Slower page loads, worse Core Web Vitals (LCP, INP), higher server load, poor mobile experience on slow networks.
- **Fix:** For static content, set `Cache-Control: public, max-age=3600, s-maxage=86400, stale-while-revalidate=604800`. For poem pages that rarely change, even `max-age=86400` (1 day) or longer is appropriate.

---

### ✅ Mobile-Friendliness — Good

- Responsive viewport configured
- No separate m. subdomain
- Tap targets (navigation links) are text-based and likely adequately sized
- Images use `width` and `height` attributes to prevent CLS

---

### ⚠️ URL Structure — Critical Weakness

| Current URL | SEO-Optimized URL |
|-------------|-------------------|
| `/poem/1` | `/poem/jum-haba` |
| `/poem/2` | `/poem/areyia-dinun` |
| `/rhyme/1` | `/rhyme/beng-dogotton` |
| `/story/1` | `/story/megho-pidhe` |
| `/song/1` | `/song/ami-nuo-dinor` |
| `/books/ful-bareng` | ✅ Already good |

- **Impact:** Numeric IDs provide zero keyword relevance in URLs. Google uses URL paths as a ranking signal. Slug-based URLs are more shareable, memorable, and indexable.
- **Fix:** Implement a slug field in the CMS/database. Redirect old numeric URLs to new slug URLs with 301. Ensure canonicals update to the new URLs.

---

## 2. On-Page SEO Findings

### ✅ Title Tags — Good

- All pages have unique, descriptive titles
- Primary keyword near the beginning
- Format: `[Content Title] | [Type] — [Brand]` (e.g., `জুম হাবা | কবিতা — আলোময় চাকমা`)
- Length: Appropriate for all checked pages

### ⚠️ Meta Descriptions — Mixed Quality

| Page | Description | Length | Assessment |
|------|-------------|--------|------------|
| Homepage | আলোময় চাকমার সাহিত্যিক পোর্টফোলিও — চাঙমা ভাষার কবিতা, ছড়া, ছোটগল্প ও গান এবং গভীর জীবনানুভূতির এক ডিজিটাল সংগ্রহশালা। | ~160 chars | ✅ Good |
| `/about` | Alomoy Chakma biography, published books... | ~120 chars | ⚠️ English-only (inconsistent) |
| `/poem/1` | জুম হাবা — ভাত্তুন্ অলাক্ হগরা, খে লগই য' থরা থরা, | ~50 chars | 🔴 Too short / thin |
| `/song/1` | আমি নুও দিনোর গাবুজ্যে-গাবুরী — আমি নুও দিনোর গাবুজ্যে-গাবুরী। | ~60 chars | 🔴 Too short / repetitive |

- **Issue:** Poem and song pages use the first line(s) as the description. This is often too short and lacks context about the author, themes, or why someone should read it.
- **Fix:** Generate richer descriptions: *"জুম হাবা — আলোময় চাকমার চাঙমা ভাষায় রচিত কবিতা। পার্বত্য চট্টগ্রামের জুম চাষ ও প্রকৃতির প্রতি ভালোবাসার কাব্যিক প্রকাশ।"* (approx. 150 chars)

---

### ⚠️ Heading Structure — Needs Improvement

**Homepage:**
- H1: `আলোময় চাকমার চাঙমা সাহিত্য সম্ভার` ✅ Good
- Section headings appear to be H2s ✅ Good hierarchy

**Individual Poem Pages (`/poem/1`):**
- H1: `জুম হাবা` ✅ Good
- No H2, H3, or H4 for poem body structure ⚠️
- **Fix:** Add H2 subheadings for thematic sections if the poem is long. At minimum, add an H2 for "কবিতার বিষয়বস্তু" or similar context to add semantic structure.

**Category Pages (`/category/poem`):**
- H1: `কবিতা / Chakma Poems` ✅ Good
- **185 H2 tags** for each poem title ⚠️ Excessive
- **Issue:** 185 H2 tags is excessive. It dilutes heading hierarchy and creates a very large DOM. This can hurt page load and user experience.
- **Fix:** Implement pagination (e.g., 20-30 poems per page) or lazy loading. Use `<ul>`/`<li>` with standard links instead of H2 for list items. Reserve H2 for sections like "নতুন কবিতা", "জনপ্রিয় কবিতা".

---

### ✅ Image Optimization — Good

- All images have `alt` text ✅
- WebP format used ✅
- `loading="lazy"` present ✅
- `width` and `height` attributes set ✅
- `decoding="async"` used ✅

**Minor Note:** The `og-banner.png` is used as the Open Graph image for every page. Consider generating unique OG images for individual poems or books, or at least use the book cover image for book pages.

---

### ✅ Social / Open Graph Tags — Excellent

- `og:title`, `og:description`, `og:url`, `og:image`, `og:type`, `og:site_name`, `og:locale` all present ✅
- Twitter Card tags (`twitter:card`, `twitter:title`, `twitter:description`, `twitter:image`) all present ✅
- `og:locale` is correctly `bn_BD` ✅

---

## 3. Schema Markup (Structured Data) — Good Foundation, Room to Grow

### ✅ Present Schemas

| Schema Type | Page | Status |
|-------------|------|--------|
| `Person` | Homepage | ✅ Author profile with `sameAs`, `jobTitle`, `nationality` |
| `WebSite` | Homepage | ✅ With `SearchAction` |
| `Book` | Homepage | ✅ 5 books listed with publisher, date, genre |
| `Book` | Book pages | ✅ Likely present (needs JS render to confirm) |

### ⚠️ Missing Schemas

| Missing Schema | Where Needed | Impact |
|----------------|--------------|--------|
| `BreadcrumbList` | All pages | Medium — Enables breadcrumb rich snippets |
| `Article` / `CreativeWork` | Poem, Story, Song pages | Medium — Better indexing of creative content |
| `FAQPage` | Homepage / Book pages | Low — Could win "People Also Ask" |
| `Review` / `AggregateRating` | Book pages | Low — Rich star ratings in SERP |
| `Organization` | Homepage | Low — For the publisher entity |

**Note:** The `Book` schema on the homepage only lists 5 books. Ensure all book pages have their own dedicated `Book` schema in the `<head>`.

---

## 4. Content Quality Assessment

### ✅ E-E-A-T Signals — Strong

| Signal | Evidence | Status |
|--------|----------|--------|
| **Experience** | Original Chakma language poetry, first-hand cultural content | ✅ Strong |
| **Expertise** | Published author with 5+ books, established poet | ✅ Strong |
| **Authoritativeness** | Google shows indexed pages for `site:alomoychakma.com` | ✅ Moderate |
| **Trustworthiness** | HTTPS, contact email, author bio, privacy not explicitly stated | ⚠️ Partial |

**Minor Note:** No explicit Privacy Policy or Terms page found. While not critical for a literature portfolio, it is a trust signal. Consider adding a simple footer link to a Privacy Policy page (especially if contact forms collect data).

---

## 5. Indexation Status (Google Search)

Based on `site:alomoychakma.com` search results:

| Finding | Status |
|---------|--------|
| Homepage indexed | ✅ Yes |
| Book pages indexed | ✅ Yes (Ful Bareng, Hakkeng Hakkeng, Tinnomuri, Monpudi, Nauri) |
| About page indexed | ✅ Yes |
| Song pages indexed | ⚠️ Only `/song/6` seen; others may be indexed but not surfaced in top 10 |
| Poem pages indexed | ⚠️ Not visible in top 10 results — likely due to thin content + numeric URLs |

**Note:** The fact that individual poem pages (`/poem/1`, `/poem/2`, etc.) are not appearing in the search results suggests they may not be ranking well. This is consistent with the thin meta descriptions and non-semantic URLs.

---

## 6. Prioritized Action Plan

### 🔴 Phase 1 — Critical Fixes (Do Immediately)

| # | Action | Expected Impact |
|---|--------|-----------------|
| 1.1 | **Enable HTTP caching** in Vercel config: set `Cache-Control: public, max-age=86400, s-maxage=604800` for static pages | Faster load times, better Core Web Vitals, higher rankings |
| 1.2 | **Add URL slugs** to all content pages: redirect `/poem/1` → `/poem/jum-haba` (301) | Better keyword relevance, higher CTR, easier sharing |
| 1.3 | **Add pagination** to `/category/poem` (20-30 items per page) | Smaller page size, faster rendering, better crawlability |

### 🟡 Phase 2 — High-Impact Improvements (Do This Month)

| # | Action | Expected Impact |
|---|--------|-----------------|
| 2.1 | **Rewrite meta descriptions** for all poem/story/song pages (150-160 chars, include themes, context) | Better CTR, stronger relevance signals |
| 2.2 | **Add `BreadcrumbList` JSON-LD** to all pages | Breadcrumb rich snippets, better site structure understanding |
| 2.3 | **Add `Article` / `CreativeWork` schema** to poem/story/song pages with `text` property | Better content indexing, potential rich results |
| 2.4 | **Fix `lastmod` dates** in sitemap to reflect actual content dates | Better crawl budget allocation |
| 2.5 | **Add `keywords` meta** to all pages (consistent with homepage) | Minor relevance reinforcement |

### 🟢 Phase 3 — Quick Wins & Long-Term (Do When Possible)

| # | Action | Expected Impact |
|---|--------|-----------------|
| 3.1 | **Create unique OG images** for book pages and popular poems | Better social sharing engagement |
| 3.2 | **Add a Privacy Policy page** and link in footer | Trust signal, compliance |
| 3.3 | **Submit sitemap to Google Search Console** and monitor Coverage report | Ensure all 318 URLs are discovered |
| 3.4 | **Add FAQ schema** to homepage for common questions about Chakma literature | "People Also Ask" eligibility |
| 3.5 | **Create a `sitemap-index.xml`** when URL count exceeds 500 | Better sitemap management |
| 3.6 | **Add H2 subheadings** to long poems or category pages | Better semantic structure |
| 3.7 | **Build internal linking** between related poems and books | Better crawl depth, topical authority |

---

## 7. Scorecard

| Category | Score | Notes |
|----------|-------|-------|
| **Crawlability & Indexation** | 8/10 | Solid, minor sitemap issues |
| **Technical Foundations** | 6/10 | Cache headers are a major weakness |
| **On-Page SEO** | 7/10 | Good titles, thin descriptions, weak URLs |
| **Content Quality** | 9/10 | Authentic, unique, culturally valuable |
| **Schema & Structured Data** | 7/10 | Good foundation, missing breadcrumbs & article schema |
| **Mobile & UX** | 8/10 | Responsive, but category page is too large |
| **Authority & Trust** | 7/10 | Strong author profile, missing privacy policy |
| **Overall** | **7.4/10** | Good foundation with clear optimization path |

---

*Report generated by Kimi SEO Audit Skill. For Core Web Vitals scores and mobile render testing, please connect the Kimi WebBridge browser extension and re-run the audit for real-time PageSpeed analysis.*
