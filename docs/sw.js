// plantilla, archivo javascript donde está todo el funcionamiento del Service Workers
// se definen 3 variables que van a permitir el service worker y también qué archivos voy a respaldar
// la idea del Service Worker es ejecutar tareas en segundo plano y una de las formas que hacer esto else {
// alojar en una caché todos los archivos estáticos o de mayor uso para luego ser consumidos cuando el usuario los requiera.

}
const version = "fc14218";
const currentCacheName = `fernanluisweb-${version}`;
const filesToCache = [
    "/",
    "/archives/",
    "/archives/index.html",
    "/author/anonimo/",
    "/author/anonimo/index.html",
    "/author/fernando-ramos/",
    "/author/fernando-ramos/index.html",
    "/author/luis-ramos/",
    "/author/luis-ramos/index.html",
    "/authors/",
    "/authors/index.html",
    "/categories/",
    "/categories/index.html",
    "/category/curso/",
    "/category/curso/index.html",
    "/category/filosofia/",
    "/category/filosofia/index.html",
    "/category/misc/",
    "/category/misc/index.html",
    "/drafts/la-soluci\u00f3n.html",
    "/drafts/pages/portfolio.html",
    "/finanzas/",
    "/finanzas/index.html",
    "/images/Pelican-logo-no-oficial-thumbnail.png",
    "/images/Pelican-logo-thumbnail.png",
    "/index.html",
    "/link/buscador/",
    "/link/buscador/index.html",
    "/link/buscardor/",
    "/link/buscardor/index.html",
    "/link/sitio-personal/",
    "/link/sitio-personal/index.html",
    "/portafolio/",
    "/portafolio/index.html",
    "/posts/con-plugins-la-vida-es-mas-sencilla/",
    "/posts/con-plugins-la-vida-es-mas-sencilla/index.html",
    "/posts/mi-primer-articulo/",
    "/posts/mi-primer-articulo/index.html",
    "/posts/mira-mas-alla/",
    "/posts/mira-mas-alla/index.html",
    "/posts/titulo-del-articulo/",
    "/posts/titulo-del-articulo/index.html",
    "/sitemap.xml",
    "/sobre-mi/",
    "/sobre-mi/index.html",
    "/tag/frases/",
    "/tag/frases/index.html",
    "/tag/reflexion/",
    "/tag/reflexion/index.html",
    "/tags/",
    "/tags/index.html",
    "/theme/css/01_w3.css",
    "/theme/css/02_style.css",
    "/theme/css/03_jqcloud.css",
    "/theme/css/04_font-awesome.min.css",
    "/theme/css/05_gruvbox.css",
    "/theme/css/06_lazy_load.css",
    "/theme/css/font-awesome.min.css",
    "/theme/css/gruvbox.css",
    "/theme/css/jqcloud.css",
    "/theme/css/pygments-highlight-github.css",
    "/theme/css/style.css",
    "/theme/css/style_bundled.css",
    "/theme/css/w3.css",
    "/theme/fonts/fontawesome-webfont.svg",
    "/theme/js/jqcloud.min.js",
    "/theme/js/lazy_loading.js",
    "/theme/js/scripts_bundled.js"
]

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
