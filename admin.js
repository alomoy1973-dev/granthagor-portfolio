// ----------------------------------------------------
// Granthagor Admin Control Panel - Logic & CRUD Operations
// ----------------------------------------------------

const CORRECT_PASSCODE = "granthagor2024";
let writings = [];

// DOM Elements Cache
const dom = {
  loginScreen: document.getElementById("loginScreen"),
  loginForm: document.getElementById("loginForm"),
  passcode: document.getElementById("passcode"),
  loginError: document.getElementById("loginError"),
  adminPanel: document.getElementById("adminPanel"),
  logoutBtn: document.getElementById("logoutBtn"),
  
  // Navigation
  navItems: document.querySelectorAll(".nav-item"),
  tabContents: document.querySelectorAll(".tab-content"),
  tabTitle: document.getElementById("tabTitle"),
  newWritingBtn: document.getElementById("newWritingBtn"),
  
  // Stats
  totalCount: document.getElementById("totalCount"),
  poemCount: document.getElementById("poemCount"),
  rhymeCount: document.getElementById("rhymeCount"),
  featuredCount: document.getElementById("featuredCount"),
  recentWritingsList: document.getElementById("recentWritingsList"),
  
  // Writings List
  allWritingsList: document.getElementById("allWritingsList"),
  searchWritings: document.getElementById("searchWritings"),
  filterCategory: document.getElementById("filterCategory"),
  
  // Editor
  writingForm: document.getElementById("writingForm"),
  editId: document.getElementById("editId"),
  wTitle: document.getElementById("wTitle"),
  wCategory: document.getElementById("wCategory"),
  wDate: document.getElementById("wDate"),
  wReadTime: document.getElementById("wReadTime"),
  wExcerpt: document.getElementById("wExcerpt"),
  wContent: document.getElementById("wContent"),
  wFeatured: document.getElementById("wFeatured"),
  editorFormTitle: document.getElementById("editorFormTitle"),
  saveBtn: document.getElementById("saveBtn"),
  cancelBtn: document.getElementById("cancelBtn"),
  livePreviewContainer: document.getElementById("livePreviewContainer"),
  
  // Code Export
  downloadAppJs: document.getElementById("downloadAppJs"),
  copyAppJs: document.getElementById("copyAppJs"),
  
  // Toast container
  toastContainer: document.getElementById("toastContainer")
};

// 1. Passcode Authorization Gate
function initAuth() {
  const isLoggedIn = sessionStorage.getItem("granthagor_admin_logged_in") === "true";
  
  if (isLoggedIn) {
    showAdminPanel();
  } else {
    dom.loginScreen.classList.remove("hidden");
    dom.adminPanel.classList.add("hidden");
  }
  
  dom.loginForm.addEventListener("submit", (e) => {
    e.preventDefault();
    if (dom.passcode.value === CORRECT_PASSCODE) {
      sessionStorage.setItem("granthagor_admin_logged_in", "true");
      showAdminPanel();
      showToast("সফলভাবে লগইন করা হয়েছে!", "success");
    } else {
      dom.loginError.classList.remove("hidden");
      dom.passcode.value = "";
      dom.passcode.focus();
    }
  });
  
  dom.logoutBtn.addEventListener("click", () => {
    sessionStorage.removeItem("granthagor_admin_logged_in");
    dom.loginScreen.classList.remove("hidden");
    dom.adminPanel.classList.add("hidden");
    dom.passcode.value = "";
    showToast("লগ আউট করা হয়েছে।", "info");
  });
}

function showAdminPanel() {
  dom.loginScreen.classList.add("hidden");
  dom.adminPanel.classList.remove("hidden");
  loadWritings();
}

// 2. Load Writings Data from app.js or localStorage
async function loadWritings() {
  // Try loading from localStorage first
  const localData = localStorage.getItem("granthagor_writings");
  if (localData) {
    try {
      writings = JSON.parse(localData);
      initDashboard();
      return;
    } catch (e) {
      console.error("Localstorage load error:", e);
    }
  }

  // Fallback to fetching app.js and extracting the writings array
  showToast("ডাটাবেজ লোড হচ্ছে...", "info");
  try {
    const res = await fetch("app.js");
    const code = await res.text();
    
    // Extract: let writings = [ ... ];
    const startIndex = code.indexOf("let writings = [");
    const endIndex = code.indexOf("// Check if localStorage has updated writings");
    
    if (startIndex !== -1 && endIndex !== -1) {
      const writingsStr = code.substring(startIndex + "let writings = ".length, endIndex).trim();
      // Remove trailing semicolon
      const cleanWritingsStr = writingsStr.replace(/;$/, "");
      
      // Parse using Function constructor for safety on JS objects (handles unquoted keys, comments etc)
      writings = new Function(`return ${cleanWritingsStr}`)();
      saveToLocal();
      showToast("ডাটাবেজ প্রস্তুত!", "success");
    } else {
      throw new Error("Could not parse writings database format inside app.js");
    }
  } catch (err) {
    console.error("Error loading app.js database:", err);
    showToast("app.js থেকে ডাটাবেজ লোড করা যায়নি!", "error");
  }
  
  initDashboard();
}

