/* Polistibrick — încarcă aplicația de devis/ofertă în iframe (multi-țară) */
(function () {
  var UNAVAILABLE = {
    FR: "Le configurateur n'est pas encore disponible. Contactez-nous via la page Contact.",
    RO: "Configuratorul nu este încă disponibil. Contactați-ne prin pagina Contact.",
    IT: "Il configuratore non è ancora disponibile. Contattaci tramite la pagina Contatti.",
    EN: "The configurator is not yet available. Please contact us via the Contact page.",
    ES: "El configurador aún no está disponible. Contáctenos a través de la página de Contacto.",
    NL: "De configurator is nog niet beschikbaar. Neem contact met ons op via de Contactpagina.",
    DE: "Der Konfigurator ist noch nicht verfügbar. Kontaktieren Sie uns über die Kontaktseite.",
    IE: "The configurator is not yet available. Please contact us via the Contact page.",
    GB: "The configurator is not yet available. Please contact us via the Contact page.",
    ME: "Konfigurator još nije dostupan. Kontaktirajte nas preko stranice Kontakt.",
  };

  function attachResize(frame) {
    window.addEventListener("message", function (e) {
      if (!e.data || e.data.type !== "pb-devis-resize") return;
      var h = parseInt(e.data.height, 10);
      if (h > 0) frame.style.height = Math.max(560, h) + "px";
    });
  }

  var FALLBACK = {
    RO: ["Configuratorul nu s-a putut deschide aici.", "Deschide-l într-o filă nouă"],
    FR: ["Le configurateur n'a pas pu s'ouvrir ici.", "Ouvrir dans un nouvel onglet"],
    EN: ["The configurator could not open here.", "Open in a new tab"],
    IT: ["Il configuratore non si è aperto qui.", "Apri in una nuova scheda"],
    ES: ["El configurador no pudo abrirse aquí.", "Abrir en una pestaña nueva"],
    DE: ["Der Konfigurator konnte hier nicht geöffnet werden.", "In neuem Tab öffnen"],
    NL: ["De configurator kon hier niet openen.", "Openen in nieuw tabblad"],
  };

  /* Dacă aplicaţia refuză să se afişeze în pagină (ex. lista frame-ancestors
     din CSP-ul ei nu include acest domeniu), iframe-ul rămâne o casetă goală
     şi nu produce nicio eroare pe care s-o putem prinde. Aşteptăm semnalul ei
     de redimensionare; dacă nu vine, oferim clientului un link direct. */
  function watchdog(frame, url, pays) {
    var viu = false;
    window.addEventListener("message", function (e) {
      if (e.data && e.data.type === "pb-devis-resize") viu = true;
    });
    setTimeout(function () {
      if (viu || !frame.parentNode) return;
      var texte = FALLBACK[pays] || FALLBACK.EN;
      var box = document.createElement("p");
      box.className = "wm-devis-unavailable";
      box.style.cssText = "padding:32px 24px;text-align:center;color:var(--gray,#666);font-size:14px;line-height:1.7;";
      box.textContent = texte[0] + " ";
      var a = document.createElement("a");
      a.href = url;
      a.target = "_blank";
      a.rel = "noopener";
      a.textContent = texte[1];
      a.style.cssText = "color:var(--red,#C8102E);font-weight:600;";
      box.appendChild(a);
      frame.replaceWith(box);
    }, 6000);
  }

  function loadFrame(frame) {
    if (!frame || frame.src) return;

    var pays = (frame.dataset.pays || "RO").toUpperCase();
    var prodUrl = frame.dataset.appUrl || "";
    var previewUrl = frame.dataset.previewUrl || "";
    var host = window.location.hostname;
    var isLocal = host === "localhost" || host === "127.0.0.1" || host === "[::1]";
    var isPreview = host.includes("github.io");
    var base = isLocal
      ? "http://localhost:3100"
      : isPreview && previewUrl
        ? previewUrl
        : prodUrl;

    if (!base) {
      frame.replaceWith(
        (function () {
          var p = document.createElement("p");
          p.className = "wm-devis-unavailable";
          p.style.cssText = "padding:32px 24px;text-align:center;color:var(--gray,#666);font-size:14px;";
          p.textContent = UNAVAILABLE[pays] || UNAVAILABLE.FR;
          return p;
        })()
      );
      return;
    }

    var url = base.replace(/\/$/, "") + "/?pays=" + encodeURIComponent(pays) + "&embed=1";
    frame.src = url;
    attachResize(frame);
    watchdog(frame, url, pays);
  }

  window.pbLoadDevisFrame = loadFrame;

  var frame = document.getElementById("pb-devis-frame");
  if (!frame) return;

  if (frame.dataset.lazy === "true") return;

  loadFrame(frame);
})();
