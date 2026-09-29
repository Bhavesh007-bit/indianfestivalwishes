/* IFW Admin — talks to the site's own server (/api/*). Vanilla JS, no build step. */
(function () {
  "use strict";

  /* ================================================================ data */

  /* ---- UI language (hi / gu / en). Strings live in i18n.js (I18N). ---- */
  var LANG_KEY = "ifw-admin-lang";
  var UI_LANGS = [["hi", "हिं", "हिंदी"], ["gu", "ગુ", "ગુજરાતી"], ["en", "EN", "English"]];
  var LOCALES = { hi: "hi-IN", gu: "gu-IN", en: "en-IN" };
  var LANG = pickLang();

  function pickLang() {
    try {
      var s = localStorage.getItem(LANG_KEY);
      if (s && I18N[s]) return s;
    } catch (e) { /* storage blocked */ }
    var list = (navigator.languages && navigator.languages.length ? navigator.languages : [navigator.language || ""]);
    for (var i = 0; i < list.length; i++) {
      var p = String(list[i] || "").toLowerCase().slice(0, 2);
      if (p === "gu" || p === "hi" || p === "en") return p;
    }
    return "en";
  }
  function has(key) { return Object.prototype.hasOwnProperty.call(I18N[LANG], key); }
  // t("key", {x: 1}) -> translated string with {x} filled in; falls back to English, then the key.
  function t(key, vars) {
    var d = I18N[LANG] || I18N.en;
    var s = d[key];
    if (s == null) s = I18N.en[key];
    if (s == null) s = key;
    if (vars) s = s.replace(/\{(\w+)\}/g, function (m, k) { return vars[k] != null ? String(vars[k]) : m; });
    return s;
  }
  // count-aware: uses "key.one" when n === 1 and the current language defines it
  function tn(key, n, vars) {
    vars = vars || {};
    vars.n = n;
    return t(n === 1 && has(key + ".one") ? key + ".one" : key, vars);
  }
  function langName(code) { return t("lang.name." + code); }
  function pageName(k) { return k === "all" ? t("page.all") : (I18N.en["page." + k] ? t("page." + k) : k); }

  // Content languages (the site's languages; settings are stored per language)
  var LANGS = [["hi"], ["gu"], ["en"]];

  // [page tag, flag "new"] — tags match data-aff / pageTag in build.js
  var PAGES = [
    ["home"], ["navratri"], ["navratri-day"], ["recipes"], ["garba"],
    ["dussehra"], ["karva-chauth"], ["diwali"],
    ["birthday"], ["anniversary"], ["wedding"], ["engagement"], ["good-morning"],
    ["shraddhanjali", 1], ["invitations", 1],
    ["invite-wedding", 1], ["invite-engagement", 1], ["invite-birthday-party", 1], ["invite-griha-pravesh", 1],
    ["invite-baby-shower", 1], ["invite-naming-ceremony", 1], ["invite-puja", 1], ["invite-shop-opening", 1],
    ["info"]
  ];

  var ALL_RELS = ["all", "friend", "family", "sibling", "spouse", "business", "devotional"];
  var OCCASIONS = [
    ["navratri", ALL_RELS],
    ["dussehra", ALL_RELS],
    ["karva-chauth", ["all", "spouse", "family", "friend", "devotional"]],
    ["diwali", ALL_RELS],
    ["birthday", ALL_RELS],
    ["anniversary", ALL_RELS],
    ["wedding", ["all", "friend", "family", "sibling", "business", "devotional"]],
    ["engagement", ["all", "friend", "family", "sibling", "business", "devotional"]],
    ["good-morning", ALL_RELS]
  ];
  var OCC = {};
  OCCASIONS.forEach(function (o) { OCC[o[0]] = o; });
  function relName(r) { return I18N.en["rel." + r] ? t("rel." + r) : r; }
  var SPEEDS = { slow: 35, medium: 60, fast: 95 };

  // [id, icon]; titles come from "view.<id>.title/.sub/.tab"
  var VIEWS = [
    ["dashboard", "grid"], ["products", "bag"], ["telegram", "send"], ["patti", "megaphone"],
    ["ads", "chart"], ["wishes", "message"], ["backup", "database"], ["account", "shield"]
  ];
  function viewTitle(id) { return t("view." + id + ".title"); }
  function viewTab(id) { return has("view." + id + ".tab") ? t("view." + id + ".tab") : viewTitle(id); }
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
      return new Date(d).toLocaleString(LOCALES[LANG] || "en-IN", { day: "numeric", month: "short", year: "numeric", hour: "numeric", minute: "2-digit", hourCycle: LANG === "en" ? "h12" : "h23" });
    } catch (e) { return String(d); }
  }
  function fmtSize(b) { return b < 1024 ? b + " B" : (b / 1024).toFixed(1) + " KB"; }
  function ago(ts) {
    var s = Math.round((Date.now() - ts) / 1000);
    if (s < 60) return t("ago.now");
    if (s < 3600) return tn("ago.min", Math.round(s / 60));
    if (s < 86400) return tn("ago.hour", Math.round(s / 3600));
    return tn("ago.day", Math.round(s / 86400));
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
      var p = ct.indexOf("json") >= 0 ? r.json().catch(function () { return {}; }) : r.text().then(function (txt) { return { text: txt }; });
      return p.then(function (data) {
        if (r.status === 401 && !opts.allow401) { sessionExpired(); }
        if (!r.ok) {
          var e = new Error(errText(r.status, data));
          e.status = r.status; e.data = data;
          throw e;
        }
        return data;
      });
    }, function () {
      var e = new Error(t("net.err"));
      e.status = 0;
      throw e;
    });
  }

  // Server error texts are English; show them as-is in English, a translated summary otherwise.
  function errText(status, data) {
    if (LANG === "en" && data && data.error) return data.error;
    if (status === 413) return t("err.tooBig", { n: status });
    if (status === 400) return t("err.invalid", { n: status });
    return t("err.status", { n: status });
  }

  /* ============================================================== toasts */

  function toast(text, kind) {
    kind = kind || "info";
    var closeBtn = h("button", { class: "icon-btn", type: "button", "aria-label": t("btn.close") }, icon("x"));
    var el = h("div", { class: "toast " + kind },
      h("span", { class: "t-ic" }, icon(kind === "ok" ? "check" : kind === "err" ? "alert" : "info")),
      h("p", { text: text }), closeBtn);
    function kill() {
      if (!el.parentNode) return;
      el.classList.add("out");
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, reduceMotion() ? 0 : 240);
    }
    closeBtn.addEventListener("click", kill);
    var box = $("toasts");
    box.appendChild(el);
    while (box.children.length > 3) box.removeChild(box.firstChild);
    setTimeout(kill, kind === "err" ? 8000 : 4200);
  }

  /* ============================================================== dialog */

  function ask(opts) {
    var d = $("dialog");
    $("dlg-title").textContent = opts.title || t("dlg.title");
    $("dlg-text").textContent = opts.text || "";
    $("dlg-ok").textContent = opts.ok || t("dlg.yes");
    $("dlg-cancel").textContent = opts.cancel || t("dlg.no");
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
  var pwState = { cur: "", next: "", again: "" };   // account form; kept here so a language switch keeps typed text

  function ensure(d) {
    if (!d || typeof d !== "object" || Array.isArray(d)) d = {};
    function obj(o, k) { if (!o[k] || typeof o[k] !== "object" || Array.isArray(o[k])) o[k] = {}; return o[k]; }
    var a = obj(d, "affiliate");
    if (!Array.isArray(a.products)) a.products = [];
    var tg = obj(d, "telegram");
    ["title", "text", "button"].forEach(function (k) { obj(tg, k); });
    if (!Array.isArray(tg.pages)) tg.pages = ["all"];
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
      $("save-chip-text").textContent = t(d ? "chip.dirty" : "chip.saved");
      refreshNavBadges();
      if (view === "dashboard") renderDashboard();
    });
  }

  /* ================================================================ auth */

  var lockTimer = null, locked = false;
  var loginMsgState = { fn: null, kind: null };
  function showLogin(msg, kind) {
    document.body.classList.remove("is-booting");
    $("app").hidden = true;
    $("login").hidden = false;
    closeDrawer();
    loginMsg(msg || "", kind);
    setTimeout(function () { ($("lg-user").value ? $("lg-pass") : $("lg-user")).focus(); }, 30);
  }
  // text may be a string or a function returning one (re-run when the UI language changes)
  function loginMsg(text, kind) {
    var fn = typeof text === "function" ? text : text ? function () { return text; } : null;
    loginMsgState = { fn: fn, kind: kind };
    paintLoginMsg();
  }
  function paintLoginMsg() {
    var m = $("login-msg"), kind = loginMsgState.kind;
    clear(m);
    var text = loginMsgState.fn ? loginMsgState.fn() : "";
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
    locked = true;
    function tick() {
      var left = Math.max(0, Math.round((end - Date.now()) / 1000));
      if (!left) { clearInterval(lockTimer); locked = false; btn.disabled = false; loginMsg(function () { return t("login.retryNow"); }, "info"); return; }
      var mm = Math.floor(left / 60), ss = left % 60;
      var time = mm + ":" + (ss < 10 ? "0" : "") + ss;
      loginMsg(function () { return t("login.locked", { time: time }); });
    }
    tick();
    lockTimer = setInterval(tick, 1000);
  }

  $("lg-eye").addEventListener("click", function () {
    var inp = $("lg-pass"), show = inp.type === "password";
    inp.type = show ? "text" : "password";
    this.setAttribute("aria-pressed", show ? "true" : "false");
    this.setAttribute("aria-label", t(show ? "login.hide" : "login.show"));
    clear(this).appendChild(icon(show ? "eyeOff" : "eye"));
    inp.focus();
  });

  $("login-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var u = $("lg-user").value.trim(), p = $("lg-pass").value;
    if (!u || !p) { loginMsg(function () { return t("login.both"); }); (u ? $("lg-pass") : $("lg-user")).focus(); return; }
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
        loginMsg(function () { return t("login.wrong") + (left ? " " + tn("login.left", left) : ""); });
        $("lg-pass").select();
      } else if (err.status === 503) {
        loginMsg(function () { return t("login.noCreds"); });
      } else {
        var em = err.message;
        loginMsg(err.status === 0 ? function () { return t("net.err"); } : function () { return em || t("login.failed"); });
      }
    }).then(function () {
      btn.classList.remove("is-busy");
      if (!locked) btn.disabled = false;
    });
  });

  var expiredShown = false;
  function sessionExpired() {
    if (expiredShown || $("app").hidden) return;
    expiredShown = true;
    var dirty = isDirty();
    showLogin(function () { return t(dirty ? "session.expiredDirty" : "session.expired"); }, "info");
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
      if (keep) toast(t("session.welcomeBack"), "info");
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
    var p = isDirty() ? ask({ title: t("logout.ask.title"), text: t("logout.ask.text"), ok: t("logout.ask.ok"), danger: true, icon: "logout" }) : Promise.resolve(true);
    p.then(function (yes) {
      if (!yes) return;
      api("POST", "/api/logout", {}, { allow401: true }).catch(function () {}).then(function () {
        S = null; saved = ""; ME = null;
        $("savebar").hidden = true;
        showLogin(function () { return t("logout.done"); }, "info");
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
    nav.appendChild(h("div", { class: "nav-group", text: t("nav.menu") }));
    VIEWS.forEach(function (v, i) {
      if (i === 6) nav.appendChild(h("div", { class: "nav-group", text: t("nav.system") }));
      nav.appendChild(h("button", { class: "nav-item", type: "button", "data-go": v[0], on: { click: function () { go(v[0]); closeDrawer(); } } },
        icon(v[1]), h("span", { text: viewTitle(v[0]) }), h("span", { class: "badge", "data-badge": v[0], hidden: true })));
    });
    var tb = clear($("tabbar"));
    TABS.forEach(function (k) {
      var v = VIEWS.filter(function (x) { return x[0] === k; })[0];
      tb.appendChild(h("button", { class: "tab", type: "button", "data-go": k, on: { click: function () { go(k); } } }, icon(v[1]), h("span", { text: viewTab(k) })));
    });
    tb.appendChild(h("button", { class: "tab", type: "button", id: "tab-more", "aria-controls": "side", "aria-expanded": $("side").classList.contains("open") ? "true" : "false", on: { click: openDrawer } }, icon("more"), h("span", { text: t("tab.more") })));
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
    $("view-title").textContent = viewTitle(name);
    $("view-sub").textContent = t("view." + name + ".sub");
    document.title = viewTitle(name) + " | " + t("app.short");
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
    var opts = (withAll ? [["all"]] : []).concat(PAGES);
    opts.forEach(function (pg) {
      var cb = h("input", { type: "checkbox", value: pg[0] });
      cb.checked = list.indexOf(pg[0]) >= 0;
      var lab = h("label", { class: "chip" + (cb.checked ? " on" : "") + (pg[1] ? " tag-new" : ""), "data-new": pg[1] ? t("chip.new") : null }, cb,
        h("span", { class: "chk", "aria-hidden": "true" }, icon("check")), h("span", { text: pageName(pg[0]) }));
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
    var list = h("div", { class: "ltabs", role: "tablist", "aria-label": t("lang.label") });
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
        filled ? h("span", { class: "fill-dot", "aria-hidden": "true" }) : null, h("span", { text: langName(l[0]) }));
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

  function vTelegram(v) { return v && !/^https:\/\/(t\.me|telegram\.me)\/[A-Za-z0-9_+\/-]+$/.test(v) ? t("v.telegram") : ""; }
  function vHttps(v) { return v && !/^https:\/\/\S+$/.test(v) ? t("v.https") : ""; }
  function vImage(v) {
    if (!v) return "";
    if (/^https:\/\/\S+$/.test(v)) return "";
    if (v.indexOf(location.origin + "/uploads/") === 0) return "";
    return t("v.image");
  }
  function vAdsense(v) { return v && !/^ca-pub-\d{10,20}$/.test(v) ? t("v.adsense") : ""; }
  function vSlot(v) { return v && !/^\d{6,15}$/.test(v) ? t("v.slot") : ""; }
  function vGa(v) { return v && !/^G-[A-Z0-9]{4,15}$/.test(v) ? t("v.ga") : ""; }
  function vTag(v) { return v && !/^[A-Za-z0-9_.-]{2,40}$/.test(v) ? t("v.tag") : ""; }

  function validateAll() {
    var tg = S.telegram;
    if (tg.enabled && !tg.url) return ["telegram", t("v.tgEmpty")];
    var e = vTelegram(tg.url || ""); if (e) return ["telegram", e];
    e = vHttps(S.announcement.url || ""); if (e) return ["patti", t("v.patti", { e: e })];
    e = vAdsense(S.ads.adsenseClient || ""); if (e) return ["ads", e];
    e = vSlot(S.ads.slotTop || "") || vSlot(S.ads.slotMiddle || ""); if (e) return ["ads", e];
    e = vGa(S.ads.gaId || ""); if (e) return ["ads", e];
    e = vTag(S.affiliate.amazonTag || ""); if (e) return ["products", e];
    for (var i = 0; i < S.affiliate.products.length; i++) {
      var p = S.affiliate.products[i];
      e = vHttps(p.url || "") || vImage(p.image || "");
      if (e) return ["products", t("v.product", { n: i + 1, e: e })];
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
      toast(t("save.ok"), "ok");
      loadBackups();
    }).catch(function (err) {
      if (err.status === 409) {
        return ask({ title: t("conflict.title"), text: t("conflict.text"), ok: t("conflict.ok"), cancel: t("conflict.cancel") })
          .then(function (yes) { saving = false; if (yes) save(true); });
      }
      if (err.status !== 401) toast(t("save.fail", { msg: err.message }), "err");
    }).then(function () {
      saving = false;
      btn.classList.remove("is-busy");
      btn.disabled = false;
    });
  }
  $("btn-save").addEventListener("click", function () { save(); });
  $("btn-discard").addEventListener("click", function () {
    ask({ title: t("discard.title"), text: t("discard.text"), ok: t("discard.ok"), danger: true, icon: "restore" })
      .then(function (yes) {
        if (!yes) return;
        S = ensure(JSON.parse(saved));
        renderAll();
        changed();
        toast(t("discard.done"), "info");
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
    var greet = t(hour < 12 ? "dash.greet.morning" : hour < 17 ? "dash.greet.day" : "dash.greet.evening");
    var ver = Number(S.version);
    var lastSaved = ver > 1e12 ? ago(ver) + " (" + fmtDate(ver) + ")" : t("dash.never");

    v.appendChild(h("div", { class: "hero" },
      (function () { var s = h("span", { class: "hero-flower", "aria-hidden": "true" }); s.innerHTML = FLOWER; return s; })(),
      h("small", { text: "Indian Festival Wishes" }),
      h("h2", null, greet + ", ", h("span", { class: "ud", text: (ME && ME.user) || "admin" })),
      h("p", { text: t(isDirty() ? "dash.dirty" : "dash.clean") }),
      h("div", { class: "hero-meta" },
        h("span", null, icon("clock"), t("dash.lastSave", { x: lastSaved })),
        h("span", null, icon("database"), backups ? tn("dash.backups", backups.length) : t("dash.backups", { n: "–" })))));

    var tag = (S.affiliate.amazonTag || "").trim();
    var live = liveProducts();
    var rows = [
      ["telegram", "send", "Telegram", t(S.telegram.enabled ? "state.on" : "state.off"), S.telegram.enabled ? "on" : "off"],
      ["patti", "megaphone", t("dash.stat.patti"), t(S.announcement.enabled ? "state.on" : "state.off"), S.announcement.enabled ? "on" : "off"],
      ["products", "tag", t("dash.stat.tag"), tag || t("state.notSet"), tag ? "on" : "warn"],
      ["products", "bag", t("dash.stat.live"), live + " / " + S.affiliate.products.length, live ? "on" : "warn"],
      ["ads", "chart", "AdSense", t(S.ads.adsenseClient ? "state.on" : "state.off"), S.ads.adsenseClient ? "on" : "off"],
      ["ads", "globe", t("dash.stat.ga"), S.ads.gaId || t("state.off"), S.ads.gaId ? "on" : "off"]
    ];
    var grid = h("div", { class: "stats" });
    rows.forEach(function (r, i) {
      grid.appendChild(h("button", { class: "stat", type: "button", "data-dash": "s" + i, on: { click: function () { go(r[0]); } }, "aria-label": r[2] + ": " + r[3] },
        h("span", { class: "s-icon" }, icon(r[1])),
        h("span", { class: "s-label", text: r[2] }),
        h("span", { class: "s-value", text: r[3] }),
        h("span", { class: "pill " + r[4], text: t(r[4] === "on" ? "pill.live" : r[4] === "warn" ? "pill.warn" : "pill.off") })));
    });
    v.appendChild(grid);

    v.appendChild(h("h3", { class: "section-title", text: t("dash.quick") }));
    var q = h("div", { class: "quick" });
    [["products", "plus", "dash.q.product", true], ["patti", "megaphone", "dash.q.patti"],
     ["wishes", "message", "dash.q.wishes"], ["backup", "database", "dash.q.backup"]].forEach(function (qa, i) {
      q.appendChild(h("button", { type: "button", "data-dash": "q" + i, on: { click: function () {
        go(qa[0]);
        if (qa[3]) addProduct();
      } } }, icon(qa[1]), h("span", null, t(qa[2]), h("small", { text: t(qa[2] + ".sub") }))));
    });
    v.appendChild(q);

    var cw = countWishes();
    v.appendChild(h("h3", { class: "section-title", text: t("dash.more") }));
    v.appendChild(h("div", { class: "note info" }, icon("info"),
      h("span", { text: t("dash.info", { n: cw }) })));

    if (focusedGo) { var f = v.querySelector('[data-dash="' + focusedGo + '"]'); if (f) f.focus(); }
  }

  /* ----------------------------------------------------------- products */

  var productListEl = null, countLineEl = null;

  function renderProducts() {
    var v = clear(viewEl("products"));
    var A = S.affiliate;
    v.appendChild(card({
      icon: "tag", title: t("prod.assoc"), desc: t("prod.assoc.desc"),
      body: h("div", { class: "grid-2" },
        textField(t("prod.tag"), A, "amazonTag", { placeholder: "yourname-21", validate: vTag, hint: t("prod.tag.hint") }),
        (function () {
          var f = textField(t("prod.max"), A, "maxPerSlot", { type: "number", inputmode: "numeric", hint: t("prod.max.hint") });
          var inp = f._input;
          inp.min = 1; inp.max = 8;
          inp.addEventListener("input", function () { A.maxPerSlot = Math.min(8, Math.max(1, parseInt(inp.value, 10) || 4)); changed(); });
          return f;
        })())
    }));

    var filterOpts = [["", t("page.all")]].concat(PAGES.map(function (p) { return [p[0], pageName(p[0])]; }));
    var fSel = select(t("prod.filter"), filterOpts, ui.pFilter, function (val) { ui.pFilter = val; drawProductList(); });
    var sid = nextId("q");
    var sInp = h("input", { id: sid, type: "search", placeholder: t("prod.search.ph"), autocomplete: "off", value: ui.pSearch });
    sInp.addEventListener("input", function () { ui.pSearch = sInp.value; drawProductList(); });
    var sField = h("div", { class: "field" }, h("label", { for: sid, text: t("prod.search") }), h("div", { class: "input-icon" }, h("span", { "data-icon": "search" }), sInp));
    hydrateIcons(sField);
    v.appendChild(h("div", { class: "toolbar" }, sField, fSel,
      h("button", { class: "btn btn-primary", type: "button", on: { click: addProduct } }, icon("plus"), t("prod.new"))));
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
    countLineEl.textContent = list.length ? (shown === list.length ? tn("prod.count", list.length) : t("prod.countOf", { a: shown, b: list.length })) : "";
    if (!list.length) {
      productListEl.appendChild(h("div", { class: "empty" }, icon("bag"), h("strong", { text: t("prod.empty") }),
        h("p", { text: t("prod.empty.hint") })));
    } else if (!shown) {
      productListEl.appendChild(h("div", { class: "empty" }, icon("search"), h("strong", { text: t("prod.none") }), h("p", { text: t("prod.none.hint") })));
    }
    if (focusIndex != null) {
      var c = productListEl.querySelector('[data-idx="' + focusIndex + '"]');
      if (c) { var tgt = c.querySelector(focusSel || ".p-main"); if (tgt && !tgt.disabled) tgt.focus(); else c.querySelector(".p-main").focus(); }
    }
  }

  function isOpen(p) { return openProducts ? openProducts.has(p) : !!p.__open; }
  function setOpen(p, on) { if (openProducts) { if (on) openProducts.add(p); else openProducts.delete(p); } }

  function thumb(p) {
    var box = h("span", { class: "p-thumb", "aria-hidden": "true" });
    var src = p.image && !vImage(p.image) ? p.image : "";
    if (src) {
      var im = h("img", { src: src, alt: "", loading: "lazy" });
      im.addEventListener("error", function () { clear(box).appendChild(icon("image")); });
      box.appendChild(im);
    } else box.appendChild(icon("bag"));
    return box;
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
      titleEl.textContent = p.title[LANG] || p.title.hi || p.title.gu || p.title.en || t("prod.new");
      clear(subEl);
      if (p.url) subEl.appendChild(document.createTextNode(t("prod.direct")));
      else if (p.search) { subEl.appendChild(document.createTextNode(t("prod.searchSrc") + " ")); subEl.appendChild(h("span", { class: "ud", text: p.search })); }
      else subEl.appendChild(document.createTextNode(t("prod.noLink")));
      clear(tagsEl);
      if (!p.pages.length) tagsEl.appendChild(h("span", { class: "none", text: t("prod.noPage") }));
      p.pages.forEach(function (pg) { tagsEl.appendChild(h("span", { text: pageName(pg) })); });
    }
    paintHead();
    var th = thumb(p);

    var cb = h("input", { type: "checkbox", role: "switch", "aria-label": t("prod.show") });
    cb.checked = p.enabled !== false;
    cb.addEventListener("change", function () { p.enabled = cb.checked; cardEl.classList.toggle("off", !cb.checked); changed(); });

    var main = h("button", { class: "p-main", type: "button", "aria-expanded": open ? "true" : "false", "aria-controls": bodyId }, titleEl, subEl, tagsEl);
    var chev = h("button", { class: "icon-btn p-chev", type: "button", "aria-label": t(open ? "prod.collapse" : "prod.expand", { name: titleEl.textContent }), "aria-expanded": open ? "true" : "false", "aria-controls": bodyId }, icon("chevDown"));
    function toggle() { setOpen(p, !isOpen(p)); drawProductList(i, ".p-main"); }
    main.addEventListener("click", toggle);
    chev.addEventListener("click", function () { setOpen(p, !isOpen(p)); drawProductList(i, ".p-chev"); });

    cardEl.appendChild(h("div", { class: "p-row" }, th, main,
      h("div", { class: "p-side" }, h("span", { class: "switch", title: t("prod.show") }, cb, h("span", { class: "track", "aria-hidden": "true" })), chev)));

    if (!open) return cardEl;

    var body = h("div", { class: "p-body", id: bodyId });
    body.appendChild(h("div", { class: "grid-3" },
      LANGS.map(function (l) { return textField(t("prod.name", { lang: langName(l[0]) }), p.title, l[0], { onInput: paintHead, spell: true }); })));
    body.appendChild(h("div", { class: "grid-2" },
      textField(t("prod.searchTerm"), p, "search", { placeholder: t("prod.searchTerm.ph"), hint: t("prod.searchTerm.hint"), onInput: paintHead }),
      textField(t("prod.url"), p, "url", { placeholder: "https://amzn.to/...", type: "url", validate: vHttps, hint: t("prod.url.hint"), onInput: paintHead })));
    body.appendChild(h("div", { class: "grid-2" },
      textField(t("prod.price"), p, "price", { placeholder: t("prod.price.ph") }),
      textField(t("prod.store"), p, "store", { placeholder: "Amazon" })));

    // image
    var prev = h("div", { class: "img-prev" });
    function paintPrev() {
      clear(prev);
      var src = p.image && !vImage(p.image) ? p.image : "";
      if (src) {
        var im = h("img", { src: src, alt: t("prod.imgAlt") });
        im.addEventListener("error", function () { clear(prev).appendChild(icon("image")); });
        prev.appendChild(im);
      } else prev.appendChild(icon("image"));
      var nt = thumb(p); th.replaceWith(nt); th = nt;
    }
    paintPrev();
    var imgField = textField(t("prod.img"), p, "image", { placeholder: "https://...", type: "url", validate: vImage, hint: t("prod.img.hint"), onInput: paintPrev });
    var fileInp = h("input", { type: "file", accept: "image/jpeg,image/png,image/webp", "aria-label": t("prod.upload") });
    var upBtn = h("span", { class: "btn btn-soft btn-sm file-btn" }, icon("upload"), h("span", { class: "btn-label", text: t("prod.upload") }), h("span", { class: "spinner", "aria-hidden": "true" }), fileInp);
    fileInp.addEventListener("change", function () {
      var f = fileInp.files && fileInp.files[0];
      fileInp.value = "";
      if (!f) return;
      if (["image/jpeg", "image/png", "image/webp"].indexOf(f.type) < 0) { toast(t("prod.upload.type"), "err"); return; }
      if (f.size > 2 * 1024 * 1024) { toast(t("prod.upload.size"), "err"); return; }
      upBtn.classList.add("is-busy");
      api("POST", "/api/upload", f, { raw: true, type: f.type }).then(function (r) {
        p.image = location.origin + r.url;
        imgField._input.value = p.image;
        imgField._input.dispatchEvent(new Event("input"));
        toast(t("prod.upload.ok"), "ok");
      }).catch(function (e) { if (e.status !== 401) toast(t("prod.upload.fail", { msg: e.message }), "err"); })
        .then(function () { upBtn.classList.remove("is-busy"); });
    });
    var clearImg = h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () {
      imgField._input.value = ""; imgField._input.dispatchEvent(new Event("input"));
    } } }, icon("x"), t("prod.imgClear"));
    body.appendChild(h("div", { class: "img-field" }, prev, h("div", { class: "img-ctrl" }, imgField, h("div", { class: "row-actions" }, upBtn, clearImg))));

    body.appendChild(pageChips(t("prod.pages"), p.pages, false, paintHead));

    function move(d) {
      var j = i + d;
      if (j < 0 || j >= list.length) return;
      list.splice(j, 0, list.splice(i, 1)[0]);
      changed();
      drawProductList(j, d < 0 ? ".mv-up" : ".mv-down");
    }
    var up = h("button", { class: "btn btn-ghost btn-sm mv-up", type: "button", disabled: i === 0, on: { click: function () { move(-1); } } }, icon("arrowUp"), t("prod.up"));
    var down = h("button", { class: "btn btn-ghost btn-sm mv-down", type: "button", disabled: i === list.length - 1, on: { click: function () { move(1); } } }, icon("arrowDown"), t("prod.down"));
    var dup = h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () {
      var c = clone(p);
      list.splice(i + 1, 0, c);
      setOpen(p, false); setOpen(c, true);
      changed();
      drawProductList(i + 1, ".p-main");
      toast(t("prod.dup.done"), "info");
    } } }, icon("copy"), t("prod.dup"));
    var del = h("button", { class: "btn btn-danger btn-sm", type: "button", on: { click: function () {
      ask({ title: t("prod.del.title"), text: t("prod.del.text", { name: titleEl.textContent }), ok: t("prod.del.ok"), danger: true, icon: "trash" })
        .then(function (yes) {
          if (!yes) return;
          list.splice(i, 1);
          changed();
          drawProductList(Math.min(i, list.length - 1), ".p-main");
          toast(t("prod.del.done"), "info");
        });
    } } }, icon("trash"), t("prod.del"));
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
    var prevBox = h("div", { class: "preview-page", "data-ud": "" });
    function paintPrev() {
      clear(prevBox);
      var L = ui.lang.tg || "hi";
      function tx(o) { return (o || {})[L] || (o || {}).en || ""; }
      if (!T.enabled) {
        prevBox.appendChild(h("div", { class: "fake" }, h("b"), h("b"), h("b")));
        prevBox.appendChild(h("p", { class: "hint preview-note", text: t("tg.off") }));
        return;
      }
      prevBox.appendChild(h("div", { class: "fake" }, h("b"), h("b"), h("b")));
      if (T.inline !== false) {
        prevBox.appendChild(h("div", { class: "tg-prev" }, h("span", { class: "tg-ic" }, icon("send")),
          h("strong", { text: tx(T.title) || t("tg.heading") }), h("p", { text: tx(T.text) || t("tg.text") }), h("span", { class: "tg-btn", text: tx(T.button) || t("tg.button") })));
      }
      if (T.sticky !== false) {
        prevBox.appendChild(h("div", { class: "tg-sticky" }, icon("send"), h("span", { text: tx(T.title) || t("tg.heading") }), h("b", { text: tx(T.button) || t("tg.button") })));
      }
    }

    v.appendChild(card({
      icon: "send", title: t("tg.card"), desc: t("tg.card.desc"),
      body: [
        switchRow(t("tg.enable"), t("tg.enable.desc"), T, "enabled", false, paintPrev),
        h("div", { class: "stack" }, textField(t("tg.url"), T, "url", { placeholder: "https://t.me/yourchannel", type: "url", validate: vTelegram, hint: t("tg.url.hint") })),
        switchRow(t("tg.inline"), t("tg.inline.desc"), T, "inline", true, paintPrev),
        switchRow(t("tg.sticky"), t("tg.sticky.desc"), T, "sticky", true, paintPrev)
      ]
    }));

    function filled(L) { return !!((T.title || {})[L] && (T.text || {})[L] && (T.button || {})[L]); }
    var tabs = langTabs("tg", function (L, panel) {
      function f(label, k, multi) {
        var holder = T[k] = T[k] || {};
        return textField(label, holder, L, { multiline: multi, rows: multi ? 3 : null, spell: true, onInput: function () { paintPrev(); tabs && tabs.refreshDots(); } });
      }
      var ta = f(t("tg.text"), "text", true);
      ta._input.style.minHeight = "96px";
      panel.appendChild(h("div", { class: "stack" }, f(t("tg.heading"), "title"), ta, f(t("tg.button"), "button")));
      paintPrev();
    }, filled);

    v.appendChild(h("div", { class: "grid-2" },
      card({ icon: "file", tone: "violet", title: t("tg.textCard"), desc: t("tg.textCard.desc"), body: tabs }),
      card({ icon: "eye", tone: "gold", title: t("tg.preview"), desc: t("tg.preview.desc"), body: h("div", { class: "preview-shell" },
        h("div", { class: "preview-top" }, h("i"), h("i"), h("i"), h("span", { text: "indianfestivalwishes.com" })), prevBox) })));

    v.appendChild(card({ icon: "globe", title: t("tg.pages"), desc: t("tg.pages.desc"), body: pageChips(t("tg.pages.legend"), T.pages, true) }));
    paintPrev();
  }

  /* -------------------------------------------------------------- patti */

  var tickerEl = null;
  function renderPatti() {
    var v = clear(viewEl("patti"));
    var A = S.announcement;
    tickerEl = h("div", { class: "ticker", "data-ud": "" });
    var prevNote = h("p", { class: "hint preview-note" });

    function paintTicker() {
      var L = ui.lang.an || "hi";
      var text = ((A.text || {})[L] || "").trim();
      clear(tickerEl);
      tickerEl.className = "ticker";
      if (!A.enabled) {
        tickerEl.classList.add("is-static", "empty-state");
        tickerEl.textContent = t("patti.off");
        prevNote.textContent = t("patti.off.note");
        return;
      }
      if (!text) {
        tickerEl.classList.add("is-static", "empty-state");
        tickerEl.textContent = t("patti.empty", { lang: langName(L) });
        prevNote.textContent = "";
        return;
      }
      var still = A.scroll === false || reduceMotion();
      if (still) {
        tickerEl.classList.add("is-static");
        tickerEl.textContent = text;
        prevNote.textContent = t(A.scroll === false ? "patti.still" : "patti.noAnim");
        return;
      }
      prevNote.textContent = t("patti.speedNote", { s: t("speed." + (SPEEDS[A.speed] ? A.speed : "medium")) }) + (A.url ? " · " + t("patti.linkNote") : "");
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

    var speedSeg = segmented(nextId("speed"), t("patti.speed"), [["slow", t("speed.slow")], ["medium", t("speed.medium")], ["fast", t("speed.fast")]], A.speed || "medium", function (val) { A.speed = val; paintTicker(); });

    v.appendChild(card({
      icon: "megaphone", title: t("patti.card"), desc: t("patti.card.desc"),
      body: [
        switchRow(t("patti.show"), t("patti.show.desc"), A, "enabled", false, paintTicker),
        switchRow(t("patti.scroll"), t("patti.scroll.desc"), A, "scroll", true, paintTicker),
        h("div", { class: "grid-2" }, speedSeg,
          textField(t("patti.url"), A, "url", { placeholder: "https://...", type: "url", validate: vHttps, onInput: paintTicker }))
      ]
    }));

    function filled(L) { return !!(A.text || {})[L]; }
    var tabs = langTabs("an", function (L, panel) {
      var f = textField(t("patti.text", { lang: langName(L) }), A.text, L, { spell: true, placeholder: t("patti.text.ph"), onInput: function () { paintTicker(); tabs && tabs.refreshDots(); } });
      panel.appendChild(f);
      requestAnimationFrame(paintTicker);
    }, filled);

    v.appendChild(card({ icon: "file", tone: "violet", title: t("patti.textCard"), desc: t("patti.textCard.desc"), body: [tabs,
      h("div", { class: "preview-block" }, h("span", { class: "label" }, t("patti.live")),
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
    v.appendChild(h("div", { class: "note warn ads-note" }, icon("alert"), h("span", { text: t("ads.note") })));
    v.appendChild(card({
      icon: "chart", title: t("ads.adsense"), desc: t("ads.adsense.desc"),
      body: h("div", { class: "stack" },
        textField(t("ads.pub"), D, "adsenseClient", { placeholder: "ca-pub-1234567890123456", validate: vAdsense }),
        h("div", { class: "grid-2" },
          textField(t("ads.slotTop"), D, "slotTop", { placeholder: "1234567890", inputmode: "numeric", validate: vSlot }),
          textField(t("ads.slotMid"), D, "slotMiddle", { placeholder: "1234567890", inputmode: "numeric", validate: vSlot })))
    }));
    v.appendChild(card({
      icon: "globe", tone: "gold", title: t("ads.ga"), desc: t("ads.ga.desc"),
      body: textField(t("ads.gaId"), D, "gaId", { placeholder: "G-XXXXXXXXXX", validate: vGa })
    }));
  }

  /* ------------------------------------------------------------- wishes */

  function renderWishes() {
    var v = clear(viewEl("wishes"));
    var W = S.custom.wishes, TH = S.custom.thoughts;
    if (!OCC[ui.wOcc]) ui.wOcc = "navratri";

    var ta = h("textarea", { id: nextId("cw"), spellcheck: "true", autocomplete: "off", placeholder: t("wish.ph") });
    var counter = h("div", { class: "counter", "aria-live": "polite" });
    var combos = h("div", { class: "combos" });
    var relField;

    function current() { return ((W[ui.wLang] || {})[ui.wOcc] || {})[ui.wRel] || []; }
    function paintCount() {
      var ls = lines(ta.value);
      var long = ls.filter(function (x) { return x.length > 160; }).length;
      clear(counter);
      counter.appendChild(h("span", { text: tn("wish.count", ls.length) }));
      if (long) counter.appendChild(h("span", { class: "warn", text: tn("wish.long", long) }));
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
              var area = viewEl("wishes").querySelector("textarea"); if (area) area.focus();
            } } }, h("span", { text: langName(l[0]) + " · " + pageName(o) + " · " + relName(r) }), h("b", { text: String(n) })));
          });
        });
      });
      if (!any) combos.appendChild(h("p", { class: "hint", text: t("wish.noneYet") }));
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

    function relOpts() { return OCC[ui.wOcc][1].map(function (r) { return [r, relName(r)]; }); }
    var langOpts = LANGS.map(function (l) { return [l[0], langName(l[0])]; });
    var langSel = select(t("wish.lang"), langOpts, ui.wLang, function (val) { ui.wLang = val; show(); });
    var occSel = select(t("wish.occ"), OCCASIONS.map(function (o) { return [o[0], pageName(o[0])]; }), ui.wOcc, function (val) {
      ui.wOcc = val;
      if (OCC[val][1].indexOf(ui.wRel) < 0) ui.wRel = "all";
      var s = relField._select;
      clear(s);
      relOpts().forEach(function (o) { s.appendChild(h("option", { value: o[0], text: o[1] })); });
      s.value = ui.wRel;
      show();
    });
    if (OCC[ui.wOcc][1].indexOf(ui.wRel) < 0) ui.wRel = "all";
    relField = select(t("wish.rel"), relOpts(), ui.wRel, function (val) { ui.wRel = val; show(); });

    var taField = h("div", { class: "field" }, h("label", { for: ta.id, text: t("wish.field") }), ta, counter);
    v.appendChild(card({
      icon: "message", title: t("wish.card"), desc: t("wish.card.desc"),
      body: h("div", { class: "stack" }, h("div", { class: "grid-3" }, langSel, occSel, relField), taField)
    }));
    v.appendChild(card({ icon: "sparkle", tone: "gold", title: t("wish.added"), desc: t("wish.added.desc"), body: combos }));

    // thoughts
    var tt = h("textarea", { id: nextId("th"), spellcheck: "true", autocomplete: "off", placeholder: t("th.ph") });
    var tcount = h("div", { class: "counter", "aria-live": "polite" });
    function showT() { tt.value = (TH[ui.tLang] || []).join("\n"); paintT(); }
    function paintT() { clear(tcount); tcount.appendChild(h("span", { text: tn("th.count", lines(tt.value).length) })); }
    tt.addEventListener("input", function () { TH[ui.tLang] = lines(tt.value); paintT(); changed(); });
    var tLang = select(t("wish.lang"), langOpts, ui.tLang, function (val) { ui.tLang = val; showT(); });
    v.appendChild(card({
      icon: "sparkle", tone: "violet", title: t("th.card"), desc: t("th.card.desc"),
      body: h("div", { class: "stack" }, tLang, h("div", { class: "field" }, h("label", { for: tt.id, text: t("th.field") }), tt, tcount))
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
    if (!backups) { backupListEl.appendChild(h("p", { class: "hint", text: t("bk.loading") })); return; }
    if (!backups.length) {
      backupListEl.appendChild(h("div", { class: "empty" }, icon("database"), h("strong", { text: t("bk.empty") }), h("p", { text: t("bk.empty.hint") })));
      return;
    }
    var list = showAllBackups ? backups : backups.slice(0, 8);
    var box = h("div", { class: "blist" });
    list.forEach(function (b, i) {
      var label = fmtDate(b.date);
      box.appendChild(h("div", { class: "bitem" },
        h("span", { class: "b-ic" }, icon("file")),
        h("span", { class: "b-text" }, h("strong", { text: label }), h("small", { text: (i === 0 ? t("bk.latest") + " · " : "") + ago(new Date(b.date).getTime()) + " · " + fmtSize(b.size) })),
        h("span", { class: "b-act" },
          h("button", { class: "icon-btn", type: "button", "aria-label": t("bk.downloadOf", { label: label }), title: t("bk.download"), on: { click: function () { downloadBackup(b.name); } } }, icon("download")),
          h("button", { class: "btn btn-ghost btn-sm", type: "button", "aria-label": t("bk.restoreOf", { label: label }), on: { click: function () { restoreBackup(b, label); } } }, icon("restore"), h("span", { class: "hide-xs", text: t("bk.restore") })))));
    });
    backupListEl.appendChild(box);
    if (backups.length > 8) {
      backupListEl.appendChild(h("div", { class: "more-row" }, h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () { showAllBackups = !showAllBackups; paintBackups(); } } },
        icon(showAllBackups ? "arrowUp" : "chevDown"), showAllBackups ? t("bk.less") : t("bk.all", { n: backups.length }))));
    }
  }

  function downloadBackup(name) {
    api("GET", "/api/backups/" + encodeURIComponent(name)).then(function (data) {
      saveFile(JSON.stringify(data, null, 2), name);
    }).catch(function (e) { if (e.status !== 401) toast(t("bk.download.fail", { msg: e.message }), "err"); });
  }

  function restoreBackup(b, label) {
    ask({ title: t("bk.restore.title"), text: t("bk.restore.text", { label: label }) + (isDirty() ? " " + t("bk.restore.dirty") : ""), ok: t("bk.restore.ok"), icon: "restore" })
      .then(function (yes) {
        if (!yes) return;
        return api("POST", "/api/backups/" + encodeURIComponent(b.name) + "/restore", {}).then(function () {
          return loadSettings();
        }).then(function () {
          changed();
          toast(t("bk.restore.done"), "ok");
        }).catch(function (e) { if (e.status !== 401) toast(t("bk.restore.fail", { msg: e.message }), "err"); });
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
      icon: "database", title: t("bk.card"), desc: t("bk.card.desc"),
      side: h("button", { class: "btn btn-ghost btn-sm", type: "button", on: { click: function () { loadBackups().then(function () { toast(t("bk.refresh.done"), "info"); }); } } }, icon("restore"), t("bk.refresh")),
      body: backupListEl
    }));
    paintBackups();

    var fileInp = h("input", { type: "file", accept: "application/json,.json", "aria-label": t("bk.pick") });
    fileInp.addEventListener("change", function () {
      var f = fileInp.files && fileInp.files[0];
      fileInp.value = "";
      if (!f) return;
      if (f.size > 1024 * 1024) { toast(t("bk.tooBig"), "err"); return; }
      f.text().then(function (txt) {
        var d = JSON.parse(txt);
        if (!d || typeof d !== "object" || Array.isArray(d) || !d.affiliate || !d.telegram) throw new Error("bad");
        var ver = S.version;
        S = ensure(d);
        S.version = ver;
        renderAll();
        changed();
        toast(t("bk.loaded"), "info");
      }).catch(function () { toast(t("bk.bad"), "err"); });
    });

    v.appendChild(card({
      icon: "download", tone: "gold", title: t("bk.io"), desc: t("bk.io.desc"),
      body: h("div", { class: "row-actions" },
        h("button", { class: "btn btn-ghost", type: "button", on: { click: function () {
          saveFile(JSON.stringify(S, null, 2) + "\n", "site-settings-" + new Date().toISOString().slice(0, 10) + ".json");
          toast(t("bk.io.done"), "ok");
        } } }, icon("download"), t("bk.io.down")),
        h("span", { class: "btn btn-ghost file-btn" }, icon("upload"), t("bk.io.up"), fileInp))
    }));
  }

  /* ------------------------------------------------------------ account */

  function renderAccount() {
    var v = clear(viewEl("account"));
    var pw = pwState;
    function pwField(label, key, ac) {
      var f = textField(label, pw, key, { type: "password", raw: true });
      f._input.setAttribute("autocomplete", ac);
      return f;
    }
    var fCur = pwField(t("acc.cur"), "cur", "current-password");
    var fNext = pwField(t("acc.next"), "next", "new-password");
    var fAgain = pwField(t("acc.again"), "again", "new-password");
    var meter = h("div", { class: "pw-meter", "aria-hidden": "true" }, h("i"));
    fNext.insertBefore(meter, fNext.querySelector(".field-err"));
    fNext._input.addEventListener("input", paintMeter);
    if (pw.next) paintMeter();
    function paintMeter() {
      var val = pw.next, s = 0;
      if (val.length >= 10) s++;
      if (val.length >= 14) s++;
      if (/[^A-Za-z]/.test(val)) s++;
      if (/[a-z]/.test(val) && /[A-Z]/.test(val)) s++;
      var bar = meter.firstChild;
      bar.style.width = Math.max(8, s * 25) + "%";
      bar.style.background = s >= 3 ? "var(--ok)" : s === 2 ? "var(--marigold)" : "var(--err)";
    }
    // password fields should not mark settings dirty
    [fCur, fNext, fAgain].forEach(function (f) { f._input.addEventListener("input", function (e) { e.stopPropagation(); }); });

    var btn = h("button", { class: "btn btn-primary", type: "submit" }, h("span", { class: "btn-label", text: t("acc.change") }), h("span", { class: "spinner", "aria-hidden": "true" }));
    var form = h("form", { class: "stack", novalidate: true }, h("input", { type: "text", name: "username", autocomplete: "username", value: (ME && ME.user) || "", hidden: true, "aria-hidden": "true", tabindex: "-1" }),
      fCur, h("div", { class: "grid-2" }, fNext, fAgain), h("div", { class: "row-actions" }, btn));
    form.addEventListener("submit", function (e) {
      e.preventDefault();
      if (!pw.cur) { toast(t("acc.needCur"), "err"); fCur._input.focus(); return; }
      if (pw.next.length < 10) { toast(t("acc.short"), "err"); fNext._input.focus(); return; }
      if (pw.next !== pw.again) { toast(t("acc.mismatch"), "err"); fAgain._input.focus(); return; }
      btn.classList.add("is-busy"); btn.disabled = true;
      api("POST", "/api/password", { current: pw.cur, next: pw.next }, { allow401: true }).then(function () {
        [fCur, fNext, fAgain].forEach(function (f) { f._input.value = ""; });
        pw.cur = pw.next = pw.again = "";
        meter.firstChild.style.width = "0";
        toast(t("acc.done"), "ok");
      }).catch(function (err) {
        toast(err.status === 403 ? t("acc.wrongCur") : err.status === 401 ? t("session.expired") : t("acc.fail", { msg: err.message }), "err");
        if (err.status === 401) sessionExpired();
      }).then(function () { btn.classList.remove("is-busy"); btn.disabled = false; });
    });

    v.appendChild(card({ icon: "key", title: t("acc.change"), desc: t("acc.card.desc"), body: form }));

    var expTxt = ME && ME.exp ? fmtDate(ME.exp) : "–";
    v.appendChild(card({
      icon: "user", tone: "violet", title: t("acc.login"), desc: t("acc.login.desc"),
      body: h("div", { class: "stack" },
        h("div", { class: "note info" }, icon("info"), h("span", null,
          t("acc.user", { user: "" }), h("span", { class: "ud", text: (ME && ME.user) || "admin" }),
          " · " + t("acc.exp", { exp: expTxt }) + (ME && ME.customPassword ? " · " + t("acc.custom") : ""))),
        h("div", { class: "row-actions" }, h("button", { class: "btn btn-danger", type: "button", on: { click: function () { $("btn-logout").click(); } } }, icon("logout"), t("logout"))))
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
  /* ======================================================= UI language */

  // [data-i18n] -> text, [data-i18n-aria] -> aria-label (static markup in index.html)
  function applyStatic() {
    document.querySelectorAll("[data-i18n]").forEach(function (n) { n.textContent = t(n.getAttribute("data-i18n")); });
    document.querySelectorAll("[data-i18n-aria]").forEach(function (n) { n.setAttribute("aria-label", t(n.getAttribute("data-i18n-aria"))); });
  }

  // हिं / ગુ / EN segmented control; one per .lang-slot (login card, sidebar, mobile top bar)
  function langSwitch(where) {
    var g = h("div", { class: "lang-switch", role: "group", "aria-label": t("lang.switch") });
    UI_LANGS.forEach(function (l) {
      g.appendChild(h("button", {
        class: "ls-btn", type: "button", lang: l[0], "data-setlang": l[0], "aria-label": l[2], title: l[2],
        "aria-pressed": l[0] === LANG ? "true" : "false",
        on: { click: function () { setLang(l[0], where); } }
      }, l[1]));
    });
    return g;
  }
  function mountSwitches() {
    document.querySelectorAll(".lang-slot").forEach(function (slot) { clear(slot).appendChild(langSwitch(slot.getAttribute("data-ls"))); });
  }

  function applyLang() {
    document.documentElement.lang = LANG;
    applyStatic();
    mountSwitches();
    var eye = $("lg-eye");
    eye.setAttribute("aria-label", t($("lg-pass").type === "password" ? "login.show" : "login.hide"));
    paintLoginMsg();
    buildNav();
    refreshNavBadges();
    if (!$("app").hidden) {
      // everything re-renders from S (the working copy), so unsaved edits survive
      var y = window.scrollY;
      if (S) renderAll();
      go(view, true);
      changed();
      window.scrollTo(0, y);
    } else {
      document.title = t("login.docTitle") + " | Indian Festival Wishes";
    }
  }

  function setLang(code, where) {
    if (!I18N[code]) return;
    LANG = code;
    try { localStorage.setItem(LANG_KEY, code); } catch (e) { /* storage blocked */ }
    applyLang();
    if (where) {
      var b = document.querySelector('.lang-slot[data-ls="' + where + '"] [data-setlang="' + code + '"]');
      if (b) b.focus();
    }
  }

  hydrateIcons();
  applyLang();

  api("GET", "/api/me", undefined, { allow401: true }).then(function (me) {
    ME = me;
    return enterApp();
  }).catch(function (err) {
    var st = err.status;
    showLogin(st && st !== 401 ? function () { return t("boot.serverErr", { n: st }); } : st === 0 ? function () { return t("net.err"); } : "", st === 401 ? null : undefined);
  });
})();
