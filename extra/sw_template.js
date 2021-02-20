// plantilla, archivo javascript donde está todo el funcionamiento del Service Workers
// se definen 3 variables que van a permitir el service worker y también qué archivos voy a respaldar
// la idea del Service Worker es ejecutar tareas en segundo plano y una de las formas que hacer esto else {
// alojar en una caché todos los archivos estáticos o de mayor uso para luego ser consumidos cuando el usuario los requiera.

}
const version = "$VERSION$";
const currentCacheName = `fernanluisweb-${version}`;
const filesToCache = "$FILES_TO_CACHE$"

self.addEventListener('install', event => {
  event.waitUntil(
    caches.open(currentCacheName)
      .then(cache => cache.addAll(filesToCache)) // guardar archivos explicitados en la caché
      .then(self.skipWaiting())
  );
});

self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys()
      .then(cacheNames => cacheNames.filter(cacheName => ! currentCacheName.includes(cacheName) )) // activación, limpiar la caché para eliminar todos los archivos previam guardados y
      .then(cachesToDelete => Promise.all(cachesToDelete.map(cacheToDelete => caches.delete(cacheToDelete)))) // y actualizarlos con la caché nueva.
      .then(self.clients.claim())
  );
});
// evento fetch se lanza cada vez que el navegador solicita un recurso al servidor web. Se intercepta la solicitud y en el caso de tener el archivo guadado en la memoria caché se va a devolver sirectamente desde la memoria caché
self.addEventListener('fetch', event => {
  const url = event.request.url;
  const scope = self.registration.scope;

	if (!url.startsWith(scope)) {
		return;
  }

  event.respondWith(
    caches.open(currentCacheName)
      .then(cache => cache.match(event.request, {ignoreSearch: true}) )
      .then(response => response || fetch(event.request) ) // en el que caso de no contar con el archivo se hará la peticiónal servidor.
  );
});