function saveToLocal() {
  localStorage.setItem("granthagor_writings", JSON.stringify(writings));
}

// 3. Tab switching & Navigation logic
function initNavigation() {
  dom.navItems.forEach(item => {
    item.addEventListener("click", (e) => {
      e.preventDefault();
      const tabId = item.getAttribute("data-tab");
      switchTab(tabId);
    });
  });

  dom.newWritingBtn.addEventListener("click", () => {
    resetEditorForm();
  });

  dom.cancelBtn.addEventListener("click", () => {
    switchTab("writings");
    resetEditorForm();
  });
}

function switchTab(tabId) {
  dom.navItems.forEach(nav => {
    if (nav.getAttribute("data-tab") === tabId) {
      nav.classList.add("active");
    } else {
      nav.classList.remove("active");
    }
  });

  dom.tabContents.forEach(content => {
    if (content.id === `tab-${tabId}`) {
      content.classList.add("active");
    } else {
      content.classList.remove("active");
    }
  });

  // Dynamic header titles
  const titles = {
    dashboard: "ড্যাশবোর্ড ওভারভিউ",
    writings: "সব রচনা তালিকা",
    editor: dom.editId.value ? "রচনা সম্পাদনা করুন" : "নতুন রচনা যোগ করুন",
    export: "কোড এক্সপোর্ট করুন"
  };
  dom.tabTitle.textContent = titles[tabId] || "অ্যাডমিন প্যানেল";
  
  if (tabId === "dashboard") {
    renderDashboardStats();
  } else if (tabId === "writings") {
    renderWritingsTable();
  }
}

// 4. Render Dashboard & Stats View
function initDashboard() {
  renderDashboardStats();
  renderWritingsTable();
  initNavigation();
  initEditor();
  initExporter();
}

function renderDashboardStats() {
  dom.totalCount.textContent = writings.length;
  dom.poemCount.textContent = writings.filter(w => w.category === "poem").length;
  dom.rhymeCount.textContent = writings.filter(w => w.category === "rhyme").length;
  dom.featuredCount.textContent = writings.filter(w => w.isFeatured).length;

  // Recent 5 table
  const sorted = [...writings].reverse().slice(0, 5);
  let html = "";
  if (sorted.length === 0) {
    html = `<tr><td colspan="5" class="text-center text-muted">কোনো রচনা খুঁজে পাওয়া যায়নি!</td></tr>`;
  } else {
    sorted.forEach(w => {
      const badgeClass = w.category === "poem" ? "poem" : "rhyme";
      const catText = w.category === "poem" ? "কবিতা" : "ছড়া";
      html += `
        <tr>
          <td style="font-weight: 500;">${w.title}</td>
          <td><span class="badge ${badgeClass}">${catText}</span></td>
          <td>${w.date || "তারিখ অজানা"}</td>
          <td>${w.isFeatured ? '<span class="badge-featured"><span class="material-symbols-outlined text-[14px]">star</span> ফিচার্ড</span>' : "না"}</td>
          <td>
            <button class="action-btn edit" onclick="editWriting('${w.id}')" title="সম্পাদনা">
              <span class="material-symbols-outlined">edit</span>
            </button>
            <button class="action-btn delete" onclick="deleteWriting('${w.id}')" title="মুছে ফেলুন">
              <span class="material-symbols-outlined">delete</span>
            </button>
          </td>
        </tr>
      `;
    });
  }
  dom.recentWritingsList.innerHTML = html;
}

