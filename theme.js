/**
 * Daurah Tafsir Makro — Theme Manager & Page Enhancements
 * Supports: Light, Dark, Sepia themes with localStorage persistence and system preference detection.
 * Automatically enriches Surah detail pages with breadcrumbs, sequential Prev/Next navigation, and responsive media.
 */

(function () {
    "use strict";

    // 1. Theme Management
    const THEME_STORAGE_KEY = "theme";
    const THEMES = ["light-theme", "dark-theme", "sepia-theme"];
    const THEME_COLORS = {
        "light-theme": "#176B55",
        "dark-theme": "#121816",
        "sepia-theme": "#F4ECD8"
    };

    function getSystemTheme() {
        if (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches) {
            return "dark-theme";
        }
        return "light-theme";
    }

    function updateThemeMeta(theme) {
        let meta = document.querySelector('meta[name="theme-color"]');
        if (!meta) {
            meta = document.createElement("meta");
            meta.setAttribute("name", "theme-color");
            document.head.appendChild(meta);
        }
        meta.setAttribute("content", THEME_COLORS[theme] || THEME_COLORS["light-theme"]);
    }

    window.loadTheme = function () {
        const savedTheme = localStorage.getItem(THEME_STORAGE_KEY) || getSystemTheme();
        const htmlElement = document.documentElement;

        THEMES.forEach(t => htmlElement.classList.remove(t));
        htmlElement.classList.add(savedTheme);
        updateThemeMeta(savedTheme);
    };

    window.toggleTheme = function () {
        const htmlElement = document.documentElement;
        let currentIndex = THEMES.findIndex(t => htmlElement.classList.contains(t));
        if (currentIndex === -1) currentIndex = 0;

        const nextIndex = (currentIndex + 1) % THEMES.length;
        const newTheme = THEMES[nextIndex];

        THEMES.forEach(t => htmlElement.classList.remove(t));
        htmlElement.classList.add(newTheme);
        localStorage.setItem(THEME_STORAGE_KEY, newTheme);
        updateThemeMeta(newTheme);
    };

    // Apply theme immediately before render to avoid flash of wrong theme
    const preSaved = localStorage.getItem(THEME_STORAGE_KEY) || getSystemTheme();
    document.documentElement.classList.add(preSaved);
    updateThemeMeta(preSaved);

    // 2. Surah Page Auto-Enhancement
    function enhanceSurahPage() {
        const path = window.location.pathname;
        const match = path.match(/surah_(\d+)\.html$/);
        if (!match) return;

        const surahNumber = parseInt(match[1], 10);
        if (isNaN(surahNumber) || surahNumber < 1 || surahNumber > 114) return;

        const contentArea = document.querySelector(".content-area");
        if (!contentArea) return;

        // Fetch surah metadata to populate breadcrumbs and navigation titles
        const jsonPath = "data/all_surahs.json";
        fetch(jsonPath)
            .then(res => res.json())
            .then(data => {
                const surahs = data.children || [];
                const currentSurah = surahs.find(s => s.number === surahNumber);
                const prevSurah = surahs.find(s => s.number === surahNumber - 1);
                const nextSurah = surahs.find(s => s.number === surahNumber + 1);

                // Inject Breadcrumbs if not present
                if (!document.querySelector(".breadcrumbs")) {
                    const breadcrumbs = document.createElement("nav");
                    breadcrumbs.className = "breadcrumbs";
                    breadcrumbs.setAttribute("aria-label", "Breadcrumb");
                    const currentTitle = currentSurah ? `${currentSurah.englishName} (${currentSurah.name})` : `Surah ${surahNumber}`;
                    breadcrumbs.innerHTML = `
                        <a href="index.html">Utama</a>
                        <span class="crumb-separator" aria-hidden="true">/</span>
                        <a href="index.html">Tafsir Mikro</a>
                        <span class="crumb-separator" aria-hidden="true">/</span>
                        <span class="crumb-current" aria-current="page">${currentTitle}</span>
                    `;
                    contentArea.parentNode.insertBefore(breadcrumbs, contentArea);
                }

                // Inject Previous / Next Navigation if not present
                if (!document.querySelector(".prev-next-nav")) {
                    const nav = document.createElement("nav");
                    nav.className = "prev-next-nav";
                    nav.setAttribute("aria-label", "Navigasi Surah");

                    let prevHtml = "";
                    if (prevSurah) {
                        prevHtml = `
                            <a href="surah_${prevSurah.number}.html" class="prev-next-btn prev" rel="prev">
                                <i class="material-icons" aria-hidden="true">arrow_back</i>
                                <div>
                                    <span class="prev-next-label">Surah Sebelumnya</span>
                                    <span class="prev-next-title">${prevSurah.number}. ${prevSurah.englishName}</span>
                                </div>
                            </a>
                        `;
                    } else {
                        prevHtml = `<div class="prev-placeholder"></div>`;
                    }

                    let nextHtml = "";
                    if (nextSurah) {
                        nextHtml = `
                            <a href="surah_${nextSurah.number}.html" class="prev-next-btn next" rel="next">
                                <div>
                                    <span class="prev-next-label">Surah Seterusnya</span>
                                    <span class="prev-next-title">${nextSurah.number}. ${nextSurah.englishName}</span>
                                </div>
                                <i class="material-icons" aria-hidden="true">arrow_forward</i>
                            </a>
                        `;
                    }

                    nav.innerHTML = prevHtml + nextHtml;
                    contentArea.appendChild(nav);
                }
            })
            .catch(() => {
                // Fallback sequential navigation using raw numbers
                if (!document.querySelector(".prev-next-nav")) {
                    const nav = document.createElement("nav");
                    nav.className = "prev-next-nav";
                    nav.setAttribute("aria-label", "Navigasi Surah");
                    let prevHtml = surahNumber > 1 ? `
                        <a href="surah_${surahNumber - 1}.html" class="prev-next-btn prev" rel="prev">
                            <i class="material-icons" aria-hidden="true">arrow_back</i>
                            <div>
                                <span class="prev-next-label">Sebelumnya</span>
                                <span class="prev-next-title">Surah ${surahNumber - 1}</span>
                            </div>
                        </a>
                    ` : `<div></div>`;

                    let nextHtml = surahNumber < 114 ? `
                        <a href="surah_${surahNumber + 1}.html" class="prev-next-btn next" rel="next">
                            <div>
                                <span class="prev-next-label">Seterusnya</span>
                                <span class="prev-next-title">Surah ${surahNumber + 1}</span>
                            </div>
                            <i class="material-icons" aria-hidden="true">arrow_forward</i>
                        </a>
                    ` : "";

                    nav.innerHTML = prevHtml + nextHtml;
                    contentArea.appendChild(nav);
                }
            });

        // Ensure YouTube iframes have lazy loading and title
        const iframes = contentArea.querySelectorAll("iframe");
        iframes.forEach(iframe => {
            if (!iframe.getAttribute("title")) {
                iframe.setAttribute("title", `Kuliah Tafsir Surah ${surahNumber}`);
            }
            if (!iframe.getAttribute("loading")) {
                iframe.setAttribute("loading", "lazy");
            }
        });
    }

    // 3. Service Worker Registration (PWA)
    function registerServiceWorker() {
        if ("serviceWorker" in navigator && window.location.protocol.startsWith("http")) {
            const swPath = window.location.pathname.includes("/daurahtafsir-makro/")
                ? "/daurahtafsir-makro/sw.js"
                : "./sw.js";

            window.addEventListener("load", () => {
                navigator.serviceWorker.register(swPath).catch(err => {
                    // Fail silently in environments where SW is disabled
                    console.debug("[SW] Registration skipped or failed:", err);
                });
            });
        }
    }

    document.addEventListener("DOMContentLoaded", function () {
        window.loadTheme();
        enhanceSurahPage();
        registerServiceWorker();
    });
})();
