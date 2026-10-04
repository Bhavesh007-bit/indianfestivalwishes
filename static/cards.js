/* Indian Festival Wishes — card maker v10
   Photo backgrounds + a frosted text panel so text always stays readable.
   Kinds: festival, person, couple, morning (wishes) and invite (invitations, shraddhanjali). */
(function () {
  "use strict";
  var dataEl = document.getElementById("page-data");
  var canvas = document.getElementById("card");
  if (!dataEl || !canvas) return;
  var D = JSON.parse(dataEl.textContent);
  var K = D.card;
  if (!K) return;
  var U = D.ui;
  var ctx = canvas.getContext("2d");
  var W = canvas.width, H = canvas.height;
  var FD = D.fonts.display, FB = D.fonts.body;
  var FDW = D.lang === "gu" ? 700 : 400; // Rozha One ships a single weight
  var DES = K.designs;
  var INVITE = K.kind === "invite";
  var IV = (function () { var sc = document.querySelector('script[src*="cards.js"]'); var m = sc && /[?&]v=([\w-]+)/.exec(sc.src); return m ? "?v=" + m[1] : ""; })();
  var FIELD_KEYS = ["name1", "name2", "dates", "date", "time", "venue", "host", "note", "phone", "map"];
  var FIELD_MAX = { venue: 90, note: 90, host: 90, map: 300, phone: 40 };
  var MAP_RE = /^https:\/\/(maps\.app\.goo\.gl|goo\.gl\/maps|(www\.)?google\.[a-z.]{2,8}\/maps|maps\.google\.[a-z.]{2,8})(\/|\?|$)[^\s<>"`]*$/i;
  function mapOk(u) { return !!u && MAP_RE.test(u); }

  function $(id) { return document.getElementById(id); }
  function fmt(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ""; }); }
  function clean(v, max) { return String(v || "").replace(/[\u0000-\u001F\u007F<>"`]/g, " ").replace(/\s+/g, " ").trim().slice(0, max || 30); }

  /* ---------------- state ---------------- */
  var P = new URLSearchParams(location.search);
  var relKeys = INVITE ? [] : K.rels.map(function (r) { return r[0]; });
  var state = {
    design: Math.min(DES.length - 1, Math.max(0, parseInt(P.get("s"), 10) || 0)),
    rel: relKeys.indexOf(P.get("r")) >= 0 ? P.get("r") : relKeys[0],
    wish: P.get("w") === "c" ? "c" : Math.max(0, parseInt(P.get("w"), 10) || 0),
    custom: clean(P.get("c"), 180),
    type: Math.max(0, parseInt(P.get("ty"), 10) || 0),
    from: clean(P.get("name") || P.get("from")),
    to: clean(P.get("to")),
    n1: clean(P.get("n1")),
    n2: clean(P.get("n2")),
    f: {},
    thought: (function () {
      if (!K.thoughts) return 0;
      var q = parseInt(P.get("t"), 10);
      if (q >= 0) return q % K.thoughts.length;
      var d = new Date(), start = new Date(d.getFullYear(), 0, 0);
      return Math.floor((d - start) / 86400000) % K.thoughts.length;
    })(),
    photoMode: !!K.photoDefault,
    pz: 1, px: 0, py: 0, fs: (P.get("fs") || ""),
    bgImg: null, bgTone: 0.5,
    photo: null,
    page: 1,
    prog: [],
    made: false
  };
  // A link can name its design by id ("d"), which survives cards being added or hidden later.
  var urlD = clean(P.get("d"), 60);
  (function () { var i = DES.map(function (d) { return d.id; }).indexOf(urlD); if (urlD && i >= 0) state.design = i; })();
  FIELD_KEYS.forEach(function (k) { state.f[k] = clean(P.get("f_" + k), FIELD_MAX[k] || 50); });
  if (!mapOk(state.f.map)) state.f.map = "";
  if (K.program) for (var pi = 1; pi <= 6; pi++) {
    var pv = String(P.get("p" + pi) || "").split("~");
    var row = { n: clean(pv[0], 40), w: clean(pv[1], 50), v: clean(pv[2], 60) };
    if (row.n || row.w) state.prog.push(row);
  }
  function hasProgram() { return !!K.program && state.prog.some(function (r) { return r.n || r.w; }); }
  if (K.types && state.type >= K.types.length) state.type = 0;
  var received = !!(state.from || state.to || state.n1 || state.f.name1);
  function wishList() { return INVITE ? K.wordings : (K.wishes[state.rel] || []); }
  if (state.wish !== "c" && state.wish >= wishList().length) state.wish = 0;

  /* ---------------- images ---------------- */
  var cache = {};
  var frame = canvas.parentNode;
  function loadImg(id) {
    var dd = DES.filter(function (d) { return d.id === id; })[0];
    if (dd && dd.url) {
      if (!cache[id]) cache[id] = new Promise(function (res) { var im = new Image(); im.onload = function () { res(im); }; im.onerror = function () { res(null); }; im.src = dd.url; });
      return cache[id];
    }
    if (cache[id]) return cache[id];
    cache[id] = new Promise(function (res) {
      var im = new Image();
      im.decoding = "async";
      im.onload = function () { res(im); };
      im.onerror = function () {
        var t = new Image();
        t.onload = function () { res(t); };
        t.onerror = function () { res(null); };
        t.src = "/static/cards/thumb/" + id + ".webp" + IV;
      };
      im.src = "/static/cards/" + id + ".webp" + IV;
    });
    return cache[id];
  }

  /* ---------------- drawing helpers ---------------- */
  function font(fam, w, s) { return w + " " + s + "px " + fam; }
  function greedy(words, maxW) {
    var lines = [], line = "";
    words.forEach(function (w) {
      var t = line ? line + " " + w : w;
      if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t;
    });
    if (line) lines.push(line);
    return lines;
  }
  // Balanced wrap: keep the greedy line count but narrow the width as far as
  // possible, so lines come out even and no single word is left alone.
  function wrap(text, maxW) {
    var words = String(text).split(" ").filter(Boolean), best = greedy(words, maxW), n = best.length;
    if (n < 2) return best;
    var lo = maxW * 0.45, hi = maxW;
    for (var i = 0; i < 12; i++) {
      var mid = (lo + hi) / 2, t = greedy(words, mid);
      if (t.length <= n) { best = t; hi = mid; } else lo = mid;
    }
    return best;
  }
  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function coverRect(img) {
    var r = Math.max(W / img.width, H / img.height), w = img.width * r, h = img.height * r;
    return [(W - w) / 2, (H - h) / 2, w, h];
  }
  function gold(y0, y1) {
    var g = ctx.createLinearGradient(0, y0, 0, y1);
    g.addColorStop(0, "#FFF6D2"); g.addColorStop(0.45, "#FFD36B"); g.addColorStop(0.75, "#F2A93B"); g.addColorStop(1, "#C9821E");
    return g;
  }
  // title fonts per template style
  var TFONTS = {
    deco: { hi: ["'Yatra One', " + FD, 400], gu: ["'Shrikhand', " + FD, 400], en: ["'Cinzel', serif", 700] },
    script: { hi: ["'Kalam', " + FD, 700], gu: ["'Mogra', " + FD, 400], en: ["'Great Vibes', cursive", 400] },
    classic: { hi: [FD, FDW], gu: [FD, FDW], en: [FD, FDW] }
  };
  var TF = [FD, FDW]; // current title font
  function setTitleFont(style) { var t = (TFONTS[style] || TFONTS.classic)[D.lang] || TFONTS.classic.en; TF = t; }

  function palette(d) {
    if (d.tpl) {
      var c = d.colors, dark = d.tone === "dark";
      return { dark: dark, tpl: true, title: c.title, text: c.text, soft: dark ? "rgba(255,248,236,.85)" : c.text, accent: c.accent, line: c.accent, ribbon: dark ? ["#E0115F", "#B80D4D"] : [c.title, c.title], shadow: dark ? "rgba(0,0,0,.55)" : "rgba(255,255,255,.85)" };
    }
    if (d.tone === "dark") return { dark: true, title: "gold", text: "#FFF8EC", soft: "rgba(255,248,236,.88)", accent: "#FFD36B", line: "rgba(255,211,107,.85)", ribbon: ["#E0115F", "#B80D4D"], shadow: "rgba(0,0,0,.5)" };
    return { dark: false, title: d.ink, text: "#2A1633", soft: "rgba(42,22,51,.82)", accent: d.ink, line: d.ink, ribbon: [d.ink, d.ink], shadow: "rgba(255,255,255,.7)" };
  }

  function currentWish() {
    if (state.wish === "c") return state.custom || (INVITE ? K.wordings[0] : (K.wishes[state.rel] || [""])[0]);
    var list = wishList();
    return list[state.wish] || list[0] || "";
  }
  function fromText() {
    var tpl = K.fromTpl;
    if (state.fs && K.fromOpts && K.fromOpts[state.fs]) tpl = K.fromOpts[state.fs];
    return fmt(tpl, { from: state.from, name: state.from });
  }
  function currentType() { return K.types ? K.types[state.type] : null; }

  /* Text blocks, top to bottom */
  function blocks() {
    var list = [], ty = currentType();
    var top = ty ? ty.top : K.topLabel, title = ty ? ty.title : K.title;
    if (top) list.push({ k: "label", t: top, fam: FB, w: 700, s: 32, min: 22, max: 1, gap: 16 });
    if (INVITE && state.page === 2 && hasProgram()) return programBlocks();
    if (INVITE) {
      var f = state.f;
      list.push({ k: "title", t: title, fam: TF[0], w: TF[1], s: 100, min: 52, max: 2, gap: 16 });
      var names = f.name1 && f.name2 ? f.name1 + (K.join ? "  " + K.join + "  " : "  ") + f.name2 : (f.name1 || "");
      if (names) list.push({ k: "names", t: names, fam: TF[0], w: TF[1], s: 64, min: 34, max: 2, gap: 12 });
      if (f.dates) list.push({ k: "detail", t: f.dates, fam: FB, w: 600, s: 30, min: 22, max: 2, gap: 12 });
      list.push({ k: "divider", h: 24, gap: 18 });
      list.push({ k: "wish", t: currentWish(), fam: FB, w: 600, s: 38, min: 24, max: 4, gap: 18 });
      var dt = [];
      if (f.date) dt.push((K.prefix.date ? K.prefix.date + " " : "") + f.date);
      if (f.time) dt.push((K.prefix.time ? K.prefix.time + " " : "") + f.time);
      if (dt.length) list.push({ k: "detail-b", t: dt.join("  |  "), fam: FB, w: 700, s: 34, min: 22, max: 2, gap: 10 });
      if (f.venue) list.push({ k: "detail", t: (K.prefix.venue ? K.prefix.venue + " " : "") + f.venue, fam: FB, w: 600, s: 32, min: 22, max: 3, gap: 14 });
      var qr1 = mapOk(f.map) && !hasProgram() && qrModules(f.map);
      if (f.note) list.push({ k: "note", t: f.note, fam: FB, w: 500, s: 28, min: 20, max: 2, gap: 10 });
      pushTail(list, f, qr1 ? f.map : "", 32);
      trimGap(list);
      return list;
    }
    if (K.kind === "couple" && state.n1 && state.n2) list.push({ k: "names", t: state.n1 + "  &  " + state.n2, fam: TF[0], w: TF[1], s: 62, min: 34, max: 2, gap: 12 });
    list.push({ k: "title", t: title, fam: TF[0], w: TF[1], s: 116, min: 56, max: 2, gap: 18 });
    if (K.kind === "person" && state.to) list.push({ k: "ribbon", t: state.to, fam: FB, w: 700, s: 48, min: 30, max: 1, gap: 24 });
    list.push({ k: "divider", h: 24, gap: 20 });
    list.push({ k: "wish", t: currentWish(), fam: FB, w: 600, s: 46, min: 26, max: 5, gap: 20 });
    if (K.kind === "morning" && K.thoughts) list.push({ k: "thought", t: "“" + K.thoughts[state.thought] + "”", fam: FB, w: 500, s: 34, min: 22, max: 4, gap: 20 });
    if (state.from) list.push({ k: "from", t: fromText(), fam: FB, w: 700, s: 36, min: 22, max: 2, gap: 0 });
    return list;
  }

  function trimGap(list) { if (list.length) list[list.length - 1].gap = 0; }
  // Host + phone lines; with a map link they sit beside a location QR code.
  function pushTail(list, f, url, s) {
    var host = f.host ? (K.prefix.host ? K.prefix.host + " " : "") + f.host : "";
    var phone = f.phone ? (K.prefix.phone ? K.prefix.phone + " " : "") + f.phone : "";
    if (url) { list.push({ k: "tail", url: url, t: U.qr_caption, host: host, phone: phone, s: s, gap: 0 }); return; }
    if (host) list.push({ k: "from", t: host, fam: FB, w: 700, s: s, min: 20, max: 3, gap: 10 });
    if (phone) list.push({ k: "detail-b", t: phone, fam: FB, w: 700, s: s - 2, min: 20, max: 1, gap: 10 });
  }
  function programBlocks() {
    var f = state.f, list = [];
    list.push({ k: "title", t: K.occasion === "invite-engagement" ? U.program_title_eng : U.program_title, fam: TF[0], w: TF[1], s: 80, min: 44, max: 1, gap: 8 });
    var names = f.name1 && f.name2 ? f.name1 + (K.join ? "  " + K.join + "  " : "  ") + f.name2 : (f.name1 || "");
    if (names) list.push({ k: "detail-b", t: names, fam: FB, w: 700, s: 32, min: 20, max: 1, gap: 8 });
    list.push({ k: "divider", h: 24, gap: 14 });
    state.prog.forEach(function (r) {
      if (!(r.n || r.w)) return;
      if (r.n) list.push({ k: "names", t: r.n, fam: TF[0], w: TF[1], s: 48, min: 26, max: 1, gap: 2 });
      var d = [r.w, r.v].filter(Boolean).join("  ·  ");
      if (d) list.push({ k: "detail", t: d, fam: FB, w: 600, s: 31, min: 18, max: 2, gap: 18 });
    });
    pushTail(list, f, mapOk(f.map) && qrModules(f.map) ? f.map : "", 30);
    trimGap(list);
    return list;
  }
  function qrModules(url) {
    if (typeof window.qrcode !== "function") return null;
    try { var q = window.qrcode(0, "M"); q.addData(url); q.make(); return q; } catch (e) { return null; }
  }
  function measure(list, maxW, scale) {
    var total = 0;
    list.forEach(function (b, i) {
      var gap = i < list.length - 1 ? b.gap * scale : 0;
      if (b.k === "divider") { b.hh = b.h; total += b.h + gap; return; }
      if (b.k === "tail") {
        b.q = qrModules(b.url);
        b.size = Math.round(170 * Math.max(scale, 0.78));
        b.cap = Math.max(17, Math.round(22 * Math.max(scale, 0.8)));
        b.tw = Math.max(200, maxW - b.size - 30);
        var ts = Math.max(20, Math.round(b.s * scale));
        b.items = [];
        [[b.host, 700], [b.phone, 700]].forEach(function (it) {
          if (!it[0]) return;
          ctx.font = font(FB, it[1], ts);
          var ls = wrap(it[0], b.tw);
          b.items.push({ lines: ls, size: ts, lh: Math.round(ts * 1.4) });
        });
        var th = b.items.reduce(function (a, it) { return a + it.lines.length * it.lh; }, 0) + (b.items.length > 1 ? 8 : 0);
        b.qh = b.size + 10 + b.cap * 1.4;
        b.th = th;
        b.hh = Math.max(b.qh, th);
        total += b.hh + gap; return;
      }
      var s = Math.round(b.s * scale), limit = b.k === "ribbon" ? maxW - 110 : maxW;
      ctx.font = font(b.fam, b.w, s);
      var lines = wrap(b.t, limit);
      while ((lines.length > b.max || lines.some(function (l) { return ctx.measureText(l).width > limit; })) && s > b.min) {
        s -= 2; ctx.font = font(b.fam, b.w, s); lines = wrap(b.t, limit);
      }
      b.size = s; b.lines = lines;
      b.lh = Math.round(s * (b.k === "title" || b.k === "names" ? 1.22 : 1.42));
      b.hh = b.lines.length * b.lh + (b.k === "ribbon" ? 30 : 0);
      total += b.hh + gap;
    });
    return total;
  }

  function drawDivider(x, y, pal, align) {
    ctx.save();
    ctx.strokeStyle = pal.line; ctx.fillStyle = pal.accent; ctx.lineWidth = 3; ctx.lineCap = "round";
    if (align === "left") {
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 150, y); ctx.stroke();
      ctx.beginPath(); ctx.arc(x + 166, y, 5, 0, Math.PI * 2); ctx.fill();
    } else {
      ctx.beginPath(); ctx.moveTo(x - 140, y); ctx.lineTo(x - 32, y); ctx.moveTo(x + 32, y); ctx.lineTo(x + 140, y); ctx.stroke();
      ctx.beginPath(); ctx.moveTo(x, y - 12); ctx.lineTo(x + 12, y); ctx.lineTo(x, y + 12); ctx.lineTo(x - 12, y); ctx.closePath(); ctx.fill();
      [-22, 22].forEach(function (dx) { ctx.beginPath(); ctx.arc(x + dx, y, 4, 0, Math.PI * 2); ctx.fill(); });
    }
    ctx.restore();
  }

  /* ---------- photo: shape paths, zoom and drag ---------- */
  function archPath(x, y, w, h) {
    var cx = x + w / 2, sh = y + h * 0.34;
    ctx.beginPath();
    ctx.moveTo(x, y + h); ctx.lineTo(x, sh);
    ctx.bezierCurveTo(x, sh - h * 0.12, x + w * 0.18, y + h * 0.1, cx - w * 0.1, y + h * 0.045);
    ctx.bezierCurveTo(cx - w * 0.04, y + h * 0.02, cx, y + h * 0.01, cx, y);
    ctx.bezierCurveTo(cx, y + h * 0.01, cx + w * 0.04, y + h * 0.02, cx + w * 0.1, y + h * 0.045);
    ctx.bezierCurveTo(x + w - w * 0.18, y + h * 0.1, x + w, sh - h * 0.12, x + w, sh);
    ctx.lineTo(x + w, y + h); ctx.closePath();
  }
  function heartPath(x, y, w, h) {
    var cx = x + w / 2;
    ctx.beginPath();
    ctx.moveTo(cx, y + h);
    ctx.bezierCurveTo(x - w * 0.2, y + h * 0.55, x, y - h * 0.05, cx, y + h * 0.22);
    ctx.bezierCurveTo(x + w, y - h * 0.05, x + w * 1.2, y + h * 0.55, cx, y + h);
    ctx.closePath();
  }
  function shapePath(ph) {
    if (ph.shape === "arch") archPath(ph.x, ph.y, ph.w, ph.h);
    else if (ph.shape === "rounded") roundRect(ph.x, ph.y, ph.w, ph.h, 28);
    else if (ph.shape === "pill") roundRect(ph.x, ph.y, ph.w, ph.h, Math.min(ph.w, ph.h) / 2);
    else if (ph.shape === "rect") { ctx.beginPath(); ctx.rect(ph.x, ph.y, ph.w, ph.h); }
    else if (ph.shape === "oval") { ctx.beginPath(); ctx.ellipse(ph.x + ph.w / 2, ph.y + ph.h / 2, ph.w / 2, ph.h / 2, 0, 0, Math.PI * 2); }
    else if (ph.shape === "heart") heartPath(ph.x, ph.y, ph.w, ph.h);
    else { ctx.beginPath(); ctx.arc(ph.cx, ph.cy, ph.r, 0, Math.PI * 2); }
  }
  function box(ph) {
    if (ph.shape === "circle") return { x: ph.cx - ph.r, y: ph.cy - ph.r, w: ph.r * 2, h: ph.r * 2 };
    return { x: ph.x, y: ph.y, w: ph.w, h: ph.h };
  }
  var photoBox = null; // last drawn photo box, for dragging
  function drawPhotoImage(ph) {
    var b = box(ph), im = state.photo;
    ctx.save(); shapePath(ph); ctx.clip();
    if (im) {
      var s = Math.max(b.w / im.width, b.h / im.height) * state.pz;
      var iw = im.width * s, ih = im.height * s;
      var ox = (iw - b.w) / 2, oy = (ih - b.h) / 2;
      ctx.drawImage(im, b.x - ox + state.px * ox, b.y - oy + state.py * oy, iw, ih);
    } else {
      ctx.fillStyle = "#EDE6DC"; ctx.fillRect(b.x, b.y, b.w, b.h);
      ctx.fillStyle = "#C9BDB0";
      var cx = b.x + b.w / 2, cy = b.y + b.h / 2, r = Math.min(b.w, b.h) / 2;
      ctx.beginPath(); ctx.arc(cx, cy - r * 0.18, r * 0.32, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(cx, cy + r * 0.62, r * 0.6, r * 0.42, 0, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
    photoBox = b;
  }
  function drawPhotoFrame(ph, pal) {
    ctx.save();
    ctx.shadowColor = "rgba(0,0,0,.3)"; ctx.shadowBlur = 24; ctx.shadowOffsetY = 8;
    if (ph.shape === "circle") { ctx.beginPath(); ctx.arc(ph.cx, ph.cy, ph.r + 12, 0, Math.PI * 2); }
    else if (ph.shape === "rounded") roundRect(ph.x - 10, ph.y - 10, ph.w + 20, ph.h + 20, 34);
    else shapePath({ shape: ph.shape, x: ph.x - 10, y: ph.y - 10, w: ph.w + 20, h: ph.h + 20 });
    ctx.fillStyle = pal.dark ? gold(ph.cy || ph.y, (ph.cy || ph.y) + 200) : "#FFFFFF"; ctx.fill();
    ctx.restore();
    drawPhotoImage(ph);
  }

  // Frosted glass panel for photo backgrounds
  function drawPanel(img, x, y, w, h, pal) {
    var r = 36;
    ctx.save();
    ctx.shadowColor = "rgba(0,0,0,.28)"; ctx.shadowBlur = 40; ctx.shadowOffsetY = 12;
    roundRect(x, y, w, h, r); ctx.fillStyle = pal.dark ? "rgba(18,8,28,.35)" : "rgba(255,252,246,.4)"; ctx.fill();
    ctx.restore();
    ctx.save();
    roundRect(x, y, w, h, r); ctx.clip();
    if (img && "filter" in ctx) {
      ctx.filter = "blur(22px) saturate(1.15)";
      var c = coverRect(img); ctx.drawImage(img, c[0], c[1], c[2], c[3]);
      ctx.filter = "none";
    }
    ctx.fillStyle = pal.dark ? "rgba(22,10,34,.55)" : "rgba(255,252,246,.74)";
    ctx.fillRect(x, y, w, h);
    ctx.restore();
    ctx.save();
    roundRect(x + 10, y + 10, w - 20, h - 20, r - 8);
    ctx.lineWidth = 2; ctx.strokeStyle = pal.dark ? "rgba(255,211,107,.7)" : "rgba(120,80,40,.28)"; ctx.stroke();
    ctx.restore();
  }

  function drawBlocks(list, x0, x1, y, align, pal, scale) {
    var cx = align === "left" ? x0 : (x0 + x1) / 2;
    ctx.textAlign = align === "left" ? "left" : "center"; ctx.textBaseline = "middle";
    list.forEach(function (b) {
      if (b.k === "divider") { drawDivider(cx, y + b.h / 2, pal, align); y += b.h + b.gap * scale; return; }
      if (b.k === "tail") { drawTail(b, x0, x1, y, align, pal); y += b.hh + b.gap * scale; return; }
      ctx.font = font(b.fam, b.w, b.size);
      if (b.k === "ribbon") {
        var tw = Math.max.apply(null, b.lines.map(function (l) { return ctx.measureText(l).width; })) + 80;
        var rx = align === "left" ? x0 : cx - tw / 2;
        ctx.save();
        var rgx = ctx.createLinearGradient(rx, 0, rx + tw, 0);
        rgx.addColorStop(0, pal.ribbon[0]); rgx.addColorStop(1, pal.ribbon[1]);
        ctx.fillStyle = rgx; roundRect(rx, y, tw, b.hh, b.hh / 2); ctx.fill();
        ctx.restore();
        ctx.fillStyle = "#FFFFFF";
        b.lines.forEach(function (l, i) { ctx.fillText(l, align === "left" ? rx + 40 : cx, y + 15 + b.lh * i + b.lh / 2); });
        y += b.hh + b.gap * scale; return;
      }
      b.lines.forEach(function (l) {
        var ly = y + b.lh / 2;
        ctx.save();
        if (b.k === "title" || b.k === "names") {
          if (pal.title === "gold") {
            ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 16; ctx.shadowOffsetY = 4;
            ctx.fillStyle = gold(ly - b.size / 2, ly + b.size / 2);
          } else { ctx.fillStyle = pal.title; if (!pal.tpl) { ctx.shadowColor = pal.shadow; ctx.shadowBlur = 10; } }
          ctx.fillText(l, cx, ly);
        } else if (b.k === "label") {
          ctx.fillStyle = pal.accent;
          if ("letterSpacing" in ctx) ctx.letterSpacing = "3px";
          ctx.fillText(l, cx, ly);
        } else {
          if (pal.dark) { ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 10; }
          ctx.fillStyle = b.k === "from" || b.k === "detail-b" ? pal.accent : b.k === "thought" || b.k === "note" ? pal.soft : pal.text;
          ctx.fillText(l, cx, ly);
        }
        ctx.restore();
        y += b.lh;
      });
      y += b.gap * scale;
    });
  }

  function drawTail(b, x0, x1, y, align, pal) {
    var widest = 0;
    b.items.forEach(function (it) { ctx.font = font(FB, 700, it.size); it.lines.forEach(function (l) { widest = Math.max(widest, ctx.measureText(l).width); }); });
    var full = widest + (widest ? 30 : 0) + b.size;
    var sx = align === "left" ? x0 : (x0 + x1) / 2 - full / 2;
    var ty = y + (b.hh - b.th) / 2;
    ctx.save();
    ctx.textAlign = "left"; ctx.textBaseline = "middle";
    b.items.forEach(function (it, i) {
      ctx.font = font(FB, 700, it.size);
      ctx.fillStyle = i === 0 && b.host ? pal.accent : pal.text;
      if (pal.dark) { ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 10; }
      it.lines.forEach(function (l) { ctx.fillText(l, sx, ty + it.lh / 2); ty += it.lh; });
      ty += 8;
    });
    ctx.restore();
    if (b.q) drawQr(b, sx + (widest ? widest + 30 : 0), y + (b.hh - b.qh) / 2, pal);
  }
  function drawQr(b, x, y, pal) {
    var n = b.q.getModuleCount(), pad = 10, cell = (b.size - pad * 2) / n;
    ctx.save();
    ctx.fillStyle = "#FFFFFF"; ctx.shadowColor = "rgba(0,0,0,.18)"; ctx.shadowBlur = 8;
    roundRect(x, y, b.size, b.size, 12); ctx.fill();
    ctx.shadowBlur = 0; ctx.fillStyle = "#1B1020";
    for (var r = 0; r < n; r++) for (var c = 0; c < n; c++) if (b.q.isDark(r, c)) ctx.fillRect(Math.floor(x + pad + c * cell), Math.floor(y + pad + r * cell), Math.ceil(cell), Math.ceil(cell));
    ctx.font = font(FB, 700, b.cap); ctx.textBaseline = "middle"; ctx.textAlign = "center";
    ctx.fillStyle = pal.accent;
    if (pal.dark) { ctx.shadowColor = "rgba(0,0,0,.5)"; ctx.shadowBlur = 8; }
    ctx.fillText(b.t, x + b.size / 2, y + b.size + 16 + b.cap * 0.6);
    ctx.restore();
  }
  function footerMark(pal) {
    ctx.save();
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    ctx.font = font(FB, 700, 24);
    var t = "indianfestivalwishes.com", tw = ctx.measureText(t).width + 44;
    roundRect(W / 2 - tw / 2, H - 58, tw, 40, 20);
    ctx.fillStyle = "rgba(20,10,30,.62)"; ctx.fill();
    ctx.fillStyle = "#FFFFFF";
    ctx.fillText(t, W / 2, H - 37);
    ctx.restore();
  }

  function fitList(maxW, availH) {
    var list = blocks(), scale = 1, total = measure(list, maxW, scale);
    while (total > availH && scale > 0.5) { scale -= 0.04; total = measure(list, maxW, scale); }
    return { list: list, scale: scale, total: total };
  }

  function drawTemplate(img, d) {
    var pal = palette(d);
    setTitleFont(d.title);
    if (img) { var c = coverRect(img); ctx.drawImage(img, c[0], c[1], c[2], c[3]); }
    var z = d.zone.slice(), ph = null;
    photoBox = null;
    if (state.photoMode && d.photo && state.page !== 2) {
      var p = d.photo;
      ph = p.shape === "circle" ? { shape: "circle", cx: p.x, cy: p.y, r: p.r } : { shape: p.shape, x: p.x, y: p.y, w: p.w, h: p.h };
      if (d.slot) drawPhotoImage(ph); else { drawPhotoFrame(ph, pal); var bb = box(ph); if (bb.y + bb.h + 30 > z[1] && (d.align !== "left" || bb.x + bb.w > z[0])) z[1] = bb.y + bb.h + 34; }
    }
    var fit = fitList(z[2] - z[0], z[3] - z[1]);
    var y = z[1] + Math.max(0, (z[3] - z[1] - fit.total) / 2);
    drawBlocks(fit.list, z[0], z[2], y, d.align, pal, fit.scale);
    footerMark(pal);
  }

  function drawPhotoCard(img, d) {
    var pal = palette(d);
    setTitleFont("classic");
    if (img) { var c = coverRect(img); ctx.drawImage(img, c[0], c[1], c[2], c[3]); }
    else {
      var g = ctx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, K.theme.primary); g.addColorStop(1, K.theme.secondary);
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    var z0 = d.zone[0], z1 = d.zone[1], cx = W / 2;
    var textW = Math.min(d.w, 820), padX = 56, padY = 52;
    var panelW = Math.min(W - 80, textW + padX * 2);
    var photoR = state.photoMode && state.page !== 2 ? (INVITE ? 150 : 128) : 0;
    var maxPanelH = H - 150 - (photoR ? photoR + 20 : 0);
    var zoneH = Math.max(z1 - z0, 0) - (photoR ? photoR + 20 : 0);
    var fit = fitList(textW, Math.max(zoneH, maxPanelH * 0.9) - padY * 2);
    var panelH = fit.total + padY * 2 + (photoR ? photoR + 16 : 0);
    var blockH = panelH + (photoR ? photoR + 12 : 0);
    var top = Math.round((z0 + z1) / 2 - blockH / 2);
    top = Math.max(50, Math.min(top, H - 90 - blockH));
    var panelY = top + (photoR ? photoR + 12 : 0);
    drawPanel(img, cx - panelW / 2, panelY, panelW, panelH, pal);
    var y = panelY + padY;
    photoBox = null;
    if (photoR) { drawPhotoFrame({ shape: "circle", cx: cx, cy: panelY, r: photoR }, pal); y += photoR + 16; }
    drawBlocks(fit.list, cx - textW / 2, cx + textW / 2, y, "center", pal, fit.scale);
    footerMark(pal);
  }

  function brightness(img) {
    try {
      var c = document.createElement("canvas"); c.width = 24; c.height = 30;
      var x = c.getContext("2d"); x.drawImage(img, 0, 0, 24, 30);
      var d = x.getImageData(0, 0, 24, 30).data, s = 0;
      for (var i = 0; i < d.length; i += 4) s += 0.299 * d[i] + 0.587 * d[i + 1] + 0.114 * d[i + 2];
      return s / (d.length / 4) / 255;
    } catch (e) { return 0.5; }
  }

  function drawCard(img) {
    var d = DES[state.design];
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, W, H);
    if (state.bgImg) {
      var tone = state.bgTone < 0.55 ? "dark" : "light";
      drawPhotoCard(state.bgImg, { tone: tone, ink: "#7A1238", zone: [180, 1170], w: 820 });
    } else if (d.tpl) drawTemplate(img, d);
    else drawPhotoCard(img, d);
    ctx.restore();
  }

  /* ---------------- fonts + redraw ---------------- */
  function sampleText() {
    var all = [];
    if (INVITE) all = K.wordings.concat((K.types || []).map(function (t) { return t.title + t.top; }));
    else Object.keys(K.wishes).forEach(function (k) { all = all.concat(K.wishes[k]); });
    return (K.title || "") + (K.topLabel || "") + (K.fromTpl || "") + all.join("") + (K.thoughts || []).join("") + JSON.stringify(state.f) + state.to + state.n1 + state.n2 + state.from + state.custom;
  }
  function fontsReady() {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    var s = sampleText();
    var d = DES[state.design];
    if (d && d.tpl) setTitleFont(d.title);
    return Promise.all([
      document.fonts.load(font(TF[0], TF[1], 100), s),
      document.fonts.load(font(FD, FDW, 100), s),
      document.fonts.load(font(FB, 500, 40), s), document.fonts.load(font(FB, 600, 40), s), document.fonts.load(font(FB, 700, 40), s)
    ]).catch(function () {});
  }
  var token = 0;
  function redraw() {
    var my = ++token, id = DES[state.design].id;
    frame.classList.add("loading");
    Promise.all([loadImg(id), fontsReady()]).then(function (r) {
      if (my !== token) return;
      drawCard(r[0]);
      frame.classList.remove("loading");
      if (state.made) queueShare(share.id ? 1500 : 250);
    });
    [state.design + 1, state.design - 1].forEach(function (i) { if (DES[i]) loadImg(DES[i].id); });
  }

  /* ---------------- form wiring ---------------- */
  var relSel = $("card-rel"), wishSel = $("card-wish"), err = $("card-error"), status = $("card-status"), shareBox = $("share-actions");
  var customBox = $("custom-box"), customIn = $("card-custom"), typeSel = $("card-type");
  var photoFs = $("photo-box"), photoIn = $("card-photo");
  var modeBtns = document.querySelectorAll("[data-photo-mode]");
  var nextThought = $("next-thought"), thoughtText = $("thought-text");
  var dzBtns = Array.prototype.slice.call(document.querySelectorAll("#design-row .dz"));

  function link() {
    var q = new URLSearchParams();
    if (state.from) q.set("name", state.from);
    if (state.to) q.set("to", state.to);
    if (state.n1) q.set("n1", state.n1);
    if (state.n2) q.set("n2", state.n2);
    FIELD_KEYS.forEach(function (k) { if (state.f[k]) q.set("f_" + k, state.f[k]); });
    if (K.types) q.set("ty", String(state.type));
    if (state.fs) q.set("fs", state.fs);
    if (!INVITE) q.set("r", state.rel);
    q.set("w", String(state.wish));
    if (state.wish === "c" && state.custom) q.set("c", state.custom);
    q.set("s", String(state.design));
    if (DES[state.design] && DES[state.design].id) q.set("d", DES[state.design].id);
    if (K.thoughts) q.set("t", String(state.thought));
    if (K.program) state.prog.forEach(function (r, i) { if (r.n || r.w) q.set("p" + (i + 1), [r.n, r.w, r.v].join("~").replace(/~+$/, "")); });
    return location.origin + location.pathname + "?" + q.toString();
  }
  /* Share links: the rendered card is uploaded so the link shows it as a preview (WhatsApp, Facebook). */
  var share = { id: "", key: "", dirty: true, pending: null, timer: 0 };
  function bestLink() { return share.id && !share.dirty ? location.origin + "/s/" + share.id : link(); }
  function waUrl() { return "https://wa.me/?text=" + encodeURIComponent((K.shareMsg || U.share_link_msg) + "\n" + bestLink()); }
  function refreshLinks() {
    $("btn-wa").href = waUrl();
    $("btn-fb").href = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(bestLink());
  }
  function shareTitle() {
    var ty = currentType(), title = ty ? ty.title : K.title, who;
    if (INVITE) who = [state.f.name1, state.f.name2].filter(Boolean).join(" & ");
    else if (K.kind === "couple" && state.n1 && state.n2) who = state.n1 + " & " + state.n2;
    else who = state.from || state.to;
    return who ? title + " – " + who : title;
  }
  function uploadShare() {
    clearTimeout(share.timer);
    var full = link(), rel = full.slice(location.origin.length);
    share.dirty = false;
    share.pending = renderPage(1).then(function (big) {
      var c = document.createElement("canvas"); c.width = 720; c.height = 900;
      c.getContext("2d").drawImage(big, 0, 0, 720, 900);
      return blobOf(c, "image/jpeg", 0.84);
    }).then(function (blob) {
      if (!blob) throw new Error("no blob");
      var q = new URLSearchParams({ link: rel, t: shareTitle(), d: K.shareMsg || U.share_link_msg, l: D.lang });
      if (share.id) { q.set("id", share.id); q.set("key", share.key); }
      return fetch("/api/share?" + q.toString(), { method: "POST", headers: { "Content-Type": "image/jpeg", "X-IFW": "1" }, body: blob });
    }).then(function (r) { return r.ok ? r.json() : null; }).then(function (j) {
      if (j && j.id) { share.id = j.id; share.key = j.key; }
      else share.dirty = true;
    }).catch(function () { share.dirty = true; }).then(function () { share.pending = null; refreshLinks(); });
    return share.pending;
  }
  function queueShare(ms) { share.dirty = true; clearTimeout(share.timer); share.timer = setTimeout(uploadShare, ms || 1500); }
  function ready(ms) {
    if (share.dirty && !share.pending) uploadShare();
    if (!share.pending) return Promise.resolve();
    return Promise.race([share.pending, new Promise(function (r) { setTimeout(r, ms); })]);
  }
  function track(a) {
    try {
      var d = DES[state.design] || {};
      fetch("/api/stat", { method: "POST", keepalive: true, headers: { "Content-Type": "application/json", "X-IFW": "1" }, body: JSON.stringify({ p: K.occasion || D.page, d: d.id, a: a, l: D.lang }) }).catch(function () {});
    } catch (e) {}
  }
  function fileName(n) { return (K.slug || "card") + (n ? "-" + n : "") + "-indianfestivalwishes.png"; }
  function pageCount() { return INVITE && hasProgram() ? 2 : 1; }
  function renderPage(n) {
    return Promise.all([loadImg(DES[state.design].id), fontsReady()]).then(function (r) {
      var prev = state.page; state.page = n; drawCard(r[0]);
      var c = document.createElement("canvas"); c.width = W; c.height = H; c.getContext("2d").drawImage(canvas, 0, 0);
      state.page = prev; drawCard(r[0]);
      return c;
    });
  }
  function pages() {
    var out = [], n = pageCount(), chain = Promise.resolve();
    for (var i = 1; i <= n; i++) (function (i) { chain = chain.then(function () { return renderPage(i).then(function (c) { out.push(c); }); }); })(i);
    return chain.then(function () { return out; });
  }
  function blobOf(c, type, q) { return new Promise(function (res) { c.toBlob(res, type || "image/png", q); }); }
  function toBlob() { return renderPage(1).then(function (c) { return blobOf(c); }); }
  function downloadAll() {
    return pages().then(function (cs) {
      return cs.reduce(function (ch, c, i) {
        return ch.then(function () { return blobOf(c); }).then(function (b) { save(b, cs.length > 1 ? fileName(i + 1) : fileName()); return new Promise(function (r) { setTimeout(r, 350); }); });
      }, Promise.resolve());
    });
  }
  // Minimal PDF writer: one JPEG image per page (432 x 540 pt = 6 x 7.5 in).
  function makePdf(jpegs) {
    var enc = new TextEncoder(), parts = [], len = 0, offs = [];
    function add(x) { var b = typeof x === "string" ? enc.encode(x) : x; parts.push(b); len += b.length; }
    function obj(n, body) { offs[n] = len; add(n + " 0 obj\n"); body(); add("\nendobj\n"); }
    var n = jpegs.length, kids = [];
    for (var i = 0; i < n; i++) kids.push((3 + i * 3) + " 0 R");
    add("%PDF-1.4\n%\xE2\xE3\xCF\xD3\n");
    obj(1, function () { add("<< /Type /Catalog /Pages 2 0 R >>"); });
    obj(2, function () { add("<< /Type /Pages /Kids [" + kids.join(" ") + "] /Count " + n + " >>"); });
    jpegs.forEach(function (j, i) {
      var pg = 3 + i * 3, ct = pg + 1, im = pg + 2, cs = "q 432 0 0 540 0 0 cm /Im0 Do Q";
      obj(pg, function () { add("<< /Type /Page /Parent 2 0 R /MediaBox [0 0 432 540] /Resources << /XObject << /Im0 " + im + " 0 R >> >> /Contents " + ct + " 0 R >>"); });
      obj(ct, function () { add("<< /Length " + cs.length + " >>\nstream\n" + cs + "\nendstream"); });
      obj(im, function () { add("<< /Type /XObject /Subtype /Image /Width " + W + " /Height " + H + " /ColorSpace /DeviceRGB /BitsPerComponent 8 /Filter /DCTDecode /Length " + j.length + " >>\nstream\n"); add(j); add("\nendstream"); });
    });
    var xref = len, total = 3 + n * 3;
    add("xref\n0 " + total + "\n0000000000 65535 f \n");
    for (var k = 1; k < total; k++) add(("0000000000" + offs[k]).slice(-10) + " 00000 n \n");
    add("trailer\n<< /Size " + total + " /Root 1 0 R >>\nstartxref\n" + xref + "\n%%EOF");
    return new Blob(parts, { type: "application/pdf" });
  }
  function downloadPdf() {
    return pages().then(function (cs) {
      return Promise.all(cs.map(function (c) { return blobOf(c, "image/jpeg", 0.92).then(function (b) { return b.arrayBuffer(); }).then(function (a) { return new Uint8Array(a); }); }));
    }).then(function (js) { save(makePdf(js), fileName().replace(/\.png$/, ".pdf")); });
  }
  function save(blob, name) {
    var url = URL.createObjectURL(blob), a = document.createElement("a");
    a.href = url; a.download = name || fileName(); document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }
  var canShareFiles = false;
  try { canShareFiles = !!(navigator.canShare && navigator.canShare({ files: [new File([new Blob(["x"], { type: "image/png" })], "t.png", { type: "image/png" })] })); } catch (e) {}
  function shareFile() {
    track("share");
    return pages().then(function (cs) { return Promise.all(cs.map(function (c) { return blobOf(c); })); }).then(function (bs) {
      var files = bs.map(function (b, i) { return new File([b], bs.length > 1 ? fileName(i + 1) : fileName(), { type: "image/png" }); });
      if (canShareFiles) return navigator.share({ files: files, text: (K.shareMsg || U.share_link_msg) + "\n" + bestLink() }).catch(function () {});
      files.forEach(function (f) { save(f, f.name); });
      status.textContent = U.insta_hint;
    });
  }
  function changed() { redraw(); }

  function fillWishes() {
    var list = wishList();
    wishSel.innerHTML = "";
    list.forEach(function (w, i) {
      var o = document.createElement("option"); o.value = String(i); o.textContent = w; wishSel.appendChild(o);
    });
    var oc = document.createElement("option"); oc.value = "c"; oc.textContent = U.custom_wish; wishSel.appendChild(oc);
    if (state.wish !== "c" && state.wish >= list.length) state.wish = 0;
    wishSel.value = String(state.wish);
    if (customBox) customBox.hidden = state.wish !== "c";
  }

  // Card designs hidden or added from the admin panel
  function rebuildPicker() {
    var row = $("design-row");
    if (!row) return;
    row.innerHTML = "";
    DES.forEach(function (d, i) {
      var b = document.createElement("button");
      b.type = "button"; b.className = "dz"; b.setAttribute("aria-pressed", i === state.design ? "true" : "false");
      b.setAttribute("aria-label", (U.step_design || "") + " " + (i + 1));
      var im = document.createElement("img");
      im.src = d.url || ("/static/cards/thumb/" + d.id + ".webp" + IV); im.alt = ""; im.loading = "lazy"; im.width = 108; im.height = 135;
      b.appendChild(im);
      b.addEventListener("click", function () { selectDesign(i); });
      row.appendChild(b);
    });
    dzBtns = Array.prototype.slice.call(row.querySelectorAll(".dz"));
    var cnt = document.querySelector("[data-design-count]");
    if (cnt) cnt.textContent = fmt(U.designs_count, { n: DES.length });
  }
  if (window.IFW_SETTINGS) {
    window.IFW_SETTINGS.then(function (S) {
      var c = (S && S.cards) || {}, key = K.occasion;
      var hidden = ((c.hidden || {})[key]) || [], extra = ((c.extra || {})[key]) || [];
      if (!hidden.length && !extra.length) return;
      var cur = DES[state.design] && DES[state.design].id;
      var list = DES.filter(function (d) { return hidden.indexOf(d.id) < 0; }), added = [];
      extra.forEach(function (x) {
        if (!x || typeof x.url !== "string" || !/^(\/uploads\/[\w.-]+|https:\/\/)/.test(x.url)) return;
        added.push({ id: x.id, url: x.url, tone: x.tone === "dark" ? "dark" : "light", ink: "#7A1238", zone: [180, 1170], w: 820, extra: true });
      });
      list = added.concat(list); // cards added from the admin panel come first
      if (!list.length) return;
      DES = list;
      var ids = DES.map(function (d) { return d.id; });
      var ni = urlD && ids.indexOf(urlD) >= 0 ? ids.indexOf(urlD)
        : (state.picked || P.get("s") !== null) ? ids.indexOf(cur) : 0;
      state.design = ni >= 0 ? ni : 0;
      rebuildPicker();
      redraw();
    });
  }

  // Extra wishes and thoughts added from the admin panel
  if (window.IFW_SETTINGS && !INVITE) {
    window.IFW_SETTINGS.then(function (S) {
      var cu = (S && S.custom) || {};
      var extra = ((cu.wishes || {})[D.lang] || {})[K.occasion] || {};
      var ch = false;
      Object.keys(extra).forEach(function (rel) {
        if (!Array.isArray(extra[rel]) || !K.wishes[rel]) return;
        extra[rel].forEach(function (w) { if (typeof w === "string" && w.trim()) { K.wishes[rel].push(w.trim().slice(0, 160)); ch = true; } });
      });
      var th = (cu.thoughts || {})[D.lang];
      if (K.thoughts && Array.isArray(th)) th.forEach(function (t) { if (typeof t === "string" && t.trim()) { K.thoughts.push(t.trim().slice(0, 160)); ch = true; } });
      if (ch) { fillWishes(); redraw(); }
    });
  }

  function selectDesign(i, scroll) {
    state.design = i; state.picked = true;
    if (state.bgImg) { state.bgImg = null; if ($("bg-remove")) $("bg-remove").hidden = true; if ($("card-bg")) $("card-bg").value = ""; }
    dzBtns.forEach(function (x, j) { x.setAttribute("aria-pressed", j === i ? "true" : "false"); });
    if (scroll && dzBtns[i]) dzBtns[i].scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    changed();
  }
  dzBtns.forEach(function (b, i) { b.addEventListener("click", function () { selectDesign(i); }); });
  dzBtns.forEach(function (x, j) { x.setAttribute("aria-pressed", j === state.design ? "true" : "false"); });

  var sx = null;
  canvas.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
  canvas.addEventListener("touchend", function (e) {
    if (sx == null) return;
    if (dragged) { dragged = false; sx = null; return; }
    var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) selectDesign((state.design + (dx < 0 ? 1 : -1) + DES.length) % DES.length, true);
  }, { passive: true });

  if (relSel) {
    relSel.value = state.rel;
    relSel.addEventListener("change", function () { state.rel = relSel.value; if (state.wish !== "c") state.wish = 0; fillWishes(); changed(); });
  }
  var fsSel = $("from-style");
  if (fsSel) {
    if (state.fs) fsSel.value = state.fs;
    fsSel.addEventListener("change", function () { state.fs = fsSel.value; changed(); });
  }
  if (typeSel) {
    typeSel.value = String(state.type);
    typeSel.addEventListener("change", function () { state.type = parseInt(typeSel.value, 10) || 0; changed(); });
  }
  wishSel.addEventListener("change", function () {
    state.wish = wishSel.value === "c" ? "c" : parseInt(wishSel.value, 10) || 0;
    if (customBox) customBox.hidden = state.wish !== "c";
    if (state.wish === "c" && customIn) customIn.focus();
    changed();
  });
  if (customIn) {
    customIn.value = state.custom;
    customIn.addEventListener("input", function () { state.custom = clean(customIn.value, 180); changed(); });
  }
  fillWishes();

  if (nextThought && K.thoughts) {
    var showThought = function () { if (thoughtText) thoughtText.textContent = K.thoughts[state.thought]; };
    showThought();
    nextThought.addEventListener("click", function () { state.thought = (state.thought + 1) % K.thoughts.length; showThought(); changed(); });
  }

  if (photoFs) {
    var setMode = function (on) {
      state.photoMode = on;
      modeBtns.forEach(function (x) { x.setAttribute("aria-pressed", (x.getAttribute("data-photo-mode") === "with") === on ? "true" : "false"); });
      $("photo-pick").hidden = !on;
    };
    setMode(state.photoMode);
    modeBtns.forEach(function (b) { b.addEventListener("click", function () { setMode(b.getAttribute("data-photo-mode") === "with"); redraw(); }); });
    photoIn.addEventListener("change", function () {
      var f = photoIn.files && photoIn.files[0];
      if (!f) return;
      var img = new Image();
      img.onload = function () { state.photo = img; state.pz = 1; state.px = 0; state.py = 0; if (zoomIn) zoomIn.value = "1"; setMode(true); redraw(); };
      img.src = URL.createObjectURL(f);
    });
  }

  /* photo zoom + drag */
  var zoomIn = $("photo-zoom"), resetBtn = $("photo-reset");
  if (zoomIn) zoomIn.addEventListener("input", function () { state.pz = parseFloat(zoomIn.value) || 1; redraw(); });
  if (resetBtn) resetBtn.addEventListener("click", function () { state.pz = 1; state.px = 0; state.py = 0; if (zoomIn) zoomIn.value = "1"; redraw(); });
  var drag = null, dragged = false;
  function canvasPt(e) {
    var r = canvas.getBoundingClientRect();
    return { x: (e.clientX - r.left) * W / r.width, y: (e.clientY - r.top) * H / r.height };
  }
  canvas.addEventListener("pointerdown", function (e) {
    if (!state.photo || !state.photoMode || !photoBox) return;
    var p = canvasPt(e), b = photoBox;
    if (p.x < b.x || p.x > b.x + b.w || p.y < b.y || p.y > b.y + b.h) return;
    drag = { x: p.x, y: p.y, px: state.px, py: state.py, b: b }; dragged = true;
    canvas.setPointerCapture(e.pointerId);
    e.preventDefault();
  });
  canvas.addEventListener("pointermove", function (e) {
    if (!drag) return;
    var p = canvasPt(e), b = drag.b, im = state.photo;
    var s = Math.max(b.w / im.width, b.h / im.height) * state.pz;
    var ox = (im.width * s - b.w) / 2 || 1, oy = (im.height * s - b.h) / 2 || 1;
    state.px = Math.max(-1, Math.min(1, drag.px + (p.x - drag.x) / ox));
    state.py = Math.max(-1, Math.min(1, drag.py + (p.y - drag.y) / oy));
    redraw();
  });
  ["pointerup", "pointercancel"].forEach(function (ev) { canvas.addEventListener(ev, function () { drag = null; }); });
  canvas.style.touchAction = "pan-y";

  /* own background */
  var bgIn = $("card-bg"), bgRemove = $("bg-remove");
  if (bgIn) bgIn.addEventListener("change", function () {
    var f = bgIn.files && bgIn.files[0];
    if (!f) return;
    var img = new Image();
    img.onload = function () { state.bgImg = img; state.bgTone = brightness(img); if (bgRemove) bgRemove.hidden = false; redraw(); };
    img.src = URL.createObjectURL(f);
  });
  if (bgRemove) bgRemove.addEventListener("click", function () { state.bgImg = null; bgRemove.hidden = true; if (bgIn) bgIn.value = ""; redraw(); });

  // live preview while typing
  var simple = { "in-from": "from", "in-to": "to", "in-n1": "n1", "in-n2": "n2" };
  Object.keys(simple).forEach(function (id) {
    var el = $(id);
    if (!el) return;
    if (!received || id !== "in-from") el.value = state[simple[id]] || "";
    el.addEventListener("input", function () { state[simple[id]] = clean(el.value); redraw(); });
  });
  if (received && $("in-from")) $("in-from").value = "";
  FIELD_KEYS.forEach(function (k) {
    var el = $("f-" + k);
    if (!el) return;
    el.value = state.f[k];
    el.addEventListener("input", function () { state.f[k] = clean(el.value, parseInt(el.getAttribute("maxlength"), 10) || 50); if (k === "map") mapHint(); redraw(); });
  });

  /* Location QR, function programme (page 2) and page tabs */
  var mapHintEl = $("map-hint");
  function mapHint() {
    if (!mapHintEl) return;
    var bad = !!state.f.map && !mapOk(state.f.map);
    mapHintEl.textContent = bad ? U.map_bad : U.map_hint;
    mapHintEl.classList.toggle("bad", bad);
  }
  mapHint();
  var tabs = $("page-tabs"), tabBtns = tabs ? Array.prototype.slice.call(tabs.querySelectorAll("[data-page]")) : [];
  function syncTabs() {
    if (!tabs) return;
    var on = hasProgram();
    tabs.hidden = !on;
    if (!on) state.page = 1;
    tabBtns.forEach(function (b) { b.setAttribute("aria-pressed", String(+b.getAttribute("data-page") === state.page)); });
  }
  tabBtns.forEach(function (b) { b.addEventListener("click", function () { state.page = +b.getAttribute("data-page"); syncTabs(); redraw(); }); });
  if (K.program) {
    var rows = [];
    for (var ri = 1; ri <= 6; ri++) rows.push([$("p" + ri + "-n"), $("p" + ri + "-w"), $("p" + ri + "-v"), $("prog-row-" + ri)]);
    var readProg = function () {
      state.prog = rows.map(function (r) { return { n: clean(r[0].value, 40), w: clean(r[1].value, 50), v: clean(r[2].value, 60) }; });
      syncTabs(); redraw();
    };
    state.prog.forEach(function (p, i) { if (!rows[i]) return; rows[i][0].value = p.n; rows[i][1].value = p.w; rows[i][2].value = p.v; rows[i][3].hidden = false; });
    rows.forEach(function (r) { r.slice(0, 3).forEach(function (el) { el.addEventListener("input", readProg); }); });
    var addBtn = $("prog-add");
    var syncAdd = function () { addBtn.hidden = rows.every(function (r) { return !r[3].hidden; }); };
    addBtn.addEventListener("click", function () {
      var next = rows.filter(function (r) { return r[3].hidden; })[0];
      if (next) { next[3].hidden = false; next[0].focus(); }
      syncAdd();
    });
    syncAdd();
    state.prog = rows.map(function (r) { return { n: clean(r[0].value, 40), w: clean(r[1].value, 50), v: clean(r[2].value, 60) }; });
  }
  syncTabs();
  if (received && mapOk(state.f.map)) {
    var mb = document.createElement("a");
    mb.className = "btn btn-soft btn-sm map-open"; mb.href = state.f.map; mb.target = "_blank"; mb.rel = "noopener nofollow";
    mb.textContent = "📍 " + U.open_map;
    var rn = $("received-note"); rn.parentNode.insertBefore(mb, rn.nextSibling);
  }

  $("card-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var ok;
    if (INVITE) ok = !!state.f.name1;
    else {
      ["in-from", "in-to", "in-n1", "in-n2"].forEach(function (id) { if ($(id)) state[simple[id]] = clean($(id).value); });
      ok = K.kind === "festival" ? !!state.from : K.kind === "person" ? !!state.to : K.kind === "couple" ? !!(state.n1 && state.n2) : true;
    }
    if (!ok) { err.textContent = U.need_name; return; }
    err.textContent = "";
    state.made = true;
    shareBox.hidden = false;
    status.textContent = "";
    redraw();
    track("make");
    refreshLinks();
    if (window.innerWidth < 900) canvas.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  $("btn-ig").addEventListener("click", shareFile);
  $("btn-share-photo").hidden = !canShareFiles;
  $("btn-share-photo").addEventListener("click", shareFile);
  $("btn-download").addEventListener("click", function () { track("download"); downloadAll(); });
  if ($("btn-pdf")) $("btn-pdf").addEventListener("click", function () { track("pdf"); downloadPdf(); });
  $("btn-wa").addEventListener("click", function (e) {
    track("wa");
    if (!share.dirty && !share.pending) return; // link already has the card preview
    e.preventDefault();
    var w = window.open("", "_blank");
    ready(3500).then(function () {
      if (w) { try { w.opener = null; } catch (x) {} w.location.href = waUrl(); } else location.href = waUrl();
    });
  });
  $("btn-copy-link").addEventListener("click", function () {
    track("link");
    var t = bestLink();
    (navigator.clipboard && window.isSecureContext ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
      status.textContent = U.copied_link;
    }).catch(function () { window.prompt("", t); });
  });

  if (received) {
    if (!INVITE) $("card-heading").textContent = U.card_heading_received;
    $("received-note").textContent = U.card_now_yours;
  }
  redraw();
})();
