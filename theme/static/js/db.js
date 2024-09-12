let db;

const dbPromise = indexdDB.open('IdeaManagerDB', 1, (upgradeDb) => {
  if(!upgradeDb.objectStoreNames.contains('ideas')) {
    upgradeDb.createObjectStore('ideas', {keyPath: 'id', autoIncrement: true});
  }
});

dbPromise.then((database) => {
  db = database;
});

async function saveIdea(idea) {
  if (navigator.onLine) {
    // Send directly to server
    const response = await fetch('/api/ideas/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(idea),
    });
    return await response.json();
  } else {
    // Store locally and queue for sync
    await addToOfflineQueue('/api/ideas/', 'POST', idea);
    return { status: 'queued' };
  }
}

async function addToOfflineQueue(url, method, data) {
  const db = await openDB();
  const tx = db.transaction(OFFLINE_QUEUE, 'readwrite');
  const store = tx.objectStore(OFFLINE_QUEUE);
  await store.add({
    url: url,
    method: method,
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  await tx.complete;
}


const getIdeas = async () => {
  const tx = db.transaction('ideas', 'readonly');
  const store = tx.objectStore('ideas');
  return await store.getAll();
};

