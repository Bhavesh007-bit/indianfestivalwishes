/* Indian Festival Wishes — card maker v9
   Photo backgrounds (made in Canva) + live text overlay on a 1080x1350 canvas. */
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

  function $(id) { return document.getElementById(id); }
  function fmt(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ""; }); }
  function clean(v) { return String(v || "").replace(/[\u0000-\u001F\u007F<>"`]/g, "").replace(/\s+/g, " ").trim().slice(0, 30); }

  /* ---------------- state ---------------- */
  var P = new URLSearchParams(location.search);
  var relKeys = K.rels.map(function (r) { return r[0]; });
  var state = {
    design: Math.min(DES.length - 1, Math.max(0, parseInt(P.get("s"), 10) || 0)),
    rel: relKeys.indexOf(P.get("r")) >= 0 ? P.get("r") : relKeys[0],
    wish: Math.max(0, parseInt(P.get("w"), 10) || 0),
    from: clean(P.get("name") || P.get("from")),
    to: clean(P.get("to")),
    n1: clean(P.get("n1")),
    n2: clean(P.get("n2")),
    thought: (function () {
      if (!K.thoughts) return 0;
      var q = parseInt(P.get("t"), 10);
      if (q >= 0) return q % K.thoughts.length;
      var d = new Date(), start = new Date(d.getFullYear(), 0, 0);
      return Math.floor((d - start) / 86400000) % K.thoughts.length;
    })(),
    photoMode: false,
    photo: null,
    made: false
  };
  var received = !!(state.from || state.to || state.n1);
  if (!K.wishes[state.rel] || state.wish >= K.wishes[state.rel].length) state.wish = 0;

  /* ---------------- images ---------------- */
  var cache = {};
  var frame = canvas.parentNode;
  function loadImg(id) {
    if (cache[id]) return cache[id];
    cache[id] = new Promise(function (res) {
      var im = new Image();
      im.decoding = "async";
      im.onload = function () { res(im); };
      im.onerror = function () {
        // fall back to the small thumbnail, then to a plain gradient
        var t = new Image();
        t.onload = function () { res(t); };
        t.onerror = function () { res(null); };
        t.src = "/static/cards/thumb/" + id + ".webp";
      };
      im.src = "/static/cards/" + id + ".webp";
    });
    return cache[id];
  }

  /* ---------------- drawing helpers ---------------- */
  function font(fam, w, s) { return w + " " + s + "px " + fam; }
  function wrap(text, maxW) {
    var words = String(text).split(" "), lines = [], line = "";
    words.forEach(function (w) {
      var t = line ? line + " " + w : w;
      if (ctx.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t;
    });
    if (line) lines.push(line);
    return lines;
  }
  function roundRect(x, y, w, h, r) {
    ctx.beginPath();
    ctx.moveTo(x + r, y); ctx.arcTo(x + w, y, x + w, y + h, r); ctx.arcTo(x + w, y + h, x, y + h, r);
    ctx.arcTo(x, y + h, x, y, r); ctx.arcTo(x, y, x + w, y, r); ctx.closePath();
  }
  function cover(img) {
    var r = Math.max(W / img.width, H / img.height), w = img.width * r, h = img.height * r;
    ctx.drawImage(img, (W - w) / 2, (H - h) / 2, w, h);
  }
  function gold(y0, y1) {
    var g = ctx.createLinearGradient(0, y0, 0, y1);
    g.addColorStop(0, "#FFF6D2"); g.addColorStop(0.45, "#FFD36B"); g.addColorStop(0.75, "#F2A93B"); g.addColorStop(1, "#C9821E");
    return g;
  }

  // palette for the current design
  function palette(d) {
    if (d.tone === "dark") return { title: "gold", text: "#FFF8EC", soft: "rgba(255,248,236,.86)", accent: "#FFD36B", line: "rgba(255,211,107,.8)", ribbon: ["#E0115F", "#B80D4D"], ribbonInk: "#FFFFFF", shadow: "rgba(0,0,0,.55)" };
    return { title: d.ink, text: "#2A1633", soft: "rgba(42,22,51,.8)", accent: d.ink, line: d.ink, ribbon: [d.ink, d.ink], ribbonInk: "#FFFFFF", shadow: "rgba(255,255,255,.9)" };
  }

  function currentWish() {
    var list = K.wishes[state.rel] || [];
    return list[state.wish] || list[0] || "";
  }
  function fromLine() {
    if (!state.from) return "";
    return fmt(K.fromTpl, { from: state.from, name: state.from });
  }

  // Text blocks, top to bottom. Each: {kind, text, font fn(size), size, min, max lines, color, gap}
  function blocks(pal) {
    var list = [];
    if (K.topLabel) list.push({ k: "label", t: K.topLabel, fam: FB, w: 700, s: 34, min: 24, max: 1, gap: 18 });
    if (K.kind === "couple" && state.n1 && state.n2) list.push({ k: "names", t: state.n1 + "  &  " + state.n2, fam: FD, w: FDW, s: 64, min: 36, max: 2, gap: 14 });
    list.push({ k: "title", t: K.title, fam: FD, w: FDW, s: 124, min: 60, max: 2, gap: 20 });
    if (K.kind === "person" && state.to) list.push({ k: "ribbon", t: state.to, fam: FB, w: 700, s: 50, min: 32, max: 1, gap: 26 });
    list.push({ k: "divider", h: 26, gap: 22 });
    list.push({ k: "wish", t: currentWish(), fam: FB, w: 600, s: 48, min: 28, max: 4, gap: 22 });
    if (K.kind === "morning" && K.thoughts) list.push({ k: "thought", t: "“" + K.thoughts[state.thought] + "”", fam: FB, w: 500, s: 36, min: 24, max: 4, gap: 22 });
    var fl = fromLine();
    if (fl) list.push({ k: "from", t: fl, fam: FB, w: 600, s: 38, min: 24, max: 2, gap: 0 });
    return list;
  }

  function measure(list, maxW, scale) {
    var total = 0;
    list.forEach(function (b, i) {
      if (b.k === "divider") { b.hh = b.h; total += b.h + (i < list.length - 1 ? b.gap * scale : 0); return; }
      var s = Math.round(b.s * scale), limit = b.k === "ribbon" ? maxW - 120 : maxW;
      ctx.font = font(b.fam, b.w, s);
      var lines = wrap(b.t, limit);
      while ((lines.length > b.max || lines.some(function (l) { return ctx.measureText(l).width > limit; })) && s > b.min) {
        s -= 2; ctx.font = font(b.fam, b.w, s); lines = wrap(b.t, limit);
      }
      b.size = s; b.lines = lines.slice(0, b.max + 1);
      b.lh = Math.round(s * (b.k === "title" || b.k === "names" ? 1.18 : 1.42));
      b.hh = b.lines.length * b.lh + (b.k === "ribbon" ? 34 : 0);
      total += b.hh + (i < list.length - 1 ? b.gap * scale : 0);
    });
    return total;
  }

  function drawDivider(cx, y, pal) {
    ctx.save();
    ctx.strokeStyle = pal.line; ctx.fillStyle = pal.accent; ctx.lineWidth = 3; ctx.lineCap = "round";
    ctx.globalAlpha = 0.9;
    ctx.beginPath(); ctx.moveTo(cx - 150, y); ctx.lineTo(cx - 34, y); ctx.moveTo(cx + 34, y); ctx.lineTo(cx + 150, y); ctx.stroke();
    ctx.beginPath(); ctx.moveTo(cx, y - 13); ctx.lineTo(cx + 13, y); ctx.lineTo(cx, y + 13); ctx.lineTo(cx - 13, y); ctx.closePath(); ctx.fill();
    [-24, 24].forEach(function (dx) { ctx.beginPath(); ctx.arc(cx + dx, y, 4, 0, Math.PI * 2); ctx.fill(); });
    ctx.restore();
  }

  function drawPhoto(cx, cy, r, pal) {
    ctx.save();
    ctx.shadowColor = "rgba(0,0,0,.35)"; ctx.shadowBlur = 30; ctx.shadowOffsetY = 10;
    ctx.beginPath(); ctx.arc(cx, cy, r + 12, 0, Math.PI * 2);
    ctx.fillStyle = pal.title === "gold" ? gold(cy - r, cy + r) : "#FFFFFF"; ctx.fill();
    ctx.restore();
    ctx.save();
    ctx.beginPath(); ctx.arc(cx, cy, r, 0, Math.PI * 2); ctx.clip();
    if (state.photo) {
      var im = state.photo, s = Math.max((2 * r) / im.width, (2 * r) / im.height);
      ctx.drawImage(im, cx - (im.width * s) / 2, cy - (im.height * s) / 2, im.width * s, im.height * s);
    } else {
      ctx.fillStyle = "rgba(255,255,255,.6)"; ctx.fillRect(cx - r, cy - r, 2 * r, 2 * r);
      ctx.fillStyle = "rgba(42,22,51,.35)";
      ctx.beginPath(); ctx.arc(cx, cy - r * 0.18, r * 0.32, 0, Math.PI * 2); ctx.fill();
      ctx.beginPath(); ctx.ellipse(cx, cy + r * 0.62, r * 0.6, r * 0.42, 0, 0, Math.PI * 2); ctx.fill();
    }
    ctx.restore();
    if (pal.title !== "gold") {
      ctx.save(); ctx.strokeStyle = pal.accent; ctx.lineWidth = 4; ctx.beginPath(); ctx.arc(cx, cy, r + 12, 0, Math.PI * 2); ctx.stroke(); ctx.restore();
    }
  }

  function drawCard(img) {
    var d = DES[state.design];
    var pal = palette(d);
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, W, H);
    if (img) cover(img);
    else {
      var g = ctx.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, K.theme.primary); g.addColorStop(1, K.theme.secondary);
      ctx.fillStyle = g; ctx.fillRect(0, 0, W, H);
    }
    var z0 = d.zone[0], z1 = d.zone[1], cx = W / 2, maxW = d.w;
    // soft scrim behind the text for readability
    var sc = d.scrim != null ? d.scrim : (d.tone === "dark" ? 0.2 : 0.35);
    if (sc > 0) {
      var my = (z0 + z1) / 2, rad = Math.max(maxW * 0.62, (z1 - z0) * 0.62);
      var rg = ctx.createRadialGradient(cx, my, 10, cx, my, rad);
      var c = d.tone === "dark" ? "0,0,0" : "255,250,242";
      rg.addColorStop(0, "rgba(" + c + "," + sc + ")"); rg.addColorStop(0.65, "rgba(" + c + "," + sc * 0.6 + ")"); rg.addColorStop(1, "rgba(" + c + ",0)");
      ctx.fillStyle = rg;
      ctx.save(); ctx.translate(cx, my); ctx.scale(1, (z1 - z0) / (maxW * 1.1)); ctx.translate(-cx, -my);
      ctx.fillRect(-W, -H * 6, W * 3, H * 13); ctx.restore();
    }
    // photo
    var photoR = 0;
    if (state.photoMode) { photoR = Math.min(150, (z1 - z0) * 0.19); }
    var avail = z1 - z0 - (photoR ? photoR * 2 + 50 : 0);
    var list = blocks(pal), scale = 1, total = measure(list, maxW, scale);
    while (total > avail && scale > 0.5) { scale -= 0.04; total = measure(list, maxW, scale); }
    var y = z0 + Math.max(0, (avail - total) / 2);
    if (photoR) { drawPhoto(cx, y + photoR + 12, photoR, pal); y += photoR * 2 + 50; }
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    list.forEach(function (b) {
      if (b.k === "divider") { drawDivider(cx, y + b.h / 2, pal); y += b.h + b.gap * scale; return; }
      ctx.font = font(b.fam, b.w, b.size);
      if (b.k === "ribbon") {
        var tw = Math.max.apply(null, b.lines.map(function (l) { return ctx.measureText(l).width; })) + 90;
        var rh = b.hh;
        ctx.save();
        ctx.shadowColor = "rgba(0,0,0,.25)"; ctx.shadowBlur = 18; ctx.shadowOffsetY = 6;
        var rgx = ctx.createLinearGradient(cx - tw / 2, 0, cx + tw / 2, 0);
        rgx.addColorStop(0, pal.ribbon[0]); rgx.addColorStop(1, pal.ribbon[1]);
        ctx.fillStyle = rgx; roundRect(cx - tw / 2, y, tw, rh, rh / 2); ctx.fill();
        ctx.restore();
        ctx.fillStyle = pal.ribbonInk;
        b.lines.forEach(function (l, i) { ctx.fillText(l, cx, y + 17 + b.lh * i + b.lh / 2); });
        y += rh + b.gap * scale; return;
      }
      b.lines.forEach(function (l) {
        var ly = y + b.lh / 2;
        ctx.save();
        if (b.k === "title" || b.k === "names") {
          if (pal.title === "gold") {
            ctx.shadowColor = "rgba(0,0,0,.55)"; ctx.shadowBlur = 22; ctx.shadowOffsetY = 6;
            ctx.fillStyle = gold(ly - b.size / 2, ly + b.size / 2);
          } else {
            ctx.shadowColor = "rgba(255,255,255,.9)"; ctx.shadowBlur = 16;
            ctx.fillStyle = pal.title;
          }
          ctx.fillText(l, cx, ly);
          if (pal.title === "gold") { ctx.shadowColor = "transparent"; ctx.lineWidth = 1.2; ctx.strokeStyle = "rgba(120,70,10,.55)"; ctx.strokeText(l, cx, ly); }
        } else if (b.k === "label") {
          ctx.fillStyle = pal.accent;
          ctx.shadowColor = pal.shadow; ctx.shadowBlur = 10;
          if ("letterSpacing" in ctx) ctx.letterSpacing = "4px";
          ctx.fillText(l, cx, ly);
        } else {
          ctx.shadowColor = pal.shadow; ctx.shadowBlur = d.tone === "dark" ? 14 : 12;
          ctx.fillStyle = b.k === "from" ? pal.accent : b.k === "thought" ? pal.soft : pal.text;
          ctx.fillText(l, cx, ly);
        }
        ctx.restore();
        y += b.lh;
      });
      y += b.gap * scale;
    });
    // footer mark
    ctx.save();
    ctx.font = font(FB, 600, 24);
    ctx.fillStyle = d.tone === "dark" ? "rgba(255,248,236,.7)" : "rgba(42,22,51,.55)";
    ctx.shadowColor = d.tone === "dark" ? "rgba(0,0,0,.6)" : "rgba(255,255,255,.8)"; ctx.shadowBlur = 8;
    ctx.fillText("indianfestivalwishes.com", cx, H - 34);
    ctx.restore();
    ctx.restore();
  }

  /* ---------------- fonts + redraw ---------------- */
  function fontsReady() {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    var all = [];
    Object.keys(K.wishes).forEach(function (k) { all = all.concat(K.wishes[k]); });
    var sample = K.title + (K.topLabel || "") + K.fromTpl + all.join("") + (K.thoughts || []).join("") + state.to + state.n1 + state.n2 + state.from;
    return Promise.all([
      document.fonts.load(font(FD, FDW, 100), sample),
      document.fonts.load(font(FB, 600, 40), sample), document.fonts.load(font(FB, 700, 40), sample)
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
    });
    // warm the cache for neighbours
    [state.design + 1, state.design - 1].forEach(function (i) { if (DES[i]) loadImg(DES[i].id); });
  }

  /* ---------------- sharing ---------------- */
  var relSel = $("card-rel"), wishSel = $("card-wish"), err = $("card-error"), status = $("card-status"), shareBox = $("share-actions");
  var photoBox = $("photo-box"), photoIn = $("card-photo");
  var modeBtns = document.querySelectorAll("[data-photo-mode]");
  var nextThought = $("next-thought"), thoughtText = $("thought-text");
  var dzBtns = Array.prototype.slice.call(document.querySelectorAll("#design-row .dz"));

  function link() {
    var q = new URLSearchParams();
    if (state.from) q.set("name", state.from);
    if (state.to) q.set("to", state.to);
    if (state.n1) q.set("n1", state.n1);
    if (state.n2) q.set("n2", state.n2);
    q.set("r", state.rel); q.set("w", String(state.wish)); q.set("s", String(state.design));
    if (K.thoughts) q.set("t", String(state.thought));
    return location.origin + location.pathname + "?" + q.toString();
  }
  function refreshLinks() {
    $("btn-wa").href = "https://wa.me/?text=" + encodeURIComponent(U.share_link_msg + "\n" + link());
    $("btn-fb").href = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(link());
  }
  function fileName() { return (K.slug || "card") + "-indianfestivalwishes.png"; }
  function toBlob() { return new Promise(function (res) { canvas.toBlob(res, "image/png"); }); }
  function save(blob) {
    var url = URL.createObjectURL(blob), a = document.createElement("a");
    a.href = url; a.download = fileName(); document.body.appendChild(a); a.click(); a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
  }
  var canShareFiles = false;
  try { canShareFiles = !!(navigator.canShare && navigator.canShare({ files: [new File([new Blob(["x"], { type: "image/png" })], "t.png", { type: "image/png" })] })); } catch (e) {}
  function shareFile() {
    return toBlob().then(function (b) {
      if (canShareFiles) return navigator.share({ files: [new File([b], fileName(), { type: "image/png" })] }).catch(function () {});
      save(b);
      status.textContent = U.insta_hint;
    });
  }

  function val(id) { var el = $(id); return el ? clean(el.value) : ""; }
  function fillWishes() {
    var list = K.wishes[state.rel] || [];
    wishSel.innerHTML = "";
    list.forEach(function (w, i) {
      var o = document.createElement("option"); o.value = String(i); o.textContent = w; wishSel.appendChild(o);
    });
    if (state.wish >= list.length) state.wish = 0;
    wishSel.value = String(state.wish);
  }

  // Extra wishes and thoughts added from the admin panel
  if (window.IFW_SETTINGS) {
    window.IFW_SETTINGS.then(function (S) {
      var cu = (S && S.custom) || {};
      var extra = ((cu.wishes || {})[D.lang] || {})[K.occasion] || {};
      var changed = false;
      Object.keys(extra).forEach(function (rel) {
        if (!Array.isArray(extra[rel]) || !K.wishes[rel]) return;
        extra[rel].forEach(function (w) {
          if (typeof w === "string" && w.trim()) { K.wishes[rel].push(w.trim().slice(0, 160)); changed = true; }
        });
      });
      var th = (cu.thoughts || {})[D.lang];
      if (K.thoughts && Array.isArray(th)) {
        th.forEach(function (t) { if (typeof t === "string" && t.trim()) { K.thoughts.push(t.trim().slice(0, 160)); changed = true; } });
      }
      if (changed) { fillWishes(); redraw(); }
    });
  }

  function selectDesign(i, focus) {
    state.design = i;
    dzBtns.forEach(function (x, j) { x.setAttribute("aria-pressed", j === i ? "true" : "false"); });
    if (focus && dzBtns[i]) dzBtns[i].scrollIntoView({ behavior: "smooth", block: "nearest", inline: "center" });
    redraw(); if (state.made) refreshLinks();
  }
  dzBtns.forEach(function (b, i) { b.addEventListener("click", function () { selectDesign(i); }); });
  if (dzBtns[state.design]) dzBtns.forEach(function (x, j) { x.setAttribute("aria-pressed", j === state.design ? "true" : "false"); });

  // swipe on the preview to change design
  var sx = null;
  canvas.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; }, { passive: true });
  canvas.addEventListener("touchend", function (e) {
    if (sx == null) return;
    var dx = e.changedTouches[0].clientX - sx; sx = null;
    if (Math.abs(dx) > 50) selectDesign((state.design + (dx < 0 ? 1 : -1) + DES.length) % DES.length, true);
  }, { passive: true });

  relSel.value = state.rel;
  relSel.addEventListener("change", function () { state.rel = relSel.value; state.wish = 0; fillWishes(); redraw(); if (state.made) refreshLinks(); });
  wishSel.addEventListener("change", function () { state.wish = parseInt(wishSel.value, 10) || 0; redraw(); if (state.made) refreshLinks(); });
  fillWishes();

  if (nextThought && K.thoughts) {
    var showThought = function () { if (thoughtText) thoughtText.textContent = K.thoughts[state.thought]; };
    showThought();
    nextThought.addEventListener("click", function () {
      state.thought = (state.thought + 1) % K.thoughts.length; showThought(); redraw(); if (state.made) refreshLinks();
    });
  }

  if (photoBox) {
    modeBtns.forEach(function (b) {
      b.addEventListener("click", function () {
        state.photoMode = b.getAttribute("data-photo-mode") === "with";
        modeBtns.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        $("photo-pick").hidden = !state.photoMode;
        redraw();
      });
    });
    photoIn.addEventListener("change", function () {
      var f = photoIn.files && photoIn.files[0];
      if (!f) return;
      var img = new Image();
      img.onload = function () { state.photo = img; state.photoMode = true; redraw(); };
      img.src = URL.createObjectURL(f);
    });
  }

  // live preview while typing
  ["in-from", "in-to", "in-n1", "in-n2"].forEach(function (id) {
    var el = $(id);
    if (!el) return;
    el.addEventListener("input", function () {
      state[{ "in-from": "from", "in-to": "to", "in-n1": "n1", "in-n2": "n2" }[id]] = val(id);
      redraw();
    });
  });
  if ($("in-from") && !received) $("in-from").value = state.from;

  $("card-form").addEventListener("submit", function (e) {
    e.preventDefault();
    var from = val("in-from"), to = val("in-to"), n1 = val("in-n1"), n2 = val("in-n2");
    var ok = K.kind === "festival" ? !!from : K.kind === "person" ? !!to : K.kind === "couple" ? !!(n1 && n2) : true;
    if (!ok) { err.textContent = U.need_name; return; }
    err.textContent = "";
    state.from = from; state.to = to; state.n1 = n1; state.n2 = n2;
    state.made = true;
    shareBox.hidden = false;
    status.textContent = "";
    refreshLinks();
    redraw();
    if (window.innerWidth < 900) canvas.scrollIntoView({ behavior: "smooth", block: "center" });
  });

  $("btn-ig").addEventListener("click", shareFile);
  $("btn-share-photo").hidden = !canShareFiles;
  $("btn-share-photo").addEventListener("click", shareFile);
  $("btn-download").addEventListener("click", function () { toBlob().then(save); });
  $("btn-copy-link").addEventListener("click", function () {
    var t = link();
    (navigator.clipboard && window.isSecureContext ? navigator.clipboard.writeText(t) : Promise.reject()).then(function () {
      status.textContent = U.copied_link;
    }).catch(function () { window.prompt("", t); });
  });

  if (received) {
    $("card-heading").textContent = U.card_heading_received;
    $("received-note").textContent = U.card_now_yours;
  }
  redraw();
})();
