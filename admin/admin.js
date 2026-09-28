/* IFW Admin — talks to the site's own server (/api/*). Vanilla JS, no build step. */
(function () {
  "use strict";

  /* ================================================================ data */

  var LANGS = [["hi", "हिंदी"], ["gu", "ગુજરાતી"], ["en", "English"]];
  var LANG_SHORT = { hi: "Hindi", gu: "Gujarati", en: "English" };

  var PAGES = [
    ["home", "Home"], ["navratri", "Navratri"], ["navratri-day", "Navratri ke 9 din"],
    ["recipes", "Vrat recipes"], ["garba", "Garba"],
    ["dussehra", "Dussehra", 1], ["karva-chauth", "Karva Chauth", 1], ["diwali", "Diwali", 1],
    ["birthday", "Birthday"], ["anniversary", "Anniversary"], ["wedding", "Wedding"],
    ["engagement", "Engagement"], ["good-morning", "Good Morning"], ["info", "About/Contact"]
  ];
  var PAGE_NAME = {};
  PAGES.forEach(function (p) { PAGE_NAME[p[0]] = p[1]; });
  PAGE_NAME.all = "Sabhi pages";

  var ALL_RELS = ["all", "friend", "family", "sibling", "spouse", "business", "devotional"];
  var OCCASIONS = [
    ["navratri", "Navratri", ALL_RELS],
    ["dussehra", "Dussehra", ALL_RELS],
    ["karva-chauth", "Karva Chauth", ["all", "spouse", "family", "friend", "devotional"]],
    ["diwali", "Diwali", ALL_RELS],
    ["birthday", "Birthday", ALL_RELS],
    ["anniversary", "Anniversary", ALL_RELS],
    ["wedding", "Wedding", ["all", "friend", "family", "sibling", "business", "devotional"]],
    ["engagement", "Engagement", ["all", "friend", "family", "sibling", "business", "devotional"]],
    ["good-morning", "Good Morning", ALL_RELS]
  ];
  var OCC = {};
  OCCASIONS.forEach(function (o) { OCC[o[0]] = o; });
  var RELS = { all: "Sabhi", friend: "Dost", family: "Parivar", sibling: "Bhai/Bahen", spouse: "Pati/Patni", business: "Business/Grahak", devotional: "Bhaktimay" };
  var SPEEDS = { slow: 35, medium: 60, fast: 95 };

  var VIEWS = [
    ["dashboard", "Haalat", "Site par abhi kya chalu hai", "grid"],
    ["products", "Products", "Amazon affiliate products", "bag"],
    ["telegram", "Telegram", "Channel box aur neeche ki patti", "send"],
    ["patti", "Patti", "Upar chalti announcement patti", "megaphone"],
    ["ads", "Ads", "AdSense aur Google Analytics", "chart"],
    ["wishes", "Wishes", "Apni wishes aur suvichar", "message"],
    ["backup", "Backup", "Purane versions, export aur import", "database"],
    ["account", "Account", "Password aur login", "shield"]
  ];
  var TABS = ["dashboard", "products", "patti", "wishes"];

  /* =============================================================== icons */

  var IC = {
    grid: '<rect x="3" y="3" width="7" height="9" rx="1.5"/><rect x="14" y="3" width="7" height="5" rx="1.5"/><rect x="14" y="12" width="7" height="9" rx="1.5"/><rect x="3" y="16" width="7" height="5" rx="1.5"/>',
    bag: '<path d="M6 2 3 6v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2V6l-3-4z"/><path d="M3 6h18"/><path d="M16 10a4 4 0 0 1-8 0"/>',
    send: '<path d="m22 2-7 20-4-9-9-4z"/><path d="M22 2 11 13"/>',
    megaphone: '<path d="m3 11 18-5v12L3 14v-3z"/><path d="M11.6 16.8a3 3 0 1 1-5.8-1.6"/>',
    chart: '<path d="M3 3v18h18"/><path d="M8 16v-5"/><path d="M13 16V8"/><path d="M18 16v-9"/>',
    message: '<path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"/><path d="M12 13.5s-3-1.8-3-3.8a1.6 1.6 0 0 1 3-.8 1.6 1.6 0 0 1 3 .8c0 2-3 3.8-3 3.8z"/>',
    database: '<ellipse cx="12" cy="5" rx="9" ry="3"/><path d="M3 5v14c0 1.7 4 3 9 3s9-1.3 9-3V5"/><path d="M3 12c0 1.7 4 3 9 3s9-1.3 9-3"/>',
    shield: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><path d="m9 12 2 2 4-4"/>',
    menu: '<path d="M4 6h16M4 12h16M4 18h16"/>',
    more: '<circle cx="5" cy="12" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="19" cy="12" r="1.5"/>',
    x: '<path d="M18 6 6 18M6 6l12 12"/>',
    external: '<path d="M15 3h6v6"/><path d="M10 14 21 3"/><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/>',
    logout: '<path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><path d="m16 17 5-5-5-5"/><path d="M21 12H9"/>',
    lock: '<rect x="4" y="11" width="16" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/>',
    user: '<circle cx="12" cy="8" r="4"/><path d="M4 21a8 8 0 0 1 16 0"/>',
    key: '<circle cx="7.5" cy="15.5" r="4.5"/><path d="m10.7 12.3 9.3-9.3"/><path d="m16 7 3 3"/><path d="m18 5 2 2"/>',
    eye: '<path d="M2 12s3.6-7 10-7 10 7 10 7-3.6 7-10 7-10-7-10-7z"/><circle cx="12" cy="12" r="3"/>',
    eyeOff: '<path d="M9.9 4.2A10 10 0 0 1 12 4c6.4 0 10 8 10 8a17 17 0 0 1-2.2 3.2"/><path d="M6.6 6.6A17 17 0 0 0 2 12s3.6 8 10 8a9.7 9.7 0 0 0 5.4-1.6"/><path d="M14.1 14.1a3 3 0 1 1-4.2-4.2"/><path d="m2 2 20 20"/>',
    plus: '<path d="M12 5v14M5 12h14"/>',
    trash: '<path d="M3 6h18"/><path d="M8 6V4h8v2"/><path d="M19 6l-1 14a2 2 0 0 1-2 2H8a2 2 0 0 1-2-2L5 6"/><path d="M10 11v6M14 11v6"/>',
    chevDown: '<path d="m6 9 6 6 6-6"/>',
    chevRight: '<path d="m9 6 6 6-6 6"/>',
    arrowUp: '<path d="M12 19V5"/><path d="m5 12 7-7 7 7"/>',
    arrowDown: '<path d="M12 5v14"/><path d="m19 12-7 7-7-7"/>',
    copy: '<rect x="9" y="9" width="12" height="12" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>',
    upload: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m17 8-5-5-5 5"/><path d="M12 3v12"/>',
    download: '<path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="m7 10 5 5 5-5"/><path d="M12 15V3"/>',
    restore: '<path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/><path d="M12 7v5l3 2"/>',
    check: '<path d="M20 6 9 17l-5-5"/>',
    alert: '<path d="M10.3 3.9 1.8 18a2 2 0 0 0 1.7 3h17a2 2 0 0 0 1.7-3L13.7 3.9a2 2 0 0 0-3.4 0z"/><path d="M12 9v4"/><path d="M12 17h.01"/>',
    info: '<circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/>',
    image: '<rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.1-3.1a2 2 0 0 0-2.8 0L6 21"/>',
    search: '<circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/>',
    sparkle: '<path d="M12 2l2.4 7.6L22 12l-7.6 2.4L12 22l-2.4-7.6L2 12l7.6-2.4z"/>',
    clock: '<circle cx="12" cy="12" r="10"/><path d="M12 6v6l4 2"/>',
    link: '<path d="M10 13a5 5 0 0 0 7.5.5l3-3a5 5 0 0 0-7-7l-1.7 1.7"/><path d="M14 11a5 5 0 0 0-7.5-.5l-3 3a5 5 0 0 0 7 7l1.7-1.7"/>',
    tag: '<path d="M20.6 13.4 13.4 20.6a2 2 0 0 1-2.8 0L3 13V3h10l7.6 7.6a2 2 0 0 1 0 2.8z"/><circle cx="7.5" cy="7.5" r="1.5"/>',
    globe: '<circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15 15 0 0 1 0 20 15 15 0 0 1 0-20z"/>',
    file: '<path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/>',
    arrowRight: '<path d="M5 12h14"/><path d="m12 5 7 7-7 7"/>'
  };
  var FLOWER = '<svg viewBox="0 0 40 40" aria-hidden="true" fill="currentColor"><g transform="translate(20 20)">' +
    [0, 45, 90, 135, 180, 225, 270, 315].map(function (a) { return '<ellipse rx="4.2" ry="9" cy="-9.5" transform="rotate(' + a + ')"/>'; }).join("") +
    '<circle r="5" fill="#D81E4A"/></g></svg>';

  function icon(name, cls) {
    var w = document.createElement("span");
    w.innerHTML = '<svg class="ico' + (cls ? " " + cls : "") + '" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true" focusable="false">' + (IC[name] || "") + "</svg>";
    return w.firstChild;
  }
  function hydrateIcons(root) {
    (root || document).querySelectorAll("[data-icon]").forEach(function (n) {
      if (n.firstChild) return;
      n.appendChild(icon(n.getAttribute("data-icon")));
    });
  }

  /* ============================================================= helpers */

  function $(id) { return document.getElementById(id); }
  var uid = 0;
  function nextId(p) { uid += 1; return (p || "f") + uid; }

  // h("div", {class:"x", on:{click:fn}, attrs...}, child, "text", ...)
  function h(tag, props) {
    var n = document.createElement(tag);
    props = props || {};
    Object.keys(props).forEach(function (k) {
      var v = props[k];
      if (v == null || v === false) return;
      if (k === "class") n.className = v;
      else if (k === "text") n.textContent = v;
      else if (k === "on") Object.keys(v).forEach(function (ev) { n.addEventListener(ev, v[ev]); });
      else if (k === "value") n.value = v;
      else if (k === "checked") n.checked = !!v;
      else if (k === "hidden") n.hidden = true;
      else n.setAttribute(k, v === true ? "" : v);
    });
    for (var i = 2; i < arguments.length; i++) add(n, arguments[i]);
    return n;
  }
  function add(n, c) {
    if (c == null || c === false) return;
    if (Array.isArray(c)) { c.forEach(function (x) { add(n, x); }); return; }
    n.appendChild(typeof c === "string" || typeof c === "number" ? document.createTextNode(String(c)) : c);
  }
  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); return n; }
  function clone(o) { return JSON.parse(JSON.stringify(o)); }
  function lines(v) { return String(v || "").split("\n").map(function (x) { return x.trim(); }).filter(Boolean); }
  function reduceMotion() { return window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches; }
  function fmtDate(d) {
    try {
      return new Date(d).toLocaleString("en-IN", { day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "2-digit" });
    } catch (e) { return String(d); }
  }
  function fmtSize(b) { return b < 1024 ? b + " B" : (b / 1024).toFixed(1) + " KB"; }
  function ago(ts) {
    var s = Math.round((Date.now() - ts) / 1000);
    if (s < 60) return "abhi abhi";
    if (s < 3600) return Math.round(s / 60) + " minute pehle";
    if (s < 86400) return Math.round(s / 3600) + " ghante pehle";
    return Math.round(s / 86400) + " din pehle";
  }

  /* ================================================================= api */

  function api(method, url, body, opts) {
    opts = opts || {};
    var headers = { "X-IFW": "1", "Accept": "application/json" };
    var init = { method: method, credentials: "same-origin", cache: "no-store", headers: headers };
    if (body !== undefined) {
      if (opts.raw) { init.body = body; headers["Content-Type"] = opts.type; }
      else { init.body = JSON.stringify(body); headers["Content-Type"] = "application/json"; }
    }
    if (opts.headers) Object.keys(opts.headers).forEach(function (k) { headers[k] = opts.headers[k]; });
    return fetch(url, init).then(function (r) {
      var ct = r.headers.get("Content-Type") || "";
      var p = ct.indexOf("json") >= 0 ? r.json().catch(function () { return {}; }) : r.text().then(function (t) { return { text: t }; });
      return p.then(function (data) {
        if (r.status === 401 && !opts.allow401) { sessionExpired(); }
        if (!r.ok) {
          var e = new Error((data && data.error) || ("Error " + r.status));
          e.status = r.status; e.data = data;
          throw e;
        }
        return data;
      });
    }, function () {
      var e = new Error("Server se connection nahi ho paaya. Internet check karo.");
      e.status = 0;
      throw e;
    });
  }

  /* ============================================================== toasts */

  function toast(text, kind) {
    kind = kind || "info";
    var closeBtn = h("button", { class: "icon-btn", type: "button", "aria-label": "Band karo" }, icon("x"));
    var t = h("div", { class: "toast " + kind },
      h("span", { class: "t-ic" }, icon(kind === "ok" ? "check" : kind === "err" ? "alert" : "info")),
      h("p", { text: text }), closeBtn);
    function kill() {
      if (!t.parentNode) return;
      t.classList.add("out");
      setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, reduceMotion() ? 0 : 240);
    }
    closeBtn.addEventListener("click", kill);
    var box = $("toasts");
    box.appendChild(t);
    while (box.children.length > 3) box.removeChild(box.firstChild);
    setTimeout(kill, kind === "err" ? 8000 : 4200);
  }

  /* ============================================================== dialog */

  function ask(opts) {
    var d = $("dialog");
    $("dlg-title").textContent = opts.title || "Pakka?";
    $("dlg-text").textContent = opts.text || "";
    $("dlg-ok").textContent = opts.ok || "Haan";
    $("dlg-cancel").textContent = opts.cancel || "Nahi";
    $("dlg-ok").className = "btn btn-primary" + (opts.danger ? " danger-ok" : "");
    var ic = $("dlg-icon");
    ic.className = "dialog-icon" + (opts.danger ? " danger" : "");
    clear(ic).appendChild(icon(opts.icon || "alert"));
    if (typeof d.showModal !== "function") return Promise.resolve(window.confirm((opts.title || "") + "\n\n" + (opts.text || "")));
    return new Promise(function (resolve) {
      d.returnValue = "";
      function done() { d.removeEventListener("close", done); resolve(d.returnValue === "ok"); }
      d.addEventListener("close", done);
      d.showModal();
      $(opts.danger ? "dlg-cancel" : "dlg-ok").focus();
    });
  }

  /* =============================================================== state */

  var S = null;          // working settings
  var saved = "";        // JSON of last saved/loaded settings
  var ME = null;
  var view = "dashboard";
  var backups = null;
  var openProducts = typeof WeakSet === "function" ? new WeakSet() : null;
  var ui = { lang: {}, wLang: "hi", wOcc: "navratri", wRel: "all", tLang: "hi", pFilter: "", pSearch: "" };

  function ensure(d) {
    if (!d || typeof d !== "object" || Array.isArray(d)) d = {};
    function obj(o, k) { if (!o[k] || typeof o[k] !== "object" || Array.isArray(o[k])) o[k] = {}; return o[k]; }
    var a = obj(d, "affiliate");
    if (!Array.isArray(a.products)) a.products = [];
    var t = obj(d, "telegram");
    ["title", "text", "button"].forEach(function (k) { obj(t, k); });
    if (!Array.isArray(t.pages)) t.pages = ["all"];
    var an = obj(d, "announcement");
    obj(an, "text");
    obj(d, "ads");
    var c = obj(d, "custom");
    var th = obj(c, "thoughts"), w = obj(c, "wishes");
    LANGS.forEach(function (l) {
      if (!Array.isArray(th[l[0]])) th[l[0]] = [];
      obj(w, l[0]);
    });
    a.products.forEach(function (p) {
      if (!p.title || typeof p.title !== "object") p.title = {};
      if (!Array.isArray(p.pages)) p.pages = [];
    });
    return d;
  }

  function isDirty() { return !!S && JSON.stringify(S) !== saved; }

  var dirtyRaf = 0;
  function changed() {
    if (dirtyRaf) return;
    dirtyRaf = requestAnimationFrame(function () {
      dirtyRaf = 0;
      var d = isDirty();
      $("savebar").hidden = !d;
      var chip = $("save-chip");
      chip.classList.toggle("dirty", d);
      $("save-chip-text").textContent = d ? "Save baaki hai" : "Sab save hai";
      refreshNavBadges();
      if (view === "dashboard") renderDashboard();
    });
  }

  /* ================================================================ auth */

  var lockTimer = null;
  function showLogin(msg, kind) {
    document.body.classList.remove("is-booting");
    $("app").hidden = true;
    $("login").hidden = false;
    closeDrawer();
    loginMsg(msg || "", kind);
    setTimeout(function () { ($("lg-user").value ? $("lg-pass") : $("lg-user")).focus(); }, 30);
  }
  function loginMsg(text, kind) {
    var m = $("login-msg");
    clear(m);
    if (!text) { m.hidden = true; return; }
    m.hidden = false;
    m.className = "login-msg" + (kind === "info" ? " info" : "");
    m.appendChild(icon(kind === "info" ? "info" : "alert"));
    m.appendChild(h("span", { text: text }));
  }
  function lockout(seconds) {
    var btn = $("lg-submit");
    var end = Date.now() + seconds * 1000;
    clearInterval(lockTimer);
    btn.disabled = true;
    function tick() {
      var left = Math.max(0, Math.round((end - Date.now()) / 1000));
      if (!left) { clearInterval(lockTimer); btn.disabled = false; loginMsg("Ab dobara koshish kar sakte ho.", "info"); return; }
      var mm = Math.floor(left / 60), ss = left % 60;
      loginMsg("Bahut baar galat password. " + mm + ":" + (ss < 10 ? "0" : "") + ss + " minute baad dobara koshish karo.");
    }
    tick();
    lockTimer = setInterval(tick, 1000);
  }

  $("lg-eye").addEventListener("click", function () {
    var inp = $("lg-pass"), show = inp.type === "password";
    inp.type = show ? "text" : "password";
    this.setAttribute("aria-pressed", show ? "true" : "false");
    this.setAttribute("aria-label", show ? "Password chhupao" : "Password dikhao");
    clear(this).appendChild(icon(show ? "eyeOff" : "eye"));
    inp.focus();
  });

  $("login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var u = $("lg-user").value.trim(), p = $("lg-pass").value;
    if (!u || !p) { loginMsg("Username aur password dono daalo."); (u ? $("lg-pass") : $("lg-user")).focus(); return; }
    var btn = $("lg-submit");
    btn.classList.add("is-busy");
    btn.disabled = true;
    api("POST", "/api/login", { username: u, password: p }, { allow401: true }).then(function (me) {
      ME = me;
      $("lg-pass").value = "";
      loginMsg("");
      return enterApp();
    }).catch(function (err) {
      if (err.status === 429) { lockout((err.data && err.data.retryAfter) || 900); return; }
      if (err.status === 401) {
        var left = err.data && err.data.attemptsLeft;
        loginMsg("Username ya password galat hai." + (left ? " " + left + " koshish baaki." : ""));
        $("lg-pass").select();
      } else if (err.status === 503) {
        loginMsg("Server par admin login set nahi hai (ADMIN_USER / ADMIN_PASSWORD).");
      } else {
        loginMsg(err.message || "Login nahi ho paaya.");
      }
    }).then(function () {
      btn.classList.remove("is-busy");
      if (!lockTimer || $("login-msg").textContent.indexOf("minute baad") < 0) btn.disabled = false;
    });
  });

  var expiredShown = false;
  function sessionExpired() {
    if (expiredShown || $("app").hidden) return;
    expiredShown = true;
    showLogin(isDirty() ? "Session khatam ho gaya. Dobara login karo, aapke badlav abhi bhi yahan hain." : "Session khatam ho gaya. Dobara login karo.", "info");
  }

  function enterApp() {
    expiredShown = false;
    var keep = S && isDirty();
    var p = keep ? Promise.resolve() : loadSettings();
    return p.then(function () {
      $("login").hidden = true;
      $("app").hidden = false;
      document.body.classList.remove("is-booting");
      var name = (ME && ME.user) || "admin";
      $("side-user").textContent = name;
      $("side-avatar").textContent = name.charAt(0).toUpperCase();
      go(viewFromHash(), true);
      changed();
      if (keep) toast("Wapas aa gaye. Badlav save karna mat bhoolna.", "info");
    });
  }

  function loadSettings() {
    return api("GET", "/api/settings").then(function (data) {
      S = ensure(data);
      saved = JSON.stringify(S);
      renderAll();
      loadBackups();
    });
  }

  $("btn-logout").addEventListener("click", function () {
    var p = isDirty() ? ask({ title: "Logout karein?", text: "Kuch badlav save nahi hue hain. Logout karne par wo chale jaayenge.", ok: "Haan, logout", danger: true, icon: "logout" }) : Promise.resolve(true);
    p.then(function (yes) {
      if (!yes) return;
      api("POST", "/api/logout", {}, { allow401: true }).catch(function () {}).then(function () {
        S = null; saved = ""; ME = null;
        $("savebar").hidden = true;
        showLogin("Logout ho gaya.", "info");
      });
    });
  });

  /* ========================================================= navigation */

  function viewFromHash() {
    var v = (location.hash || "").replace(/^#\/?/, "");
    return VIEWS.some(function (x) { return x[0] === v; }) ? v : "dashboard";
  }

  function buildNav() {
    var nav = clear($("side-nav"));
    nav.appendChild(h("div", { class: "nav-group", text: "Menu" }));
    VIEWS.forEach(function (v, i) {
      if (i === 6) nav.appendChild(h("div", { class: "nav-group", text: "System" }));
      nav.appendChild(h("button", { class: "nav-item", type: "button", "data-go": v[0], on: { click: function () { go(v[0]); closeDrawer(); } } },
        icon(v[3]), h("span", { text: v[1] }), h("span", { class: "badge", "data-badge": v[0], hidden: true })));
    });
    var tb = clear($("tabbar"));
    TABS.forEach(function (k) {
      var v = VIEWS.filter(function (x) { return x[0] === k; })[0];
      tb.appendChild(h("button", { class: "tab", type: "button", "data-go": k, on: { click: function () { go(k); } } }, icon(v[3]), h("span", { text: v[1] })));
    });
    tb.appendChild(h("button", { class: "tab", type: "button", id: "tab-more", "aria-controls": "side", "aria-expanded": "false", on: { click: openDrawer } }, icon("more"), h("span", { text: "Aur" })));
  }

  function refreshNavBadges() {
    if (!S) return;
    var n = S.affiliate.products.length;
    document.querySelectorAll('[data-badge="products"]').forEach(function (b) { b.textContent = n; b.hidden = !n; });
  }

  function go(name, initial) {
    if (!VIEWS.some(function (v) { return v[0] === name; })) name = "dashboard";
    var prev = view;
    view = name;
    var meta = VIEWS.filter(function (v) { return v[0] === name; })[0];
    $("view-title").textContent = meta[1];
    $("view-sub").textContent = meta[2];
    document.title = meta[1] + " | IFW Admin";
    document.querySelectorAll("[data-go]").forEach(function (b) {
      if (b.getAttribute("data-go") === name) b.setAttribute("aria-current", "page"); else b.removeAttribute("aria-current");
    });
    var moreActive = TABS.indexOf(name) < 0;
    var more = $("tab-more");
    if (more) { if (moreActive) more.setAttribute("aria-current", "page"); else more.removeAttribute("aria-current"); }
    document.querySelectorAll(".view").forEach(function (s) { s.hidden = s.getAttribute("data-view") !== name; });
    if (name === "dashboard") renderDashboard();
    if (name === "patti" && S && prev !== name) renderPatti();
    if (name === "backup" && !initial) loadBackups();
    if (location.hash.replace("#", "") !== name) history.replaceState(null, "", "#" + name);
    if (!initial && prev !== name) {
      window.scrollTo(0, 0);
      $("main").focus({ preventScroll: true });
    }
  }
  window.addEventListener("hashchange", function () { if (!$("app").hidden) go(viewFromHash()); });

  function openDrawer() {
    var s = $("side");
    s.classList.add("open");
    $("scrim").hidden = false;
    $("menu-btn").setAttribute("aria-expanded", "true");
    var m = $("tab-more"); if (m) m.setAttribute("aria-expanded", "true");
    setTimeout(function () { var c = s.querySelector('[aria-current="page"]') || s.querySelector(".nav-item"); if (c) c.focus(); }, 60);
  }
  function closeDrawer() {
    var s = $("side");
    if (!s.classList.contains("open")) return;
    s.classList.remove("open");
    $("scrim").hidden = true;
    $("menu-btn").setAttribute("aria-expanded", "false");
    var m = $("tab-more"); if (m) m.setAttribute("aria-expanded", "false");
  }
  $("menu-btn").addEventListener("click", openDrawer);
  $("side-close").addEventListener("click", function () { closeDrawer(); $("menu-btn").focus(); });
  $("scrim").addEventListener("click", closeDrawer);
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && $("side").classList.contains("open")) { closeDrawer(); $("menu-btn").focus(); }
    if ((e.ctrlKey || e.metaKey) && (e.key === "s" || e.key === "S") && !$("app").hidden) {
      e.preventDefault();
      if (isDirty()) save();
    }
  });

  /* ======================================================= form builders */

  function card(opts) {
    var headKids = [
      opts.icon ? h("span", { class: "ch-icon" + (opts.tone ? " " + opts.tone : "") }, icon(opts.icon)) : null,
      h("div", { class: "ch-text" }, h("h3", { text: opts.title }), opts.desc ? h("p", { text: opts.desc }) : null),
      opts.side ? h("div", { class: "ch-side" }, opts.side) : null
    ];
    var c = h("div", { class: "card" }, h("div", { class: "card-head" }, headKids));
    add(c, opts.body);
    return c;
  }

  // text input bound to obj[key]
  function textField(label, obj, key, o) {
    o = o || {};
    var id = nextId("t");
    var err = h("p", { class: "field-err", hidden: true });
    var inp = h(o.multiline ? "textarea" : "input", {
      id: id, type: o.multiline ? null : (o.type || "text"), placeholder: o.placeholder || null,
      autocomplete: "off", spellcheck: o.spell ? "true" : "false", inputmode: o.inputmode || null,
      "aria-describedby": o.hint ? id + "-h" : null, rows: o.rows || null
    });
    inp.value = obj[key] == null ? "" : String(obj[key]);
    var wrap = h("div", { class: "field" }, h("label", { for: id, text: label }), inp,
      o.hint ? h("p", { class: "hint", id: id + "-h", text: o.hint }) : null, err);
    function check() {
      var msg = o.validate ? o.validate(inp.value.trim()) : "";
      wrap.classList.toggle("is-invalid", !!msg);
      clear(err);
      if (msg) { err.appendChild(icon("alert")); err.appendChild(h("span", { text: msg })); }
      err.hidden = !msg;
      if (msg) inp.setAttribute("aria-invalid", "true"); else inp.removeAttribute("aria-invalid");
    }
    inp.addEventListener("input", function () {
      obj[key] = o.raw ? inp.value : inp.value.trim();
      if (o.onInput) o.onInput(obj[key]);
      check();
      changed();
    });
    if (o.validate) check();
    wrap._input = inp;
    return wrap;
  }

  function switchRow(label, desc, obj, key, def, onChange) {
    var id = nextId("s");
    var cb = h("input", { type: "checkbox", id: id, role: "switch" });
    cb.checked = obj[key] == null ? def : !!obj[key];
    cb.addEventListener("change", function () {
      obj[key] = cb.checked;
      if (onChange) onChange(cb.checked);
      changed();
    });
    return h("label", { class: "switch-row", for: id },
      h("span", { class: "sw-text" }, h("strong", { text: label }), desc ? h("small", { text: desc }) : null),
      h("span", { class: "switch" }, cb, h("span", { class: "track", "aria-hidden": "true" })));
  }

  function pageChips(legend, list, withAll, onChange) {
    var fs = h("fieldset", { class: "chips" }, h("legend", { text: legend }));
    var opts = (withAll ? [["all", "Sabhi pages"]] : []).concat(PAGES);
    opts.forEach(function (pg) {
      var cb = h("input", { type: "checkbox", value: pg[0] });
      cb.checked = list.indexOf(pg[0]) >= 0;
      var lab = h("label", { class: "chip" + (cb.checked ? " on" : "") + (pg[2] ? " tag-new" : "") }, cb,
        h("span", { class: "chk", "aria-hidden": "true" }, icon("check")), h("span", { text: pg[1] }));
      cb.addEventListener("change", function () {
        var i = list.indexOf(pg[0]);
        if (cb.checked && i < 0) list.push(pg[0]);
        if (!cb.checked && i >= 0) list.splice(i, 1);
        lab.classList.toggle("on", cb.checked);
        if (onChange) onChange();
        changed();
      });
      fs.appendChild(lab);
    });
    return fs;
  }

  function segmented(name, label, options, value, onChange) {
    var g = h("div", { class: "seg", role: "radiogroup", "aria-label": label });
    options.forEach(function (o) {
      var r = h("input", { type: "radio", name: name, value: o[0] });
      r.checked = o[0] === value;
      r.addEventListener("change", function () { if (r.checked) { onChange(o[0]); changed(); } });
      g.appendChild(h("label", null, r, h("span", { text: o[1] })));
    });
    return h("div", { class: "field" }, h("span", { class: "label", text: label }), g);
  }

  function select(label, options, value, onChange) {
    var id = nextId("sel");
    var s = h("select", { id: id });
    options.forEach(function (o) { s.appendChild(h("option", { value: o[0], text: o[1] })); });
    s.value = value;
    s.addEventListener("change", function () { onChange(s.value); });
    var f = h("div", { class: "field" }, h("label", { for: id, text: label }), s);
    f._select = s;
    return f;
  }

  // Language tabs: build(langCode, panel) fills the panel for that language.
  function langTabs(key, build, filled) {
    var wrap = h("div", { class: "ltabs-wrap" });
    var list = h("div", { class: "ltabs", role: "tablist", "aria-label": "Bhasha" });
    var panel = h("div", { role: "tabpanel" });
    var pid = nextId("lp");
    panel.id = pid;
    var cur = ui.lang[key] || "hi";
    var btns = [];
    function paint() {
      btns.forEach(function (b) {
        var on = b.getAttribute("data-l") === cur;
        b.setAttribute("aria-selected", on ? "true" : "false");
        b.tabIndex = on ? 0 : -1;
        if (on) panel.setAttribute("aria-labelledby", b.id);
        var dot = b.querySelector(".fill-dot");
        if (dot && filled) dot.classList.toggle("full", filled(b.getAttribute("data-l")));
      });
      clear(panel);
      build(cur, panel, paint);
    }
    LANGS.forEach(function (l, i) {
      var b = h("button", { class: "ltab", type: "button", role: "tab", id: nextId("lt"), "data-l": l[0], "aria-controls": pid },
        filled ? h("span", { class: "fill-dot", "aria-hidden": "true" }) : null, h("span", { text: l[1] }));
      b.addEventListener("click", function () { cur = ui.lang[key] = l[0]; paint(); });
      b.addEventListener("keydown", function (e) {
        var d = e.key === "ArrowRight" ? 1 : e.key === "ArrowLeft" ? -1 : 0;
        if (!d) return;
        e.preventDefault();
        var j = (i + d + LANGS.length) % LANGS.length;
        cur = ui.lang[key] = LANGS[j][0];
        paint();
        btns[j].focus();
      });
      btns.push(b);
      list.appendChild(b);
    });
    wrap.appendChild(list);
    wrap.appendChild(panel);
    paint();
    wrap.refreshDots = function () {
      if (!filled) return;
      btns.forEach(function (b) { b.querySelector(".fill-dot").classList.toggle("full", filled(b.getAttribute("data-l"))); });
    };
    return wrap;
  }

  /* ========================================================== validation */

  function vTelegram(v) { return v && !/^https:\/\/(t\.me|telegram\.me)\/[A-Za-z0-9_+\/-]+$/.test(v) ? "Link https://t.me/channelname jaisa hona chahiye." : ""; }
  function vHttps(v) { return v && !/^https:\/\/\S+$/.test(v) ? "Link https:// se shuru hona chahiye." : ""; }
  function vImage(v) {
    if (!v) return "";
    if (/^https:\/\/\S+$/.test(v)) return "";
    if (v.indexOf(location.origin + "/uploads/") === 0) return "";
    return "Photo link https:// se shuru hona chahiye.";
  }
  function vAdsense(v) { return v && !/^ca-pub-\d{10,20}$/.test(v) ? "Publisher ID ca-pub- aur number jaisa hona chahiye." : ""; }
  function vSlot(v) { return v && !/^\d{6,15}$/.test(v) ? "Slot ID sirf number hota hai." : ""; }
  function vGa(v) { return v && !/^G-[A-Z0-9]{4,15}$/.test(v) ? "Measurement ID G- se shuru hota hai." : ""; }
  function vTag(v) { return v && !/^[A-Za-z0-9_.-]{2,40}$/.test(v) ? "Tracking ID me space ya ajeeb akshar nahi hone chahiye." : ""; }

  function validateAll() {
    var t = S.telegram;
    if (t.enabled && !t.url) return ["telegram", "Telegram chalu hai par channel link khali hai."];
    var e = vTelegram(t.url || ""); if (e) return ["telegram", e];
    e = vHttps(S.announcement.url || ""); if (e) return ["patti", "Patti: " + e];
    e = vAdsense(S.ads.adsenseClient || ""); if (e) return ["ads", e];
    e = vSlot(S.ads.slotTop || "") || vSlot(S.ads.slotMiddle || ""); if (e) return ["ads", e];
    e = vGa(S.ads.gaId || ""); if (e) return ["ads", e];
    e = vTag(S.affiliate.amazonTag || ""); if (e) return ["products", e];
    for (var i = 0; i < S.affiliate.products.length; i++) {
      var p = S.affiliate.products[i];
      e = vHttps(p.url || "") || vImage(p.image || "");
      if (e) return ["products", "Product " + (i + 1) + ": " + e];
    }
    return null;
  }

  /* ================================================================ save */

  var saving = false;
  function save(force) {
    if (!S || saving) return;
    var bad = validateAll();
    if (bad) { go(bad[0]); toast(bad[1], "err"); return; }
    saving = true;
    var btn = $("btn-save");
    btn.classList.add("is-busy");
    btn.disabled = true;
    var headers = {};
    if (!force && S.version != null) headers["X-IFW-Base-Version"] = String(S.version);
    var body = clone(S);
    api("PUT", "/api/settings", body, { headers: headers }).then(function (r) {
      S.version = r.version;
      saved = JSON.stringify(S);
      changed();
      toast("Save ho gaya. Site par turant dikhega.", "ok");
      loadBackups();
    }).catch(function (err) {
      if (err.status === 409) {
        return ask({ title: "File kahin aur se badli hai", text: "Aapke login ke baad settings kisi aur jagah se save hui hain. Apne badlav se unhe badal dein?", ok: "Haan, mere badlav rakho", cancel: "Ruko" })
          .then(function (yes) { saving = false; if (yes) save(true); });
      }
      if (err.status !== 401) toast("Save nahi hua: " + err.message, "err");
    }).then(function () {
      saving = false;
      btn.classList.remove("is-busy");
      btn.disabled = false;
    });
  }
  $("btn-save").addEventListener("click", function () { save(); });
  $("btn-discard").addEventListener("click", function () {
    ask({ title: "Badlav wapas lein?", text: "Jo badlav save nahi hue, wo hat jaayenge aur pichhli saved settings wapas aa jaayengi.", ok: "Haan, wapas lo", danger: true, icon: "restore" })
      .then(function (yes) {
        if (!yes) return;
        S = ensure(JSON.parse(saved));
        renderAll();
        changed();
        toast("Badlav wapas le liye.", "info");
      });
  });
  window.addEventListener("beforeunload", function (e) { if (isDirty()) { e.preventDefault(); e.returnValue = ""; } });

  /* ============================================================ renderers */

  function viewEl(name) { return document.querySelector('.view[data-view="' + name + '"]'); }

  function renderAll() {
    renderDashboard();
    renderProducts();
    renderTelegram();
    renderPatti();
    renderAds();
    renderWishes();
    renderBackup();
    renderAccount();
    refreshNavBadges();
  }

  /* ---------------------------------------------------------- dashboard */

  function liveProducts() {
    var tag = (S.affiliate.amazonTag || "").trim();
    return S.affiliate.products.filter(function (p) {
      return p.enabled !== false && (p.pages || []).length && ((p.url || "").trim() || ((p.search || "").trim() && tag));
    }).length;
  }
  function countWishes() {
    var n = 0;
    LANGS.forEach(function (l) {
      var w = S.custom.wishes[l[0]] || {};
      Object.keys(w).forEach(function (o) { Object.keys(w[o] || {}).forEach(function (r) { n += (w[o][r] || []).length; }); });
      n += (S.custom.thoughts[l[0]] || []).length;
    });
    return n;
  }

  function renderDashboard() {
    var v = viewEl("dashboard");
    if (!S) return;
    var focusedGo = document.activeElement && v.contains(document.activeElement) ? document.activeElement.getAttribute("data-dash") : null;
    clear(v);
    var hour = new Date().getHours();
    var greet = hour < 12 ? "Suprabhat" : hour < 17 ? "Namaste" : "Shubh sandhya";
    var ver = Number(S.version);
    var lastSaved = ver > 1e12 ? ago(ver) + " (" + fmtDate(ver) + ")" : "Abhi tak is panel se save nahi hua";

    v.appendChild(h("div", { class: "hero" },
      (function () { var s = h("span", { class: "hero-flower", "aria-hidden": "true" }); s.innerHTML = FLOWER; return s; })(),
      h("small", { text: "Indian Festival Wishes" }),
      h("h2", { text: greet + ", " + ((ME && ME.user) || "admin") }),
      h("p", { text: isDirty() ? "Kuch badlav abhi save nahi hue hain. Neeche wali patti se Save karo." : "Sab kuch save hai. Koi bhi hissa chuno aur badlav karo." }),
      h("div", { class: "hero-meta" },
        h("span", null, icon("clock"), "Last save: " + lastSaved),
        h("span", null, icon("database"), (backups ? backups.length : "–") + " backups"))));

    var tag = (S.affiliate.amazonTag || "").trim();
    var live = liveProducts();
    var rows = [
      ["telegram", "send", "Telegram", S.telegram.enabled ? "Chalu" : "Band", S.telegram.enabled ? "on" : "off"],
      ["patti", "megaphone", "Announcement patti", S.announcement.enabled ? "Chalu" : "Band", S.announcement.enabled ? "on" : "off"],
      ["products", "tag", "Amazon tracking ID", tag || "Nahi daala", tag ? "on" : "warn"],
      ["products", "bag", "Site par dikhte products", live + " / " + S.affiliate.products.length, live ? "on" : "warn"],
      ["ads", "chart", "AdSense", S.ads.adsenseClient ? "Chalu" : "Band", S.ads.adsenseClient ? "on" : "off"],
      ["ads", "globe", "Analytics", S.ads.gaId || "Band", S.ads.gaId ? "on" : "off"]
    ];
    var grid = h("div", { class: "stats" });
    rows.forEach(function (r, i) {
      grid.appendChild(h("button", { class: "stat", type: "button", "data-dash": "s" + i, on: { click: function () { go(r[0]); } }, "aria-label": r[2] + ": " + r[3] },
        h("span", { class: "s-icon" }, icon(r[1])),
        h("span", { class: "s-label", text: r[2] }),
        h("span", { class: "s-value", text: r[3] }),
        h("span", { class: "pill " + r[4], text: r[4] === "on" ? "Live" : r[4] === "warn" ? "Dhyan do" : "Band" })));
    });
    v.appendChild(grid);

    v.appendChild(h("h3", { class: "section-title", text: "Jaldi kaam" }));
    var q = h("div", { class: "quick" });
    [["products", "plus", "Naya product", "Amazon box me jodo"], ["patti", "megaphone", "Patti ka text", "Upar ki chalti line"],
     ["wishes", "message", "Wishes jodo", "Card ki list me"], ["backup", "database", "Backup", "Purana version wapas"]].forEach(function (t, i) {
      q.appendChild(h("button", { type: "button", "data-dash": "q" + i, on: { click: function () {
        go(t[0]);
        if (t[2] === "Naya product") addProduct();
      } } }, icon(t[1]), h("span", null, t[2], h("small", { text: t[3] }))));
    });
    v.appendChild(q);

    var cw = countWishes();
    v.appendChild(h("h3", { class: "section-title", text: "Aur jaankari" }));
    v.appendChild(h("div", { class: "note info" }, icon("info"),
      h("span", { text: "Apni jodi hui wishes aur suvichar: " + cw + ". Har save se pehle server apne aap purani settings ka backup rakhta hai (aakhri 50)." })));

    if (focusedGo) { var f = v.querySelector('[data-dash="' + focusedGo + '"]'); if (f) f.focus(); }
  }

  /* ----------------------------------------------------------- products */

  var productListEl = null, countLineEl = null;

  function renderProducts() {
    var v = clear(viewEl("products"));
    var A = S.affiliate;
    v.appendChild(card({
      icon: "tag", title: "Amazon Associates", desc: "Tracking ID ke bina search wale products site par nahi dikhte.",
      body: h("div", { class: "grid-2" },
        textField("Tracking ID", A, "amazonTag", { placeholder: "yourname-21", validate: vTag, hint: "Jaise saverhub-21" }),
        (function () {
          var f = textField("Ek box me kitne products", A, "maxPerSlot", { type: "number", inputmode: "numeric", hint: "1 se 8 tak" });
          var inp = f._input;
          inp.min = 1; inp.max = 8;
          inp.addEventListener("input", function () { A.maxPerSlot = Math.min(8, Math.max(1, parseInt(inp.value, 10) || 4)); changed(); });
          return f;
        })())
    }));

    var filterOpts = [["", "Sabhi pages"]].concat(PAGES.map(function (p) { return [p[0], p[1]]; }));
    var fSel = select("Page se chuno", filterOpts, ui.pFilter, function (val) { ui.pFilter = val; drawProductList(); });
    var sid = nextId("q");
    var sInp = h("input", { id: sid, type: "search", placeholder: "Naam ya search shabd", autocomplete: "off", value: ui.pSearch });
    sInp.addEventListener("input", function () { ui.pSearch = sInp.value; drawProductList(); });
    var sField = h("div", { class: "field" }, h("label", { for: sid, text: "Dhoondo" }), h("div", { class: "input-icon" }, h("span", { "data-icon": "search" }), sInp));
    hydrateIcons(sField);
    v.appendChild(h("div", { class: "toolbar" }, sField, fSel,
      h("button", { class: "btn btn-primary", type: "button", on: { click: addProduct } }, icon("plus"), "Naya product")));
    countLineEl = h("p", { class: "count-line", "aria-live": "polite" });
    v.appendChild(countLineEl);
    productListEl = h("div", { class: "plist" });
    v.appendChild(productListEl);
    drawProductList();
  }

  function productMatches(p) {
    if (ui.pFilter && (p.pages || []).indexOf(ui.pFilter) < 0) return false;
    var q = (ui.pSearch || "").trim().toLowerCase();
    if (!q) return true;
    var hay = [p.search, p.url, p.store, p.price].concat(LANGS.map(function (l) { return (p.title || {})[l[0]]; })).join(" ").toLowerCase();
    return hay.indexOf(q) >= 0;
  }

  function drawProductList(focusIndex, focusSel) {
    var list = S.affiliate.products;
    clear(productListEl);
    var shown = 0;
    list.forEach(function (p, i) {
      if (!productMatches(p)) return;
      shown++;
      productListEl.appendChild(productCard(p, i));
    });
    countLineEl.textContent = list.length ? (shown === list.length ? list.length + " products" : shown + " / " + list.length + " products dikh rahe hain") : "";
    if (!list.length) {
      productListEl.appendChild(h("div", { class: "empty" }, icon("bag"), h("strong", { text: "Abhi koi product nahi hai" }),
        h("p", { text: "Upar \"Naya product\" dabake pehla product jodo." })));
    } else if (!shown) {
      productListEl.appendChild(h("div", { class: "empty" }, icon("search"), h("strong", { text: "Kuch nahi mila" }), h("p", { text: "Filter ya search badal ke dekho." })));
    }
    if (focusIndex != null) {
      var c = productListEl.querySelector('[data-idx="' + focusIndex + '"]');
      if (c) { var t = c.querySelector(focusSel || ".p-main"); if (t && !t.disabled) t.focus(); else c.querySelector(".p-main").focus(); }
    }
  }

  function isOpen(p) { return openProducts ? openProducts.has(p) : !!p.__open; }
  function setOpen(p, on) { if (openProducts) { if (on) openProducts.add(p); else openProducts.delete(p); } }

  function thumb(p) {
    var t = h("span", { class: "p-thumb", "aria-hidden": "true" });
    var src = p.image && !vImage(p.image) ? p.image : "";
    if (src) {
      var im = h("img", { src: src, alt: "", loading: "lazy" });
      im.addEventListener("error", function () { clear(t).appendChild(icon("image")); });
      t.appendChild(im);
    } else t.appendChild(icon("bag"));
    return t;
  }

  function productCard(p, i) {
    var list = S.affiliate.products;
    var open = isOpen(p);
    var cardEl = h("article", { class: "prod" + (p.enabled === false ? " off" : "") + (open ? " open" : ""), "data-idx": i });
    var bodyId = nextId("pb");

    var titleEl = h("span", { class: "p-title" });
    var subEl = h("span", { class: "p-sub" });
    var tagsEl = h("span", { class: "p-tags" });
    function paintHead() {
      titleEl.textContent = p.title.hi || p.title.en || p.title.gu || "Naya product";
      var src = p.url ? "Direct link" : p.search ? "Search: " + p.search : "Link nahi hai";
      subEl.textContent = (p.title.en && p.title.hi ? p.title.en + " · " : "") + src;
      clear(tagsEl);
      if (!p.pages.length) tagsEl.appendChild(h("span", { class: "none", text: "Kisi page par nahi" }));
      p.pages.forEach(function (pg) { tagsEl.appendChild(h("span", { text: PAGE_NAME[pg] || pg })); });
    }
    paintHead();
    var th = thumb(p);

    var cb = h("input", { type: "checkbox", role: "switch", "aria-label": "Site par dikhao" });
    cb.checked = p.enabled !== false;
    cb.addEventListener("change", function () { p.enabled = cb.checked; cardEl.classList.toggle("off", !cb.checked); changed(); });

    var main = h("button", { class: "p-main", type: "button", "aria-expanded": open ? "true" : "false", "aria-controls": bodyId }, titleEl, subEl, tagsEl);
    var chev = h("button", { class: "icon-btn p-chev", type: "button", "aria-label": (open ? "Band karo: " : "Kholo: ") + titleEl.textContent, "aria-expanded": open ? "true" : "false", "aria-controls": bodyId }, icon("chevDown"));
    function toggle() { setOpen(p, !isOpen(p)); drawProductList(i, ".p-main"); }
    main.addEventListener("click", toggle);
    chev.addEventListener("click", function () { setOpen(p, !isOpen(p)); drawProductList(i, ".p-chev"); });

    cardEl.appendChild(h("div", { class: "p-row" }, th, main,
      h("div", { class: "p-side" }, h("span", { class: "switch", title: "Site par dikhao" }, cb, h("span", { class: "track", "aria-hidden": "true" })), chev)));

    if (!open) return cardEl;

    var body = h("div", { class: "p-body", id: bodyId });
    body.appendChild(h("div", { class: "grid-3" },
      textField("Naam (हिंदी)", p.title, "hi", { onInput: paintHead, spell: true }),
      textField("Naam (ગુજરાતી)", p.title, "gu", { onInput: paintHead, spell: true }),
      textField("Naam (English)", p.title, "en", { onInput: paintHead, spell: true })));
    body.appendChild(h("div", { class: "grid-2" },
      textField("Amazon search shabd", p, "search", { placeholder: "jaise: chaniya choli", hint: "Isse apne aap tracking ID wala search link banta hai.", onInput: paintHead }),
      textField("Direct link (zaroori nahi)", p, "url", { placeholder: "https://amzn.to/...", type: "url", validate: vHttps, hint: "Ek khaas product ka link ho to yahan daalo.", onInput: paintHead })));
    body.appendChild(h("div", { class: "grid-2" },
      textField("Keemat", p, "price", { placeholder: "₹499 se" }),
      textField("Store", p, "store", { placeholder: "Amazon" })));

    // image
    var prev = h("div", { class: "img-prev" });
    function paintPrev() {
      clear(prev);
      var src = p.image && !vImage(p.image) ? p.image : "";
      if (src) {
        var im = h("img", { src: src, alt: "Product photo preview" });
        im.addEventListener("error", function () { clear(prev).appendChild(icon("image")); });
        prev.appendChild(im);
      } else prev.appendChild(icon("image"));
      var nt = thumb(p); th.replaceWith(nt); th = nt;
    }
    paintPrev();
    var imgField = textField("Photo link", p, "image", { placeholder: "https://...", type: "url", validate: vImage, hint: "Link daalo ya photo upload karo (JPG, PNG, WebP, 2 MB tak).", onInput: paintPrev });
    var fileInp = h("input", { type: "file", accept: "image/jpeg,image/png,image/webp", "aria-label": "Photo upload karo" });
    var upBtn = h("span", { class: "btn btn-soft btn-sm file-btn" }, icon("upload"), h("span", { class: "btn-label", text: "Photo upload" }), h("span", { class: "spinner", "aria-hidden": "true" }), fileInp);
    fileInp.addEventListener("change", function () {
      var f = fileInp.files && fileInp.files[0];
      fileInp.value = "";
      if (!f) return;
      if (["image/jpeg", "image/png", "image/webp"].indexOf(f.type) < 0) { toast("Sirf JPG, PNG ya WebP photo chalegi.", "err"); return; }
      if (f.size > 2 * 1024 * 1024) { toast("Photo 2 MB se chhoti honi chahiye.", "err"); return; }
      upBtn.classList.add("is-busy");
      api("POST", "/api/upload", f, { raw: true, type: f.type }).then(function (r) {
        p.image = location.origin + r.url;
        imgField._input.value = p.image;
        imgField._input.dispatchEvent(new Event("input"));
        toast("Photo upload ho gayi. Save karna mat bhoolna.", "ok");
      }).catch(function (e) { if (e.status !== 401) toast("Upload nahi hua: " + e.message, "err"); })
        .then(function () { upBtn.classList.remove("is-busy"); });
    });
    var clearImg = h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () {
      imgField._input.value = ""; imgField._input.dispatchEvent(new Event("input"));
    } } }, icon("x"), "Photo hatao");
    body.appendChild(h("div", { class: "img-field" }, prev, h("div", { class: "img-ctrl" }, imgField, h("div", { class: "row-actions" }, upBtn, clearImg))));

    body.appendChild(pageChips("Kin pages par dikhe", p.pages, false, paintHead));

    function move(d) {
      var j = i + d;
      if (j < 0 || j >= list.length) return;
      list.splice(j, 0, list.splice(i, 1)[0]);
      changed();
      drawProductList(j, d < 0 ? ".mv-up" : ".mv-down");
    }
    var up = h("button", { class: "btn btn-ghost btn-sm mv-up", type: "button", disabled: i === 0, on: { click: function () { move(-1); } } }, icon("arrowUp"), "Upar");
    var down = h("button", { class: "btn btn-ghost btn-sm mv-down", type: "button", disabled: i === list.length - 1, on: { click: function () { move(1); } } }, icon("arrowDown"), "Neeche");
    var dup = h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () {
      var c = clone(p);
      list.splice(i + 1, 0, c);
      setOpen(p, false); setOpen(c, true);
      changed();
      drawProductList(i + 1, ".p-main");
      toast("Product ki copy ban gayi.", "info");
    } } }, icon("copy"), "Copy");
    var del = h("button", { class: "btn btn-danger btn-sm", type: "button", on: { click: function () {
      ask({ title: "Product hatayein?", text: "\"" + titleEl.textContent + "\" list se hat jaayega. Save karne ke baad hi site se hatega.", ok: "Haan, hatao", danger: true, icon: "trash" })
        .then(function (yes) {
          if (!yes) return;
          list.splice(i, 1);
          changed();
          drawProductList(Math.min(i, list.length - 1), ".p-main");
          toast("Product hata diya.", "info");
        });
    } } }, icon("trash"), "Hatao");
    body.appendChild(h("div", { class: "p-foot" }, h("div", { class: "grp" }, up, down, dup), h("div", { class: "grp" }, del)));
    cardEl.appendChild(body);
    return cardEl;
  }

  function addProduct() {
    if (!S) return;
    var p = { enabled: true, pages: ui.pFilter ? [ui.pFilter] : [], store: "Amazon", search: "", url: "", price: "", image: "", title: { hi: "", gu: "", en: "" } };
    S.affiliate.products.push(p);
    setOpen(p, true);
    ui.pSearch = "";
    changed();
    renderProducts();
    var last = productListEl.querySelector('[data-idx="' + (S.affiliate.products.length - 1) + '"]');
    if (last) {
      last.scrollIntoView({ behavior: reduceMotion() ? "auto" : "smooth", block: "center" });
      var f = last.querySelector(".p-body input");
      if (f) setTimeout(function () { f.focus({ preventScroll: true }); }, 200);
    }
  }

  /* ----------------------------------------------------------- telegram */

  function renderTelegram() {
    var v = clear(viewEl("telegram"));
    var T = S.telegram;
    var prevBox = h("div", { class: "preview-page" });
    function paintPrev() {
      clear(prevBox);
      var L = ui.lang.tg || "hi";
      function tx(o) { return (o || {})[L] || (o || {}).en || ""; }
      if (!T.enabled) {
        prevBox.appendChild(h("div", { class: "fake" }, h("b"), h("b"), h("b")));
        prevBox.appendChild(h("p", { class: "hint preview-note", text: "Telegram band hai, isliye site par kuch nahi dikhega." }));
        return;
      }
      prevBox.appendChild(h("div", { class: "fake" }, h("b"), h("b"), h("b")));
      if (T.inline !== false) {
        prevBox.appendChild(h("div", { class: "tg-prev" }, h("span", { class: "tg-ic" }, icon("send")),
          h("strong", { text: tx(T.title) || "Heading" }), h("p", { text: tx(T.text) || "Chhota text" }), h("span", { class: "tg-btn", text: tx(T.button) || "Button" })));
      }
      if (T.sticky !== false) {
        prevBox.appendChild(h("div", { class: "tg-sticky" }, icon("send"), h("span", { text: tx(T.title) || "Heading" }), h("b", { text: tx(T.button) || "Button" })));
      }
    }

    v.appendChild(card({
      icon: "send", title: "Telegram promotion", desc: "Page ke beech me box aur neeche chipki patti.",
      body: [
        switchRow("Telegram promotion chalu karo", "Band karne par site par kahin nahi dikhega", T, "enabled", false, paintPrev),
        h("div", { class: "stack" }, textField("Channel link", T, "url", { placeholder: "https://t.me/yourchannel", type: "url", validate: vTelegram, hint: "Link https://t.me/ se shuru hona chahiye." })),
        switchRow("Page ke beech me box", "Content ke beech ek bada card", T, "inline", true, paintPrev),
        switchRow("Neeche chipki patti", "Screen ke neeche hamesha dikhne wali patti", T, "sticky", true, paintPrev)
      ]
    }));

    function filled(L) { return !!((T.title || {})[L] && (T.text || {})[L] && (T.button || {})[L]); }
    var tabs = langTabs("tg", function (L, panel) {
      function f(label, k, multi) {
        var holder = T[k] = T[k] || {};
        return textField(label, holder, L, { multiline: multi, rows: multi ? 3 : null, spell: true, onInput: function () { paintPrev(); tabs && tabs.refreshDots(); } });
      }
      var ta = f("Chhota text", "text", true);
      ta._input.style.minHeight = "96px";
      panel.appendChild(h("div", { class: "stack" }, f("Heading", "title"), ta, f("Button", "button")));
      paintPrev();
    }, filled);

    v.appendChild(h("div", { class: "grid-2" },
      card({ icon: "file", tone: "violet", title: "Text", desc: "Teeno bhasha me likho. Hara nishaan = poora bhara hua.", body: tabs }),
      card({ icon: "eye", tone: "gold", title: "Preview", desc: "Site par lagbhag aisa dikhega.", body: h("div", { class: "preview-shell" },
        h("div", { class: "preview-top" }, h("i"), h("i"), h("i"), h("span", { text: "indianfestivalwishes.com" })), prevBox) })));

    v.appendChild(card({ icon: "globe", title: "Kin pages par", desc: "\"Sabhi pages\" chuna to poori site par dikhega.", body: pageChips("Pages", T.pages, true) }));
    paintPrev();
  }

  /* -------------------------------------------------------------- patti */

  var tickerEl = null;
  function renderPatti() {
    var v = clear(viewEl("patti"));
    var A = S.announcement;
    tickerEl = h("div", { class: "ticker" });
    var prevNote = h("p", { class: "hint preview-note" });

    function paintTicker() {
      var L = ui.lang.an || "hi";
      var text = ((A.text || {})[L] || "").trim();
      clear(tickerEl);
      tickerEl.className = "ticker";
      if (!A.enabled) {
        tickerEl.classList.add("is-static", "empty-state");
        tickerEl.textContent = "Patti band hai";
        prevNote.textContent = "Patti chalu karne par har page ke upar dikhegi.";
        return;
      }
      if (!text) {
        tickerEl.classList.add("is-static", "empty-state");
        tickerEl.textContent = "Is bhasha me text khali hai, ye patti " + LANG_SHORT[L] + " page par nahi dikhegi";
        prevNote.textContent = "";
        return;
      }
      var still = A.scroll === false || reduceMotion();
      if (still) {
        tickerEl.classList.add("is-static");
        tickerEl.textContent = text;
        prevNote.textContent = A.scroll === false ? "Text ek jagah ruka hua dikhega." : "Aapke device par animation band hai, isliye preview ruka hua hai.";
        return;
      }
      prevNote.textContent = "Raftaar: " + ({ slow: "Dheemi", medium: "Madhyam", fast: "Tez" }[A.speed || "medium"] || "Madhyam") + (A.url ? " · Click karne par link khulega" : "");
      var track = h("div", { class: "ticker-track", "aria-hidden": "true" });
      function group() { return h("span", { class: "ticker-group" }, h("span", { text: text }), icon("sparkle")); }
      tickerEl.setAttribute("aria-label", text);
      tickerEl.appendChild(track);
      var g = group();
      track.appendChild(g);
      var one = g.getBoundingClientRect().width || 200;
      var need = Math.ceil((tickerEl.clientWidth || 600) / one) + 1;
      for (var i = 1; i < need; i++) track.appendChild(group());
      Array.prototype.slice.call(track.children).forEach(function (n) { track.appendChild(n.cloneNode(true)); });
      var px = SPEEDS[A.speed] || SPEEDS.medium;
      track.style.animationDuration = Math.max(6, (one * need) / px) + "s";
    }

    var speedSeg = segmented(nextId("speed"), "Chalne ki raftaar", [["slow", "Dheemi"], ["medium", "Madhyam"], ["fast", "Tez"]], A.speed || "medium", function (val) { A.speed = val; paintTicker(); });

    v.appendChild(card({
      icon: "megaphone", title: "Announcement patti", desc: "Har page ke upar ek chalti hui line.",
      body: [
        switchRow("Patti dikhao", "Site ke har page ke upar", A, "enabled", false, paintTicker),
        switchRow("Text chalta hua dikhao (ticker)", "Band karne par text ek jagah ruka rahega", A, "scroll", true, paintTicker),
        h("div", { class: "grid-2" }, speedSeg,
          textField("Link (zaroori nahi)", A, "url", { placeholder: "https://...", type: "url", validate: vHttps, onInput: paintTicker }))
      ]
    }));

    function filled(L) { return !!(A.text || {})[L]; }
    var tabs = langTabs("an", function (L, panel) {
      var f = textField("Patti ka text (" + LANG_SHORT[L] + ")", A.text, L, { spell: true, placeholder: "Jaise: Navratri 2026 ke card banayein", onInput: function () { paintTicker(); tabs && tabs.refreshDots(); } });
      panel.appendChild(f);
      requestAnimationFrame(paintTicker);
    }, filled);

    v.appendChild(card({ icon: "file", tone: "violet", title: "Patti ka text", desc: "Teeno bhasha me alag-alag likho. Khali bhasha me patti nahi dikhti.", body: [tabs,
      h("div", { class: "preview-block" }, h("span", { class: "label" }, "Live preview (chuni hui bhasha)"),
        h("div", { class: "preview-shell" }, h("div", { class: "preview-top" }, h("i"), h("i"), h("i"), h("span", { text: "indianfestivalwishes.com" })),
          h("div", { class: "preview-page" }, tickerEl, prevNote, h("div", { class: "fake" }, h("b"), h("b"), h("b")))))] }));
  }
  var rsz = 0;
  window.addEventListener("resize", function () {
    clearTimeout(rsz);
    rsz = setTimeout(function () { if (view === "patti" && S) renderPatti(); }, 250);
  });

  /* ---------------------------------------------------------------- ads */

  function renderAds() {
    var v = clear(viewEl("ads"));
    var D = S.ads;
    v.appendChild(h("div", { class: "note warn ads-note" }, icon("alert"), h("span", { text: "AdSense approve hone ke baad hi Publisher ID daalna. Galat ID se site par khaali jagah dikh sakti hai." })));
    v.appendChild(card({
      icon: "chart", title: "Google AdSense", desc: "Slot ID AdSense me \"Ads > By ad unit\" se milta hai. Sirf Auto ads chahiye to slot khali chhod do.",
      body: h("div", { class: "stack" },
        textField("Publisher ID", D, "adsenseClient", { placeholder: "ca-pub-1234567890123456", validate: vAdsense }),
        h("div", { class: "grid-2" },
          textField("Slot: upar wali jagah", D, "slotTop", { placeholder: "1234567890", inputmode: "numeric", validate: vSlot }),
          textField("Slot: beech wali jagah", D, "slotMiddle", { placeholder: "1234567890", inputmode: "numeric", validate: vSlot })))
    }));
    v.appendChild(card({
      icon: "globe", tone: "gold", title: "Google Analytics", desc: "Kitne log site par aaye, ye dekhne ke liye.",
      body: textField("Measurement ID", D, "gaId", { placeholder: "G-XXXXXXXXXX", validate: vGa })
    }));
  }

  /* ------------------------------------------------------------- wishes */

  function renderWishes() {
    var v = clear(viewEl("wishes"));
    var W = S.custom.wishes, TH = S.custom.thoughts;
    if (!OCC[ui.wOcc]) ui.wOcc = "navratri";

    var ta = h("textarea", { id: nextId("cw"), spellcheck: "true", autocomplete: "off", placeholder: "Ek line me ek wish likho..." });
    var counter = h("div", { class: "counter", "aria-live": "polite" });
    var combos = h("div", { class: "combos" });
    var relField;

    function current() { return ((W[ui.wLang] || {})[ui.wOcc] || {})[ui.wRel] || []; }
    function paintCount() {
      var ls = lines(ta.value);
      var long = ls.filter(function (x) { return x.length > 160; }).length;
      clear(counter);
      counter.appendChild(h("span", { text: ls.length + " wish jodi hui hain" }));
      if (long) counter.appendChild(h("span", { class: "warn", text: long + " line 160 akshar se lambi hai, kaat di jaayegi" }));
    }
    function show() { ta.value = current().join("\n"); paintCount(); }
    function paintCombos() {
      clear(combos);
      var any = false;
      LANGS.forEach(function (l) {
        var byOcc = W[l[0]] || {};
        Object.keys(byOcc).forEach(function (o) {
          Object.keys(byOcc[o] || {}).forEach(function (r) {
            var n = (byOcc[o][r] || []).length;
            if (!n) return;
            any = true;
            combos.appendChild(h("button", { class: "combo", type: "button", on: { click: function () {
              ui.wLang = l[0]; ui.wOcc = o; ui.wRel = r; renderWishes();
              var t = viewEl("wishes").querySelector("textarea"); if (t) t.focus();
            } } }, h("span", { text: LANG_SHORT[l[0]] + " · " + ((OCC[o] || [0, o])[1]) + " · " + (RELS[r] || r) }), h("b", { text: String(n) })));
          });
        });
      });
      if (!any) combos.appendChild(h("p", { class: "hint", text: "Abhi koi apni wish nahi jodi gayi." }));
    }

    ta.addEventListener("input", function () {
      var ls = lines(ta.value);
      var byLang = W[ui.wLang] = W[ui.wLang] || {};
      if (ls.length) {
        byLang[ui.wOcc] = byLang[ui.wOcc] || {};
        byLang[ui.wOcc][ui.wRel] = ls;
      } else if (byLang[ui.wOcc]) {
        delete byLang[ui.wOcc][ui.wRel];
        if (!Object.keys(byLang[ui.wOcc]).length) delete byLang[ui.wOcc];
      }
      paintCount();
      paintCombos();
      changed();
    });

    function relOpts() { return OCC[ui.wOcc][2].map(function (r) { return [r, RELS[r]]; }); }
    var langSel = select("Bhasha", LANGS, ui.wLang, function (val) { ui.wLang = val; show(); });
    var occSel = select("Mauka", OCCASIONS.map(function (o) { return [o[0], o[1]]; }), ui.wOcc, function (val) {
      ui.wOcc = val;
      if (OCC[val][2].indexOf(ui.wRel) < 0) ui.wRel = "all";
      var s = relField._select;
      clear(s);
      relOpts().forEach(function (o) { s.appendChild(h("option", { value: o[0], text: o[1] })); });
      s.value = ui.wRel;
      show();
    });
    if (OCC[ui.wOcc][2].indexOf(ui.wRel) < 0) ui.wRel = "all";
    relField = select("Kiske liye", relOpts(), ui.wRel, function (val) { ui.wRel = val; show(); });

    var taField = h("div", { class: "field" }, h("label", { for: ta.id, text: "Wishes (ek line = ek wish)" }), ta, counter);
    v.appendChild(card({
      icon: "message", title: "Apni wishes", desc: "Yahan likhi lines card banane wale page ki list me sabse neeche jud jaati hain.",
      body: h("div", { class: "stack" }, h("div", { class: "grid-3" }, langSel, occSel, relField), taField)
    }));
    v.appendChild(card({ icon: "sparkle", tone: "gold", title: "Jodi hui wishes", desc: "Kisi par dabao to wo khul jaayegi.", body: combos }));

    // thoughts
    var tt = h("textarea", { id: nextId("th"), spellcheck: "true", autocomplete: "off", placeholder: "Ek line me ek suvichar..." });
    var tcount = h("div", { class: "counter", "aria-live": "polite" });
    function showT() { tt.value = (TH[ui.tLang] || []).join("\n"); paintT(); }
    function paintT() { clear(tcount); tcount.appendChild(h("span", { text: lines(tt.value).length + " suvichar jode hue hain" })); }
    tt.addEventListener("input", function () { TH[ui.tLang] = lines(tt.value); paintT(); changed(); });
    var tLang = select("Bhasha", LANGS, ui.tLang, function (val) { ui.tLang = val; showT(); });
    v.appendChild(card({
      icon: "sparkle", tone: "violet", title: "Good Morning ke suvichar", desc: "Good Morning card par \"agla suvichar\" me ye bhi aayenge.",
      body: h("div", { class: "stack" }, tLang, h("div", { class: "field" }, h("label", { for: tt.id, text: "Suvichar (ek line = ek suvichar)" }), tt, tcount))
    }));

    show(); showT(); paintCombos();
  }

  /* ------------------------------------------------------------- backup */

  var backupListEl = null, showAllBackups = false;

  function loadBackups() {
    return api("GET", "/api/backups").then(function (r) {
      backups = r.backups || [];
      paintBackups();
      if (view === "dashboard") renderDashboard();
    }).catch(function () {});
  }

  function paintBackups() {
    if (!backupListEl) return;
    clear(backupListEl);
    if (!backups) { backupListEl.appendChild(h("p", { class: "hint", text: "Load ho raha hai..." })); return; }
    if (!backups.length) {
      backupListEl.appendChild(h("div", { class: "empty" }, icon("database"), h("strong", { text: "Abhi koi backup nahi" }), h("p", { text: "Pehli baar save karte hi yahan backup ban jaayega." })));
      return;
    }
    var list = showAllBackups ? backups : backups.slice(0, 8);
    var box = h("div", { class: "blist" });
    list.forEach(function (b, i) {
      var label = fmtDate(b.date);
      box.appendChild(h("div", { class: "bitem" },
        h("span", { class: "b-ic" }, icon("file")),
        h("span", { class: "b-text" }, h("strong", { text: label }), h("small", { text: (i === 0 ? "Sabse naya · " : "") + ago(new Date(b.date).getTime()) + " · " + fmtSize(b.size) })),
        h("span", { class: "b-act" },
          h("button", { class: "icon-btn", type: "button", "aria-label": "Download: " + label, title: "Download", on: { click: function () { downloadBackup(b.name); } } }, icon("download")),
          h("button", { class: "btn btn-ghost btn-sm", type: "button", "aria-label": "Wapas lagao: " + label, on: { click: function () { restoreBackup(b, label); } } }, icon("restore"), h("span", { class: "hide-xs", text: "Wapas lagao" })))));
    });
    backupListEl.appendChild(box);
    if (backups.length > 8) {
      backupListEl.appendChild(h("div", { class: "more-row" }, h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () { showAllBackups = !showAllBackups; paintBackups(); } } },
        icon(showAllBackups ? "arrowUp" : "chevDown"), showAllBackups ? "Kam dikhao" : "Sabhi " + backups.length + " dikhao")));
    }
  }

  function downloadBackup(name) {
    api("GET", "/api/backups/" + encodeURIComponent(name)).then(function (data) {
      saveFile(JSON.stringify(data, null, 2), name);
    }).catch(function (e) { if (e.status !== 401) toast("Download nahi hua: " + e.message, "err"); });
  }

  function restoreBackup(b, label) {
    ask({ title: "Ye backup wapas lagayein?", text: label + " wali settings site par turant lag jaayengi. Abhi wali settings ka bhi backup ban jaayega." + (isDirty() ? " Aapke unsaved badlav hat jaayenge." : ""), ok: "Haan, wapas lagao", icon: "restore" })
      .then(function (yes) {
        if (!yes) return;
        return api("POST", "/api/backups/" + encodeURIComponent(b.name) + "/restore", {}).then(function () {
          return loadSettings();
        }).then(function () {
          changed();
          toast("Backup wapas lag gaya.", "ok");
        }).catch(function (e) { if (e.status !== 401) toast("Restore nahi hua: " + e.message, "err"); });
      });
  }

  function saveFile(text, name) {
    var blob = new Blob([text], { type: "application/json" });
    var url = URL.createObjectURL(blob);
    var a = h("a", { href: url, download: name });
    document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 2000);
  }

  function renderBackup() {
    var v = clear(viewEl("backup"));
    backupListEl = h("div");
    v.appendChild(card({
      icon: "database", title: "Server par backups", desc: "Har save se pehle purani settings apne aap yahan rakh di jaati hain (aakhri 50).",
      side: h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () { loadBackups().then(function () { toast("List taaza ho gayi.", "info"); }); } } }, icon("restore"), "Refresh"),
      body: backupListEl
    }));
    paintBackups();

    var fileInp = h("input", { type: "file", accept: "application/json,.json", "aria-label": "Backup file chuno" });
    fileInp.addEventListener("change", function () {
      var f = fileInp.files && fileInp.files[0];
      fileInp.value = "";
      if (!f) return;
      if (f.size > 1024 * 1024) { toast("File bahut badi hai.", "err"); return; }
      f.text().then(function (t) {
        var d = JSON.parse(t);
        if (!d || typeof d !== "object" || Array.isArray(d) || !d.affiliate || !d.telegram) throw new Error("bad");
        var ver = S.version;
        S = ensure(d);
        S.version = ver;
        renderAll();
        changed();
        toast("File load ho gayi. Site par lagane ke liye Save dabao.", "info");
      }).catch(function () { toast("Ye sahi settings file nahi hai.", "err"); });
    });

    v.appendChild(card({
      icon: "download", tone: "gold", title: "Export / Import", desc: "Apne computer ya phone me copy rakho, ya purani file se settings wapas lao.",
      body: h("div", { class: "row-actions" },
        h("button", { class: "btn btn-ghost", type: "button", on: { click: function () {
          saveFile(JSON.stringify(S, null, 2) + "\n", "site-settings-" + new Date().toISOString().slice(0, 10) + ".json");
          toast("File download ho gayi.", "ok");
        } } }, icon("download"), "JSON download"),
        h("span", { class: "btn btn-ghost file-btn" }, icon("upload"), "JSON file se lao", fileInp))
    }));
  }

  /* ------------------------------------------------------------ account */

  function renderAccount() {
    var v = clear(viewEl("account"));
    var pw = { cur: "", next: "", again: "" };
    function pwField(label, key, ac) {
      var f = textField(label, pw, key, { type: "password", raw: true });
      f._input.setAttribute("autocomplete", ac);
      return f;
    }
    var fCur = pwField("Abhi ka password", "cur", "current-password");
    var fNext = pwField("Naya password (kam se kam 10 akshar)", "next", "new-password");
    var fAgain = pwField("Naya password dobara", "again", "new-password");
    var meter = h("div", { class: "pw-meter", "aria-hidden": "true" }, h("i"));
    fNext.insertBefore(meter, fNext.querySelector(".field-err"));
    fNext._input.addEventListener("input", function () {
      var val = pw.next, s = 0;
      if (val.length >= 10) s++;
      if (val.length >= 14) s++;
      if (/[^A-Za-z]/.test(val)) s++;
      if (/[a-z]/.test(val) && /[A-Z]/.test(val)) s++;
      var bar = meter.firstChild;
      bar.style.width = Math.max(8, s * 25) + "%";
      bar.style.background = s >= 3 ? "var(--ok)" : s === 2 ? "var(--marigold)" : "var(--err)";
    });
    // password fields should not mark settings dirty
    [fCur, fNext, fAgain].forEach(function (f) { f._input.addEventListener("input", function (e) { e.stopPropagation(); }); });

    var btn = h("button", { class: "btn btn-primary", type: "submit" }, h("span", { class: "btn-label", text: "Password badlo" }), h("span", { class: "spinner", "aria-hidden": "true" }));
    var form = h("form", { class: "stack", novalidate: true }, h("input", { type: "text", name: "username", autocomplete: "username", value: (ME && ME.user) || "", hidden: true, "aria-hidden": "true", tabindex: "-1" }),
      fCur, h("div", { class: "grid-2" }, fNext, fAgain), h("div", { class: "row-actions" }, btn));
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!pw.cur) { toast("Abhi ka password daalo.", "err"); fCur._input.focus(); return; }
      if (pw.next.length < 10) { toast("Naya password kam se kam 10 akshar ka rakho.", "err"); fNext._input.focus(); return; }
      if (pw.next !== pw.again) { toast("Dono naye password ek jaise nahi hain.", "err"); fAgain._input.focus(); return; }
      btn.classList.add("is-busy"); btn.disabled = true;
      api("POST", "/api/password", { current: pw.cur, next: pw.next }, { allow401: true }).then(function () {
        [fCur, fNext, fAgain].forEach(function (f) { f._input.value = ""; });
        pw.cur = pw.next = pw.again = "";
        meter.firstChild.style.width = "0";
        toast("Password badal gaya. Baaki sab jagah se logout ho gaya.", "ok");
      }).catch(function (err) {
        toast(err.status === 403 ? "Abhi ka password galat hai." : err.status === 401 ? "Session khatam, dobara login karo." : "Password nahi badla: " + err.message, "err");
        if (err.status === 401) sessionExpired();
      }).then(function () { btn.classList.remove("is-busy"); btn.disabled = false; });
    });

    v.appendChild(card({ icon: "key", title: "Password badlo", desc: "Naya password sirf server par (scrypt hash) save hota hai. Badalne ke baad purane login band ho jaate hain.", body: form }));

    var expTxt = ME && ME.exp ? fmtDate(ME.exp) : "–";
    v.appendChild(card({
      icon: "user", tone: "violet", title: "Login", desc: "Is browser ka login 12 ghante tak chalta hai.",
      body: h("div", { class: "stack" },
        h("div", { class: "note info" }, icon("info"), h("span", { text: "Login: " + ((ME && ME.user) || "admin") + " · Session khatam: " + expTxt + (ME && ME.customPassword ? " · Panel se badla hua password chal raha hai" : "") })),
        h("div", { class: "row-actions" }, h("button", { class: "btn btn-danger", type: "button", on: { click: function () { $("btn-logout").click(); } } }, icon("logout"), "Logout")))
    }));
  }

  /* ============================================================== start */

  (function brand() {
    document.querySelectorAll(".brand-mark").forEach(function (b) { b.innerHTML = FLOWER; });
    var ring = document.getElementById("petal-ring");
    if (ring) {
      var s = "";
      for (var i = 0; i < 16; i++) s += '<ellipse cx="100" cy="30" rx="7" ry="20" transform="rotate(' + (i * 22.5) + ' 100 100)"/>';
      for (var j = 0; j < 8; j++) s += '<ellipse cx="100" cy="60" rx="5" ry="13" transform="rotate(' + (j * 45 + 22.5) + ' 100 100)"/>';
      ring.innerHTML = s;
    }
  })();
  hydrateIcons();
  buildNav();

  api("GET", "/api/me", undefined, { allow401: true }).then(function (me) {
    ME = me;
    return enterApp();
  }).catch(function (err) {
    showLogin(err.status && err.status !== 401 ? "Server se baat nahi ho paayi (" + err.status + ")." : err.status === 0 ? err.message : "", err.status === 401 ? null : undefined);
  });
})();