// 5. Render All Writings Table View
function renderWritingsTable() {
  const searchQuery = dom.searchWritings.value.toLowerCase().trim();
  const categoryFilter = dom.filterCategory.value;

  const filtered = writings.filter(w => {
    const matchesSearch = w.title.toLowerCase().includes(searchQuery) || 
                          (w.excerpt && w.excerpt.toLowerCase().includes(searchQuery)) ||
                          w.id.toLowerCase().includes(searchQuery);
    const matchesCategory = categoryFilter === "all" || w.category === categoryFilter;
    return matchesSearch && matchesCategory;
  });

  let html = "";
  if (filtered.length === 0) {
    html = `<tr><td colspan="6" class="text-center text-muted">কোনো রচনা খুঁজে পাওয়া যায়নি!</td></tr>`;
  } else {
    filtered.forEach(w => {
      const badgeClass = w.category === "poem" ? "poem" : "rhyme";
      const catText = w.category === "poem" ? "কবিতা" : "ছড়া";
      html += `
        <tr>
          <td style="color: var(--admin-text-secondary); font-family: monospace;">${w.id}</td>
          <td style="font-weight: 500;">${w.title}</td>
          <td><span class="badge ${badgeClass}">${catText}</span></td>
          <td>${w.date || "তারিখ অজানা"}</td>
          <td>${w.isFeatured ? '<span class="badge-featured"><span class="material-symbols-outlined text-[14px]">star</span> ফিচার্ড</span>' : "না"}</td>
          <td>
            <button class="action-btn edit" onclick="editWriting('${w.id}')" title="সম্পাদনা">
              <span class="material-symbols-outlined">edit</span>
            </button>
            <button class="action-btn delete" onclick="deleteWriting('${w.id}')" title="মুছে ফেলুন">
              <span class="material-symbols-outlined">delete</span>
            </button>
          </td>
        </tr>
      `;
    });
  }
  dom.allWritingsList.innerHTML = html;
}

// Search and Filter Listeners
dom.searchWritings.addEventListener("input", renderWritingsTable);
dom.filterCategory.addEventListener("change", renderWritingsTable);

// 6. Editor Logic & Live Preview
function initEditor() {
  dom.writingForm.addEventListener("submit", handleSaveWriting);
  
  // Live preview auto updates on form inputs
  const inputs = [dom.wTitle, dom.wCategory, dom.wDate, dom.wReadTime, dom.wContent];
  inputs.forEach(input => {
    input.addEventListener("input", updateLivePreview);
  });
}

function updateLivePreview() {
  const title = dom.wTitle.value.trim() || "রচনার শিরোনাম";
  const cat = dom.wCategory.value;
  const date = dom.wDate.value.trim() || "তারিখ অজানা";
  const readTime = dom.wReadTime.value.trim() || "2 মিনিট পাঠ";
  const contentRaw = dom.wContent.value;
  
  const catText = cat === "poem" ? "কবিতা" : "ছড়া";
  const metaText = `${catText} • ${date} • ${readTime}`;
  
  let linesHtml = "";
  if (contentRaw.trim()) {
    const rawLines = contentRaw.split("\n");
    let lastWasEmpty = false;
    
    rawLines.forEach(line => {
      const cleanLine = line.trim();
      if (cleanLine === "") {
        if (!lastWasEmpty) {
          linesHtml += `<div class="poem-stanza-break"></div>`;
          lastWasEmpty = true;
        }
      } else {
        linesHtml += `<div class="poem-line">${cleanLine}</div>`;
        lastWasEmpty = false;
      }
    });
  } else {
    linesHtml = `<div class="text-center text-muted">লেখা শুরু করুন...</div>`;
  }
  
  dom.livePreviewContainer.innerHTML = `
    <h1 class="poem-title">${title}</h1>
    <div class="poem-meta">${metaText}</div>
    <div class="poem-content-preview">${linesHtml}</div>
  `;
}

function resetEditorForm() {
  dom.writingForm.reset();
  dom.editId.value = "";
  dom.editorFormTitle.textContent = "নতুন রচনা তৈরি করুন";
  dom.saveBtn.textContent = "সংরক্ষণ করুন";
  updateLivePreview();
}

// Global functions for actions
window.editWriting = function(id) {
  const w = writings.find(item => item.id === id);
  if (!w) return;
  
  dom.editId.value = w.id;
  dom.wTitle.value = w.title;
  dom.wCategory.value = w.category;
  dom.wDate.value = w.date || "";
  dom.wReadTime.value = w.readTime || "";
  dom.wExcerpt.value = w.excerpt || "";
  dom.wFeatured.checked = w.isFeatured || false;
  
  // Transform content array to double newlines textarea format
  let textareaContent = "";
  if (w.content) {
    const rawTextLines = w.content.map(line => line === "__STANZA__" ? "" : line);
    textareaContent = rawTextLines.join("\n");
  }
  dom.wContent.value = textareaContent;
  
  dom.editorFormTitle.textContent = "রচনা সম্পাদনা করুন";
  dom.saveBtn.textContent = "আপডেট করুন";
  
  switchTab("editor");
  updateLivePreview();
};

window.deleteWriting = function(id) {
  const w = writings.find(item => item.id === id);
  if (!w) return;
  
  const confirmMsg = `আপনি কি নিশ্চিতভাবে "${w.title}" মুছে ফেলতে চান?`;
  if (confirm(confirmMsg)) {
    writings = writings.filter(item => item.id !== id);
    saveToLocal();
    renderDashboardStats();
    renderWritingsTable();
    showToast("রচনাটি মুছে ফেলা হয়েছে!", "success");
  }
};

