/* Ember service worker — network-first.
   Scop: utilizatorul primeste MEREU ultima versiune cand e online (gata cu cache-ul vechi
   blocat in PWA-ul iOS), iar offline serveste ultima copie buna. Atinge DOAR resurse
   same-origin (GET); cererile catre fonturi/AI/releu (cross-origin) trec neatinse. */
const CACHE = 'ember-cache-v1';

self.addEventListener('install', (e) => { self.skipWaiting(); });

self.addEventListener('activate', (e) => {
  e.waitUntil((async () => {
    const keys = await caches.keys();
    await Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    await self.clients.claim();
  })());
});

self.addEventListener('fetch', (e) => {
  const req = e.request;
  if (req.method !== 'GET') return;
  let url;
  try { url = new URL(req.url); } catch (_) { return; }
  if (url.origin !== self.location.origin) return; // nu atingem tertii (fonturi/AI/releu)
  e.respondWith((async () => {
    try {
      const net = await fetch(req);                 // mereu incearca reteaua intai
      if (net && net.ok) {
        try { const c = await caches.open(CACHE); c.put(req, net.clone()); } catch (_) {}
      }
      return net;
    } catch (_) {
      const cached = await caches.match(req);        // offline -> ultima copie buna
      return cached || new Response('Offline', { status: 503, statusText: 'Offline' });
    }
  })());
});
