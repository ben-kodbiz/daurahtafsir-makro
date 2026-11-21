/**
 * Daurah Tafsir Makro — Service Worker (PWA Shell Caching)
 * Policy:
 * 1. Cache UI shell (HTML, CSS, JS, JSON data, Icons) for instant offline availability.
 * 2. Stale-While-Revalidate for app assets so updates propagate smoothly on new deployments.
 * 3. Strictly exclude heavy PDFs from automatic precaching to conserve user bandwidth and storage.
 */

const CACHE_NAME = "dtm-shell-v1.1";

const APP_SHELL = [
    "./",
    "index.html",
    "about.html",
    "reader.html",
    "styles.css",
    "script.js?v=3",
    "theme.js?v=2",
    "js/reader.js?v=2",
    "data/all_surahs.json",
    "data/surah_pdfs.json",
    "data/ms.json",
    "data/en.json",
    "images/icon.svg"
];

// Install: precache app shell
self.addEventListener("install", (event) => {
    event.waitUntil(
        caches.open(CACHE_NAME).then((cache) => {
            return cache.addAll(APP_SHELL).catch((err) => {
                console.warn("[SW] Some shell assets failed to precache:", err);
            });
        }).then(() => self.skipWaiting())
    );
});

// Activate: clean up outdated caches
self.addEventListener("activate", (event) => {
    event.waitUntil(
        caches.keys().then((keys) => {
            return Promise.all(
                keys.filter((key) => key !== CACHE_NAME).map((key) => caches.delete(key))
            );
        }).then(() => self.clients.claim())
    );
});

// Fetch strategy
self.addEventListener("fetch", (event) => {
    const request = event.request;
    const url = new URL(request.url);

    // Only handle GET requests
    if (request.method !== "GET") return;

    // RULE: NEVER auto-cache bulk PDF files in the service worker
    if (url.pathname.endsWith(".pdf") || url.pathname.includes("/pdfs/")) {
        return; // Let browser handle normally
    }

    // Network-First for HTML navigation requests (ensures updates deploy immediately)
    if (request.mode === "navigate") {
        event.respondWith(
            fetch(request)
                .then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        const copy = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
                    }
                    return networkResponse;
                })
                .catch(() => caches.match(request).then((cached) => cached || caches.match("index.html")))
        );
        return;
    }

    // Stale-While-Revalidate for static assets (CSS, JS, JSON, Images)
    if (url.origin === self.location.origin) {
        event.respondWith(
            caches.match(request).then((cachedResponse) => {
                const fetchPromise = fetch(request).then((networkResponse) => {
                    if (networkResponse && networkResponse.status === 200) {
                        const copy = networkResponse.clone();
                        caches.open(CACHE_NAME).then((cache) => cache.put(request, copy));
                    }
                    return networkResponse;
                }).catch(() => null);

                return cachedResponse || fetchPromise;
            })
        );
    }
});