function handleSaveWriting(e) {
  e.preventDefault();
  
  const id = dom.editId.value;
  const title = dom.wTitle.value.trim();
  const category = dom.wCategory.value;
  const date = dom.wDate.value.trim() || "তারিখ অজানা";
  const readTime = dom.wReadTime.value.trim() || "2 মিনিট পাঠ";
  const excerpt = dom.wExcerpt.value.trim() || (title + " - একটি সংগ্রহশালা লেখা।");
  const isFeatured = dom.wFeatured.checked;
  const badge = category === "poem" ? "কবিতা" : "ছড়া";
  
  // Process raw text content to lines array
  const rawLines = dom.wContent.value.split("\n");
  const content = [];
  let lastWasEmpty = false;
  
  rawLines.forEach(line => {
    const cleanLine = line.trim();
    if (cleanLine === "") {
      if (!lastWasEmpty) {
        content.push("__STANZA__");
        lastWasEmpty = true;
      }
    } else {
      content.push(cleanLine);
      lastWasEmpty = false;
    }
  });
  
  // Remove trailing stanza indicators
  while (content.length > 0 && content[content.length - 1] === "__STANZA__") {
    content.pop();
  }
  
  // Handle single featured story constraint
  if (isFeatured) {
    writings.forEach(item => {
      item.isFeatured = false;
    });
  }
  
  if (id) {
    // Edit Mode
    const index = writings.findIndex(item => item.id === id);
    if (index !== -1) {
      writings[index] = { id, title, category, badge, excerpt, date, readTime, isFeatured, content };
      showToast("রচনাটি আপডেট করা হয়েছে!", "success");
    }
  } else {
    // Add Mode - generate new id
    const prefix = category === "poem" ? "poem" : "rhyme";
    // Find highest numeric ID suffix
    let maxNum = 0;
    writings.forEach(item => {
      const match = item.id.match(new RegExp(`${prefix}-(\\d+)`));
      if (match) {
        const num = parseInt(match[1]);
        if (num > maxNum) maxNum = num;
      }
    });
    const nextNum = String(maxNum + 1).padStart(2, "0");
    const newId = `${prefix}-${nextNum}`;
    
    writings.push({ id: newId, title, category, badge, excerpt, date, readTime, isFeatured, content });
    showToast("নতুন রচনা যুক্ত করা হয়েছে!", "success");
  }
  
  saveToLocal();
  resetEditorForm();
  switchTab("writings");
}

// 7. Exporter tools: rebuilding app.js
function initExporter() {
  dom.downloadAppJs.addEventListener("click", generateAndDownloadCode);
  dom.copyAppJs.addEventListener("click", copyCodeToClipboard);
}

async function getRebuildCode() {
  try {
    const res = await fetch("app.js");
    const appJsText = await res.text();
    
    const startIndex = appJsText.indexOf("let writings = [");
    const endIndex = appJsText.indexOf("// Check if localStorage has updated writings");
    
    if (startIndex !== -1 && endIndex !== -1) {
      const beforeWritings = appJsText.substring(0, startIndex);
      const afterWritings = appJsText.substring(endIndex);
      
      // Build clean JSON layout for writings array
      const writingsJson = JSON.stringify(writings, null, 2);
      
      return `${beforeWritings}let writings = ${writingsJson};\n\n${afterWritings}`;
    } else {
      throw new Error("Unable to reconstruct template bounds.");
    }
  } catch (err) {
    console.error("Export generation error:", err);
    showToast("কোড জেনারেট করতে সমস্যা হচ্ছে!", "error");
    return "";
  }
}

async function generateAndDownloadCode() {
  const code = await getRebuildCode();
  if (!code) return;
  
  const blob = new Blob([code], { type: "text/javascript;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  
  const link = document.createElement("a");
  link.href = url;
  link.download = "app.js";
  
  document.body.appendChild(link);
  link.click();
  
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  
  showToast("app.js ফাইল ডাউনলোড সফল!", "success");
}

async function copyCodeToClipboard() {
  const code = await getRebuildCode();
  if (!code) return;
  
  try {
    await navigator.clipboard.writeText(code);
    showToast("কোড ক্লিপবোর্ডে কপি করা হয়েছে!", "success");
  } catch (err) {
    showToast("কপি করা যায়নি!", "error");
  }
}

// 8. Toast Helper
function showToast(message, type = "info") {
  const toast = document.createElement("div");
  toast.className = `toast ${type}`;
  toast.innerHTML = `
    <span class="material-symbols-outlined">
      ${type === 'success' ? 'check_circle' : type === 'error' ? 'error' : 'info'}
    </span>
    <span>${message}</span>
  `;
  
  dom.toastContainer.appendChild(toast);
  
  setTimeout(() => {
    toast.style.animation = "slideIn 0.3s reverse forwards";
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3000);
}

// Initialize gates on page load
document.addEventListener("DOMContentLoaded", initAuth);
