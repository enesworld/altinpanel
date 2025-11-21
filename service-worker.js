self.addEventListener('install', (event) => {
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  clients.claim();
});

// Şimdilik tüm istekleri direkt ağa gönderiyoruz
self.addEventListener('fetch', () => {
  // Buraya cache mantığı ekleyebilirsin; şimdilik boş.
});
