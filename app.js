// ----------------------------------------------------
// Literary Minimalist - Application Scripts
// Writer: Alomoy Chakma (আলোময় চাকমা)
// ----------------------------------------------------

// 1. Database of Literary Works (All content in Bengali)
let writings = []; // Loaded from writings.json

// Load writings data from external JSON (improves performance)
async function loadWritingsData() {
  try {
    const response = await fetch('./writings.json?v=1781014789828');
    if (!response.ok) throw new Error('Failed to fetch writings.json');
    const defaultWritings = await response.json();
    writings = defaultWritings;
    
    // Check if localStorage has updated writings (e.g. from admin panel) and merge
    // Keep new bundled entries visible even when a browser has older admin data cached.
    if (localStorage.getItem("granthagor_writings")) {
      try {
        const savedWritings = JSON.parse(localStorage.getItem("granthagor_writings"));
        const savedIds = new Set(savedWritings.map((writing) => writing.id));
        writings = [
          ...savedWritings,
          ...defaultWritings.filter((writing) => !savedIds.has(writing.id))
        ];
      } catch (e) {
        console.error("Error loading writings from localStorage:", e);
      }
    }
  } catch(e) {
    console.warn('Could not load writings.json, falling back to empty:', e.message);
  }
}

// 2. Application State

// Convert numbers to Bengali digits
function toBengaliNumber(num) {
  const mapping = {
    '0': '০', '1': '১', '2': '২', '3': '৩', '4': '৪',
    '5': '৫', '6': '৬', '7': '৭', '8': '৮', '9': '৯'
  };
  return String(num).split('').map(char => mapping[char] || char).join('');
}

// Generate pagination HTML structure
function generatePaginationHtml(currentPage, totalPages, type) {
  let html = `<div class="pagination-container">`;
  
  const prevDisabled = currentPage === 1 ? 'disabled' : '';
  html += `
    <button class="page-btn page-btn-prev" ${prevDisabled} data-type="${type}" data-page="${currentPage - 1}">
      <span class="material-symbols-outlined" style="font-size: 16px;">chevron_left</span>
      পূর্ববর্তী
    </button>
  `;
  
  const range = [];
  if (totalPages <= 7) {
    for (let i = 1; i <= totalPages; i++) {
      range.push(i);
    }
  } else {
    range.push(1);
    
    let start = Math.max(2, currentPage - 1);
    let end = Math.min(totalPages - 1, currentPage + 1);
    
    if (currentPage <= 3) {
      end = 4;
    } else if (currentPage >= totalPages - 2) {
      start = totalPages - 3;
    }
    
    if (start > 2) {
      range.push('...');
    }
    
    for (let i = start; i <= end; i++) {
      range.push(i);
    }
    
    if (end < totalPages - 1) {
      range.push('...');
    }
    
    range.push(totalPages);
  }
  
  range.forEach(item => {
    if (item === '...') {
      html += `<span class="page-ellipsis">...</span>`;
    } else {
      const activeClass = currentPage === item ? 'active' : '';
      html += `
        <button class="page-btn page-btn-num ${activeClass}" data-type="${type}" data-page="${item}">
          ${toBengaliNumber(item)}
        </button>
      `;
    }
  });
  
  const nextDisabled = currentPage === totalPages ? 'disabled' : '';
  html += `
    <button class="page-btn page-btn-next" ${nextDisabled} data-type="${type}" data-page="${currentPage + 1}">
      পরবর্তী
      <span class="material-symbols-outlined" style="font-size: 16px;">chevron_right</span>
    </button>
  `;
  
  html += `</div>`;
  return html;
}

// Bind pagination click events and handle smooth-scroll
function bindPaginationEvents(paginationContainer, type, sectionHeaderSelector) {
  if (!paginationContainer) return;
  const buttons = paginationContainer.querySelectorAll(".page-btn");
  buttons.forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      if (btn.disabled || btn.hasAttribute("disabled")) return;
      const page = parseInt(btn.getAttribute("data-page"), 10);
      if (isNaN(page)) return;
      
      if (type === 'poem') {
        state.poemPage = page;
      } else if (type === 'rhyme') {
        state.rhymePage = page;
      } else if (type === 'story') {
        state.storyPage = page;
      } else if (type === 'song') {
        state.songPage = page;
      }
      
      renderContent();
      
      const section = document.querySelector(sectionHeaderSelector);
      if (section) {
        section.scrollIntoView({ behavior: "smooth", block: "start" });
      }
    });
  });
}

const state = {
  currentPage: "home", // "home", "about", "reader"
  currentCategory: "all", // "all", "poem", "rhyme", "story", "song"
  currentReadingId: null,
  poemPage: 1,
  rhymePage: 1,
  storyPage: 1,
  songPage: 1
};

