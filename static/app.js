(function () {
  "use strict";
  var dataEl = document.getElementById("page-data");
  if (!dataEl) return;
  var D = JSON.parse(dataEl.textContent);
  var U = D.ui;

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

  /* ---------- Site settings (edited from the admin panel) ---------- */
  var L = D.lang;
  var PAGE = D.page || "";
  var settingsUrl = (D.rel || "") + "static/site-settings.json";
  window.IFW_SETTINGS = fetch(settingsUrl, { cache: "no-cache" })
    .then(function (r) { return r.ok ? r.json() : {}; })
    .catch(function () { return {}; });
  window.IFW_SETTINGS.then(applySettings);

  function tx(obj) { return obj ? (obj[L] || obj.en || "") : ""; }
  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }
  function safeUrl(u) { return typeof u === "string" && /^https:\/\//.test(u) ? u : ""; }
  function onPage(list) {
    if (!list || !list.length) return false;
    return list.indexOf("all") >= 0 || list.indexOf(PAGE) >= 0;
  }

  function productUrl(p, tag) {
    var u = safeUrl(p.url);
    if (u) {
      if (tag && /amazon\.in/.test(u) && !/[?&]tag=/.test(u)) u += (u.indexOf("?") >= 0 ? "&" : "?") + "tag=" + encodeURIComponent(tag);
      return u;
    }
    if (p.search && tag) return "https://www.amazon.in/s?k=" + encodeURIComponent(p.search) + "&tag=" + encodeURIComponent(tag);
    return "";
  }

  function applySettings(S) {
    S = S || {};
    renderAnnouncement(S.announcement);
    renderAffiliates(S.affiliate);
    renderTelegram(S.telegram);
    runAds(S.ads);
  }

  function renderAnnouncement(A) {
    if (!A || !A.enabled || !tx(A.text)) return;
    var bar = el("div", "announce");
    var u = safeUrl(A.url);
    var inner = u ? el("a", "", tx(A.text)) : el("span", "", tx(A.text));
    if (u) { inner.href = u; inner.rel = "noopener"; }
    bar.appendChild(inner);
    var main = document.querySelector("main");
    if (main) main.insertBefore(bar, main.firstChild);
  }

  function renderAffiliates(A) {
    if (!A || !A.products) return;
    var tag = (A.amazonTag || "").trim();
    document.querySelectorAll(".aff-slot").forEach(function (slot) {
      var key = slot.getAttribute("data-aff");
      var list = A.products.filter(function (p) {
        return p.enabled !== false && (p.pages || []).indexOf(key) >= 0 && productUrl(p, tag);
      }).slice(0, A.maxPerSlot || 4);
      if (!list.length) return;
      slot.appendChild(el("h2", "small-h", slot.getAttribute("data-title")));
      var ul = el("ul", "aff-list");
      list.forEach(function (p) {
        var li = el("li"), a = el("a", "aff-card");
        a.href = productUrl(p, tag); a.target = "_blank"; a.rel = "sponsored nofollow noopener";
        var img = safeUrl(p.image);
        if (img) { var im = el("img"); im.src = img; im.alt = ""; im.loading = "lazy"; a.appendChild(im); }
        else { var ic = el("span", "aff-icon", "🛍"); ic.setAttribute("aria-hidden", "true"); a.appendChild(ic); }
        a.appendChild(el("span", "aff-title", tx(p.title)));
        if (p.price) a.appendChild(el("span", "aff-price", p.price));
        a.appendChild(el("span", "aff-store", (p.store || "Shop") + " →"));
        li.appendChild(a); ul.appendChild(li);
      });
      slot.appendChild(ul);
      slot.appendChild(el("p", "hint", slot.getAttribute("data-note")));
    });
  }

  var TG_ICON = '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="12" fill="#229ED9"/><path d="M5.4 11.8l11.1-4.3c.5-.2 1 .1.8.9l-1.9 8.9c-.1.6-.5.8-1 .5l-2.9-2.1-1.4 1.3c-.2.2-.3.3-.6.3l.2-3 5.4-4.9c.2-.2 0-.3-.3-.1l-6.7 4.2-2.9-.9c-.6-.2-.6-.6.2-.8z" fill="#fff"/></svg>';

  function renderTelegram(T) {
    if (!T || !T.enabled) return;
    var u = safeUrl(T.url);
    if (!u || !/^https:\/\/(t\.me|telegram\.me)\//.test(u)) return;
    if (!onPage(T.pages)) return;
    if (T.inline !== false) {
      document.querySelectorAll(".tg-slot").forEach(function (slot) {
        var box = el("a", "tg-box");
        box.href = u; box.target = "_blank"; box.rel = "noopener";
        var icon = el("span", "tg-icon"); icon.innerHTML = TG_ICON;
        var body = el("span", "tg-body");
        body.appendChild(el("span", "tg-title", tx(T.title)));
        body.appendChild(el("span", "tg-text", tx(T.text)));
        box.appendChild(icon); box.appendChild(body);
        box.appendChild(el("span", "tg-btn", tx(T.button)));
        slot.appendChild(box);
      });
    }
    var closed = false;
    try { closed = sessionStorage.getItem("tgClosed") === "1"; } catch (e) {}
    if (T.sticky !== false && !closed) {
      var bar = el("div", "tg-sticky");
      var link = el("a", "tg-sticky-link");
      link.href = u; link.target = "_blank"; link.rel = "noopener";
      var ic2 = el("span", "tg-icon"); ic2.innerHTML = TG_ICON;
      link.appendChild(ic2);
      link.appendChild(el("span", "tg-sticky-text", tx(T.title)));
      link.appendChild(el("span", "tg-btn", tx(T.button)));
      var x = el("button", "tg-close", "×");
      x.type = "button"; x.setAttribute("aria-label", "Close");
      x.addEventListener("click", function () {
        bar.remove();
        document.body.classList.remove("has-sticky");
        try { sessionStorage.setItem("tgClosed", "1"); } catch (e) {}
      });
      bar.appendChild(link); bar.appendChild(x);
      document.body.appendChild(bar);
      document.body.classList.add("has-sticky");
    }
  }

  function runAds(Ad) {
    Ad = Ad || {};
    var client = (Ad.adsenseClient || "").trim();
    if (/^ca-pub-\d{10,20}$/.test(client)) {
      if (!document.querySelector('script[src*="adsbygoogle.js"]')) {
        var sc = document.createElement("script");
        sc.async = true; sc.crossOrigin = "anonymous";
        sc.src = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=" + encodeURIComponent(client);
        document.head.appendChild(sc);
      }
      var slots = { top: (Ad.slotTop || "").trim(), middle: (Ad.slotMiddle || "").trim() };
      document.querySelectorAll(".ad-slot").forEach(function (box) {
        var id = slots[box.getAttribute("data-slot")];
        if (!/^\d{6,20}$/.test(id || "")) return;
        var ins = document.createElement("ins");
        ins.className = "adsbygoogle"; ins.style.display = "block";
        ins.setAttribute("data-ad-client", client); ins.setAttribute("data-ad-slot", id);
        ins.setAttribute("data-ad-format", "auto"); ins.setAttribute("data-full-width-responsive", "true");
        box.appendChild(ins);
        (window.adsbygoogle = window.adsbygoogle || []).push({});
      });
    }
    var ga = (Ad.gaId || "").trim();
    if (/^G-[A-Z0-9]{4,15}$/.test(ga)) {
      var g = document.createElement("script");
      g.async = true; g.src = "https://www.googletagmanager.com/gtag/js?id=" + encodeURIComponent(ga);
      document.head.appendChild(g);
      window.dataLayer = window.dataLayer || [];
      window.gtag = function () { window.dataLayer.push(arguments); };
      window.gtag("js", new Date()); window.gtag("config", ga);
    }
  }
})();
