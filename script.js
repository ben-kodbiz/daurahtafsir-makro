/**
 * Daurah Tafsir Makro — Homepage & Surah Grid Script
 * Accessible, Mobile-First, Semantic Links, Live Search & Continue Reading
 */

let currentLanguage = "ms"; // Default to Malay as requested for local audience, toggleable to English
let allSurahs = [];

function setLanguage(lang) {
    currentLanguage = lang;
    try {
        localStorage.setItem("dtm-lang", lang);
    } catch (e) { /* ignore */ }
    loadTranslations();
    updateSearchCount(allSurahs.length);
}

function loadTranslations() {
    fetch(`data/${currentLanguage}.json`)
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(translations => {
            document.querySelectorAll(".back-button").forEach(el => {
                const icon = el.querySelector("i");
                el.innerHTML = icon ? `${icon.outerHTML} ${translations.backButton}` : translations.backButton;
            });
            document.querySelectorAll(".surah-title").forEach(el => {
                if (el.getAttribute("data-original-title")) {
                    el.textContent = el.getAttribute("data-original-title");
                }
            });
            document.querySelectorAll(".section-heading").forEach(el => {
                const text = el.textContent.trim();
                if (text === "Key Themes" || text === "Tema Utama") el.textContent = translations.keyThemes;
                else if (text === "Detailed Explanation" || text === "Penerangan Terperinci") el.textContent = translations.detailedExplanation;
                else if (text === "YouTube Videos" || text === "Video Kuliah YouTube") el.textContent = translations.youtubeVideos;
                else if (text === "Other Materials" || text === "Bahan Pembelajaran Lain") el.textContent = translations.otherMaterials;
            });
            document.querySelectorAll(".download-button").forEach(el => {
                const text = el.textContent.trim();
                if (text === "Download Video" || text === "Muat Turun Video") el.textContent = translations.downloadVideo;
                else if (text === "PDF Explanation" || text === "Nota Tafsir PDF") el.textContent = translations.pdfExplanation;
            });
        })
        .catch(error => {
            console.error("Error loading translations:", error);
        });
}

function createSurahGrid() {
    const surahGrid = document.getElementById("surah-grid");
    if (!surahGrid) return;

    surahGrid.innerHTML = `
        <div class="pdf-loading" role="status" aria-live="polite">
            <p>Memuatkan senarai surah…</p>
        </div>
    `;

    fetch("data/all_surahs.json")
        .then(response => {
            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            return response.json();
        })
        .then(data => {
            allSurahs = data.children || [];
            displaySurahs(allSurahs);
            setupSearchFunctionality();
            setupContinueReading();
        })
        .catch(error => {
            console.error("Error loading surahs:", error);
            surahGrid.innerHTML = `
                <div class="no-results">
                    <i class="material-icons" aria-hidden="true">error_outline</i>
                    <p>Ralat memuatkan senarai surah. Sila muat semula halaman.</p>
                </div>
            `;
        });
}

function displaySurahs(surahs) {
    const surahGrid = document.getElementById("surah-grid");
    if (!surahGrid) return;

    surahGrid.innerHTML = "";

    if (surahs.length === 0) {
        const noResults = document.createElement("div");
        noResults.className = "no-results";
        noResults.setAttribute("role", "status");
        noResults.innerHTML = `
            <i class="material-icons" aria-hidden="true">search_off</i>
            <p>Tiada surah dijumpai untuk carian ini.</p>
            <button type="button" class="reset-search-btn" onclick="resetSearch()">
                <i class="material-icons" aria-hidden="true">refresh</i> Tunjukkan Semua Surah
            </button>
        `;
        surahGrid.appendChild(noResults);
        updateSearchCount(0);
        return;
    }

    const fragment = document.createDocumentFragment();

    surahs.forEach(surah => {
        // Semantic accessible anchor tag
        const card = document.createElement("a");
        card.href = `surah_${surah.number}.html`;
        card.className = "surah-item";
        card.setAttribute("aria-label", `Surah ${surah.number}: ${surah.englishName}, ${surah.name}. Terjemahan: ${surah.englishNameTranslation}. ${surah.numberOfAyahs} ayat.`);
        card.setAttribute("data-surah-number", surah.number);

        card.innerHTML = `
            <div class="surah-card-header">
                <span class="surah-badge" aria-hidden="true">${surah.number}</span>
                <span class="surah-arabic-name" dir="rtl" lang="ar">${surah.name}</span>
            </div>
            <div class="surah-info">
                <span class="surah-name">${surah.englishName}</span>
                <span class="surah-translation">${surah.englishNameTranslation}</span>
                <span class="surah-meta-info">${surah.revelationType} • ${surah.numberOfAyahs} Ayat</span>
            </div>
        `;

        fragment.appendChild(card);
    });

    surahGrid.appendChild(fragment);
    updateSearchCount(surahs.length);
}

