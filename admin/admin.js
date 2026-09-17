(function () {
  "use strict";
  var FILE = "static/site-settings.json";
  var LANGS = [["hi", "हिंदी"], ["gu", "ગુજરાતી"], ["en", "English"]];
  var PAGES = [
    ["home", "Home"], ["navratri", "Navratri page"], ["navratri-day", "Navratri ke 9 din"], ["recipes", "Vrat recipes"],
    ["garba", "Garba"], ["birthday", "Birthday"], ["anniversary", "Anniversary"], ["wedding", "Wedding"],
    ["engagement", "Engagement"], ["good-morning", "Good Morning"], ["info", "About/Contact wagairah"]
  ];
  var OCCASIONS = {
    "navratri": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "birthday": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "anniversary": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"],
    "wedding": ["all", "friend", "family", "sibling", "business", "devotional"],
    "engagement": ["all", "friend", "family", "sibling", "business", "devotional"],
    "good-morning": ["all", "friend", "family", "sibling", "spouse", "business", "devotional"]
  };
  var REL_NAMES = { all: "Sabhi", friend: "Dost", family: "Parivar", sibling: "Bhai/Bahen", spouse: "Pati/Patni", business: "Business/Grahak", devotional: "Bhaktimay" };
  var TABS = [["setup", "1. Jodo"], ["affiliate", "2. Products"], ["telegram", "3. Telegram"], ["announce", "4. Patti"], ["ads", "5. Ads"], ["wishes", "6. Wishes"], ["backup", "7. Backup"]];

  var S = null;        // settings object
  var sha = null;      // GitHub file sha
  var canSave = false;

  function $(id) { return document.getElementById(id); }
  function el(tag, attrs, text) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    if (text != null) n.textContent = text;
    return n;
  }
  function msg(text, kind) { var m = $("msg"); m.textContent = text; m.className = "msg " + (kind || ""); }
  function dirty(on) { $("dirty").hidden = !on; }

  /* ---------- tabs ---------- */
  TABS.forEach(function (t, i) {
    var b = el("button", { type: "button", role: "tab", "aria-selected": i === 0 ? "true" : "false" }, t[1]);
    b.addEventListener("click", function () {
      document.querySelectorAll("#tabs button").forEach(function (x) { x.setAttribute("aria-selected", x === b ? "true" : "false"); });
      document.querySelectorAll("section.panel").forEach(function (p) { p.hidden = p.getAttribute("data-tab") !== t[0]; });
    });
    $("tabs").appendChild(b);
  });

  /* ---------- UTF-8 base64 ---------- */
  function b64encode(str) {
    var bytes = new TextEncoder().encode(str), bin = "";
    for (var i = 0; i < bytes.length; i += 0x8000) bin += String.fromCharCode.apply(null, bytes.subarray(i, i + 0x8000));
    return btoa(bin);
  }
  function b64decode(b64) {
    var bin = atob(b64.replace(/\s/g, "")), bytes = new Uint8Array(bin.length);
    for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
    return new TextDecoder().decode(bytes);
  }

  /* ---------- GitHub ---------- */
  var saved = {};
  try { saved = JSON.parse(localStorage.getItem("ifw-admin") || "{}"); } catch (e) {}
  if (saved.owner) $("gh-owner").value = saved.owner;
  if (saved.repo) $("gh-repo").value = saved.repo;
  if (saved.branch) $("gh-branch").value = saved.branch;
  if (saved.token) { $("gh-token").value = saved.token; $("gh-remember").checked = true; }

  function cfg() {
    return { owner: $("gh-owner").value.trim(), repo: $("gh-repo").value.trim(), branch: $("gh-branch").value.trim() || "main", token: $("gh-token").value.trim() };
  }
  function api(method, body) {
    var c = cfg();
    var url = "https://api.github.com/repos/" + encodeURIComponent(c.owner) + "/" + encodeURIComponent(c.repo) + "/contents/" + FILE +
      (method === "GET" ? "?ref=" + encodeURIComponent(c.branch) + "&t=" + Date.now() : "");
    return fetch(url, {
      method: method,
      headers: { "Accept": "application/vnd.github+json", "Authorization": "Bearer " + c.token, "X-GitHub-Api-Version": "2022-11-28" },
      body: body ? JSON.stringify(body) : undefined,
      cache: "no-store"
    });
  }
  function remember() {
    var c = cfg();
    var keep = { owner: c.owner, repo: c.repo, branch: c.branch };
    if ($("gh-remember").checked) keep.token = c.token;
    try { localStorage.setItem("ifw-admin", JSON.stringify(keep)); } catch (e) {}
  }

  $("btn-connect").addEventListener("click", connect);
  function connect() {
    var c = cfg();
    if (!c.token) { msg("Token daalo.", "err"); return; }
    remember();
    msg("GitHub se load ho raha hai...");
    api("GET").then(function (r) {
      if (r.status === 404) { sha = null; return fetchLive(); }
      if (r.status === 401 || r.status === 403) throw new Error("Token galat hai ya uske paas permission nahi hai (Contents: Read and write chahiye).");
      if (!r.ok) throw new Error("GitHub error " + r.status);
      return r.json().then(function (j) { sha = j.sha; return JSON.parse(b64decode(j.content)); });
    }).then(function (data) {
      canSave = true;
      load(data);
      msg("Jud gaya. Ab badlav karo aur Save dabao.", "ok");
    }).catch(function (e) { msg(e.message, "err"); });
  }
  function fetchLive() {
    return fetch("../" + FILE + "?t=" + Date.now(), { cache: "no-store" }).then(function (r) {
      if (!r.ok) throw new Error("Site se settings nahi mili.");
      return r.json();
    });
  }
  $("btn-load-live").addEventListener("click", function () {
    fetchLive().then(function (d) { canSave = false; load(d); msg("Sirf dekhne ke liye load hua. Save karne ke liye token se jodo.", "warn"); })
      .catch(function (e) { msg(e.message, "err"); });
  });
  $("btn-forget").addEventListener("click", function () {
    $("gh-token").value = ""; $("gh-remember").checked = false; remember();
    msg("Token is device se hata diya.", "ok");
  });

  function openTab(name) {
    document.querySelectorAll("#tabs button").forEach(function (x, i) { x.setAttribute("aria-selected", TABS[i][0] === name ? "true" : "false"); });
    document.querySelectorAll("section.panel").forEach(function (p) { p.hidden = p.getAttribute("data-tab") !== name; });
  }
  $("btn-save").addEventListener("click", function () {
    if (!S) { msg("Pehle settings load karo: '1. Jodo' tab me token daal ke 'Jodo aur settings load karo' dabao.", "err"); openTab("setup"); return; }
    if (!canSave) { msg("Abhi sirf dekhne wala mode hai. Save ke liye token daal ke 'Jodo aur settings load karo' dabao.", "err"); openTab("setup"); return; }
    var err = validate();
    if (err) { msg(err, "err"); return; }
    var body = { message: "Admin panel: settings update", content: b64encode(JSON.stringify(S, null, 2) + "\n"), branch: cfg().branch };
    if (sha) body.sha = sha;
    $("btn-save").disabled = true;
    $("btn-save").textContent = "⏳ Save ho raha hai...";
    msg("Save ho raha hai...");
    api("PUT", body).then(function (r) {
      if (r.status === 409 || r.status === 422) throw new Error("File beech me badal gayi. Dobara 'Jodo aur load karo' dabao, phir badlav karke save karo.");
      if (!r.ok) throw new Error("Save nahi hua (GitHub error " + r.status + ").");
      return r.json();
    }).then(function (j) {
      sha = j.content.sha;
      dirty(false);
      msg("✓ Save ho gaya! Site par 1-3 minute me dikhega (phone par refresh karna).", "ok");
    }).catch(function (e) { msg(e.message, "err"); })
      .then(function () { $("btn-save").disabled = false; $("btn-save").textContent = "💾 Save karo (site par lagao)"; });
  });

  function validate() {
    var t = S.telegram;
    if (t.enabled && !/^https:\/\/(t\.me|telegram\.me)\/[A-Za-z0-9_+\/-]+$/.test(t.url || "")) return "Telegram link sahi nahi hai. https://t.me/channelname jaisa hona chahiye.";
    if (S.ads.adsenseClient && !/^ca-pub-\d{10,20}$/.test(S.ads.adsenseClient)) return "AdSense ID ca-pub- se shuru honi chahiye.";
    if (S.ads.gaId && !/^G-[A-Z0-9]{4,15}$/.test(S.ads.gaId)) return "Analytics ID G- se shuru honi chahiye.";
    for (var i = 0; i < S.affiliate.products.length; i++) {
      var p = S.affiliate.products[i];
      if (p.url && !/^https:\/\//.test(p.url)) return "Product " + (i + 1) + ": direct link https:// se shuru hona chahiye.";
      if (p.image && !/^https:\/\//.test(p.image)) return "Product " + (i + 1) + ": image link https:// se shuru hona chahiye.";
    }
    return "";
  }

  /* ---------- defaults ---------- */
  function norm(d) {
    d = d || {};
    d.version = 1;
    d.affiliate = d.affiliate || {};
    d.affiliate.products = Array.isArray(d.affiliate.products) ? d.affiliate.products : [];
    d.affiliate.amazonTag = d.affiliate.amazonTag || "";
    d.affiliate.maxPerSlot = d.affiliate.maxPerSlot || 4;
    d.telegram = d.telegram || {};
    ["title", "text", "button"].forEach(function (k) { d.telegram[k] = d.telegram[k] || {}; });
    d.telegram.pages = d.telegram.pages || ["all"];
    d.announcement = d.announcement || { text: {} };
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

  /* ---------- binding helpers ---------- */
  function bindText(id, obj, key) {
    var n = $(id);
    n.value = obj[key] || "";
    n.oninput = function () { obj[key] = n.value.trim(); dirty(true); };
  }
  function bindCheck(id, obj, key, def) {
    var n = $(id);
    n.checked = obj[key] == null ? def : !!obj[key];
    n.onchange = function () { obj[key] = n.checked; dirty(true); };
  }
  function langInputs(container, obj, key, label, area) {
    LANGS.forEach(function (l) {
      var id = container.id + "-" + key + "-" + l[0];
      container.appendChild(el("label", { for: id }, label + " (" + l[1] + ")"));
      var inp = el(area ? "textarea" : "input", area ? { id: id, rows: "2" } : { id: id, type: "text" });
      if (area) inp.style.minHeight = "60px";
      inp.value = (obj[key] || {})[l[0]] || "";
      inp.oninput = function () { obj[key] = obj[key] || {}; obj[key][l[0]] = inp.value; dirty(true); };
      container.appendChild(inp);
    });
  }
  function pageChips(container, list, withAll) {
    container.innerHTML = "";
    var opts = (withAll ? [["all", "Sabhi pages"]] : []).concat(PAGES);
    opts.forEach(function (pg) {
      var lab = el("label"), cb = el("input", { type: "checkbox" });
      cb.checked = list.indexOf(pg[0]) >= 0;
      cb.onchange = function () {
        var i = list.indexOf(pg[0]);
        if (cb.checked && i < 0) list.push(pg[0]);
        if (!cb.checked && i >= 0) list.splice(i, 1);
        dirty(true);
      };
      lab.appendChild(cb); lab.appendChild(document.createTextNode(pg[1]));
      container.appendChild(lab);
    });
  }

  /* ---------- load into forms ---------- */
  function load(d) {
    S = norm(d);
    document.body.classList.remove("not-loaded");
    $("need-load").hidden = true;
    dirty(false);
    // affiliate
    bindText("aff-tag", S.affiliate, "amazonTag");
    var mx = $("aff-max"); mx.value = S.affiliate.maxPerSlot;
    mx.oninput = function () { S.affiliate.maxPerSlot = Math.min(8, Math.max(1, parseInt(mx.value, 10) || 4)); dirty(true); };
    renderProducts();
    // telegram
    var T = S.telegram;
    bindCheck("tg-enabled", T, "enabled", false);
    bindText("tg-url", T, "url");
    bindCheck("tg-inline", T, "inline", true);
    bindCheck("tg-sticky", T, "sticky", true);
    pageChips($("tg-pages"), T.pages, true);
    var tt = $("tg-texts"); tt.innerHTML = "";
    langInputs(tt, T, "title", "Heading");
    langInputs(tt, T, "text", "Chhota text", true);
    langInputs(tt, T, "button", "Button ka text");
    // announcement
    bindCheck("an-enabled", S.announcement, "enabled", false);
    bindText("an-url", S.announcement, "url");
    bindCheck("an-scroll", S.announcement, "scroll", true);
    var sp = $("an-speed");
    sp.value = S.announcement.speed || "medium";
    sp.onchange = function () { S.announcement.speed = sp.value; dirty(true); };
    var at = $("an-texts"); at.innerHTML = "";
    langInputs(at, S.announcement, "text", "Patti ka text");
    // ads
    bindText("ad-client", S.ads, "adsenseClient");
    bindText("ad-top", S.ads, "slotTop");
    bindText("ad-mid", S.ads, "slotMiddle");
    bindText("ga-id", S.ads, "gaId");
    // wishes
    setupWishes();
  }

  function renderProducts() {
    var box = $("products");
    box.innerHTML = "";
    var list = S.affiliate.products;
    list.forEach(function (p, i) {
      p.title = p.title || {};
      p.pages = p.pages || [];
      var card = el("div", { class: "product" + (p.enabled === false ? " off" : "") });
      var head = el("div", { class: "product-head" });
      head.appendChild(el("strong", null, (i + 1) + ". " + (p.title.hi || p.title.en || "Naya product")));
      var btns = el("div", { class: "actions" });
      btns.style.marginTop = "0";
      function btn(label, cls, fn) { var b = el("button", { type: "button", class: "btn small " + cls }, label); b.onclick = fn; btns.appendChild(b); }
      btn("↑", "ghost", function () { if (i > 0) { list.splice(i - 1, 0, list.splice(i, 1)[0]); dirty(true); renderProducts(); } });
      btn("↓", "ghost", function () { if (i < list.length - 1) { list.splice(i + 1, 0, list.splice(i, 1)[0]); dirty(true); renderProducts(); } });
      btn("Hatao", "danger", function () { if (confirm("Ye product hata dein?")) { list.splice(i, 1); dirty(true); renderProducts(); } });
      head.appendChild(btns);
      card.appendChild(head);

      var on = el("label", { class: "check" }), cb = el("input", { type: "checkbox" });
      cb.checked = p.enabled !== false;
      cb.onchange = function () { p.enabled = cb.checked; card.className = "product" + (cb.checked ? "" : " off"); dirty(true); };
      on.appendChild(cb); on.appendChild(document.createTextNode("Site par dikhao"));
      card.appendChild(on);

      var grid = el("div", { class: "row" });
      function field(label, key, ph, obj) {
        obj = obj || p;
        var wrap = el("div"), id = "p" + i + "-" + key + (obj === p ? "" : "-t");
        wrap.appendChild(el("label", { for: id }, label));
        var inp = el("input", { id: id, type: "text", placeholder: ph || "" });
        inp.value = obj[key] || "";
        inp.oninput = function () { obj[key] = inp.value.trim(); dirty(true); };
        wrap.appendChild(inp);
        grid.appendChild(wrap);
      }
      field("Naam (हिंदी)", "hi", "", p.title);
      field("Naam (ગુજરાતી)", "gu", "", p.title);
      field("Naam (English)", "en", "", p.title);
      field("Amazon search shabd", "search", "jaise: chaniya choli");
      field("Direct link (optional)", "url", "https://amzn.to/...");
      field("Keemat (optional)", "price", "₹499 se");
      field("Store ka naam", "store", "Amazon");
      field("Photo link (optional)", "image", "https://...");
      card.appendChild(grid);
      card.appendChild(el("label", null, "Kin pages par dikhe"));
      var chips = el("div", { class: "chips" });
      pageChips(chips, p.pages, false);
      card.appendChild(chips);
      box.appendChild(card);
    });
  }
  $("btn-add-product").addEventListener("click", function () {
    if (!S) { msg("Pehle settings load karo.", "err"); return; }
    S.affiliate.products.push({ enabled: true, pages: [], store: "Amazon", search: "", url: "", price: "", image: "", title: { hi: "", gu: "", en: "" } });
    dirty(true);
    renderProducts();
    $("products").lastChild.scrollIntoView({ behavior: "smooth" });
  });

  function setupWishes() {
    var ls = $("cw-lang"), os = $("cw-occ"), rs = $("cw-rel"), ta = $("cw-text");
    var tl = $("th-lang"), tt = $("th-text");
    [ls, tl].forEach(function (s) {
      s.innerHTML = "";
      LANGS.forEach(function (l) { s.appendChild(el("option", { value: l[0] }, l[1])); });
    });
    os.innerHTML = "";
    Object.keys(OCCASIONS).forEach(function (o) { os.appendChild(el("option", { value: o }, o)); });
    function fillRels() {
      var cur = rs.value;
      rs.innerHTML = "";
      OCCASIONS[os.value].forEach(function (r) { rs.appendChild(el("option", { value: r }, REL_NAMES[r])); });
      if (OCCASIONS[os.value].indexOf(cur) >= 0) rs.value = cur;
    }
    function showWishes() {
      var w = S.custom.wishes[ls.value][os.value] || {};
      ta.value = (w[rs.value] || []).join("\n");
    }
    ls.onchange = showWishes;
    os.onchange = function () { fillRels(); showWishes(); };
    rs.onchange = showWishes;
    ta.oninput = function () {
      var byOcc = S.custom.wishes[ls.value][os.value] = S.custom.wishes[ls.value][os.value] || {};
      byOcc[rs.value] = ta.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean);
      dirty(true);
    };
    fillRels(); showWishes();
    function showThoughts() { tt.value = (S.custom.thoughts[tl.value] || []).join("\n"); }
    tl.onchange = showThoughts;
    tt.oninput = function () {
      S.custom.thoughts[tl.value] = tt.value.split("\n").map(function (x) { return x.trim(); }).filter(Boolean);
      dirty(true);
    };
    showThoughts();
  }

  /* ---------- backup ---------- */
  $("btn-download").addEventListener("click", function () {
    if (!S) { msg("Pehle settings load karo.", "err"); return; }
    var blob = new Blob([JSON.stringify(S, null, 2)], { type: "application/json" });
    var a = el("a", { href: URL.createObjectURL(blob), download: "site-settings-backup-" + new Date().toISOString().slice(0, 10) + ".json" });
    document.body.appendChild(a); a.click(); a.remove();
  });
  $("file-restore").addEventListener("change", function (e) {
    var f = e.target.files[0];
    if (!f) return;
    f.text().then(function (t) {
      var d = JSON.parse(t);
      load(d);
      dirty(true);
      msg("Backup load ho gaya. Site par lagane ke liye Save dabao.", "warn");
    }).catch(function () { msg("Ye sahi backup file nahi hai.", "err"); });
  });

  if (saved.token) connect();

  window.addEventListener("beforeunload", function (e) {
    if (!$("dirty").hidden) { e.preventDefault(); e.returnValue = ""; }
  });
})();
