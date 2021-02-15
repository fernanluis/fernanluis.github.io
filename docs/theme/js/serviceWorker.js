"use strict";
// pregunta si el navegador tienesoporte para Service Workers
if ("serviceWorker" in navigator) {
  window.addEventListener("load", function() { //en caso de que lo tenga se suscribe al evento Load
    navigator.serviceWorker // invocar dentro del Service Worker
      .register("/sw.js", { scope: "/" }) // la función register para indicar qué archivo será el Service Worker
      .catch(function(e) { // en caso de la presencia de algún error se mostrará por consola.
        console.error("Error during service worker registration:", e);
      });
  });
}