// 3. Elements Selector Cache
const elements = {
  body: document.body,
  navLinks: document.querySelectorAll(".nav-link"),
  // Views
  homeView: document.getElementById("homeView"),
  aboutView: document.getElementById("aboutView"),
  readerView: document.getElementById("readerView"),
  
  // Grid/Lists
  featuredContainer: document.getElementById("featuredContainer"),
  poetrySection: document.getElementById("poetrySection"),
  poetryContainer: document.getElementById("poetryContainer"),
  poetryPagination: document.getElementById("poetryPagination"),
  rhymesSection: document.getElementById("rhymesSection"),
  rhymesContainer: document.getElementById("rhymesContainer"),
  rhymesPagination: document.getElementById("rhymesPagination"),
  storiesSection: document.getElementById("storiesSection"),
  storiesContainer: document.getElementById("storiesContainer"),
  storiesPagination: document.getElementById("storiesPagination"),
  songsSection: document.getElementById("songsSection"),
  songsContainer: document.getElementById("songsContainer"),
  songsPagination: document.getElementById("songsPagination"),
  
  // Filter tabs
  filterTabs: document.querySelectorAll(".filter-tab"),
  
  // Reader Detail Elements
  readerContent: document.getElementById("readerContent"),
  backButton: document.getElementById("backButton"),
  
  // Modal Drawer
  contactBtn: document.getElementById("contactBtn"),
  footerContactBtn: document.getElementById("footerContactBtn"),
  contactModal: document.getElementById("contactModal"),
  closeModal: document.getElementById("closeModal"),
  contactForm: document.getElementById("contactForm"),
  
  // Newsletter Form
  newsletterForm: document.getElementById("newsletterForm"),
  
  // Toast container
  toastContainer: document.getElementById("toastContainer")
};

// ─── SEO Constants ───
const SITE_URL = "https://alomoy.vercel.app";
const SITE_DEFAULT_TITLE = "গ্রন্থাগার | আলোময় চাকমা — চাঙমা সাহিত্য সম্ভার";
const SITE_DEFAULT_DESC  = "আলোময় চাকমার সাহিত্যিক পোর্টফোলিও — চাঙমা ভাষার কবিতা, ছড়া, ছোটগল্প ও গান এবং গভীর জীবনানুভূতির এক ডিজিটাল সংগ্রহশালা।";

// ─── Dynamic SEO updater ───
function updateSEOMeta({ title, description, url }) {
  const t = title || SITE_DEFAULT_TITLE;
  const d = description || SITE_DEFAULT_DESC;
  const u = url || SITE_URL + "/";

  document.title = t;
  setMeta("pageDesc",  d, "content");
  setMeta("ogTitle",   t, "content");
  setMeta("ogDesc",    d, "content");
  setMeta("ogUrl",     u, "content");
  setMeta("twTitle",   t, "content");
  setMeta("twDesc",    d, "content");
  const canonical = document.getElementById("canonicalUrl");
  if (canonical) canonical.setAttribute("href", u);
}
function setMeta(id, value, attr) {
  const el = document.getElementById(id);
  if (el) el.setAttribute(attr, value);
}

// ─── Share Utility ───
function buildShareUrl(category, serialNumber) {
  return `${SITE_URL}/#${category}/${serialNumber}`;
}

function getShareHtml(shareUrl, shareTitle) {
  const fbUrl  = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
  const waUrl  = `https://wa.me/?text=${encodeURIComponent(shareTitle + " — " + shareUrl)}`;
  const twUrl  = `https://twitter.com/intent/tweet?text=${encodeURIComponent(shareTitle)}&url=${encodeURIComponent(shareUrl)}`;
  const hasNativeShare = !!navigator.share;

  return `
    <div class="reader-share-bar" id="readerShareBar" role="group" aria-label="শেয়ার করুন">
      <span class="reader-share-label">এই লেখাটি শেয়ার করুন</span>
      <a href="${fbUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--facebook" aria-label="ফেসবুকে শেয়ার করুন">
        <span class="material-symbols-outlined">thumb_up</span>
        Facebook
      </a>
      <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--whatsapp" aria-label="হোয়াটসঅ্যাপে শেয়ার করুন">
        <span class="material-symbols-outlined">chat</span>
        WhatsApp
      </a>
      <a href="${twUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--twitter" aria-label="X (Twitter)-এ শেয়ার করুন">
        <span class="material-symbols-outlined">close</span>
        𝕏 Twitter
      </a>
      <button class="share-btn share-btn--copy" data-copy-url="${shareUrl}" aria-label="লিংক কপি করুন">
        <span class="material-symbols-outlined">content_copy</span>
        লিংক কপি
      </button>
      ${hasNativeShare ? `<button class="share-btn share-btn--native" id="nativeShareBtn" aria-label="শেয়ার করুন">
        <span class="material-symbols-outlined">share</span>
        শেয়ার
      </button>` : ""}
    </div>
  `;
}

function buildSectionSharePopupHtml(shareUrl, categoryName) {
  const fbUrl  = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(shareUrl)}`;
  const waUrl  = `https://wa.me/?text=${encodeURIComponent(categoryName + " — আলোময় চাকমার " + categoryName + " সংগ্রহ: " + shareUrl)}`;
  const twUrl  = `https://twitter.com/intent/tweet?text=${encodeURIComponent("আলোময় চাকমার " + categoryName + " পড়ুন:")}&url=${encodeURIComponent(shareUrl)}`;
  return `
    <div class="share-popup" role="dialog" aria-label="${categoryName} শেয়ার">
      <div class="share-popup-title">${categoryName} শেয়ার করুন</div>
      <div class="share-popup-btns">
        <a href="${fbUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--facebook">Facebook</a>
        <a href="${waUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--whatsapp">WhatsApp</a>
        <a href="${twUrl}" target="_blank" rel="noopener noreferrer" class="share-btn share-btn--twitter">𝕏 Twitter</a>
        <button class="share-btn share-btn--copy" data-copy-url="${shareUrl}">লিংক কপি</button>
      </div>
    </div>
  `;
}

