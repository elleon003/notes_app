const CACHE_NAME = 'idea-manager-cache-v1';
const OFFLINE_QUEUE = 'offline-queue';
const urlsToCache = [
  '/',
  '/static/css/styles.css',
  '/static/js/main.js',
  '/static/js/db.js',
  '/static/manifest.json',
  '/static/img/icon-192x192.png',
  '/static/img/icon-512x512.png',
  // Add other important assets
];

self.addEventListener('install', (event) => {
  event.waitUntil(
    caches.open(CACHE_NAME)
      .then((cache) => cache.addAll(urlsToCache))
  );
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((cacheNames) => {
      return Promise.all(
        cacheNames.map((cacheName) => {
          if (cacheName !== CACHE_NAME) {
            return caches.delete(cacheName);
          }
        })
      );
    })
  );
});

self.addEventListener('fetch', (event) => {
  if (event.request.method === 'GET') {
    event.respondWith(
      caches.match(event.request)
        .then((response) => {
          if (response) {
            return response;
          }
          return fetch(event.request).then(
            (response) => {
              if(!response || response.status !== 200 || response.type !== 'basic') {
                return response;
              }
              const responseToCache = response.clone();
              caches.open(CACHE_NAME)
                .then((cache) => {
                  cache.put(event.request, responseToCache);
                });
              return response;
            }
          );
        })
    );
  } else if (event.request.method === 'POST' && !navigator.onLine) {
    // If it's a POST request and we're offline, add it to the offline queue
    event.respondWith(
      addToOfflineQueue(event.request.clone())
        .then(() => new Response(JSON.stringify({ status: 'queued' }), {
          headers: { 'Content-Type': 'application/json' }
        }))
    );
  }
});

async function addToOfflineQueue(request) {
  const db = await openDB();
  const tx = db.transaction(OFFLINE_QUEUE, 'readwrite');
  const store = tx.objectStore(OFFLINE_QUEUE);
  const serializedRequest = await serializeRequest(request);
  await store.add(serializedRequest);
  await tx.complete;
}

async function serializeRequest(request) {
  const body = await request.text();
  return {
    url: request.url,
    method: request.method,
    headers: Object.fromEntries(request.headers.entries()),
    body: body
  };
}

self.addEventListener('sync', (event) => {
  if (event.tag === 'sync-ideas') {
    event.waitUntil(syncOfflineQueue());
  }
});

async function syncOfflineQueue() {
  const db = await openDB();
  const tx = db.transaction(OFFLINE_QUEUE, 'readwrite');
  const store = tx.objectStore(OFFLINE_QUEUE);
  const requests = await store.getAll();

  for (const request of requests) {
    try {
      await fetch(request.url, {
        method: request.method,
        headers: request.headers,
        body: request.body
      });
      await store.delete(request.id);
    } catch (error) {
      console.error('Failed to sync request:', error);
      // You might want to implement a retry mechanism here
    }
  }

  await tx.complete;
}

function openDB() {
  return new Promise((resolve, reject) => {
    const request = indexedDB.open('IdeaManagerDB', 1);
    
    request.onerror = (event) => reject(event.target.error);
    
    request.onsuccess = (event) => resolve(event.target.result);
    
    request.onupgradeneeded = (event) => {
      const db = event.target.result;
      if (!db.objectStoreNames.contains(OFFLINE_QUEUE)) {
        db.createObjectStore(OFFLINE_QUEUE, { keyPath: 'id', autoIncrement: true });
      }
    };
  });
}
