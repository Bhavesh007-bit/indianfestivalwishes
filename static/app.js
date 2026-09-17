(function () {
  "use strict";
  var dataEl = document.getElementById("page-data");
  if (!dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var U = D.ui;
  var S = window.SITE || {};

  function fmt(s, o) {
    return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ""; });
  }
  // Keep names short and plain. The name is only drawn on canvas or set via textContent.
  function cleanName(v) {
    return String(v || "").replace(/[\u0000-\u001F\u007F<>"`]/g, "").replace(/\s+/g, " ").trim().slice(0, 30);
  }

  var params = new URLSearchParams(location.search);
  var incoming = cleanName(params.get("name"));

  try { localStorage.setItem("lang", D.lang); } catch (e) {}

  // Keep the card settings when switching language
  if (location.search) {
    document.querySelectorAll(".lang-list a").forEach(function (a) {
      var u = new URL(a.getAttribute("href"), location.href);
      ["name", "to", "n1", "n2", "r", "w", "s", "t"].forEach(function (k) { if (params.get(k)) u.searchParams.set(k, params.get(k)); });
      a.setAttribute("href", u.pathname + u.search);
    });
  }

  /* ---------- Today indicator ---------- */
  function todayISO() {
    var d = new Date();
    return d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0") + "-" + String(d.getDate()).padStart(2, "0");
  }
  var t = todayISO();
  var todayIdx = D.dates.indexOf(t);
  if (todayIdx >= 0) {
    var tile = document.querySelector('.days-grid a[data-day="' + (todayIdx + 1) + '"]');
    if (tile) {
      tile.classList.add("is-today");
      var tag = document.createElement("span");
      tag.className = "today-tag";
      tag.textContent = U.today_short;
      tile.appendChild(tag);
    }
  }
  var note = document.getElementById("today-note");
  if (note) {
    var span = document.createElement("span");
    note.appendChild(span);
    if (todayIdx >= 0) {
      span.textContent = fmt(U.today_is, { n: todayIdx + 1 });
      var a = document.createElement("a");
      a.className = "btn btn-primary btn-small";
      a.href = "day-" + (todayIdx + 1) + ".html";
      a.textContent = U.open_today;
      note.appendChild(a);
    } else if (t < D.dates[0]) {
      span.textContent = fmt(U.starts_in, { d: Math.round((Date.parse(D.dates[0]) - Date.parse(t)) / 86400000) });
    } else if (t === D.dussehra) {
      span.textContent = U.dussehra_today;
    } else {
      span.textContent = U.over;
    }
  }

  /* ---------- Copy buttons ---------- */
  function copyText(text) {
    if (navigator.clipboard && window.isSecureContext) return navigator.clipboard.writeText(text);
    return new Promise(function (res, rej) {
      var ta = document.createElement("textarea");
      ta.value = text; ta.setAttribute("readonly", ""); ta.style.position = "fixed"; ta.style.opacity = "0";
      document.body.appendChild(ta); ta.select();
      try { document.execCommand("copy"); res(); } catch (e) { rej(e); }
      document.body.removeChild(ta);
    });
  }
  document.querySelectorAll("[data-copy]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var src = document.getElementById(btn.getAttribute("data-copy"));
      if (!src) return;
      copyText(src.textContent.trim() + "\n" + location.origin + location.pathname).then(function () {
        btn.textContent = U.copied;
        setTimeout(function () { btn.textContent = U.copy; }, 1800);
      });
    });
  });

  /* ---------- Recipe servings ---------- */
  var serv = document.getElementById("servings");
  if (serv) {
    var fmtQty = function (q, unit) {
      if (unit === "g" || unit === "ml") return String(q >= 50 ? Math.round(q / 5) * 5 : Math.round(q));
      if (unit === "pinch") return String(Math.max(1, Math.round(q)));
      var whole = Math.floor(q + 1e-9);
      var quarters = Math.round((q - whole) * 4);
      if (quarters === 4) { whole += 1; quarters = 0; }
      var s = (whole ? String(whole) : "") + ["", "¼", "½", "¾"][quarters];
      return s || "0";
    };
    var apply = function () {
      var n = Math.min(30, Math.max(1, parseInt(serv.value, 10) || 1));
      serv.value = n;
      document.querySelectorAll(".qty").forEach(function (el) {
        el.textContent = fmtQty(parseFloat(el.getAttribute("data-q")) * n, el.getAttribute("data-u"));
      });
    };
    serv.addEventListener("input", apply);
    serv.addEventListener("change", apply);
    document.querySelectorAll(".step-btn").forEach(function (b) {
      b.addEventListener("click", function () {
        serv.value = (parseInt(serv.value, 10) || 1) + parseInt(b.getAttribute("data-step"), 10);
        apply();
      });
    });
  }

  /* ---------- Menu and language ---------- */
  var menuBtn = document.getElementById("menu-btn");
  var menu = document.getElementById("site-menu");
  if (menuBtn && menu) {
    menuBtn.addEventListener("click", function () {
      var open = menuBtn.getAttribute("aria-expanded") === "true";
      menuBtn.setAttribute("aria-expanded", open ? "false" : "true");
      menu.classList.toggle("is-open", !open);
    });
  }
  var langBtn = document.getElementById("lang-btn");
  var langList = document.getElementById("lang-list");
  if (langBtn && langList) {
    langBtn.addEventListener("click", function (e) {
      e.stopPropagation();
      var open = langBtn.getAttribute("aria-expanded") === "true";
      langBtn.setAttribute("aria-expanded", open ? "false" : "true");
      langList.hidden = open;
    });
    document.addEventListener("click", function () { langBtn.setAttribute("aria-expanded", "false"); langList.hidden = true; });
  }

  /* ---------- Affiliate products (edit static/affiliates.js) ---------- */
  var A = window.AFFILIATES;
  document.querySelectorAll(".aff-slot").forEach(function (slot) {
    if (!A || !A.products) return;
    var tag = slot.getAttribute("data-aff");
    var list = A.products.filter(function (p) {
      return p.url && /^https:\/\//.test(p.url) && (p.pages || []).indexOf(tag) >= 0;
    }).slice(0, A.maxPerSlot || 4);
    if (!list.length) return;
    var h = document.createElement("h2");
    h.className = "small-h";
    h.textContent = slot.getAttribute("data-title");
    slot.appendChild(h);
    var ul = document.createElement("ul");
    ul.className = "aff-list";
    list.forEach(function (p) {
      var li = document.createElement("li");
      var a = document.createElement("a");
      a.href = p.url;
      a.target = "_blank";
      a.rel = "sponsored nofollow noopener";
      a.className = "aff-card";
      if (p.image && /^https:\/\//.test(p.image)) {
        var im = document.createElement("img");
        im.src = p.image; im.alt = ""; im.loading = "lazy";
        a.appendChild(im);
      }
      var t = document.createElement("span");
      t.className = "aff-title";
      t.textContent = (p.title && (p.title[D.lang] || p.title.en)) || "";
      a.appendChild(t);
      if (p.price) { var pr = document.createElement("span"); pr.className = "aff-price"; pr.textContent = p.price; a.appendChild(pr); }
      var st = document.createElement("span");
      st.className = "aff-store";
      st.textContent = (p.store || "Shop") + " →";
      a.appendChild(st);
      li.appendChild(a);
      ul.appendChild(li);
    });
    slot.appendChild(ul);
    var n = document.createElement("p");
    n.className = "hint";
    n.textContent = slot.getAttribute("data-note");
    slot.appendChild(n);
  });

  /* ---------- Ads and analytics (set IDs in static/config.js) ---------- */
  if (S.adsenseClient) {
    if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
      var s = document.createElement("script");
      s.async = true;
      s.crossOrigin = "anonymous";
      s.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(S.adsenseClient);
      document.head.appendChild(s);
    }
    document.querySelectorAll(".ad-slot").forEach(function (el) {
      var slotId = (S.adSlots || {})[el.getAttribute("data-slot")];
      if (!slotId) return;
      var ins = document.createElement("ins");
      ins.className = "adsbygoogle";
      ins.style.display = "block";
      ins.setAttribute("data-ad-client", S.adsenseClient);
      ins.setAttribute("data-ad-slot", slotId);
      ins.setAttribute("data-ad-format", "auto");
      ins.setAttribute("data-full-width-responsive", "true");
      el.appendChild(ins);
      (window.adsbygoogle = window.adsbygoogle || []).push({});
    });
  }
  if (S.gaId) {
    var g = document.createElement("script");
    g.async = true;
    g.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(S.gaId);
    document.head.appendChild(g);
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag("js", new Date());
    window.gtag("config", S.gaId);
  }
})();
