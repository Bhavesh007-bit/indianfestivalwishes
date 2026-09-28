/* Indian Festival Wishes — admin console v8
   Login: the GitHub token is encrypted on THIS device with a password
   (PBKDF2-SHA256 + AES-GCM). The password never leaves the browser and
   nothing is stored on a server. Without the password the stored token
   cannot be read, and without the token nothing can be saved. */
(function () {
  "use strict";

  var FILE = "static/site-settings.json";
  var VAULT = "ifw-vault";
  var IDLE_MIN = 30;

  var LANGS = [["hi", "हिंदी"], ["gu", "ગુજરાતી"], ["en", "English"]];
  var PAGES = [
    ["home", "Home"], ["navratri", "Navratri"], ["navratri-day", "Navratri ke 9 din"],
    ["recipes", "Vrat recipes"], ["garba", "Garba"], ["birthday", "Birthday"],
    ["anniversary", "Anniversary"], ["wedding", "Wedding"], ["engagement", "Engagement"],
    ["good-morning", "Good Morning"], ["info", "About/Contact"]
  ];
  var OCCASIONS = {
    "navratri": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "birthday": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "anniversary": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "wedding": ["all", "friend", "family", "sibling", "business", "devotional"],
    "engagement": ["all", "friend", "family", "sibling", "business", "devotional"],
    "good-morning": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"]
  };
  var OCC_NAMES = { "navratri": "Navratri", "birthday": "Birthday", "anniversary": "Anniversary", "wedding": "Wedding", "engagement": "Engagement", "good-morning": "Good Morning" };
  var RELS = { all: "Sabhi", friend: "Dost", family: "Parivar", sibling: "Bhai/Bahen", spouse: "Pati/Patni", business: "Business/Grahak", devotional: "Bhaktimay" };

  var ICON = {
    home: '<path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5"/>',
    products: '<path d="M4 8h16l-1.2 12H5.2z"/><path d="M9 8V6a3 3 0 0 1 6 0v2"/>',
    telegram: '<path d="M21 4 3 11l6 2 2 6 3-4 5 4z"/>',
    announce: '<path d="M4 10v4h4l6 4V6l-6 4z"/><path d="M18 9a4 4 0 0 1 0 6"/>',
    ads: '<rect x="3" y="4" width="18" height="14" rx="2"/><path d="M8 20h8"/><path d="M7 12l2.5-4 2.5 4 2-2 3 6H7z"/>',
    wishes: '<path d="M21 12a8 8 0 0 1-11.6 7.1L4 21l1.9-5.4A8 8 0 1 1 21 12z"/>',
    account: '<path d="M12 3 4 6v6c0 5 3.4 8.3 8 9 4.6-.7 8-4 8-9V6z"/><path d="m9 12 2 2 4-4"/>'
  };
  var NAV = [
    ["home", "Haalat"], ["products", "Products"], ["telegram", "Telegram"],
    ["announce", "Patti"], ["ads", "Ads"], ["wishes", "Wishes"], ["account", "Backup"]
  ];

  var S = null;            // settings object
  var sha = null;          // github file sha
  var TOKEN = null;        // in memory only
  var CFG = { owner: "Bhavesh007-bit", repo: "indianfestivalwishes", branch: "main" };
  var idleTimer = null;

  /* ---------------- tiny helpers ---------------- */
  function $(id) { return document.getElementById(id); }
  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text != null) n.textContent = text;
    return n;
  }
  function svg(paths, cls) {
    var s = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">' + paths + "</svg>";
    var w = document.createElement("span");
    if (cls) w.className = cls;
    w.innerHTML = s;
    return w.firstChild;
  }
  var toastTimer = null;
  function toast(text, kind) {
    var t = $("toast");
    t.textContent = text;
    t.className = "toast show" + (kind ? " " + kind : "");
    clearTimeout(toastTimer);
    toastTimer = setTimeout(function () { t.className = "toast"; }, kind === "err" ? 7000 : 3800);
  }
  function gateMsg(text, kind) {
    var m = $("gate-msg");
    m.textContent = text || "";
    m.style.color = kind === "err" ? "#A81239" : "";
  }
  var isDirty = false;
  function dirty(on) {
    isDirty = on;
    $("save-dot").className = "dot" + (on ? " dirty" : "");
    $("save-state").textContent = on ? "Save nahi hua" : "Sab save hai";
  }

  /* ---------------- crypto vault ---------------- */
  var enc = new TextEncoder(), dec = new TextDecoder();
  function b64(buf) {
    var b = new Uint8Array(buf), s = "";
    for (var i = 0; i < b.length; i++) s += String.fromCharCode(b[i]);
    return btoa(s);
  }
  function unb64(str) {
    var s = atob(str), b = new Uint8Array(s.length);
    for (var i = 0; i < s.length; i++) b[i] = s.charCodeAt(i);
    return b;
  }
  function deriveKey(password, salt) {
    return crypto.subtle.importKey("raw", enc.encode(password), "PBKDF2", false, ["deriveKey"])
      .then(function (base) {
        return crypto.subtle.deriveKey(
          { name: "PBKDF2", salt: salt, iterations: 250000, hash: "SHA-256" },
          base, { name: "AES-GCM", length: 256 }, false, ["encrypt", "decrypt"]);
      });
  }
  function sealVault(password, token, cfg) {
    var salt = crypto.getRandomValues(new Uint8Array(16));
    var iv = crypto.getRandomValues(new Uint8Array(12));
    return deriveKey(password, salt).then(function (key) {
      return crypto.subtle.encrypt({ name: "AES-GCM", iv: iv }, key, enc.encode(token));
    }).then(function (ct) {
      var v = { v: 1, salt: b64(salt), iv: b64(iv), ct: b64(ct), owner: cfg.owner, repo: cfg.repo, branch: cfg.branch };
      localStorage.setItem(VAULT, JSON.stringify(v));
      return v;
    });
  }
  function openVault(password) {
    var v = readVault();
    if (!v) return Promise.reject(new Error("no-vault"));
    return deriveKey(password, unb64(v.salt)).then(function (key) {
      return crypto.subtle.decrypt({ name: "AES-GCM", iv: unb64(v.iv) }, key, unb64(v.ct));
    }).then(function (pt) { return dec.decode(pt); });
  }
  function readVault() {
    try { return JSON.parse(localStorage.getItem(VAULT) || "null"); } catch (e) { return null; }
  }

  /* ---------------- gate ---------------- */
  function showGate() {
    var v = readVault();
    document.body.classList.remove("is-in");
    $("form-unlock").hidden = !v;
    $("form-setup").hidden = !!v;
    if (v) { CFG = { owner: v.owner || CFG.owner, repo: v.repo || CFG.repo, branch: v.branch || CFG.branch }; }
    gateMsg("");
    setTimeout(function () { (v ? $("pw") : $("su-token")).focus(); }, 60);
  }
  function enterApp() {
    document.body.classList.add("is-in");
    resetIdle();
  }
  function lock() {
    TOKEN = null; S = null; sha = null;
    $("pw").value = "";
    dirty(false);
    showGate();
  }
  function resetIdle() {
    clearTimeout(idleTimer);
    if (!TOKEN) return;
    idleTimer = setTimeout(function () {
      if (isDirty) { resetIdle(); return; }   // never lock away unsaved work
      lock();
      gateMsg("Kaafi der se koi kaam nahi hua, isliye panel lock ho gaya.");
    }, IDLE_MIN * 60000);
  }
  ["click", "keydown", "input"].forEach(function (ev) {
    document.addEventListener(ev, function () { if (TOKEN) resetIdle(); }, true);
  });

  document.querySelectorAll(".pw-toggle").forEach(function (b) {
    b.addEventListener("click", function () {
      var inp = $(b.getAttribute("data-toggle"));
      inp.type = inp.type === "password" ? "text" : "password";
      b.setAttribute("aria-label", inp.type === "password" ? "Password dikhao" : "Password chhupao");
    });
  });
  $("su-pw").addEventListener("input", function () {
    var v = $("su-pw").value, s = 0;
    if (v.length >= 8) s++;
    if (v.length >= 12) s++;
    if (/[^a-zA-Z]/.test(v)) s++;
    if (/[a-z]/.test(v) && /[A-Z]/.test(v)) s++;
    $("pw-meter").className = "meter s" + Math.max(1, s);
  });

  $("form-setup").addEventListener("submit", function (e) {
    e.preventDefault();
    var token = $("su-token").value.trim();
    var pw = $("su-pw").value, pw2 = $("su-pw2").value;
    if (!token) { gateMsg("Token daalo.", "err"); return; }
    if (pw.length < 8) { gateMsg("Password kam se kam 8 akshar ka rakho.", "err"); return; }
    if (pw !== pw2) { gateMsg("Dono password ek jaise nahi hain.", "err"); return; }
    var cfg = {
      owner: $("su-owner").value.trim() || CFG.owner,
      repo: $("su-repo").value.trim() || CFG.repo,
      branch: "main"
    };
    gateMsg("Token check ho raha hai...");
    TOKEN = token; CFG = cfg;
    loadSettings().then(function () {
      return sealVault(pw, token, cfg);
    }).then(function () {
      $("su-token").value = $("su-pw").value = $("su-pw2").value = "";
      enterApp();
      toast("Setup poora. Panel ab password se khulega.", "ok");
    }).catch(function (err) {
      TOKEN = null;
      gateMsg(err.message, "err");
    });
  });

  $("form-unlock").addEventListener("submit", function (e) {
    e.preventDefault();
    var pw = $("pw").value;
    if (!pw) return;
    gateMsg("Khol raha hai...");
    openVault(pw).then(function (token) {
      TOKEN = token;
      return loadSettings();
    }).then(function () {
      $("pw").value = "";
      enterApp();
      toast("Khul gaya. Ab badlav karke Save dabao.", "ok");
    }).catch(function (err) {
      TOKEN = null;
      gateMsg(err && err.message === "no-vault" ? "Is device par koi setup nahi mila." :
        (err && err.name === "OperationError") || !err ? "Password galat hai." : err.message, "err");
    });
  });

  $("btn-reset").addEventListener("click", function () {
    if (!confirm("Is device se token aur password hata dein? Naya token daal ke dobara setup karna hoga. Site par koi asar nahi hoga.")) return;
    localStorage.removeItem(VAULT);
    showGate();
    gateMsg("Hata diya. Ab naye token se setup karo.");
  });
  $("btn-lock").addEventListener("click", function () {
    if (isDirty && !confirm("Kuch badlav save nahi hua hai. Phir bhi lock karein?")) return;
    lock();
  });

  /* ---------------- github ---------------- */
  function api(method, body) {
    var url = "https://api.github.com/repos/" + encodeURIComponent(CFG.owner) + "/" +
      encodeURIComponent(CFG.repo) + "/contents/" + FILE +
      (method === "GET" ? "?ref=" + encodeURIComponent(CFG.branch) + "&t=" + Date.now() : "");
    return fetch(url, {
      method: method, cache: "no-store",
      headers: {
        "Accept": "application/vnd.github+json",
        "Authorization": "Bearer " + TOKEN,
        "X-GitHub-Api-Version": "2022-11-28"
      },
      body: body ? JSON.stringify(body) : undefined
    });
  }
  function ghError(status) {
    if (status === 401) return new Error("Token galat hai ya khatam ho gaya hai.");
    if (status === 403) return new Error("Token ke paas permission nahi hai (Contents: Read and write chahiye).");
    if (status === 404) return new Error("Repository ya file nahi mili. Username aur repository naam dekh lo.");
    return new Error("GitHub se baat nahi ho paayi (error " + status + ").");
  }
  function loadSettings() {
    return api("GET").then(function (r) {
      if (!r.ok) throw ghError(r.status);
      return r.json();
    }).then(function (j) {
      sha = j.sha;
      var txt = dec.decode(unb64(j.content.replace(/\s/g, "")));
      build(JSON.parse(txt));
    });
  }

  function validate() {
    var t = S.telegram;
    if (t.enabled && !/^https:\/\/(t\.me|telegram\.me)\/[A-Za-z0-9_+\/-]+$/.test(t.url || ""))
      return "Telegram link sahi nahi hai. https://t.me/channelname jaisa hona chahiye.";
    if (S.ads.adsenseClient && !/^ca-pub-\d{10,20}$/.test(S.ads.adsenseClient))
      return "AdSense ID ca-pub- se shuru honi chahiye.";
    if (S.ads.gaId && !/^G-[A-Z0-9]{4,15}$/.test(S.ads.gaId))
      return "Analytics ID G- se shuru honi chahiye.";
    for (var i = 0; i < S.affiliate.products.length; i++) {
      var p = S.affiliate.products[i];
      if (p.url && !/^https:\/\//.test(p.url)) return "Product " + (i + 1) + ": link https:// se shuru hona chahiye.";
      if (p.image && !/^https:\/\//.test(p.image)) return "Product " + (i + 1) + ": photo link https:// se shuru hona chahiye.";
    }
    return "";
  }

  $("btn-save").addEventListener("click", function () {
    if (!S || !TOKEN) { toast("Pehle panel kholo.", "err"); return; }
    var err = validate();
    if (err) { toast(err, "err"); return; }
    var btn = $("btn-save");
    btn.disabled = true;
    $("save-state").textContent = "Save ho raha hai...";
    var body = {
      message: "Admin console: settings update",
      content: b64(enc.encode(JSON.stringify(S, null, 2) + "\n")),
      branch: CFG.branch
    };
    if (sha) body.sha = sha;
    api("PUT", body).then(function (r) {
      if (r.status === 409 || r.status === 422)
        throw new Error("File beech me kahin aur se badal gayi. Panel dobara kholo, phir badlav karke save karo.");
      if (!r.ok) throw ghError(r.status);
      return r.json();
    }).then(function (j) {
      sha = j.content.sha;
      dirty(false);
      renderStats();
      toast("Save ho gaya. Site par 1-3 minute me dikhega.", "ok");
    }).catch(function (e) {
      toast(e.message, "err");
      $("save-state").textContent = "Save nahi hua";
    }).then(function () { btn.disabled = false; });
  });

  window.addEventListener("beforeunload", function (e) {
    if (isDirty) { e.preventDefault(); e.returnValue = ""; }
  });

  /* ---------------- nav ---------------- */
  NAV.forEach(function (t, i) {
    var b = el("button", { type: "button", "data-go": t[0], "aria-current": i === 0 ? "true" : "false" });
    b.appendChild(svg(ICON[t[0]]));
    b.appendChild(el("span", null, t[1]));
    b.addEventListener("click", function () { go(t[0]); });
    $("nav").appendChild(b);
  });
  function go(name) {
    document.querySelectorAll("#nav button").forEach(function (b) {
      b.setAttribute("aria-current", b.getAttribute("data-go") === name ? "true" : "false");
    });
    document.querySelectorAll(".page").forEach(function (p) {
      p.classList.toggle("is-on", p.getAttribute("data-page") === name);
    });
    window.scrollTo({ top: 0, behavior: "instant" });
  }

  /* ---------------- settings shape ---------------- */
  function norm(d) {
    d = d || {};
    d.version = 1;
    d.affiliate = d.affiliate || {};
    d.affiliate.products = Array.isArray(d.affiliate.products) ? d.affiliate.products : [];
    d.affiliate.amazonTag = d.affiliate.amazonTag || "";
    d.affiliate.maxPerSlot = d.affiliate.maxPerSlot || 4;
    d.telegram = d.telegram || {};
    ["title", "text", "button"].forEach(function (k) { d.telegram[k] = d.telegram[k] || {}; });
    d.telegram.pages = Array.isArray(d.telegram.pages) ? d.telegram.pages : ["all"];
    d.announcement = d.announcement || {};
    d.announcement.text = d.announcement.text || {};
    d.ads = d.ads || {};
    d.custom = d.custom || {};
    d.custom.thoughts = d.custom.thoughts || {};
    d.custom.wishes = d.custom.wishes || {};
    LANGS.forEach(function (l) {
      d.custom.thoughts[l[0]] = d.custom.thoughts[l[0]] || [];
      d.custom.wishes[l[0]] = d.custom.wishes[l[0]] || {};
    });
    return d;
  }

  /* ---------------- binding ---------------- */
  function bindText(id, obj, key) {
    var n = $(id);
    n.value = obj[key] || "";
    n.oninput = function () { obj[key] = n.value.trim(); dirty(true); };
  }
  function bindSwitch(id, obj, key, def) {
    var n = $(id);
    n.checked = obj[key] == null ? def : !!obj[key];
    n.onchange = function () { obj[key] = n.checked; dirty(true); renderStats(); };
  }
  function langFields(box, obj, key, label, big) {
    LANGS.forEach(function (l) {
      var id = box.id + "-" + key + "-" + l[0];
      var f = el("div", { class: "field" });
      f.appendChild(el("label", { for: id }, label + " — " + l[1]));
      var inp = el(big ? "textarea" : "input", { id: id, autocomplete: "off" });
      if (big) inp.style.minHeight = "72px"; else inp.type = "text";
      inp.value = (obj[key] || {})[l[0]] || "";
      inp.oninput = function () { obj[key] = obj[key] || {}; obj[key][l[0]] = inp.value; dirty(true); };
      f.appendChild(inp);
      box.appendChild(f);
    });
  }
  function pageChips(box, list, withAll) {
    box.innerHTML = "";
    var opts = (withAll ? [["all", "Sabhi pages"]] : []).concat(PAGES);
    opts.forEach(function (pg) {
      var lab = el("label"), cb = el("input", { type: "checkbox" });
      cb.checked = list.indexOf(pg[0]) >= 0;
      lab.classList.toggle("on", cb.checked);
      cb.onchange = function () {
        var i = list.indexOf(pg[0]);
        if (cb.checked && i < 0) list.push(pg[0]);
        if (!cb.checked && i >= 0) list.splice(i, 1);
        lab.classList.toggle("on", cb.checked);
        dirty(true);
      };
      lab.appendChild(cb);
      lab.appendChild(el("span", null, pg[1]));
      box.appendChild(lab);
    });
  }

  /* ---------------- build all sections ---------------- */
  function build(data) {
    S = norm(data);
    dirty(false);

    bindText("aff-tag", S.affiliate, "amazonTag");
    var mx = $("aff-max");
    mx.value = S.affiliate.maxPerSlot;
    mx.oninput = function () { S.affiliate.maxPerSlot = Math.min(8, Math.max(1, parseInt(mx.value, 10) || 4)); dirty(true); };
    renderProducts();

    var T = S.telegram;
    bindSwitch("tg-enabled", T, "enabled", false);
    bindText("tg-url", T, "url");
    bindSwitch("tg-inline", T, "inline", true);
    bindSwitch("tg-sticky", T, "sticky", true);
    pageChips($("tg-pages"), T.pages, true);
    var tt = $("tg-texts"); tt.innerHTML = "";
    langFields(tt, T, "title", "Heading");
    langFields(tt, T, "text", "Chhota text", true);
    langFields(tt, T, "button", "Button");

    bindSwitch("an-enabled", S.announcement, "enabled", false);
    bindSwitch("an-scroll", S.announcement, "scroll", true);
    bindText("an-url", S.announcement, "url");
    var sp = $("an-speed");
    sp.value = S.announcement.speed || "medium";
    sp.onchange = function () { S.announcement.speed = sp.value; dirty(true); };
    var at = $("an-texts"); at.innerHTML = "";
    langFields(at, S.announcement, "text", "Patti ka text");

    bindText("ad-client", S.ads, "adsenseClient");
    bindText("ad-top", S.ads, "slotTop");
    bindText("ad-mid", S.ads, "slotMiddle");
    bindText("ga-id", S.ads, "gaId");

    setupWishes();
    renderStats();
  }

  function renderStats() {
    if (!S) return;
    var box = $("stats");
    box.innerHTML = "";
    var tag = (S.affiliate.amazonTag || "").trim();
    var live = S.affiliate.products.filter(function (p) {
      return p.enabled !== false && (p.pages || []).length && (p.url || (p.search && tag));
    }).length;
    var rows = [
      ["Telegram", S.telegram.enabled ? "Chalu" : "Band", S.telegram.enabled ? "on" : "off"],
      ["Announcement patti", S.announcement.enabled ? "Chalu" : "Band", S.announcement.enabled ? "on" : "off"],
      ["Amazon tracking ID", tag || "Nahi daala", tag ? "on" : "warn"],
      ["Site par dikhte products", String(live), live ? "on" : "warn"],
      ["AdSense", S.ads.adsenseClient ? "Chalu" : "Band", S.ads.adsenseClient ? "on" : "off"],
      ["Analytics", S.ads.gaId ? "Chalu" : "Band", S.ads.gaId ? "on" : "off"]
    ];
    rows.forEach(function (r) {
      var c = el("div", { class: "stat" });
      c.appendChild(el("span", { class: "k" }, r[0]));
      c.appendChild(el("span", { class: "v" }, r[1]));
      c.appendChild(el("span", { class: "pill " + r[2] }, r[2] === "on" ? "Live" : r[2] === "warn" ? "Dhyan do" : "Band"));
      box.appendChild(c);
    });
    var q = $("quick");
    q.innerHTML = "";
    [["products", "Products"], ["telegram", "Telegram"], ["announce", "Patti ka text"], ["wishes", "Wishes jodo"]].forEach(function (t) {
      var b = el("button", { class: "btn ghost", type: "button" }, t[1]);
      b.addEventListener("click", function () { go(t[0]); });
      q.appendChild(b);
    });
  }

  function renderProducts() {
    var box = $("products");
    box.innerHTML = "";
    var list = S.affiliate.products;
    if (!list.length) {
      box.appendChild(el("p", { class: "note info" }, "Abhi koi product nahi hai. Neeche se naya jodo."));
    }
    list.forEach(function (p, i) {
      p.title = p.title || {};
      p.pages = Array.isArray(p.pages) ? p.pages : [];
      var card = el("div", { class: "prod" + (p.enabled === false ? " off" : "") });

      var head = el("div", { class: "prod-head" });
      head.appendChild(el("span", { class: "grab" }, String(i + 1)));

      var sw = el("label", { class: "switch", title: "Site par dikhao" });
      var cb = el("input", { type: "checkbox" });
      cb.checked = p.enabled !== false;
      cb.onchange = function () { p.enabled = cb.checked; card.className = "prod" + (cb.checked ? "" : " off"); dirty(true); renderStats(); };
      sw.appendChild(cb); sw.appendChild(el("i"));
      head.appendChild(sw);

      var nm = el("span", { class: "prod-name" });
      var title = p.title.hi || p.title.en || "Naya product";
      nm.appendChild(document.createTextNode(title));
      var subEl = el("small", null, (p.pages.length ? p.pages.join(", ") : "kisi page par nahi"));
      nm.appendChild(subEl);
      head.appendChild(nm);

      var tools = el("div", { class: "prod-tools" });
      function tool(label, paths, fn) {
        var b = el("button", { class: "btn ghost icon small", type: "button", "aria-label": label, title: label });
        b.appendChild(svg(paths));
        b.addEventListener("click", fn);
        tools.appendChild(b);
        return b;
      }
      var body = el("div", { class: "prod-body", hidden: "" });
      tool("Kholo / band karo", '<path d="m6 9 6 6 6-6"/>', function () { body.hidden = !body.hidden; });
      tool("Upar", '<path d="m6 15 6-6 6 6"/>', function () {
        if (i > 0) { list.splice(i - 1, 0, list.splice(i, 1)[0]); dirty(true); renderProducts(); }
      });
      tool("Neeche", '<path d="m6 9 6 6 6-6"/>', function () {
        if (i < list.length - 1) { list.splice(i + 1, 0, list.splice(i, 1)[0]); dirty(true); renderProducts(); }
      });
      var del = tool("Hatao", '<path d="M4 7h16"/><path d="M9 7V5h6v2"/><path d="M6 7l1 13h10l1-13"/>', function () {
        if (confirm("Ye product hata dein?")) { list.splice(i, 1); dirty(true); renderProducts(); renderStats(); }
      });
      del.classList.remove("ghost"); del.classList.add("danger");
      head.appendChild(tools);
      card.appendChild(head);

      var grid = el("div", { class: "row" });
      function field(label, key, ph, obj, hint) {
        obj = obj || p;
        var wrap = el("div", { class: "field" });
        var id = "p" + i + "-" + key + (obj === p ? "" : "-t");
        wrap.appendChild(el("label", { for: id }, label));
        var inp = el("input", { id: id, type: "text", placeholder: ph || "", autocomplete: "off" });
        inp.value = obj[key] || "";
        inp.oninput = function () {
          obj[key] = inp.value.trim();
          if (obj === p.title && key === "hi") nm.firstChild.nodeValue = inp.value || "Naya product";
          dirty(true);
        };
        wrap.appendChild(inp);
        if (hint) wrap.appendChild(el("p", { class: "hint" }, hint));
        grid.appendChild(wrap);
      }
      field("Naam (हिंदी)", "hi", "", p.title);
      field("Naam (ગુજરાતી)", "gu", "", p.title);
      field("Naam (English)", "en", "", p.title);
      field("Amazon search shabd", "search", "jaise: chaniya choli", null, "Isse apne aap tracking ID wala search link banta hai.");
      field("Direct link", "url", "https://amzn.to/...", null, "Kisi ek product ka link ho to yahan daalo.");
      field("Keemat", "price", "₹499 se");
      field("Store", "store", "Amazon");
      field("Photo link", "image", "https://...");
      body.appendChild(grid);
      body.appendChild(el("label", null, "Kin pages par dikhe"));
      var chips = el("div", { class: "chips" });
      pageChips(chips, p.pages, false);
      chips.addEventListener("change", function () { subEl.textContent = p.pages.length ? p.pages.join(", ") : "kisi page par nahi"; });
      body.appendChild(chips);
      card.appendChild(body);
      box.appendChild(card);
    });
  }
  $("btn-add-product").addEventListener("click", function () {
    if (!S) { toast("Pehle panel kholo.", "err"); return; }
    S.affiliate.products.push({ enabled: true, pages: [], store: "Amazon", search: "", url: "", price: "", image: "", title: { hi: "", gu: "", en: "" } });
    dirty(true);
    renderProducts();
    var last = $("products").lastElementChild;
    last.querySelector(".prod-body").hidden = false;
    last.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  function setupWishes() {
    var ls = $("cw-lang"), os = $("cw-occ"), rs = $("cw-rel"), ta = $("cw-text");
    var tl = $("th-lang"), tt = $("th-text");
    [ls, tl].forEach(function (s) {
      s.innerHTML = "";
      LANGS.forEach(function (l) { s.appendChild(el("option", { value: l[0] }, l[1])); });
    });
    os.innerHTML = "";
    Object.keys(OCCASIONS).forEach(function (o) { os.appendChild(el("option", { value: o }, OCC_NAMES[o])); });
    function fillRels() {
      var cur = rs.value;
      rs.innerHTML = "";
      OCCASIONS[os.value].forEach(function (r) { rs.appendChild(el("option", { value: r }, RELS[r])); });
      if (OCCASIONS[os.value].indexOf(cur) >= 0) rs.value = cur;
    }
    function lines(v) { return v.split("\n").map(function (x) { return x.trim(); }).filter(Boolean); }
    function showWishes() {
      var w = S.custom.wishes[ls.value][os.value] || {};
      ta.value = (w[rs.value] || []).join("\n");
      $("cw-count").textContent = lines(ta.value).length + " wish jodi hui hain";
    }
    ls.onchange = showWishes;
    os.onchange = function () { fillRels(); showWishes(); };
    rs.onchange = showWishes;
    ta.oninput = function () {
      var byOcc = S.custom.wishes[ls.value][os.value] = S.custom.wishes[ls.value][os.value] || {};
      byOcc[rs.value] = lines(ta.value);
      $("cw-count").textContent = byOcc[rs.value].length + " wish jodi hui hain";
      dirty(true);
    };
    fillRels(); showWishes();
    function showThoughts() {
      tt.value = (S.custom.thoughts[tl.value] || []).join("\n");
      $("th-count").textContent = lines(tt.value).length + " suvichar jode hue hain";
    }
    tl.onchange = showThoughts;
    tt.oninput = function () {
      S.custom.thoughts[tl.value] = lines(tt.value);
      $("th-count").textContent = S.custom.thoughts[tl.value].length + " suvichar jode hue hain";
      dirty(true);
    };
    showThoughts();
  }

  /* ---------------- backup / account ---------------- */
  $("btn-download").addEventListener("click", function () {
    if (!S) { toast("Pehle panel kholo.", "err"); return; }
    var blob = new Blob([JSON.stringify(S, null, 2)], { type: "application/json" });
    var a = el("a", { href: URL.createObjectURL(blob), download: "site-settings-" + new Date().toISOString().slice(0, 10) + ".json" });
    document.body.appendChild(a); a.click(); a.remove();
    toast("Backup download ho gaya.", "ok");
  });
  $("file-restore").addEventListener("change", function (e) {
    var f = e.target.files[0];
    if (!f) return;
    f.text().then(function (t) {
      build(JSON.parse(t));
      dirty(true);
      toast("Backup load ho gaya. Site par lagane ke liye Save dabao.");
    }).catch(function () { toast("Ye sahi backup file nahi hai.", "err"); });
    e.target.value = "";
  });

  $("btn-chpw").addEventListener("click", function () {
    var oldPw = $("ch-old").value, np = $("ch-new").value;
    if (np.length < 8) { toast("Naya password kam se kam 8 akshar ka rakho.", "err"); return; }
    openVault(oldPw).then(function (token) {
      return sealVault(np, token, CFG);
    }).then(function () {
      $("ch-old").value = $("ch-new").value = "";
      toast("Password badal gaya.", "ok");
    }).catch(function () { toast("Abhi ka password galat hai.", "err"); });
  });
  $("btn-chtoken").addEventListener("click", function () {
    var nt = $("ch-token").value.trim();
    if (!nt) { toast("Naya token daalo.", "err"); return; }
    var pw = prompt("Pakka karne ke liye apna admin password daalo:");
    if (!pw) return;
    openVault(pw).then(function () {
      return sealVault(pw, nt, CFG);
    }).then(function () {
      TOKEN = nt;
      $("ch-token").value = "";
      return loadSettings();
    }).then(function () { toast("Token badal gaya aur chal raha hai.", "ok"); })
      .catch(function (e) { toast(e && e.message === "no-vault" ? "Setup nahi mila." : "Password galat hai ya naya token nahi chala.", "err"); });
  });
  $("btn-wipe").addEventListener("click", function () {
    if (!confirm("Is device se token aur password hata dein? Site par koi asar nahi hoga.")) return;
    localStorage.removeItem(VAULT);
    lock();
    gateMsg("Is device se hata diya gaya.");
  });

  /* ---------------- start ---------------- */
  if (!window.crypto || !crypto.subtle) {
    gateMsg("Ye browser password lock nahi chala sakta. Chrome ka naya version use karo, aur page https:// se kholo.", "err");
  }
  showGate();
})();