function updateSearchCount(count) {
    const countEl = document.getElementById("search-count");
    if (!countEl) return;

    if (currentLanguage === "ms") {
        countEl.textContent = count === 114
            ? "Memaparkan semua 114 surah"
            : `Menjumpai ${count} daripada 114 surah`;
    } else {
        countEl.textContent = count === 114
            ? "Showing all 114 surahs"
            : `Found ${count} of 114 surahs`;
    }
}

function resetSearch() {
    const searchInput = document.getElementById("surah-search");
    const clearButton = document.getElementById("clear-search");
    if (searchInput) searchInput.value = "";
    if (clearButton) clearButton.style.display = "none";
    displaySurahs(allSurahs);
    if (searchInput) searchInput.focus();
}

function setupContinueReading() {
    const container = document.getElementById("continue-reading");
    if (!container) return;

    let state = null;
    try {
        state = JSON.parse(localStorage.getItem("dtm-reading"));
    } catch (e) { /* ignore */ }

    if (!state || !state.surah || !state.page) return;

    const surah = (allSurahs || []).find(s => s.number === Number(state.surah));
    const title = surah ? `${surah.number}. ${surah.englishName}` : `Surah ${state.surah}`;

    const titleEl = document.getElementById("continue-title");
    const pageEl = document.getElementById("continue-page");
    const btn = document.getElementById("continue-button");

    if (titleEl) titleEl.textContent = title;
    if (pageEl) pageEl.textContent = `Halaman / Muka Surat ${state.page}`;
    if (btn) {
        btn.onclick = () => {
            window.location.href = `reader.html?surah=${state.surah}&page=${state.page}`;
        };
    }

    container.hidden = false;
}

function setupSearchFunctionality() {
    const searchInput = document.getElementById("surah-search");
    const clearButton = document.getElementById("clear-search");
    if (!searchInput) return;

    searchInput.addEventListener("input", function () {
        const val = this.value.trim();
        if (clearButton) {
            clearButton.style.display = val.length > 0 ? "inline-flex" : "none";
        }
        filterSurahs(val.toLowerCase());
    });

    if (clearButton) {
        clearButton.addEventListener("click", resetSearch);
    }

    // Keyboard support: Escape clears search
    searchInput.addEventListener("keydown", function (e) {
        if (e.key === "Escape") {
            resetSearch();
        }
    });
}

function filterSurahs(searchTerm) {
    if (!allSurahs || allSurahs.length === 0) return;

    if (!searchTerm) {
        displaySurahs(allSurahs);
        return;
    }

    const filtered = allSurahs.filter(surah => {
        const numStr = surah.number.toString();
        const engName = (surah.englishName || "").toLowerCase();
        const arName = surah.name || "";
        const trans = (surah.englishNameTranslation || "").toLowerCase();

        return numStr === searchTerm ||
               numStr.includes(searchTerm) ||
               engName.includes(searchTerm) ||
               arName.includes(searchTerm) ||
               trans.includes(searchTerm);
    });

    displaySurahs(filtered);
}

// Initialize on load
document.addEventListener("DOMContentLoaded", function () {
    const savedLang = localStorage.getItem("dtm-lang");
    if (savedLang) {
        currentLanguage = savedLang;
        const selector = document.getElementById("language-selector");
        if (selector) selector.value = savedLang;
    }
    loadTranslations();
    createSurahGrid();
});