function bindShareEvents(container) {
  if (!container) return;
  // Copy buttons
  container.querySelectorAll(".share-btn--copy[data-copy-url]").forEach(btn => {
    btn.addEventListener("click", (e) => {
      e.preventDefault();
      const url = btn.getAttribute("data-copy-url");
      navigator.clipboard.writeText(url).then(() => {
        showToast("লিংকটি কপি হয়েছে!");
      }).catch(() => {
        showToast("লিংক: " + url);
      });
    });
  });
  // Native share button
  const nativeBtn = container.querySelector("#nativeShareBtn");
  if (nativeBtn && navigator.share) {
    nativeBtn.addEventListener("click", async () => {
      try {
        const url = container.querySelector(".share-btn--copy")?.getAttribute("data-copy-url") || SITE_URL;
        await navigator.share({ title: document.title, url });
      } catch (err) {
        // User cancelled — do nothing
      }
    });
  }
}

function openSectionSharePopup(wrapEl, shareUrl, categoryName) {
  // Close any existing
  document.querySelectorAll(".share-popup").forEach(p => p.remove());
  document.querySelectorAll(".share-popup-overlay").forEach(o => o.remove());

  const popup = document.createElement("div");
  popup.innerHTML = buildSectionSharePopupHtml(shareUrl, categoryName);
  const popupEl = popup.firstElementChild;
  wrapEl.appendChild(popupEl);

  // Overlay to close on outside click
  const overlay = document.createElement("div");
  overlay.className = "share-popup-overlay";
  document.body.appendChild(overlay);
  overlay.addEventListener("click", () => {
    popupEl.remove();
    overlay.remove();
  });

  bindShareEvents(popupEl);
}

// ─── Hash routing helpers ───
function getCategorySerial(writing) {
  const sameCat = writings.filter(w => w.category === writing.category);
  return sameCat.findIndex(w => w.id === writing.id) + 1;
}

function pushHash(hashStr) {
  history.pushState(null, "", "#" + hashStr);
}

