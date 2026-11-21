# Daurah Tafsir Makro — UX/UI & Accessibility Audit (Phase 0)

**Date:** 2026-11-21  
**Project:** [Daurah Tafsir Makro](https://ben-kodbiz.github.io/daurahtafsir-makro/)  
**Target:** Mobile-First Responsive Redesign, Accessibility (WCAG 2.2 AA), Typography, Reading Experience, PWA  
**Compliance Standard:** Strict preservation of all Islamic texts, Arabic verses, translations, tafsir, hadith classifications, original lecture materials, and video/PDF links.

---

## 1. Executive Summary

This repository hosts an Islamic digital library containing structured learning materials from Maulana Asri (Darul Kautsar). The content includes:
- Tafsir Makro & Mikro notes for all 114 Surahs of the Holy Quran (PDFs and YouTube lecture recordings).
- Hadith and Usul study modules (Usul Tafsir, Tafsir Quran bil Quran, Usul Dirayat Hadis, Jami' at-Tirmizi, 'Ilal at-Tirmizi, Sahih Bukhari Kitab Perang, and Sahih Bukhari Kitab Azan Edisi 2).

The baseline architecture is lightweight (vanilla HTML5, CSS3, JavaScript ES6+, PDF.js, and static JSON data), making it fast and deployable to GitHub Pages. However, an in-depth audit reveals significant opportunities to modernize usability, mobile responsiveness, touch ergonomic standards, typography, accessibility, and offline readiness without touching the underlying religious scholarship.

---

## 2. Baseline Architecture & Asset Inventory

| Component | Files & Locations | Purpose & Tech Stack |
|---|---|---|
| **Root Shell** | `index.html`, `about.html`, `reader.html` | Core entry points, metadata, search container, PDF viewer |
| **Styles** | `styles.css` (670 lines), module `tutorial_styles.css` | Global themes (Light, Dark, Sepia), layouts, buttons |
| **Logic** | `script.js` (274 lines), `theme.js`, `js/reader.js` | Surah grid rendering, live search, PDF.js integration |
| **Quran Surah Pages** | `surah_1.html` through `surah_114.html` (114 files) | Individual surah hubs linking to PDF reader and video lectures |
| **Data Indexes** | `data/all_surahs.json`, `data/surah_pdfs.json`, `data/en.json`, `data/ms.json` | Quran metadata, PDF routing table, language translations |
| **Submodules** | 7 specialized modules (`qawaid_tafsir/`, `jami_at_tirmizi/`, etc.) | ~740 session files with embedded notes and YouTube lectures |

---

## 3. Detailed Audit Findings by Area

### 3.1 Layout & Mobile Responsiveness (320px to 1440px)
- **Viewport Constraints at 320px–390px (Mobile Portrait):**
  - **Header Structure:** The homepage lacks a structured `<header>` and `<nav>`. The language selector (`<select>`) is floating nakedly at the top-left, and the main heading (`h1.main-heading`) consumes disproportionate vertical space on smaller displays.
  - **Module Widgets (`.widget-container`):** Currently set to a 2-column grid. On narrow 320px screens, cards become cramped, causing multi-line text wraps with insufficient tap padding.
  - **YouTube Video Embeds:** The `iframe` tags throughout `surah_*.html` and session files contain hardcoded `width="560" height="315"`. While `max-width: 100%` is applied, the fixed height can distort aspect ratios on mobile devices. Needs modern `aspect-ratio: 16 / 9; width: 100%; height: auto;`.
  - **Floating Theme Button:** Pinned via `fixed` positioning at `bottom: 20px; right: 20px;` with `z-index: 1000`. On mobile smartphones, this floating button obscures content cards, interferes with scrolling, and conflicts with mobile touch gestures.
- **Tablet & Desktop (768px–1440px):**
  - The content area max-width of 800px is appropriate for single-column reading, but desktop screens lack structured breadcrumbs and navigation between surahs.

### 3.2 Design System & Palette
- **Current Palette:** Uses a standard Material Design palette (indigo `#3f51b5`, grey `#f0f0f0`).
- **Improvement Direction:** Shift to an authentic, calm Islamic library aesthetic:
  - Primary: Deep Emerald (`#176B55` / `#10513F` / light tint `#E6F1EC`).
  - Secondary: Warm Amber Gold (`#C49A45` / `#F7F0DF`).
  - Backgrounds: Natural parchment / clean off-white (`#F8FAF8`, `#FFFFFF`).
  - Dark Mode: Deep pine charcoal (`#121816`, `#1B2421`, `#24332D`) with high contrast text (`#E8EFEA`).
  - Sepia Mode: Warm cream paper (`#F4ECD8`, `#FBF6EB`) with rich dark walnut text (`#433422`).
- **CSS Architecture:** Maintain backwards compatibility for existing variable names (`--bg`, `--surface`, `--accent`, etc.) while adding the modernized token system (`--color-primary`, `--color-surface`, `--radius-*`, `--shadow-*`).

### 3.3 Typography & Arabic Script Handling
- **Arabic Rendering:** Currently uses system sans-serif or generic fonts with standard letter spacing.
- **Issues:**
  - Arabic font size and line height must be properly calibrated for diacritics (harakat) and ayah markers so they are never clipped or crowded.
  - Missing specialized Arabic fonts (e.g. `'Amiri'`, `'Scheherazade New'`, `'Noto Naskh Arabic'`).
  - RTL directionality must be enforced explicitly on all Arabic elements with `dir="rtl"`.
- **Readability:** Establish typographic hierarchy:
  - Arabic: `font-size: clamp(1.6rem, 3.2vw, 2.2rem); line-height: 2.2; word-spacing: 0.15em; font-family: 'Amiri', 'Traditional Arabic', serif;`
  - Translations / Explanations: `font-size: 1.05rem; line-height: 1.8; color: var(--color-text);`

### 3.4 PDF Reader Experience (`reader.html` & `js/reader.js`)
- **Strengths:** Dedicated PDF.js canvas renderer, fit-width calculation, zoom buttons, page jump input, position persistence in `localStorage`.
- **Mobile Weaknesses:**
  - Toolbar layout at `bottom: 0` is crowded on screens below 400px.
  - Lacks touch gesture support (tap left/right edge or swipe for next/previous page).
  - Lacks full-screen or distraction-free reading mode.
  - Lacks visual feedback on PDF page loading and error retry state.
  - Safe-area insets (`env(safe-area-inset-bottom)`) are missing, causing bottom toolbar buttons to clash with iOS/Android home bars.

### 3.5 Surah & Lesson Navigation
- **Semantic HTML:** In `script.js`, surah cards are rendered as `<div class="surah-item">` with event listeners instead of semantic `<a href="surah_N.html">` links. This impedes search engines, browser history, middle-click/open in new tab, and assistive technologies.
- **Sequential Navigation:** Surah pages (`surah_1.html` to `surah_114.html`) only have a "Back" button to `index.html`. Users cannot browse sequentially to "Previous Surah" or "Next Surah" without repeatedly returning to the home directory.
- **Breadcrumbs:** Missing breadcrumb hierarchy (`Home / Tafsir Mikro / Surah Al-Baqarah`).

### 3.6 Search & Discoverability
- **Current Search:** Instant substring filter on surah number, English name, and Arabic name.
- **Enhancements Needed:**
  - Live ARIA announcements (`aria-live="polite"`) indicating number of matching results to screen readers.
  - Keyboard shortcut: `Esc` to clear search and return focus.
  - Clear empty-state feedback with search reset action.
  - Filter by Revelation Type (Makkiyyah / Madaniyyah) or Juz indicator where available.

### 3.7 Accessibility & WCAG 2.2 AA Compliance
- **Touch Target Sizes:** Several buttons and inputs hover around 36px–40px. Must strictly enforce the 44×44 CSS pixel minimum touch target guideline.
- **Reduced Motion:** Missing `@media (prefers-reduced-motion: reduce)` rules for users sensitive to motion.
- **Skip Links:** Missing a "Skip to content" link for keyboard users.
- **Contrast Ratios:** Muted text in dark mode (`#444444` borders, `#9e9e9e` placeholders) needs verification to guarantee minimum 4.5:1 ratio for normal text.

### 3.8 Progressive Web App (PWA) & Offline Capabilities
- **Status:** Neither `manifest.json` nor `sw.js` is present.
- **Requirements:**
  - Provide a valid Web App Manifest (`manifest.json`) for home-screen installation.
  - Implement a Service Worker (`sw.js`) that caches core UI assets (HTML, CSS, JS, JSON metadata, icons) for instant offline loading.
  - **Critical Rule:** Never auto-cache heavy PDF files in the service worker to prevent exhausting mobile data and storage.

---

## 4. Remediation Implementation Plan

- **Phase 1: Design System & Shared CSS Foundations**
  - Implement Islamic library palette (emerald, gold, natural paper) and unified CSS custom properties.
  - Add typography rules for Arabic (`Amiri`), translations, and interface text.
  - Add WCAG focus rings, reduced-motion rules, touch targets, and mobile-first responsive media queries.
- **Phase 2: Modern Responsive Homepage & Navigation**
  - Build clean app header with integrated theme and language selector.
  - Add introductory card using existing approved text.
  - Redesign module cards with clear categorization (Tafsir vs. Hadith).
  - Convert surah cards to semantic `<a>` links with accessible badges.
  - Add sticky bottom navigation bar for quick access on mobile (Home, Tafsir, Hadith, Search).
- **Phase 3: Reading Experience & Sequential Navigation**
  - Optimize `reader.html` and `js/reader.js` with edge-tap page flipping, fit-to-width, and mobile safe-area insets.
  - Add breadcrumbs and Previous/Next Surah navigation to detail pages.
  - Ensure all video embeds use modern responsive aspect ratios (`16:9`).
- **Phase 4: Search & Accessibility Enhancements**
  - Enhance live search with result counters and ARIA live regions.
  - Verify WCAG 2.2 AA contrast across Light, Dark, and Sepia modes.
  - Provide keyboard access and skip links.
- **Phase 5: PWA & Offline Support**
  - Add `manifest.json` and generate lightweight SVG/PNG app icons.
  - Add `sw.js` for robust caching of app shell without prefetching heavy PDFs.
  - Register service worker across pages.

---
*Audit completed in accordance with all constraints specified in `improve.md`.*
