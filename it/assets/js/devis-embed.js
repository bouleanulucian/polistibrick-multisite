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
  };

  function attachResize(frame) {
    window.addEventListener("message", function (e) {
      if (!e.data || e.data.type !== "pb-devis-resize") return;
      var h = parseInt(e.data.height, 10);
      if (h > 0) frame.style.height = Math.max(560, h) + "px";
    });
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

    frame.src = base.replace(/\/$/, "") + "/?pays=" + encodeURIComponent(pays) + "&embed=1";
    attachResize(frame);
  }

  window.pbLoadDevisFrame = loadFrame;

  var frame = document.getElementById("pb-devis-frame");
  if (!frame) return;

  if (frame.dataset.lazy === "true") return;

  loadFrame(frame);
})();