function routeFromHash(hash) {
  if (!hash || hash === "#" || hash === "#home") {
    switchPage("home", false);
    return;
  }
  if (hash === "#about") {
    switchPage("about", false);
    return;
  }
  const catMatch = hash.match(/^#category\/(.+)$/);
  if (catMatch) {
    const cat = catMatch[1];
    const validCats = ["all", "poem", "rhyme", "story", "song"];
    if (validCats.includes(cat)) {
      switchPage("home", false);
      state.currentCategory = cat;
      elements.filterTabs.forEach(t => {
        t.classList.toggle("active", t.getAttribute("data-category") === cat);
      });
      renderContent();
      return;
    }
  }
  // Pattern: #poem/3, #rhyme/7, #story/2, #song/1
  const articleMatch = hash.match(/^#(poem|rhyme|story|song)\/([0-9]+)$/);
  if (articleMatch) {
    const cat = articleMatch[1];
    const serial = parseInt(articleMatch[2], 10);
    const catWritings = writings.filter(w => w.category === cat);
    const writing = catWritings[serial - 1];
    if (writing) {
      openReaderView(writing.id, false);
      return;
    }
  }
  // Fallback
  switchPage("home", false);
}

// 4. Initialize Function
async function init() {
  // Load writings data from external JSON first (performance split)
  await loadWritingsData();

  // Hide and remove loading overlay
  const loadingOverlay = document.getElementById("loadingOverlay");
  if (loadingOverlay) {
    loadingOverlay.classList.add("fade-out");
    setTimeout(() => {
      loadingOverlay.remove();
    }, 450); // Matches CSS transition duration
  }

  setupNavigation();
  setupFilters();
  setupForms();
  renderContent();
  // Route from hash on load
  if (window.location.hash && window.location.hash !== "#") {
    routeFromHash(window.location.hash);
  }
  // Listen to browser back/forward
  window.addEventListener("hashchange", () => {
    routeFromHash(window.location.hash);
  });
}

// 5. Navigation Router (SPA Style Transitions)
function setupNavigation() {
  elements.navLinks.forEach(link => {
    link.addEventListener("click", (e) => {
      e.preventDefault();
      const pageTarget = link.getAttribute("data-page");
      
      if (pageTarget === "contact") {
        openContactModal();
      } else {
        switchPage(pageTarget);
      }
    });
  });
  
  // Back button in reader view
  elements.backButton.addEventListener("click", () => {
    switchPage("home");
    // Scroll back to where articles are
    const filterSection = document.querySelector(".filter-bar");
    if (filterSection) {
      filterSection.scrollIntoView({ behavior: "smooth", block: "start" });
    }
  });

  // Contact Modal triggers
  elements.contactBtn.addEventListener("click", openContactModal);
  if (elements.footerContactBtn) {
    elements.footerContactBtn.addEventListener("click", (e) => {
      e.preventDefault();
      openContactModal();
    });
  }
  elements.closeModal.addEventListener("click", closeContactModal);
  
  // Close modal when clicking outside the modal box
  elements.contactModal.addEventListener("click", (e) => {
    if (e.target === elements.contactModal) {
      closeContactModal();
    }
  });

  // Extra Navigation & Footer Links Logic
  const navWritingsLink = document.getElementById("navWritingsLink");
  if (navWritingsLink) {
    navWritingsLink.addEventListener("click", (e) => {
      e.preventDefault();
      if (state.currentPage !== "home") {
        switchPage("home");
      }
      setTimeout(() => {
        const filterSection = document.querySelector(".filter-bar");
        if (filterSection) {
          filterSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 50);
    });
  }

  const footerNewsletterLink = document.getElementById("footerNewsletterLink");
  if (footerNewsletterLink) {
    footerNewsletterLink.addEventListener("click", (e) => {
      e.preventDefault();
      const newsSection = document.querySelector(".newsletter-section");
      if (newsSection) {
        newsSection.scrollIntoView({ behavior: "smooth" });
        setTimeout(() => {
          const input = newsSection.querySelector("input");
          if (input) input.focus();
        }, 600);
      }
    });
  }



  const footerPdfCollectionLink = document.getElementById("footerPdfCollectionLink");
  if (footerPdfCollectionLink) {
    footerPdfCollectionLink.addEventListener("click", (e) => {
      e.preventDefault();
      if (state.currentPage !== "home") {
        switchPage("home");
      }
      setTimeout(() => {
        const pdfSection = document.getElementById("pdfCollectionSection");
        if (pdfSection) {
          pdfSection.scrollIntoView({ behavior: "smooth", block: "start" });
        }
      }, 50);
    });
  }
}

function switchPage(pageId, updateHash = true) {
  state.currentPage = pageId;
  state.currentReadingId = null;

  // Clean up reader background classes if navigating away
  elements.body.classList.remove("rhyme-reader-active");
  elements.body.classList.remove("poem-reader-active");
  elements.body.classList.remove("story-reader-active");
  elements.body.classList.remove("song-reader-active");

  // Update active state in navigation links
  elements.navLinks.forEach(link => {
    const pageTarget = link.getAttribute("data-page");
    if (pageTarget === pageId) {
      link.classList.add("active");
    } else {
      link.classList.remove("active");
    }
  });

  // Handle transitions and displays
  if (pageId === "home") {
    elements.homeView.style.display = "block";
    elements.aboutView.style.display = "none";
    elements.readerView.style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (updateHash) pushHash("home");
    updateSEOMeta({
      title: SITE_DEFAULT_TITLE,
      description: SITE_DEFAULT_DESC,
      url: SITE_URL + "/#home"
    });
  } else if (pageId === "about") {
    elements.homeView.style.display = "none";
    elements.aboutView.style.display = "block";
    elements.readerView.style.display = "none";
    window.scrollTo({ top: 0, behavior: "smooth" });
    if (updateHash) pushHash("about");
    updateSEOMeta({
      title: "পরিচিতি | আলোময় চাকমা",
      description: "আলোময় চাকমা — চাঙমা ভাষার কবি ও কথাসাহিত্যিক। পার্বত্য চট্টগ্রামের জীবন ও প্রকৃতি নিয়ে রচিত সাহিত্যের স্রষ্টার পরিচয়।",
      url: SITE_URL + "/#about"
    });
  }
}

// 7. Reading View Dynamic Rendering
function openReaderView(articleId, updateHash = true) {
  const article = writings.find(w => w.id === articleId);
  if (!article) return;

  state.currentPage = "reader";
  state.currentReadingId = articleId;

  // Find serial number for this category
  const categoryWritings = writings.filter(w => w.category === article.category);
  const articleIndex = categoryWritings.findIndex(w => w.id === article.id);
  const serialNumBengali = toBengaliNumber(articleIndex + 1);
  const serialNumInt = articleIndex + 1;

  // Build share URL: https://alomoy.vercel.app/#poem/3
  const shareUrl = buildShareUrl(article.category, serialNumInt);

  // Update URL hash
  if (updateHash) pushHash(`${article.category}/${serialNumInt}`);

  // Toggle background image for reader categories
  const allReaderClasses = ["rhyme-reader-active", "poem-reader-active", "story-reader-active", "song-reader-active"];
  allReaderClasses.forEach(c => elements.body.classList.remove(c));
  if (article.category === "rhyme")  elements.body.classList.add("rhyme-reader-active");
  if (article.category === "poem")   elements.body.classList.add("poem-reader-active");
  if (article.category === "story")  elements.body.classList.add("story-reader-active");
  if (article.category === "song")   elements.body.classList.add("song-reader-active");

  // Update SEO for this article
  const articleDesc = article.excerpt
    ? `${article.badge} — ${article.excerpt.slice(0, 120)}`
    : `${article.badge} | আলোময় চাকমা`;
  updateSEOMeta({
    title: `${serialNumBengali}. ${article.title} | ${article.badge} — আলোময় চাকমা`,
    description: articleDesc,
    url: shareUrl
  });

  // Render details inside reader
  let contentHtml = "";
  if (article.category === "poem" || article.category === "rhyme" || article.category === "song") {
    article.content.forEach(line => {
      if (line === "__STANZA__") {
        contentHtml += `<p class="poem-stanza-break"></p>`;
      } else {
        contentHtml += `<p class="poem-line">${line}</p>`;
      }
    });
  } else {
    article.content.forEach((para, idx) => {
      if (idx === 0 && article.quote) {
        contentHtml += `<p class="body-lg">${para}</p>`;
        contentHtml += `<blockquote class="block-quote">${article.quote}</blockquote>`;
      } else {
        contentHtml += `<p>${para}</p>`;
      }
    });
  }

  // Build share bar HTML
  const shareBarHtml = getShareHtml(shareUrl, `${article.title} — আলোময় চাকমা`);

  elements.readerContent.innerHTML = `
    <div class="reader-header">
      <span class="label-sm text-secondary uppercase tracking-widest block mb-2">${article.badge}</span>
      <h1 class="headline-lg">${serialNumBengali}. ${article.title}</h1>
      <div class="reader-meta">
        <span>${article.date}</span>
        <span style="margin: 0 12px;">—</span>
        <span>${article.readTime}</span>
      </div>
    </div>
    <div class="reader-content">
      ${contentHtml}
    </div>
    ${shareBarHtml}
  `;

  // Bind share events inside reader
  bindShareEvents(elements.readerContent);

  // Smooth scroll to top and switch view
  elements.homeView.style.display = "none";
  elements.aboutView.style.display = "none";
  elements.readerView.style.display = "block";
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// 8. Filters setup (Category Tabs)
function setupFilters() {
  elements.filterTabs.forEach(tab => {
    tab.addEventListener("click", () => {
      elements.filterTabs.forEach(t => t.classList.remove("active"));
      tab.classList.add("active");
      
      state.currentCategory = tab.getAttribute("data-category");
      state.poemPage = 1;
      state.rhymePage = 1;
      state.storyPage = 1;
      state.songPage = 1;
      renderContent();
    });
  });
}

// 9. Forms & Validation Handler
function setupForms() {
  // Newsletter form submission
  if (elements.newsletterForm) {
    elements.newsletterForm.addEventListener("submit", (e) => {
      e.preventDefault();
      const emailInput = elements.newsletterForm.querySelector("input[type='email']");
      const email = emailInput.value.trim();
      
      if (email === "") {
        showToast("দয়া করে একটি সঠিক ইমেইল ঠিকানা দিন।");
        return;
      }
      
      // Simulate API Call
      showToast("নিউজলেটারে সফলভাবে সাবস্ক্রাইব করা হয়েছে!");
      emailInput.value = "";
    });
  }
  
  // Contact form — real email via FormSubmit.co (free, no signup needed)
  elements.contactForm.addEventListener("submit", async (e) => {
    e.preventDefault();
    const nameInput    = document.getElementById("contactName");
    const emailInput   = document.getElementById("contactEmail");
    const messageInput = document.getElementById("contactMessage");
    const submitBtn    = elements.contactForm.querySelector("button[type='submit']");

    const name    = nameInput.value.trim();
    const email   = emailInput.value.trim();
    const message = messageInput.value.trim();

    if (!name || !email || !message) {
      showToast("\u09b8\u09ac\u0997\u09c1\u09b2\u09cb \u0998\u09b0 \u09b8\u09a0\u09bf\u0995\u09ad\u09be\u09ac\u09c7 \u09aa\u09c2\u09b0\u09a3 \u0995\u09b0\u09c1\u09a8\u0964");
      return;
    }

    // Show loading state on button
    const originalBtnText = submitBtn.textContent;
    submitBtn.textContent  = "\u09aa\u09be\u09a0\u09be\u09a8\u09cb \u09b9\u099a\u09cd\u099b\u09c7\u2026";
    submitBtn.disabled     = true;

    try {
      const response = await fetch("https://formsubmit.co/ajax/alomoyc6@gmail.com", {
        method:  "POST",
        headers: { "Content-Type": "application/json", "Accept": "application/json" },
        body: JSON.stringify({
          name:      name,
          email:     email,
          message:   message,
          _subject:  "\u0997\u09cd\u09b0\u09a8\u09cd\u09a5\u09be\u0997\u09be\u09b0 \u2014 \u09a8\u09a4\u09c1\u09a8 \u09ac\u09be\u09b0\u09cd\u09a4\u09be: " + name,
          _template: "table",
          _captcha:  "false"
        })
      });

      const result = await response.json();

      if (response.ok && result.success === "true") {
        showToast("\u2705 \u0986\u09aa\u09a8\u09be\u09b0 \u09ac\u09be\u09b0\u09cd\u09a4\u09be \u0986\u09b2\u09cb\u09ae\u09af\u09bc \u099a\u09be\u0995\u09ae\u09be\u09b0 \u0995\u09be\u099b\u09c7 \u09aa\u09be\u09a0\u09be\u09a8\u09cb \u09b9\u09af\u09bc\u09c7\u099b\u09c7!");
        closeContactModal();
        nameInput.value    = "";
        emailInput.value   = "";
        messageInput.value = "";
      } else {
        showToast("\u2716 \u09ac\u09be\u09b0\u09cd\u09a4\u09be \u09aa\u09be\u09a0\u09be\u09a8\u09cb \u09af\u09be\u09af\u09bc\u09a8\u09bf\u0964 \u09b8\u09b0\u09be\u09b8\u09b0\u09bf alomoyc6@gmail.com \u098f\u09b0 \u0995\u09be\u099b\u09c7 \u0987\u09ae\u09c7\u0987\u09b2 \u0995\u09b0\u09c1\u09a8\u0964");
      }
    } catch (err) {
      showToast("\u2716 \u09a8\u09c7\u099f\u0993\u09af\u09bc\u09be\u09b0\u09cd\u0995 \u09b8\u09ae\u09b8\u09cd\u09af\u09be\u0964 \u09b8\u09b0\u09be\u09b8\u09b0\u09bf alomoyc6@gmail.com \u098f\u09b0 \u0995\u09be\u099b\u09c7 \u0987\u09ae\u09c7\u0987\u09b2 \u0995\u09b0\u09c1\u09a8\u0964");
    } finally {
      submitBtn.textContent = originalBtnText;
      submitBtn.disabled    = false;
    }
  });
}

function openContactModal() {
  elements.contactModal.style.display = "block";
  // Force a reflow to trigger animation
  elements.contactModal.offsetHeight;
  elements.contactModal.classList.add("open");
  elements.body.style.overflow = "hidden"; // Disable scroll when modal is open
}

function closeContactModal() {
  elements.contactModal.classList.remove("open");
  elements.body.style.overflow = ""; // Re-enable scroll
  // Delay removing display block until slide transition is done
  setTimeout(() => {
    if (!elements.contactModal.classList.contains("open")) {
      elements.contactModal.style.display = "none";
    }
  }, 300);
}

// 11. Toast Notifications Manager
function showToast(message) {
  const toast = document.createElement("div");
  toast.className = "toast";
  toast.innerHTML = `
    <span class="material-symbols-outlined text-[18px]">done</span>
    <span>${message}</span>
  `;
  
  elements.toastContainer.appendChild(toast);
  
  // Auto remove after 4 seconds
  setTimeout(() => {
    toast.classList.add("fade-out");
    toast.addEventListener("animationend", () => {
      toast.remove();
    });
  }, 3500);
}

// 12. View Renderer (Dynamic HTML Generator)
function renderContent() {
  const category = state.currentCategory;
  
  // Filter writings
  const filtered = writings.filter(w => category === "all" || w.category === category);
  
  // A. Render Featured Card
  const featured = writings.find(w => w.isFeatured);
  if (featured && (category === "all" || category === featured.category)) {
    const allStories = writings.filter(w => w.category === "story");
    const sIdx = allStories.findIndex(s => s.id === featured.id);
    const serialNum = toBengaliNumber(sIdx + 1);
    elements.featuredContainer.style.display = "block";
    elements.featuredContainer.innerHTML = `
      <div class="grid-12">
        <div class="col-8">
          <div class="writing-card group" data-id="${featured.id}">
            <div>
              <span class="card-category">${featured.badge}</span>
              <h2 class="headline-md card-title">${serialNum}. ${featured.title}</h2>
              <p class="body-md card-excerpt">${featured.excerpt}</p>
            </div>
            <div class="card-meta">
              <span>${featured.date} — ${featured.readTime}</span>
              <a href="#" class="card-link font-label-md">
                গল্পটি পড়ুন <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
              </a>
            </div>
          </div>
        </div>
        <div class="col-4">
          <div class="mood-card">
            <img src="screen.png" alt="বই এবং দোয়াত কালির নান্দনিক ছবি" class="mood-image">
            <div class="mood-overlay">
              <p class="mood-quote">"${featured.quote}"</p>
            </div>
          </div>
        </div>
      </div>
    `;
    
    // Bind click event to featured card
    elements.featuredContainer.querySelector(".writing-card").addEventListener("click", (e) => {
      e.preventDefault();
      openReaderView(featured.id);
    });
  } else {
    elements.featuredContainer.style.display = "none";
  }
  
  // B. Render Poetry Section
  const poems = filtered.filter(w => w.category === "poem");
  if (poems.length > 0) {
    elements.poetrySection.style.display = "block";
    // Section share button
    const poetrySectionDivider = elements.poetrySection.querySelector(".section-divider");
    if (poetrySectionDivider && !poetrySectionDivider.parentElement.classList.contains("section-divider-wrap")) {
      const wrap = document.createElement("div");
      wrap.className = "section-divider-wrap";
      poetrySectionDivider.parentNode.insertBefore(wrap, poetrySectionDivider);
      wrap.appendChild(poetrySectionDivider);
      const shareWrap = document.createElement("div");
      shareWrap.className = "section-share-wrap";
      shareWrap.innerHTML = `<button class="section-share-btn" aria-label="কবিতা শেয়ার করুন"><span class="material-symbols-outlined">share</span><span>শেয়ার</span></button>`;
      wrap.appendChild(shareWrap);
      shareWrap.querySelector(".section-share-btn").addEventListener("click", () => {
        const catUrl = SITE_URL + "/#category/poem";
        openSectionSharePopup(shareWrap, catUrl, "কবিতা");
      });
    }
    const itemsPerPage = category === "all" ? 5 : 10;
    const totalPages = Math.ceil(poems.length / itemsPerPage);
    if (state.poemPage > totalPages) state.poemPage = totalPages;
    if (state.poemPage < 1) state.poemPage = 1;
    
    const startIndex = (state.poemPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedPoems = poems.slice(startIndex, endIndex);
    
    let poemsHtml = "";
    const allPoems = writings.filter(w => w.category === "poem");
    
    paginatedPoems.forEach(poem => {
      const pIdx = allPoems.findIndex(p => p.id === poem.id);
      const serialNum = toBengaliNumber(pIdx + 1);
      poemsHtml += `
        <article class="poetry-item" data-id="${poem.id}">
          <div class="poetry-header">
            <h4 class="headline-sm poetry-title">${serialNum}. ${poem.title}</h4>
            <span class="poetry-date">${poem.date}</span>
          </div>
          <p class="body-md poetry-excerpt">${poem.excerpt}</p>
          <a href="#" class="link-editorial">কবিতাটি দেখুন</a>
        </article>
      `;
    });
    
    elements.poetryContainer.innerHTML = poemsHtml;
    
    // Render pagination
    if (totalPages > 1) {
      elements.poetryPagination.innerHTML = generatePaginationHtml(state.poemPage, totalPages, 'poem');
      bindPaginationEvents(elements.poetryPagination, 'poem', '#poetrySection');
    } else {
      elements.poetryPagination.innerHTML = "";
    }
    
    // Bind click events to poetry articles
    elements.poetryContainer.querySelectorAll(".poetry-item").forEach(item => {
      const id = item.getAttribute("data-id");
      item.querySelector(".poetry-title").addEventListener("click", () => openReaderView(id));
      item.querySelector(".link-editorial").addEventListener("click", (e) => {
        e.preventDefault();
        openReaderView(id);
      });
    });
  } else {
    elements.poetrySection.style.display = "none";
    elements.poetryPagination.innerHTML = "";
  }
  
  // C. Render Rhymes Section
  const rhymes = filtered.filter(w => w.category === "rhyme");
  if (rhymes.length > 0) {
    elements.rhymesSection.style.display = "block";
    // Section share button
    const rhymesSectionDivider = elements.rhymesSection.querySelector(".section-divider");
    if (rhymesSectionDivider && !rhymesSectionDivider.parentElement.classList.contains("section-divider-wrap")) {
      const wrap = document.createElement("div");
      wrap.className = "section-divider-wrap";
      rhymesSectionDivider.parentNode.insertBefore(wrap, rhymesSectionDivider);
      wrap.appendChild(rhymesSectionDivider);
      const shareWrap = document.createElement("div");
      shareWrap.className = "section-share-wrap";
      shareWrap.innerHTML = `<button class="section-share-btn" aria-label="ছড়া শেয়ার করুন"><span class="material-symbols-outlined">share</span><span>শেয়ার</span></button>`;
      wrap.appendChild(shareWrap);
      shareWrap.querySelector(".section-share-btn").addEventListener("click", () => {
        const catUrl = SITE_URL + "/#category/rhyme";
        openSectionSharePopup(shareWrap, catUrl, "ছড়া");
      });
    }
    const itemsPerPage = category === "all" ? 5 : 10;
    const totalPages = Math.ceil(rhymes.length / itemsPerPage);
    if (state.rhymePage > totalPages) state.rhymePage = totalPages;
    if (state.rhymePage < 1) state.rhymePage = 1;
    
    const startIndex = (state.rhymePage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedRhymes = rhymes.slice(startIndex, endIndex);
    
    let rhymesHtml = "";
    const allRhymes = writings.filter(w => w.category === "rhyme");
    
    paginatedRhymes.forEach(rhyme => {
      const rIdx = allRhymes.findIndex(r => r.id === rhyme.id);
      const serialNum = toBengaliNumber(rIdx + 1);
      rhymesHtml += `
        <article class="poetry-item" data-id="${rhyme.id}">
          <div class="poetry-header">
            <h4 class="headline-sm poetry-title">${serialNum}. ${rhyme.title}</h4>
            <span class="poetry-date">${rhyme.date}</span>
          </div>
          <p class="body-md poetry-excerpt">${rhyme.excerpt}</p>
          <a href="#" class="link-editorial">ছড়াটি দেখুন</a>
        </article>
      `;
    });
    
    elements.rhymesContainer.innerHTML = rhymesHtml;
    
    // Render pagination
    if (totalPages > 1) {
      elements.rhymesPagination.innerHTML = generatePaginationHtml(state.rhymePage, totalPages, 'rhyme');
      bindPaginationEvents(elements.rhymesPagination, 'rhyme', '#rhymesSection');
    } else {
      elements.rhymesPagination.innerHTML = "";
    }
    
    // Bind click events to rhymes articles
    elements.rhymesContainer.querySelectorAll(".poetry-item").forEach(item => {
      const id = item.getAttribute("data-id");
      item.querySelector(".poetry-title").addEventListener("click", () => openReaderView(id));
      item.querySelector(".link-editorial").addEventListener("click", (e) => {
        e.preventDefault();
        openReaderView(id);
      });
    });
  } else {
    elements.rhymesSection.style.display = "none";
    elements.rhymesPagination.innerHTML = "";
  }

  // D. Render Stories Section
  const stories = filtered.filter(w => w.category === "story" && !w.isFeatured);
  if (stories.length > 0) {
    elements.storiesSection.style.display = "block";
    // Section share button
    const storiesSectionDivider = elements.storiesSection.querySelector(".section-divider");
    if (storiesSectionDivider && !storiesSectionDivider.parentElement.classList.contains("section-divider-wrap")) {
      const wrap = document.createElement("div");
      wrap.className = "section-divider-wrap";
      storiesSectionDivider.parentNode.insertBefore(wrap, storiesSectionDivider);
      wrap.appendChild(storiesSectionDivider);
      const shareWrap = document.createElement("div");
      shareWrap.className = "section-share-wrap";
      shareWrap.innerHTML = `<button class="section-share-btn" aria-label="গল্প শেয়ার করুন"><span class="material-symbols-outlined">share</span><span>শেয়ার</span></button>`;
      wrap.appendChild(shareWrap);
      shareWrap.querySelector(".section-share-btn").addEventListener("click", () => {
        const catUrl = SITE_URL + "/#category/story";
        openSectionSharePopup(shareWrap, catUrl, "ছোটগল্প");
      });
    }
    const itemsPerPage = category === "all" ? 5 : 10;
    const totalPages = Math.ceil(stories.length / itemsPerPage);
    if (state.storyPage > totalPages) state.storyPage = totalPages;
    if (state.storyPage < 1) state.storyPage = 1;
    
    const startIndex = (state.storyPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedStories = stories.slice(startIndex, endIndex);
    
    let storiesHtml = "";
    const allStories = writings.filter(w => w.category === "story");
    
    paginatedStories.forEach(story => {
      const sIdx = allStories.findIndex(s => s.id === story.id);
      const serialNum = toBengaliNumber(sIdx + 1);
      storiesHtml += `
        <div class="writing-card" data-id="${story.id}">
          <div>
            <span class="story-badge">${story.badge}</span>
            <h4 class="headline-sm" style="margin-bottom:12px;">${serialNum}. ${story.title}</h4>
            <p class="body-md card-excerpt" style="margin-bottom:24px;">${story.excerpt}</p>
          </div>
          <div class="card-meta">
            <span class="italic">${story.date}</span>
            <a href="#" class="card-link font-label-md">
              আরও পড়ুন <span class="material-symbols-outlined text-[16px]">open_in_new</span>
            </a>
          </div>
        </div>
      `;
    });
    
    elements.storiesContainer.innerHTML = storiesHtml;
    
    // Render pagination
    if (totalPages > 1) {
      elements.storiesPagination.innerHTML = generatePaginationHtml(state.storyPage, totalPages, 'story');
      bindPaginationEvents(elements.storiesPagination, 'story', '#storiesSection');
    } else {
      elements.storiesPagination.innerHTML = "";
    }
    
    // Bind click events to stories cards
    elements.storiesContainer.querySelectorAll(".writing-card").forEach(card => {
      const id = card.getAttribute("data-id");
      card.addEventListener("click", (e) => {
        e.preventDefault();
        openReaderView(id);
      });
    });
  } else {
    elements.storiesSection.style.display = "none";
    elements.storiesPagination.innerHTML = "";
  }

  // E. Render Songs Section
  const songs = filtered.filter(w => w.category === "song");
  if (songs.length > 0) {
    elements.songsSection.style.display = "block";
    // Section share button
    const songsSectionDivider = elements.songsSection.querySelector(".section-divider");
    if (songsSectionDivider && !songsSectionDivider.parentElement.classList.contains("section-divider-wrap")) {
      const wrap = document.createElement("div");
      wrap.className = "section-divider-wrap";
      songsSectionDivider.parentNode.insertBefore(wrap, songsSectionDivider);
      wrap.appendChild(songsSectionDivider);
      const shareWrap = document.createElement("div");
      shareWrap.className = "section-share-wrap";
      shareWrap.innerHTML = `<button class="section-share-btn" aria-label="গান শেয়ার করুন"><span class="material-symbols-outlined">share</span><span>শেয়ার</span></button>`;
      wrap.appendChild(shareWrap);
      shareWrap.querySelector(".section-share-btn").addEventListener("click", () => {
        const catUrl = SITE_URL + "/#category/song";
        openSectionSharePopup(shareWrap, catUrl, "গান");
      });
    }
    const itemsPerPage = category === "all" ? 5 : 10;
    const totalPages = Math.ceil(songs.length / itemsPerPage);
    if (state.songPage > totalPages) state.songPage = totalPages;
    if (state.songPage < 1) state.songPage = 1;

    const startIndex = (state.songPage - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    const paginatedSongs = songs.slice(startIndex, endIndex);

    let songsHtml = "";
    const allSongs = writings.filter(w => w.category === "song");

    paginatedSongs.forEach(song => {
      const songIdx = allSongs.findIndex(s => s.id === song.id);
      const serialNum = toBengaliNumber(songIdx + 1);
      songsHtml += `
        <article class="poetry-item" data-id="${song.id}">
          <div class="poetry-header">
            <h4 class="headline-sm poetry-title">${serialNum}. ${song.title}</h4>
            <span class="poetry-date">${song.date}</span>
          </div>
          <p class="body-md poetry-excerpt">${song.excerpt}</p>
          <a href="#" class="link-editorial">গানটি দেখুন</a>
        </article>
      `;
    });

    elements.songsContainer.innerHTML = songsHtml;

    if (totalPages > 1) {
      elements.songsPagination.innerHTML = generatePaginationHtml(state.songPage, totalPages, 'song');
      bindPaginationEvents(elements.songsPagination, 'song', '#songsSection');
    } else {
      elements.songsPagination.innerHTML = "";
    }

    elements.songsContainer.querySelectorAll(".poetry-item").forEach(item => {
      const id = item.getAttribute("data-id");
      item.querySelector(".poetry-title").addEventListener("click", () => openReaderView(id));
      item.querySelector(".link-editorial").addEventListener("click", (e) => {
        e.preventDefault();
        openReaderView(id);
      });
    });
  } else {
    elements.songsSection.style.display = "none";
    elements.songsPagination.innerHTML = "";
  }
}

// Start Application — async init to await data loading
document.addEventListener("DOMContentLoaded", () => init().catch(console.error));
