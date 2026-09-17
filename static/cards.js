/* Indian Festival Wishes: card maker (10 styles, optional photo, relation-based wishes) */
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
  var F = D.font;
  var T = K.theme; // primary, secondary, ink, accent
  function lum(hex) { var n = parseInt(hex.slice(1), 16); return (0.299 * (n >> 16) + 0.587 * ((n >> 8) & 255) + 0.114 * (n & 255)) / 255; }
  // strong colour for styles that put the theme colour on a light background
  var PR = lum(T.primary) > 0.7 ? T.accent : T.primary;

  function $(id) { return document.getElementById(id); }
  function fmt(s, o) { return String(s).replace(/\{(\w+)\}/g, function (_, k) { return o[k] != null ? o[k] : ""; }); }
  function clean(v) { return String(v || "").replace(/[\u0000-\u001F\u007F<>"`]/g, "").replace(/\s+/g, " ").trim().slice(0, 30); }
  function rgba(hex, a) {
    var n = parseInt(hex.slice(1), 16);
    return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
  }
  function mix(hex, to, t) {
    var a = parseInt(hex.slice(1), 16), b = parseInt(to.slice(1), 16);
    var r = Math.round((a >> 16) * (1 - t) + (b >> 16) * t);
    var g = Math.round(((a >> 8) & 255) * (1 - t) + ((b >> 8) & 255) * t);
    var bl = Math.round((a & 255) * (1 - t) + (b & 255) * t);
    return "#" + ((1 << 24) + (r << 16) + (g << 8) + bl).toString(16).slice(1);
  }
  function rng(seed) { var s = seed; return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; }

  /* ---------------- state ---------------- */
  var P = new URLSearchParams(location.search);
  var relKeys = K.rels.map(function (r) { return r[0]; });
  var state = {
    style: Math.min(9, Math.max(0, parseInt(P.get("s"), 10) || 0)),
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

  /* ---------------- text helpers ---------------- */
  function setFont(c, w, s) { c.font = w + " " + s + "px " + F; }
  function wrap(c, text, maxW) {
    var words = String(text).split(" "), lines = [], line = "";
    words.forEach(function (w) {
      var t = line ? line + " " + w : w;
      if (c.measureText(t).width > maxW && line) { lines.push(line); line = w; } else line = t;
    });
    if (line) lines.push(line);
    return lines;
  }
  function roundRect(c, x, y, w, h, r) {
    c.beginPath();
    c.moveTo(x + r, y); c.arcTo(x + w, y, x + w, y + h, r); c.arcTo(x + w, y + h, x, y + h, r);
    c.arcTo(x, y + h, x, y, r); c.arcTo(x, y, x + w, y, r); c.closePath();
  }

  // Build text items for the current card, then fit them into the area.
  function items(col) {
    var list = [];
    if (K.topLabel) list.push({ t: K.topLabel, w: 600, s: 34, c: col.label, max: 1, gap: 14 });
    list.push({ t: K.title, w: 800, s: K.kind === "festival" ? 96 : 88, c: col.title, max: 1, gap: 16 });
    if (K.kind === "person" && state.to) list.push({ t: state.to, w: 800, s: 84, c: col.accent, max: 1, gap: 18 });
    if (K.kind === "couple" && (state.n1 || state.n2)) {
      list.push({ t: [state.n1, state.n2].filter(Boolean).join("  ♥  "), w: 800, s: 72, c: col.accent, max: 2, gap: 18 });
    }
    if (K.kind === "morning" && K.thoughts) {
      list.push({ t: "“" + K.thoughts[state.thought] + "”", w: 700, s: 54, c: col.title, max: 4, gap: 18 });
    }
    var wish = (K.wishes[state.rel] || [])[state.wish] || "";
    if (wish) list.push({ t: wish, w: 600, s: K.kind === "morning" ? 36 : 42, c: col.body, max: 4, gap: 22 });
    if (state.from) list.push({ t: fmt(K.fromTpl, { from: state.from, name: state.from }), w: 700, s: 38, c: col.boxText, max: 2, box: col.boxFill, gap: 0 });
    return list;
  }

  function layout(c, list, maxW, scale) {
    var total = 0;
    list.forEach(function (it) {
      it.size = Math.round(it.s * scale);
      setFont(c, it.w, it.size);
      var s = it.size;
      it.lines = wrap(c, it.t, it.box ? maxW - 80 : maxW);
      while ((it.lines.length > it.max || it.lines.some(function (l) { return c.measureText(l).width > (it.box ? maxW - 80 : maxW); })) && s > 22) {
        s -= 2; setFont(c, it.w, s); it.lines = wrap(c, it.t, it.box ? maxW - 80 : maxW);
      }
      it.size = s;
      it.lines = it.lines.slice(0, it.max);
      it.lh = s * 1.3;
      it.h = it.lines.length * it.lh + (it.box ? 40 : 0);
      total += it.h + it.gap * scale;
    });
    return total;
  }

  function drawText(c, area, col) {
    var list = items(col);
    var maxW = area.x1 - area.x0;
    var avail = area.bottom - area.top;
    var scale = 1.3, total = layout(c, list, maxW, scale);
    while (total > avail * 0.92 && scale > 0.55) { scale -= 0.05; total = layout(c, list, maxW, scale); }
    var y = area.top + Math.max(0, (avail - total) / 2);
    var cx = (area.x0 + area.x1) / 2;
    c.textAlign = "center";
    c.textBaseline = "middle";
    list.forEach(function (it) {
      setFont(c, it.w, it.size);
      if (it.box) {
        var widest = Math.max.apply(null, it.lines.map(function (l) { return c.measureText(l).width; }));
        var bw = Math.min(maxW, widest + 80), bh = it.h;
        roundRect(c, cx - bw / 2, y, bw, bh, Math.min(34, bh / 2));
        c.fillStyle = it.box; c.fill();
        var yy = y + 20;
        it.lines.forEach(function (l) { c.fillStyle = it.c; c.fillText(l, cx, yy + it.lh / 2 + 2); yy += it.lh; });
      } else {
        var yy2 = y;
        it.lines.forEach(function (l) {
          if (col.glow) { c.shadowColor = col.glow; c.shadowBlur = 18; }
          c.fillStyle = it.c; c.fillText(l, cx, yy2 + it.lh / 2 + 2);
          c.shadowBlur = 0;
          yy2 += it.lh;
        });
      }
      y += it.h + it.gap * scale;
    });
  }

  function host(c, color, y) {
    c.textAlign = "center"; c.textBaseline = "middle";
    setFont(c, 600, 26); c.fillStyle = color;
    c.fillText(location.host || "indianfestivalwishes.com", W / 2, y);
  }

  /* ---------------- motifs ---------------- */
  function heart(c, x, y, s, color) {
    c.beginPath();
    c.moveTo(x, y + s * 0.35);
    c.bezierCurveTo(x - s, y - s * 0.3, x - s * 0.45, y - s, x, y - s * 0.45);
    c.bezierCurveTo(x + s * 0.45, y - s, x + s, y - s * 0.3, x, y + s * 0.35);
    c.fillStyle = color; c.fill();
  }
  function flame(c, x, y, s, color) {
    c.beginPath(); c.moveTo(x, y - s);
    c.quadraticCurveTo(x + s * 0.7, y, x, y + s * 0.65);
    c.quadraticCurveTo(x - s * 0.7, y, x, y - s);
    c.fillStyle = color; c.fill();
  }
  function diya(c, x, y, s, bowl, fl) {
    c.beginPath(); c.moveTo(x - s, y); c.quadraticCurveTo(x, y + s * 1.1, x + s, y); c.closePath();
    c.fillStyle = bowl; c.fill();
    flame(c, x, y - s * 0.45, s * 0.45, fl);
  }
  function mandala(c, r, ink, acc, bg, num) {
    [{ n: 16, rx: 0.16, ry: 0.42, d: 0.58, a: 0.2 }, { n: 12, rx: 0.13, ry: 0.32, d: 0.38, a: 0.35 }].forEach(function (g) {
      for (var i = 0; i < g.n; i++) {
        c.save(); c.rotate((Math.PI * 2 * i) / g.n);
        c.beginPath(); c.ellipse(0, -r * g.d, r * g.rx, r * g.ry, 0, 0, Math.PI * 2);
        c.fillStyle = rgba(ink, g.a); c.fill(); c.restore();
      }
    });
    c.beginPath(); c.arc(0, 0, r * 0.3, 0, Math.PI * 2); c.fillStyle = acc; c.fill();
    c.beginPath(); c.arc(0, 0, r * 0.25, 0, Math.PI * 2); c.fillStyle = bg; c.fill();
    if (num) {
      c.fillStyle = ink; c.textAlign = "center"; c.textBaseline = "middle";
      setFont(c, 800, Math.round(r * 0.34)); c.fillText(String(num), 0, r * 0.03);
    } else flame(c, 0, 0, r * 0.18, acc);
  }
  function symbol(c, day, col, acc) {
    c.fillStyle = col; c.strokeStyle = col; c.lineWidth = 12; c.lineCap = "round"; c.lineJoin = "round";
    var i;
    switch (day) {
      case 1:
        c.fillRect(-6, -40, 12, 140);
        c.beginPath(); c.moveTo(0, -100); c.lineTo(14, -60); c.lineTo(-14, -60); c.closePath(); c.fill();
        c.beginPath(); c.moveTo(-60, -85); c.quadraticCurveTo(-60, -30, 0, -35); c.quadraticCurveTo(60, -30, 60, -85); c.stroke();
        c.fillStyle = acc; c.fillRect(-18, -20, 36, 12); break;
      case 2:
        for (i = 0; i < 22; i++) { var a = (Math.PI * 2 * i) / 22; c.beginPath(); c.arc(Math.cos(a) * 62, Math.sin(a) * 62 - 20, 9, 0, Math.PI * 2); c.fill(); }
        c.fillStyle = acc; c.beginPath(); c.arc(0, 52, 12, 0, Math.PI * 2); c.fill(); break;
      case 3:
        c.beginPath(); c.moveTo(-55, 55); c.quadraticCurveTo(-50, -40, 0, -45); c.quadraticCurveTo(50, -40, 55, 55); c.closePath(); c.fill();
        c.fillRect(-70, 50, 140, 14);
        c.fillStyle = acc; c.beginPath(); c.arc(0, 80, 14, 0, Math.PI * 2); c.fill(); break;
      case 4:
        for (i = 0; i < 12; i++) { c.save(); c.rotate((Math.PI * 2 * i) / 12); c.beginPath(); c.moveTo(-12, -58); c.lineTo(0, -98); c.lineTo(12, -58); c.closePath(); c.fill(); c.restore(); }
        c.beginPath(); c.arc(0, 0, 48, 0, Math.PI * 2); c.fill();
        c.fillStyle = acc; c.beginPath(); c.arc(0, 0, 30, 0, Math.PI * 2); c.fill(); break;
      case 5:
        [-60, -30, 0, 30, 60].forEach(function (deg, k) {
          c.save(); c.translate(0, 40); c.rotate(deg * Math.PI / 180);
          c.beginPath(); c.ellipse(0, -55, 22, 58, 0, 0, Math.PI * 2); c.fillStyle = k === 2 ? acc : col; c.fill(); c.restore();
        }); break;
      case 6:
        c.beginPath(); c.moveTo(-8, 40); c.lineTo(8, 40); c.quadraticCurveTo(24, -40, 0, -100); c.quadraticCurveTo(-10, -40, -8, 40); c.fill();
        c.fillStyle = acc; c.fillRect(-40, 40, 80, 12); c.fillStyle = col; c.fillRect(-7, 52, 14, 40); break;
      case 7:
        diya(c, 0, 30, 70, col, acc); flame(c, 0, -40, 40, acc); break;
      case 8:
        c.beginPath(); c.moveTo(-50, -60); c.lineTo(50, -60); c.lineTo(0, 0); c.closePath(); c.fill();
        c.beginPath(); c.moveTo(-50, 60); c.lineTo(50, 60); c.lineTo(0, 0); c.closePath(); c.fill();
        c.fillStyle = acc; c.beginPath(); c.arc(78, -12, 10, 0, Math.PI * 2); c.arc(-78, -12, 10, 0, Math.PI * 2); c.fill(); break;
      default:
        c.beginPath(); c.arc(0, 0, 80, 0, Math.PI * 2); c.stroke();
        for (i = 0; i < 12; i++) { c.save(); c.rotate((Math.PI * 2 * i) / 12); c.fillRect(-3, -76, 6, 60); c.restore(); }
        c.fillStyle = acc; c.beginPath(); c.arc(0, 0, 18, 0, Math.PI * 2); c.fill();
    }
  }
  // Draw the occasion motif centred at 0,0 inside a ~220px box
  function motif(c, p, s) {
    var kind = K.motif;
    if (kind === "devi" && s === 0) kind = "mandala";
    if (kind === "mandala") { mandala(c, 110, p.ink, p.acc, p.bg, K.dayNum); return; }
    if (kind === "devi") { c.scale(0.95, 0.95); symbol(c, K.dayNum, p.main, p.acc); return; }
    if (kind === "cake") {
      c.fillStyle = p.main; roundRect(c, -90, 10, 180, 70, 14); c.fill();
      c.fillStyle = p.acc; roundRect(c, -70, -45, 140, 60, 12); c.fill();
      c.fillStyle = "#FFFFFF"; for (var i = -60; i <= 60; i += 30) { c.beginPath(); c.arc(i, 12, 10, 0, Math.PI); c.fill(); }
      for (var k = -40; k <= 40; k += 40) { c.fillStyle = p.main; c.fillRect(k - 5, -85, 10, 40); flame(c, k, -100, 14, "#F2A007"); }
      return;
    }
    if (kind === "hearts") { heart(c, -35, 10, 80, p.main); heart(c, 40, -10, 70, p.acc); return; }
    if (kind === "rings") {
      c.lineWidth = 16; c.strokeStyle = p.acc; c.beginPath(); c.arc(-35, 20, 55, 0, Math.PI * 2); c.stroke();
      c.strokeStyle = p.main; c.beginPath(); c.arc(35, 20, 55, 0, Math.PI * 2); c.stroke();
      c.fillStyle = "#FFFFFF"; c.beginPath(); c.moveTo(35, -55); c.lineTo(55, -35); c.lineTo(35, -15); c.lineTo(15, -35); c.closePath(); c.fill();
      c.strokeStyle = p.main; c.lineWidth = 4; c.stroke(); return;
    }
    if (kind === "kalash") {
      c.fillStyle = p.acc; c.beginPath(); c.moveTo(-40, -40); c.lineTo(40, -40); c.quadraticCurveTo(110, 20, 50, 90); c.lineTo(-50, 90); c.quadraticCurveTo(-110, 20, -40, -40); c.fill();
      c.fillStyle = p.main; c.fillRect(-60, 20, 120, 14);
      c.fillStyle = "#2E7D32"; for (var j = -2; j <= 2; j++) { c.save(); c.translate(0, -45); c.rotate(j * 0.45); c.beginPath(); c.ellipse(0, -35, 12, 38, 0, 0, Math.PI * 2); c.fill(); c.restore(); }
      c.fillStyle = "#8D5524"; c.beginPath(); c.ellipse(0, -60, 32, 36, 0, 0, Math.PI * 2); c.fill();
      return;
    }
    if (kind === "sun") {
      c.fillStyle = p.acc;
      for (var r = 0; r < 12; r++) { c.save(); c.rotate(r * Math.PI / 6); c.beginPath(); c.moveTo(-10, -70); c.lineTo(0, -110); c.lineTo(10, -70); c.fill(); c.restore(); }
      c.beginPath(); c.arc(0, 0, 60, 0, Math.PI * 2); c.fillStyle = p.main; c.fill();
      c.fillStyle = "#FFFFFF"; c.fillRect(-100, 70, 200, 8); c.fillRect(-70, 90, 140, 8);
    }
  }

  /* ---------------- slot (photo or motif) ---------------- */
  function clipShape(c, sl) {
    c.beginPath();
    if (sl.shape === "circle") c.arc(sl.cx, sl.cy, sl.w / 2, 0, Math.PI * 2);
    else if (sl.shape === "arch") {
      var x = sl.cx - sl.w / 2, y = sl.cy - sl.h / 2;
      c.moveTo(x, y + sl.h); c.lineTo(x, y + sl.w / 2); c.arc(sl.cx, y + sl.w / 2, sl.w / 2, Math.PI, 0); c.lineTo(x + sl.w, y + sl.h); c.closePath();
    } else roundRect(c, sl.cx - sl.w / 2, sl.cy - sl.h / 2, sl.w, sl.h, sl.shape === "rounded" ? 36 : 6);
  }
  function drawSlot(c, sl, p) {
    c.save();
    clipShape(c, sl);
    if (state.photoMode && state.photo) {
      c.clip();
      var im = state.photo, sc = Math.max(sl.w / im.width, sl.h / im.height);
      c.drawImage(im, sl.cx - (im.width * sc) / 2, sl.cy - (im.height * sc) / 2, im.width * sc, im.height * sc);
    } else {
      c.fillStyle = p.fill; c.fill();
      c.clip();
      c.translate(sl.cx, sl.cy);
      var k = Math.min(sl.w, sl.h) / 260;
      c.scale(k, k);
      motif(c, p, state.style);
    }
    c.restore();
    if (sl.ring) {
      c.save(); clipShape(c, sl); c.lineWidth = sl.ringW || 10; c.strokeStyle = sl.ring; c.stroke(); c.restore();
    }
  }

  /* ---------------- decorations ---------------- */
  function bandhani(c, ink, acc) {
    for (var x = 40; x <= W - 40; x += 30) { dot(x, 40, x); dot(x, H - 40, x); }
    for (var y = 70; y < H - 40; y += 30) { dot(40, y, y); dot(W - 40, y, y); }
    function dot(x, y, i) {
      var odd = Math.round(i / 30) % 2;
      c.beginPath(); c.arc(x, y, odd ? 5 : 7, 0, Math.PI * 2);
      c.fillStyle = odd ? rgba(ink, 0.5) : acc; c.fill();
    }
  }
  function toran(c) {
    function ry(x) { var u = x / W; return 70 + Math.sin(u * Math.PI * 4) * 18 + 30 * Math.sin(u * Math.PI); }
    c.strokeStyle = "#2E7D32"; c.lineWidth = 4; c.beginPath();
    for (var x = 40; x <= W - 40; x += 8) { if (x === 40) c.moveTo(x, ry(x)); else c.lineTo(x, ry(x)); }
    c.stroke();
    for (x = 64; x < W - 44; x += 42) {
      var y = ry(x);
      c.beginPath(); c.moveTo(x, y + 6); c.lineTo(x - 11, y + 30); c.lineTo(x + 11, y + 30); c.closePath(); c.fillStyle = "#2E7D32"; c.fill();
      c.beginPath(); c.arc(x, y, 16, 0, Math.PI * 2); c.fillStyle = (x / 42) % 2 < 1 ? "#F29100" : "#F7C21A"; c.fill();
      c.beginPath(); c.arc(x, y, 5, 0, Math.PI * 2); c.fillStyle = "#B3122E"; c.fill();
    }
    for (x = 150; x < W - 100; x += 195) {
      var t = ry(x);
      for (var j = 1; j <= 3; j++) { c.beginPath(); c.arc(x, t + j * 30, 12, 0, Math.PI * 2); c.fillStyle = j % 2 ? "#F7C21A" : "#F29100"; c.fill(); }
    }
  }
  function flower(c, x, y, r, col, center) {
    for (var i = 0; i < 6; i++) {
      var a = i * Math.PI / 3;
      c.beginPath(); c.arc(x + Math.cos(a) * r, y + Math.sin(a) * r, r * 0.8, 0, Math.PI * 2);
      c.fillStyle = col; c.fill();
    }
    c.beginPath(); c.arc(x, y, r * 0.7, 0, Math.PI * 2); c.fillStyle = center; c.fill();
  }

  /* ---------------- the 10 styles ---------------- */
  var dark = "#2B1B14", white = "#FFFFFF";
  var STYLES = [
    // 1 Classic
    function (c) {
      c.fillStyle = T.primary; c.fillRect(0, 0, W, H);
      var g = c.createRadialGradient(W / 2, 320, 40, W / 2, 320, 640);
      g.addColorStop(0, "rgba(255,255,255,0.25)"); g.addColorStop(1, "rgba(255,255,255,0)");
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      bandhani(c, T.ink, T.accent);
      c.strokeStyle = rgba(T.ink, 0.35); c.lineWidth = 2; c.strokeRect(72, 72, W - 144, H - 144);
      drawSlot(c, { cx: W / 2, cy: 330, w: 400, h: 400, shape: "circle", ring: T.accent, ringW: 10 },
        { fill: rgba(T.ink === white ? "#FFFFFF" : "#FFFFFF", 0.22), main: T.ink, acc: T.accent, ink: T.ink, bg: T.primary });
      drawText(c, { top: 560, bottom: 1215, x0: 130, x1: W - 130 },
        { label: rgba(T.ink, 0.85), title: T.ink, accent: T.ink, body: T.ink, boxFill: T.ink, boxText: T.primary });
      host(c, rgba(T.ink, 0.7), H - 105);
    },
    // 2 Royal
    function (c) {
      var g = c.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, mix(PR, "#000000", 0.55)); g.addColorStop(1, mix(PR, "#000000", 0.2));
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      var gold = "#E9B949";
      c.strokeStyle = gold; c.lineWidth = 6; c.strokeRect(40, 40, W - 80, H - 80);
      c.lineWidth = 2; c.strokeRect(62, 62, W - 124, H - 124);
      [[62, 62], [W - 62, 62], [62, H - 62], [W - 62, H - 62]].forEach(function (p) {
        c.beginPath(); c.arc(p[0], p[1], 26, 0, Math.PI * 2); c.fillStyle = gold; c.fill();
        c.beginPath(); c.arc(p[0], p[1], 12, 0, Math.PI * 2); c.fillStyle = mix(PR, "#000000", 0.4); c.fill();
      });
      drawSlot(c, { cx: W / 2, cy: 330, w: 340, h: 420, shape: "arch", ring: gold, ringW: 8 },
        { fill: rgba("#FFFFFF", 0.1), main: gold, acc: T.secondary, ink: gold, bg: mix(PR, "#000000", 0.4) });
      drawText(c, { top: 570, bottom: 1210, x0: 130, x1: W - 130 },
        { label: rgba("#FFFFFF", 0.75), title: gold, accent: "#FFFFFF", body: "#FFF6E0", boxFill: gold, boxText: "#2B1B14" });
      host(c, rgba(gold, 0.85), H - 100);
    },
    // 3 Pastel
    function (c) {
      var g = c.createLinearGradient(0, 0, W, H);
      g.addColorStop(0, mix(PR, "#FFFFFF", 0.78)); g.addColorStop(1, mix(T.secondary, "#FFFFFF", 0.7));
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      var r = rng(7);
      for (var i = 0; i < 26; i++) { c.beginPath(); c.arc(r() * W, r() * H, 20 + r() * 70, 0, Math.PI * 2); c.fillStyle = "rgba(255,255,255," + (0.15 + r() * 0.3) + ")"; c.fill(); }
      c.fillStyle = "rgba(255,255,255,0.88)"; roundRect(c, 70, 560, W - 140, 690, 40); c.fill();
      drawSlot(c, { cx: W / 2, cy: 300, w: 440, h: 380, shape: "rounded", ring: "#FFFFFF", ringW: 14 },
        { fill: rgba("#FFFFFF", 0.7), main: PR, acc: T.secondary, ink: PR, bg: "#FFFFFF" });
      var deep = mix(PR, "#000000", 0.2);
      drawText(c, { top: 590, bottom: 1220, x0: 120, x1: W - 120 },
        { label: rgba(dark, 0.6), title: deep, accent: mix(T.secondary, "#000000", 0.25), body: dark, boxFill: deep, boxText: white });
      host(c, rgba(dark, 0.55), H - 45);
    },
    // 4 Confetti
    function (c) {
      c.fillStyle = "#FFFFFF"; c.fillRect(0, 0, W, H);
      var r = rng(42), cols = [PR, T.secondary, "#F2A007", "#2EC4B6", "#FF5D8F"];
      for (var i = 0; i < 140; i++) {
        c.save(); c.translate(r() * W, r() * H); c.rotate(r() * Math.PI);
        c.fillStyle = cols[i % cols.length];
        if (i % 3) c.fillRect(-8, -3, 16 + r() * 10, 6); else { c.beginPath(); c.arc(0, 0, 5 + r() * 5, 0, Math.PI * 2); c.fill(); }
        c.restore();
      }
      c.fillStyle = "rgba(255,255,255,0.9)"; roundRect(c, 90, 580, W - 180, 640, 30); c.fill();
      drawSlot(c, { cx: W / 2, cy: 320, w: 400, h: 400, shape: "circle", ring: PR, ringW: 14 },
        { fill: mix(T.secondary, "#FFFFFF", 0.8), main: PR, acc: T.secondary, ink: PR, bg: "#FFFFFF" });
      drawText(c, { top: 600, bottom: 1200, x0: 130, x1: W - 130 },
        { label: rgba(dark, 0.6), title: PR, accent: mix(T.secondary, "#000000", 0.2), body: dark, boxFill: PR, boxText: white });
      host(c, rgba(dark, 0.6), H - 50);
    },
    // 5 Floral
    function (c) {
      c.fillStyle = "#FFF8F0"; c.fillRect(0, 0, W, H);
      var fc = [PR, T.secondary, mix(PR, "#FFFFFF", 0.4)];
      [[40, 40], [W - 40, 40], [40, H - 40], [W - 40, H - 40]].forEach(function (p, k) {
        for (var i = 0; i < 5; i++) {
          c.save(); c.translate(p[0], p[1]);
          var ang = (k * Math.PI / 2) + i * 0.35, dist = 40 + i * 42;
          c.beginPath(); c.ellipse(Math.cos(ang) * dist, Math.sin(ang) * dist, 30, 12, ang, 0, Math.PI * 2);
          c.fillStyle = "#5B8C51"; c.fill(); c.restore();
        }
        flower(c, p[0] + (k % 2 ? -40 : 40), p[1] + (k < 2 ? 40 : -40), 34, fc[k % 3], "#F7C21A");
        flower(c, p[0] + (k % 2 ? -110 : 110), p[1] + (k < 2 ? 20 : -20), 22, fc[(k + 1) % 3], "#FFFFFF");
      });
      drawSlot(c, { cx: W / 2, cy: 320, w: 390, h: 390, shape: "circle", ring: T.secondary, ringW: 8 },
        { fill: mix(PR, "#FFFFFF", 0.85), main: PR, acc: T.secondary, ink: PR, bg: "#FFF8F0" });
      var deep = mix(PR, "#000000", 0.15);
      drawText(c, { top: 560, bottom: 1190, x0: 150, x1: W - 150 },
        { label: rgba(dark, 0.6), title: deep, accent: mix(T.secondary, "#000000", 0.3), body: dark, boxFill: deep, boxText: white });
      host(c, rgba(dark, 0.55), H - 110);
    },
    // 6 Starry night
    function (c) {
      var g = c.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, "#0B1437"); g.addColorStop(1, mix(PR, "#0B1437", 0.6));
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      var r = rng(99);
      for (var i = 0; i < 160; i++) { c.beginPath(); c.arc(r() * W, r() * H, r() * 2.6 + 0.4, 0, Math.PI * 2); c.fillStyle = "rgba(255,255,255," + (0.3 + r() * 0.7) + ")"; c.fill(); }
      c.beginPath(); c.arc(900, 150, 55, 0, Math.PI * 2); c.fillStyle = "#FFE9A8"; c.fill();
      c.beginPath(); c.arc(925, 135, 50, 0, Math.PI * 2); c.fillStyle = "#0B1437"; c.fill();
      var gold = "#F4C95D";
      drawSlot(c, { cx: W / 2, cy: 330, w: 380, h: 380, shape: "circle", ring: gold, ringW: 8 },
        { fill: rgba("#FFFFFF", 0.1), main: gold, acc: T.secondary, ink: gold, bg: "#0B1437" });
      drawText(c, { top: 560, bottom: 1220, x0: 120, x1: W - 120 },
        { label: rgba("#FFFFFF", 0.7), title: gold, accent: "#FFFFFF", body: "#E8ECFF", boxFill: gold, boxText: "#0B1437", glow: "rgba(244,201,93,0.35)" });
      host(c, rgba("#FFFFFF", 0.6), H - 50);
    },
    // 7 Modern split
    function (c) {
      c.fillStyle = "#FFFFFF"; c.fillRect(0, 0, W, H);
      c.fillStyle = PR; c.beginPath(); c.moveTo(0, 0); c.lineTo(W, 0); c.lineTo(W, 470); c.lineTo(0, 560); c.closePath(); c.fill();
      c.fillStyle = T.accent; c.fillRect(0, H - 22, W, 22);
      c.textAlign = "left"; c.textBaseline = "alphabetic"; setFont(c, 800, 150); c.fillStyle = rgba(T.ink, 0.12);
      c.fillText(K.dayNum ? String(K.dayNum) : "✦", 60, 200);
      drawSlot(c, { cx: W / 2, cy: 300, w: 380, h: 380, shape: "circle", ring: "#FFFFFF", ringW: 16 },
        { fill: mix(PR, "#FFFFFF", 0.82), main: PR, acc: T.secondary, ink: PR, bg: "#FFFFFF" });
      drawText(c, { top: 570, bottom: 1250, x0: 110, x1: W - 110 },
        { label: rgba(dark, 0.55), title: dark, accent: PR === "#F7F3EE" ? T.accent : mix(PR, "#000000", 0.1), body: rgba(dark, 0.85), boxFill: PR === "#F7F3EE" ? dark : PR, boxText: PR === "#F7F3EE" ? white : T.ink });
      host(c, rgba(dark, 0.5), H - 48);
    },
    // 8 Polaroid
    function (c) {
      c.fillStyle = "#EFE3D0"; c.fillRect(0, 0, W, H);
      var r = rng(3);
      for (var i = 0; i < 400; i++) { c.fillStyle = "rgba(120,90,50," + (r() * 0.08) + ")"; c.fillRect(r() * W, r() * H, 3, 3); }
      c.save(); c.translate(W / 2, 330); c.rotate(-0.05);
      c.shadowColor = "rgba(0,0,0,0.25)"; c.shadowBlur = 24; c.shadowOffsetY = 10;
      c.fillStyle = "#FFFFFF"; c.fillRect(-230, -230, 460, 520); c.shadowColor = "transparent";
      c.fillStyle = "rgba(255,230,150,0.75)"; c.fillRect(-60, -255, 120, 44);
      c.restore();
      c.save(); c.translate(W / 2, 330); c.rotate(-0.05); c.translate(-W / 2, -330);
      drawSlot(c, { cx: W / 2, cy: 310, w: 400, h: 400, shape: "rect" },
        { fill: mix(PR, "#FFFFFF", 0.8), main: PR, acc: T.secondary, ink: PR, bg: "#FFFFFF" });
      c.restore();
      drawText(c, { top: 660, bottom: 1250, x0: 110, x1: W - 110 },
        { label: rgba(dark, 0.6), title: mix(PR, "#000000", 0.25), accent: mix(T.secondary, "#000000", 0.35), body: dark, boxFill: dark, boxText: "#EFE3D0" });
      host(c, rgba(dark, 0.5), H - 40);
    },
    // 9 Glow
    function (c) {
      c.fillStyle = "#120318"; c.fillRect(0, 0, W, H);
      var cols = [PR, T.secondary, "#7B2CBF"];
      c.lineWidth = 3;
      for (var i = 0; i < 9; i++) {
        c.shadowColor = cols[i % 3]; c.shadowBlur = 30; c.strokeStyle = rgba(cols[i % 3] === "#F7F3EE" ? "#FFFFFF" : cols[i % 3], 0.6);
        c.beginPath(); c.arc(W / 2, 330, 220 + i * 60, 0, Math.PI * 2); c.stroke();
      }
      c.shadowBlur = 0;
      var neon = mix(T.secondary, "#FFFFFF", 0.35);
      drawSlot(c, { cx: W / 2, cy: 330, w: 360, h: 360, shape: "circle", ring: neon, ringW: 6 },
        { fill: rgba("#FFFFFF", 0.08), main: neon, acc: mix(PR, "#FFFFFF", 0.3), ink: neon, bg: "#120318" });
      c.fillStyle = "rgba(18,3,24,0.7)"; roundRect(c, 70, 560, W - 140, 680, 30); c.fill();
      drawText(c, { top: 580, bottom: 1220, x0: 120, x1: W - 120 },
        { label: rgba("#FFFFFF", 0.7), title: neon, accent: "#FFFFFF", body: "#F3E8FF", boxFill: neon, boxText: "#120318", glow: rgba(neon, 0.7) });
      host(c, rgba("#FFFFFF", 0.55), H - 45);
    },
    // 10 Toran
    function (c) {
      c.fillStyle = "#FFF8EC"; c.fillRect(0, 0, W, H);
      var strong = PR === "#F7F3EE" || PR === "#F5C518" || PR === "#F07C12" ? mix(T.accent, "#000000", 0.1) : PR;
      c.strokeStyle = strong; c.lineWidth = 14; c.strokeRect(22, 22, W - 44, H - 44);
      c.lineWidth = 3; c.strokeRect(44, 44, W - 88, H - 88);
      toran(c);
      drawSlot(c, { cx: W / 2, cy: 360, w: 300, h: 300, shape: "circle", ring: "#F29100", ringW: 8 },
        { fill: mix(strong, "#FFFFFF", 0.85), main: strong, acc: "#F29100", ink: strong, bg: "#FFF8EC" });
      drawText(c, { top: 540, bottom: 1150, x0: 130, x1: W - 130 },
        { label: rgba(dark, 0.65), title: strong, accent: mix(strong, "#000000", 0.2), body: dark, boxFill: strong, boxText: white });
      for (var k = 0; k < 7; k++) diya(c, 200 + k * 113, 1215, 28, "#B3122E", "#F29100");
      host(c, rgba(dark, 0.6), 1265);
    }
  ];

  /* ---------------- UI wiring ---------------- */
  var relSel = $("card-rel"), wishSel = $("card-wish"), err = $("card-error"), status = $("card-status");
  var shareBox = $("share-actions");
  var styleBtns = document.querySelectorAll("#style-grid .style-btn");
  var photoBox = $("photo-box"), photoIn = $("card-photo");
  var modeBtns = document.querySelectorAll("[data-photo-mode]");
  var nextThought = $("next-thought"), thoughtText = $("thought-text");

  function fillWishes() {
    var list = K.wishes[state.rel] || [];
    wishSel.innerHTML = "";
    list.forEach(function (w, i) {
      var o = document.createElement("option"); o.value = String(i); o.textContent = w; wishSel.appendChild(o);
    });
    if (state.wish >= list.length) state.wish = 0;
    wishSel.value = String(state.wish);
  }

  function fontsReady() {
    if (!document.fonts || !document.fonts.load) return Promise.resolve();
    var all = [];
    Object.keys(K.wishes).forEach(function (k) { all = all.concat(K.wishes[k]); });
    var sample = K.title + (K.topLabel || "") + K.fromTpl + all.join("") + (K.thoughts || []).join("") + state.to + state.n1 + state.n2 + state.from;
    return Promise.all([document.fonts.load("800 90px " + F, sample), document.fonts.load("600 40px " + F, sample), document.fonts.load("700 40px " + F, sample)]).catch(function () {});
  }
  function draw() {
    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, W, H);
    STYLES[state.style](ctx);
    ctx.restore();
  }
  var pending = false;
  function redraw() {
    if (pending) return;
    pending = true;
    fontsReady().then(function () { pending = false; draw(); });
  }

  function link() {
    var q = new URLSearchParams();
    if (state.from) q.set("name", state.from);
    if (state.to) q.set("to", state.to);
    if (state.n1) q.set("n1", state.n1);
    if (state.n2) q.set("n2", state.n2);
    q.set("r", state.rel); q.set("w", String(state.wish)); q.set("s", String(state.style));
    if (K.thoughts) q.set("t", String(state.thought));
    return location.origin + location.pathname + "?" + q.toString();
  }
  function message() {
    return U.share_link_msg + "\n" + link();
  }
  function refreshLinks() {
    $("btn-wa").href = "https://wa.me/?text=" + encodeURIComponent(message());
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

  // inputs
  function val(id) { var el = $(id); return el ? clean(el.value) : ""; }
  if ($("in-from")) $("in-from").value = received ? "" : state.from;

  styleBtns.forEach(function (b, i) {
    b.setAttribute("aria-pressed", i === state.style ? "true" : "false");
    b.addEventListener("click", function () {
      state.style = i;
      styleBtns.forEach(function (x, j) { x.setAttribute("aria-pressed", j === i ? "true" : "false"); });
      redraw(); if (state.made) refreshLinks();
    });
  });
  relSel.value = state.rel;
  relSel.addEventListener("change", function () { state.rel = relSel.value; state.wish = 0; fillWishes(); redraw(); if (state.made) refreshLinks(); });
  wishSel.addEventListener("change", function () { state.wish = parseInt(wishSel.value, 10) || 0; redraw(); if (state.made) refreshLinks(); });
  fillWishes();

  if (nextThought) {
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
    if (window.innerWidth < 760) canvas.scrollIntoView({ behavior: "smooth", block: "start" });
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
