/* Daurah Tafsir Makro – Mobile-Optimized PDF Reader (PDF.js) */
(function () {
    "use strict";

    const STORAGE_KEY = "dtm-reading";

    pdfjsLib.GlobalWorkerOptions.workerSrc =
        "https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js";

    const container = document.getElementById("pdf-container");
    const view = document.getElementById("pdf-view");
    const loading = document.getElementById("pdf-loading");
    const message = document.getElementById("pdf-message");
    const messageText = document.getElementById("pdf-message-text");
    const retryButton = document.getElementById("retry-button");
    const errorDownload = document.getElementById("error-download-link");
    const titleEl = document.getElementById("reader-title");
    const backLink = document.getElementById("reader-back");
    const pageInput = document.getElementById("page-input");
    const pageCountEl = document.getElementById("page-count");
    const downloadLink = document.getElementById("download-pdf");
    const fitWidthBtn = document.getElementById("fit-width");

    let pdfDoc = null;
    let currentPage = 1;
    let scaleMode = "fit-width"; // fit-width | number
    let manualScale = 1;
    let lastScale = 1;
    let renderSeq = 0;
    let surahNumber = null;

    function getParam(name) {
        return new URLSearchParams(window.location.search).get(name);
    }

    function savePosition(page) {
        try {
            localStorage.setItem(STORAGE_KEY, JSON.stringify({
                surah: Number(surahNumber),
                page: page
            }));
        } catch (e) { /* storage unavailable */ }
    }

    function showError(text) {
        console.error("[reader]", text);
        messageText.textContent = text || "Tidak dapat memuatkan fail PDF tafsir ini.";
        message.hidden = false;
        loading.hidden = true;
    }

    function hideMessages() {
        message.hidden = true;
        loading.hidden = false;
    }

    function computeScale(page) {
        if (scaleMode === "fit-width") {
            const viewport = page.getViewport({ scale: 1 });
            const available = Math.max(280, container.clientWidth - 16);
            return Math.max(0.2, available / viewport.width);
        }
        return manualScale;
    }

    async function renderPage(num) {
        if (!pdfDoc) return;
        num = Math.min(Math.max(1, num), pdfDoc.numPages);
        currentPage = num;
        renderSeq += 1;
        const seq = renderSeq;

        try {
            const page = await pdfDoc.getPage(num);
            if (seq !== renderSeq) return;

            const scale = computeScale(page);
            lastScale = scale;
            const viewport = page.getViewport({ scale: scale });
            const dpr = window.devicePixelRatio || 1;
            const cssScale = scale * Math.min(dpr, 2.5); // Cap high-DPI scaling to prevent memory spikes on mobile
            const hiResViewport = page.getViewport({ scale: cssScale });

            view.innerHTML = "";
            const canvas = document.createElement("canvas");
            canvas.width = Math.floor(hiResViewport.width);
            canvas.height = Math.floor(hiResViewport.height);
            canvas.style.width = Math.floor(viewport.width) + "px";
            canvas.style.height = Math.floor(viewport.height) + "px";
            canvas.setAttribute("role", "img");
            canvas.setAttribute("aria-label", `Halaman ${num} daripada ${pdfDoc.numPages}`);
            view.appendChild(canvas);

            await page.render({
                canvasContext: canvas.getContext("2d"),
                viewport: hiResViewport
            }).promise;
            if (seq !== renderSeq) return;

            pageInput.value = num;
            pageInput.max = pdfDoc.numPages;
            pageCountEl.textContent = "/ " + pdfDoc.numPages;
            loading.hidden = true;
            window.scrollTo(0, 0);
            savePosition(num);
        } catch (err) {
            console.error("[reader] render failed:", err);
            if (seq === renderSeq) showError("Gagal memaparkan halaman ini.");
        }
    }

    function zoom(delta) {
        if (!pdfDoc) return;
        if (scaleMode === "fit-width") {
            manualScale = lastScale;
            scaleMode = "number";
        }
        manualScale = Math.min(4, Math.max(0.4, manualScale + delta));
        renderPage(currentPage);
    }

    function toggleFitWidth() {
        if (!pdfDoc) return;
        scaleMode = "fit-width";
        renderPage(currentPage);
    }

    async function load() {
        hideMessages();
        pdfDoc = null;

        surahNumber = parseInt(getParam("surah"), 10);
        const startPage = parseInt(getParam("page"), 10);

        if (!surahNumber || surahNumber < 1 || surahNumber > 114) {
            showError("Nombor surah tidak sah.");
            backLink.href = "index.html";
            return;
        }

        let mapping;
        try {
            const res = await fetch("data/surah_pdfs.json");
            if (!res.ok) throw new Error("HTTP " + res.status);
            mapping = await res.json();
        } catch (err) {
            console.error("[reader] failed to load PDF mapping:", err);
            showError("Gagal memuatkan indeks fail PDF.");
            return;
        }

        const pdfUrl = mapping.pdfs && mapping.pdfs[String(surahNumber)];
        if (!pdfUrl) {
            showError("Nota tafsir PDF untuk surah ini belum tersedia.");
            return;
        }

        backLink.href = "surah_" + surahNumber + ".html";
        downloadLink.href = pdfUrl;
        errorDownload.href = pdfUrl;

        try {
            const task = pdfjsLib.getDocument(pdfUrl);
            pdfDoc = await task.promise;
        } catch (err) {
            console.error("[reader] failed to load PDF:", pdfUrl, err);
            showError("Tidak dapat memuatkan fail PDF tafsir ini. Sila periksa sambungan internet anda atau muat turun fail secara terus.");
            return;
        }

        titleEl.textContent = "Surah " + surahNumber;
        fetch("data/all_surahs.json")
            .then(r => r.json())
            .then(data => {
                const s = data.children.find(x => x.number === surahNumber);
                if (s) {
                    titleEl.textContent = `${s.number}. ${s.englishName} (${s.name})`;
                    document.title = `${s.englishName} – Nota Tafsir Maulana Asri`;
                }
            })
            .catch(() => { /* keep numeric title */ });

        await renderPage(startPage >= 1 && startPage <= pdfDoc.numPages ? startPage : 1);
    }

    // Touch swipe navigation for mobile
    let touchStartX = 0;
    let touchStartY = 0;

    view.addEventListener("touchstart", (e) => {
        if (e.touches.length === 1) {
            touchStartX = e.touches[0].clientX;
            touchStartY = e.touches[0].clientY;
        }
    }, { passive: true });

    view.addEventListener("touchend", (e) => {
        if (e.changedTouches.length === 1) {
            const deltaX = e.changedTouches[0].clientX - touchStartX;
            const deltaY = e.changedTouches[0].clientY - touchStartY;

            // Only trigger if horizontal swipe is prominent (> 60px) and vertical displacement is small (< 50px)
            if (Math.abs(deltaX) > 60 && Math.abs(deltaY) < 50) {
                if (deltaX < 0) {
                    // Swiped left -> Next page
                    renderPage(currentPage + 1);
                } else {
                    // Swiped right -> Previous page
                    renderPage(currentPage - 1);
                }
            }
        }
    }, { passive: true });

    document.getElementById("prev-page").addEventListener("click", () => renderPage(currentPage - 1));
    document.getElementById("next-page").addEventListener("click", () => renderPage(currentPage + 1));
    document.getElementById("zoom-in").addEventListener("click", () => zoom(0.2));
    document.getElementById("zoom-out").addEventListener("click", () => zoom(-0.2));
    if (fitWidthBtn) fitWidthBtn.addEventListener("click", toggleFitWidth);
    retryButton.addEventListener("click", load);

    document.getElementById("goto-form").addEventListener("submit", (event) => {
        event.preventDefault();
        const n = parseInt(pageInput.value, 10);
        if (n >= 1) renderPage(n);
    });

    pageInput.addEventListener("change", () => {
        const n = parseInt(pageInput.value, 10);
        if (n >= 1) renderPage(n);
    });

    document.addEventListener("keydown", (event) => {
        if (event.target.tagName === "INPUT") return;
        if (event.key === "ArrowLeft") renderPage(currentPage - 1);
        else if (event.key === "ArrowRight") renderPage(currentPage + 1);
    });

    // Re-render on resize when in fit-width mode
    let resizeTimer = null;
    window.addEventListener("resize", () => {
        if (scaleMode !== "fit-width" || !pdfDoc) return;
        clearTimeout(resizeTimer);
        resizeTimer = setTimeout(() => renderPage(currentPage), 250);
    });

    load();
})();
