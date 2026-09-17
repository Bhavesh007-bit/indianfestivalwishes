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
    document.querySelectorAll(".lang-switch a").forEach(function (a) {
      var u = new URL(a.getAttribute("href"), location.href);
      ["name", "w", "d"].forEach(function (k) { if (params.get(k)) u.searchParams.set(k, params.get(k)); });
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

  /* ---------- Greeting card ---------- */
  var canvas = document.getElementById("card");
  if (canvas && D.wishes) initCard();

  function initCard() {
    var ctx = canvas.getContext("2d");
    var W = canvas.width, H = canvas.height;
    var F = D.font;
    var form = document.getElementById("card-form");
    var input = document.getElementById("card-name");
    var wishSel = document.getElementById("card-wish");
    var err = document.getElementById("card-error");
    var shareBox = document.getElementById("share-actions");
    var waBtn = document.getElementById("btn-wa");
    var dlBtn = document.getElementById("btn-download");
    var spBtn = document.getElementById("btn-share-photo");
    var clBtn = document.getElementById("btn-copy-link");
    var status = document.getElementById("card-status");
    var heading = document.getElementById("card-heading");
    var received = document.getElementById("received-note");
    var segs = document.querySelectorAll("#design-segs .seg");

    var DESIGNS = ["mandala", "devi", "toran"];
    var state = {
      design: DESIGNS.indexOf(params.get("d")) >= 0 ? params.get("d") : "mandala",
      wish: Math.min(D.wishes.length - 1, Math.max(0, parseInt(params.get("w"), 10) || 0)),
      name: incoming,
      mine: false
    };
    wishSel.value = String(state.wish);

    var deviImg = null;
    if (D.deviImg) {
      var im = new Image();
      im.onload = function () { deviImg = im; if (state.design === "devi") redraw(); };
      im.src = D.deviImg;
    }

    function fontsReady() {
      if (!document.fonts || !document.fonts.load) return Promise.resolve();
      var sample = D.cardTitle + D.wishes.join("") + D.dayLabel + U.card_top + D.fromTpl + (D.slides || []).join("");
      return Promise.all([
        document.fonts.load("800 100px " + F, sample),
        document.fonts.load("700 44px " + F, sample),
        document.fonts.load("600 44px " + F, sample)
      ]).catch(function () {});
    }

    function rgba(hex, a) {
      var n = parseInt(hex.slice(1), 16);
      return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
    }

    /* ---- shared drawing helpers (work on any 2D context) ---- */
    function setFont(c, weight, size) { c.font = weight + " " + size + "px " + F; }
    function wrap(c, text, maxW) {
      var words = String(text).split(" "), lines = [], line = "";
      words.forEach(function (w) {
        var test = line ? line + " " + w : w;
        if (c.measureText(test).width > maxW && line) { lines.push(line); line = w; } else line = test;
      });
      if (line) lines.push(line);
      return lines;
    }
    function metrics(c, text) {
      var m = c.measureText(text);
      var asc = m.actualBoundingBoxAscent, desc = m.actualBoundingBoxDescent;
      if (!(asc > 0)) { var s = parseFloat(c.font.match(/(\d+)px/)[1]); asc = s * 0.8; desc = s * 0.3; }
      return { w: m.width, asc: asc, desc: desc };
    }
    // Fit text in up to maxLines lines, shrinking the font if needed
    function fitLines(c, text, weight, size, minSize, maxW, maxLines) {
      var s = size, lines;
      do {
        setFont(c, weight, s);
        lines = wrap(c, text, maxW);
        if (lines.length <= maxLines && lines.every(function (l) { return c.measureText(l).width <= maxW; })) break;
        s -= 2;
      } while (s > minSize);
      return { size: s, lines: lines.slice(0, maxLines) };
    }
    // Draw centred lines starting at y (top). Returns new y (bottom).
    function drawLines(c, lines, weight, size, color, cx, y, gap) {
      setFont(c, weight, size);
      c.fillStyle = color;
      c.textAlign = "center";
      c.textBaseline = "alphabetic";
      lines.forEach(function (l, i) {
        var m = metrics(c, l);
        var lineAsc = Math.max(m.asc, size * 0.72);
        var lineDesc = Math.max(m.desc, size * 0.22);
        y += lineAsc;
        c.fillText(l, cx, y);
        y += lineDesc + (i < lines.length - 1 ? gap : 0);
      });
      return y;
    }
    function roundRect(c, x, y, w, h, r) {
      c.beginPath();
      c.moveTo(x + r, y);
      c.arcTo(x + w, y, x + w, y + h, r);
      c.arcTo(x + w, y + h, x, y + h, r);
      c.arcTo(x, y + h, x, y, r);
      c.arcTo(x, y, x + w, y, r);
      c.closePath();
    }
    function senderBox(c, cx, top, maxW, fill, textColor, name) {
      var text = fmt(D.fromTpl, { name: name });
      var f = fitLines(c, text, 700, 44, 28, maxW - 80, 2);
      setFont(c, 700, f.size);
      var widest = Math.max.apply(null, f.lines.map(function (l) { return c.measureText(l).width; }));
      var lh = f.size * 1.35;
      var bw = Math.min(maxW, widest + 90), bh = f.lines.length * lh + 44;
      roundRect(c, cx - bw / 2, top, bw, bh, Math.min(38, bh / 2));
      c.fillStyle = fill;
      c.fill();
      drawLines(c, f.lines, 700, f.size, textColor, cx, top + 22 + (lh - f.size * 1.02) / 2, lh - f.size * 0.94);
      return top + bh;
    }
    function bandhani(c, w, h, inset, gap, ink, accent) {
      function dot(x, y, i) {
        var odd = Math.round(i) % 2;
        c.beginPath();
        c.arc(x, y, odd ? 5 : 7, 0, Math.PI * 2);
        c.fillStyle = odd ? rgba(ink, 0.55) : accent;
        c.fill();
      }
      for (var x = inset; x <= w - inset; x += gap) { dot(x, inset, x / gap); dot(x, h - inset, x / gap); }
      for (var y = inset + gap; y < h - inset; y += gap) { dot(inset, y, y / gap); dot(w - inset, y, y / gap); }
      c.strokeStyle = rgba(ink, 0.35);
      c.lineWidth = 2;
      c.strokeRect(inset + 30, inset + 30, w - 2 * (inset + 30), h - 2 * (inset + 30));
    }
    function mandala(c, cx, cy, r, rot, showNum) {
      c.save();
      c.translate(cx, cy);
      c.rotate(rot || 0);
      [{ n: 16, rx: 0.16, ry: 0.42, d: 0.58, a: 0.16 }, { n: 12, rx: 0.13, ry: 0.32, d: 0.38, a: 0.28 }].forEach(function (g) {
        for (var i = 0; i < g.n; i++) {
          c.save();
          c.rotate((Math.PI * 2 * i) / g.n);
          c.beginPath();
          c.ellipse(0, -r * g.d, r * g.rx, r * g.ry, 0, 0, Math.PI * 2);
          c.fillStyle = rgba(D.ink, g.a);
          c.fill();
          c.restore();
        }
      });
      for (var k = 0; k < 36; k++) {
        var ang = (Math.PI * 2 * k) / 36;
        c.beginPath();
        c.arc(Math.cos(ang) * r, Math.sin(ang) * r, 5, 0, Math.PI * 2);
        c.fillStyle = D.accent;
        c.fill();
      }
      c.restore();
      c.save();
      c.translate(cx, cy);
      c.beginPath(); c.arc(0, 0, r * 0.3, 0, Math.PI * 2); c.fillStyle = D.accent; c.fill();
      c.beginPath(); c.arc(0, 0, r * 0.25, 0, Math.PI * 2); c.fillStyle = D.color; c.fill();
      if (showNum && D.day) {
        c.fillStyle = D.ink;
        c.textAlign = "center";
        c.textBaseline = "middle";
        setFont(c, 800, Math.round(r * 0.34));
        c.fillText(String(D.day), 0, r * 0.03);
      } else {
        flame(c, 0, 0, r * 0.18, D.accent);
      }
      c.restore();
    }
    function flame(c, x, y, s, color) {
      c.beginPath();
      c.moveTo(x, y - s);
      c.quadraticCurveTo(x + s * 0.7, y, x, y + s * 0.65);
      c.quadraticCurveTo(x - s * 0.7, y, x, y - s);
      c.fillStyle = color;
      c.fill();
    }
    function diya(c, x, y, s, bowl, flameColor) {
      c.beginPath();
      c.moveTo(x - s, y);
      c.quadraticCurveTo(x, y + s * 1.1, x + s, y);
      c.closePath();
      c.fillStyle = bowl;
      c.fill();
      flame(c, x, y - s * 0.45, s * 0.45, flameColor);
    }

    // Symbols for each goddess (drawn in a 200x200 box centred on 0,0)
    function symbol(c, day, col, acc) {
      c.fillStyle = col; c.strokeStyle = col; c.lineWidth = 12; c.lineCap = "round"; c.lineJoin = "round";
      var i;
      switch (day) {
        case 1: // trishul
          c.fillRect(-6, -40, 12, 140);
          c.beginPath(); c.moveTo(0, -100); c.lineTo(14, -60); c.lineTo(-14, -60); c.closePath(); c.fill();
          c.beginPath(); c.moveTo(-60, -85); c.quadraticCurveTo(-60, -30, 0, -35); c.quadraticCurveTo(60, -30, 60, -85); c.stroke();
          c.beginPath(); c.moveTo(-60, -95); c.lineTo(-70, -75); c.lineTo(-50, -75); c.closePath(); c.fill();
          c.beginPath(); c.moveTo(60, -95); c.lineTo(70, -75); c.lineTo(50, -75); c.closePath(); c.fill();
          c.fillStyle = acc; c.fillRect(-18, -20, 36, 12);
          break;
        case 2: // prayer beads + kamandal
          for (i = 0; i < 22; i++) {
            var a = (Math.PI * 2 * i) / 22;
            c.beginPath(); c.arc(Math.cos(a) * 62, Math.sin(a) * 62 - 20, 9, 0, Math.PI * 2); c.fill();
          }
          c.fillStyle = acc;
          c.beginPath(); c.arc(0, 52, 12, 0, Math.PI * 2); c.fill();
          c.fillStyle = col;
          c.beginPath(); c.moveTo(-6, 62); c.lineTo(6, 62); c.lineTo(10, 100); c.lineTo(-10, 100); c.closePath(); c.fill();
          break;
        case 3: // bell with crescent
          c.beginPath(); c.moveTo(-55, 55); c.quadraticCurveTo(-50, -40, 0, -45); c.quadraticCurveTo(50, -40, 55, 55); c.closePath(); c.fill();
          c.fillRect(-70, 50, 140, 14);
          c.fillStyle = acc; c.beginPath(); c.arc(0, 80, 14, 0, Math.PI * 2); c.fill();
          c.fillStyle = col;
          c.beginPath(); c.arc(0, -78, 30, 0.15 * Math.PI, 0.85 * Math.PI, true); c.arc(0, -92, 26, 0.85 * Math.PI, 0.15 * Math.PI, false); c.closePath(); c.fill();
          break;
        case 4: // sun
          for (i = 0; i < 12; i++) {
            c.save(); c.rotate((Math.PI * 2 * i) / 12);
            c.beginPath(); c.moveTo(-12, -58); c.lineTo(0, -98); c.lineTo(12, -58); c.closePath(); c.fill();
            c.restore();
          }
          c.beginPath(); c.arc(0, 0, 48, 0, Math.PI * 2); c.fill();
          c.fillStyle = acc; c.beginPath(); c.arc(0, 0, 30, 0, Math.PI * 2); c.fill();
          break;
        case 5: // lotus
          [-60, -30, 0, 30, 60].forEach(function (deg, k) {
            c.save(); c.translate(0, 40); c.rotate(deg * Math.PI / 180);
            c.beginPath(); c.ellipse(0, -55, 22, 58, 0, 0, Math.PI * 2);
            c.fillStyle = k === 2 ? acc : col; c.fill();
            c.restore();
          });
          c.fillStyle = col; c.fillRect(-70, 72, 140, 12);
          break;
        case 6: // sword
          c.beginPath(); c.moveTo(-8, 40); c.lineTo(8, 40); c.quadraticCurveTo(24, -40, 0, -100); c.quadraticCurveTo(-10, -40, -8, 40); c.fill();
          c.fillStyle = acc; c.fillRect(-40, 40, 80, 12);
          c.fillStyle = col; c.fillRect(-7, 52, 14, 40);
          c.beginPath(); c.arc(0, 98, 10, 0, Math.PI * 2); c.fill();
          break;
        case 7: // lamp in the dark
          c.beginPath(); c.arc(0, 0, 90, 0, Math.PI * 2); c.fillStyle = rgba(col, 0.25); c.fill();
          diya(c, 0, 30, 70, col, acc);
          flame(c, 0, -40, 40, acc);
          break;
        case 8: // damru
          c.beginPath(); c.moveTo(-50, -60); c.lineTo(50, -60); c.lineTo(0, 0); c.closePath(); c.fill();
          c.beginPath(); c.moveTo(-50, 60); c.lineTo(50, 60); c.lineTo(0, 0); c.closePath(); c.fill();
          c.lineWidth = 5;
          c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(45, 10, 75, -10); c.stroke();
          c.beginPath(); c.moveTo(0, 0); c.quadraticCurveTo(-45, 10, -75, -10); c.stroke();
          c.fillStyle = acc;
          c.beginPath(); c.arc(78, -12, 10, 0, Math.PI * 2); c.fill();
          c.beginPath(); c.arc(-78, -12, 10, 0, Math.PI * 2); c.fill();
          break;
        default: // chakra
          c.beginPath(); c.arc(0, 0, 80, 0, Math.PI * 2); c.stroke();
          for (i = 0; i < 12; i++) {
            c.save(); c.rotate((Math.PI * 2 * i) / 12);
            c.fillRect(-3, -76, 6, 60);
            c.beginPath(); c.moveTo(-10, -86); c.lineTo(0, -104); c.lineTo(10, -86); c.closePath(); c.fill();
            c.restore();
          }
          c.fillStyle = acc; c.beginPath(); c.arc(0, 0, 18, 0, Math.PI * 2); c.fill();
      }
    }

    /* ---- the three card designs ---- */
    function textStack(c, y, color, titleColor, maxBottom) {
      var cx = W / 2;
      if (D.dayLabel) {
        y = drawLines(c, [D.dayLabel], 600, 46, rgba(color === "#FFFFFF" ? "#FFFFFF" : color, 0.9), cx, y, 0) + 18;
      }
      var tf = fitLines(c, D.cardTitle, 800, 100, 60, W - 220, 1);
      y = drawLines(c, tf.lines, 800, tf.size, titleColor, cx, y, 0) + 26;
      var wish = D.wishes[state.wish] || "";
      var size = 44, res, end;
      do {
        res = fitLines(c, wish, 600, size, 26, W - 250, 3);
        setFont(c, 600, res.size);
        end = y + res.lines.length * res.size * 1.35;
        size = res.size - 2;
      } while (end > maxBottom && size > 26);
      return drawLines(c, res.lines, 600, res.size, color, cx, y, res.size * 0.35);
    }

    function drawMandala(c, name) {
      c.fillStyle = D.color; c.fillRect(0, 0, W, H);
      var g = c.createRadialGradient(W / 2, 400, 40, W / 2, 400, 620);
      g.addColorStop(0, "rgba(255,255,255,0.22)"); g.addColorStop(1, "rgba(255,255,255,0)");
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      bandhani(c, W, H, 40, 30, D.ink, D.accent);
      drawLines(c, [U.card_top], 600, 38, rgba(D.ink, 0.85), W / 2, 110, 0);
      mandala(c, W / 2, 400, 200, 0, true);
      var boxTop = name ? 1060 : 1180;
      textStack(c, 650, D.ink, D.ink, boxTop - 30);
      if (name) senderBox(c, W / 2, boxTop, W - 200, D.ink, D.color, name);
      drawLines(c, [location.host || U.site_name], 600, 28, rgba(D.ink, 0.7), W / 2, H - 118, 0);
    }

    function drawDevi(c, name) {
      var g = c.createLinearGradient(0, 0, 0, H);
      g.addColorStop(0, D.color); g.addColorStop(1, rgba(D.strong, 1));
      c.fillStyle = g; c.fillRect(0, 0, W, H);
      c.fillStyle = "rgba(0,0,0,0.08)"; c.fillRect(0, 0, W, H);
      // rays
      c.save(); c.translate(W / 2, 400);
      for (var i = 0; i < 24; i++) {
        c.rotate(Math.PI / 12);
        c.beginPath(); c.moveTo(-18, 0); c.lineTo(0, -700); c.lineTo(18, 0); c.closePath();
        c.fillStyle = "rgba(255,255,255,0.06)"; c.fill();
      }
      c.restore();
      var cx = W / 2, cy = 400, R = 225;
      c.beginPath(); c.arc(cx, cy, R + 18, 0, Math.PI * 2); c.fillStyle = D.accent; c.fill();
      c.beginPath(); c.arc(cx, cy, R, 0, Math.PI * 2); c.fillStyle = "#FFF8EC"; c.fill();
      if (deviImg) {
        c.save();
        c.beginPath(); c.arc(cx, cy, R - 8, 0, Math.PI * 2); c.clip();
        var s = Math.max((2 * R) / deviImg.width, (2 * R) / deviImg.height);
        c.drawImage(deviImg, cx - (deviImg.width * s) / 2, cy - (deviImg.height * s) / 2, deviImg.width * s, deviImg.height * s);
        c.restore();
      } else {
        c.save(); c.translate(cx, cy); c.scale(1.6, 1.6);
        symbol(c, D.day || 7, D.strong, D.accent === "#F2A007" ? "#E08A00" : D.accent);
        c.restore();
      }
      for (var k = 0; k < 40; k++) {
        var a = (Math.PI * 2 * k) / 40;
        c.beginPath(); c.arc(cx + Math.cos(a) * (R + 40), cy + Math.sin(a) * (R + 40), 5, 0, Math.PI * 2);
        c.fillStyle = "rgba(255,255,255,0.8)"; c.fill();
      }
      var ink = "#FFFFFF";
      var light = D.ink !== "#FFFFFF";
      if (light) {
        // soft panel keeps text readable on light colours
        c.fillStyle = "rgba(43,27,20,0.55)";
        roundRect(c, 60, 690, W - 120, H - 750, 30); c.fill();
      }
      drawLines(c, [U.card_top], 600, 36, light ? rgba("#2B1B14", 0.8) : "rgba(255,255,255,0.9)", W / 2, 70, 0);
      var boxTop = name ? 1070 : 1190;
      textStack(c, 720, ink, ink, boxTop - 30);
      if (name) senderBox(c, W / 2, boxTop, W - 200, "#FFFFFF", D.strong, name);
      drawLines(c, [location.host || U.site_name], 600, 28, "rgba(255,255,255,0.8)", W / 2, H - 70, 0);
    }

    function drawToran(c, name) {
      c.fillStyle = "#FFF8EC"; c.fillRect(0, 0, W, H);
      c.strokeStyle = D.strong; c.lineWidth = 14; c.strokeRect(22, 22, W - 44, H - 44);
      c.lineWidth = 3; c.strokeRect(44, 44, W - 88, H - 88);
      // garland rope
      function ropeY(x) { var u = x / W; return 80 + Math.sin(u * Math.PI * 4) * 22 + 40 * Math.sin(u * Math.PI); }
      var x;
      c.strokeStyle = "#2E7D32"; c.lineWidth = 4; c.beginPath();
      for (x = 44; x <= W - 44; x += 8) { if (x === 44) c.moveTo(x, ropeY(x)); else c.lineTo(x, ropeY(x)); }
      c.stroke();
      for (x = 70; x < W - 50; x += 44) {
        var y = ropeY(x);
        c.beginPath(); c.moveTo(x, y + 6); c.lineTo(x - 12, y + 34); c.lineTo(x + 12, y + 34); c.closePath();
        c.fillStyle = "#2E7D32"; c.fill();
        c.beginPath(); c.arc(x, y, 17, 0, Math.PI * 2);
        c.fillStyle = (x / 44) % 2 < 1 ? "#F29100" : "#F7C21A"; c.fill();
        c.beginPath(); c.arc(x, y, 6, 0, Math.PI * 2); c.fillStyle = "#B3122E"; c.fill();
      }
      // hanging strands
      for (x = 160; x < W - 100; x += 190) {
        var top = ropeY(x);
        for (var j = 1; j <= 3; j++) {
          c.beginPath(); c.arc(x, top + j * 34, 14, 0, Math.PI * 2);
          c.fillStyle = j % 2 ? "#F7C21A" : "#F29100"; c.fill();
        }
        c.beginPath(); c.moveTo(x - 10, top + 125); c.lineTo(x, top + 150); c.lineTo(x + 10, top + 125); c.closePath();
        c.fillStyle = "#B3122E"; c.fill();
      }
      drawLines(c, [U.card_top], 600, 36, rgba("#2B1B14", 0.75), W / 2, 280, 0);
      var y = 350;
      if (D.dayLabel) {
        setFont(c, 700, 40);
        var m = metrics(c, D.dayLabel);
        var pw = m.w + 70, ph = 70;
        roundRect(c, W / 2 - pw / 2, y, pw, ph, 35);
        c.fillStyle = D.strong; c.fill();
        c.fillStyle = "#FFFFFF"; c.textAlign = "center"; c.textBaseline = "middle";
        c.fillText(D.dayLabel, W / 2, y + ph / 2 + 3);
        c.textBaseline = "alphabetic";
        y += ph + 30;
      }
      var tf = fitLines(c, D.cardTitle, 800, 104, 60, W - 200, 1);
      y = drawLines(c, tf.lines, 800, tf.size, D.strong, W / 2, y, 0) + 24;
      c.fillStyle = "#F29100";
      for (var d = -2; d <= 2; d++) { c.beginPath(); c.arc(W / 2 + d * 26, y + 6, d === 0 ? 7 : 4, 0, Math.PI * 2); c.fill(); }
      y += 40;
      var boxTop = name ? 1000 : 1120;
      var wish = D.wishes[state.wish] || "";
      var res = fitLines(c, wish, 600, 46, 28, W - 240, 4);
      while (y + res.lines.length * res.size * 1.35 > boxTop - 30 && res.size > 28) {
        res = fitLines(c, wish, 600, res.size - 2, 26, W - 240, 4);
      }
      drawLines(c, res.lines, 600, res.size, "#2B1B14", W / 2, y, res.size * 0.35);
      if (name) senderBox(c, W / 2, boxTop, W - 180, D.strong, "#FFFFFF", name);
      for (var k = 0; k < 7; k++) diya(c, 200 + k * 113, 1215, 30, "#B3122E", "#F29100");
      drawLines(c, [location.host || U.site_name], 600, 28, rgba("#2B1B14", 0.65), W / 2, 1262, 0);
    }

    function draw(name) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.globalAlpha = 1;
      if (state.design === "devi") drawDevi(ctx, name);
      else if (state.design === "toran") drawToran(ctx, name);
      else drawMandala(ctx, name);
      canvas.classList.remove("is-new");
      void canvas.offsetWidth;
      canvas.classList.add("is-new");
    }
    function redraw() { fontsReady().then(function () { draw(state.name); }); }

    function shareLink(name) {
      var q = new URLSearchParams({ name: name, w: String(state.wish), d: state.design });
      return location.origin + location.pathname + "?" + q.toString();
    }
    function shareMessage(name) {
      var tpl = D.day ? U.share_msg : U.share_msg_home;
      return fmt(tpl, { name: name, n: D.day }) + "\n" + shareLink(name);
    }
    function fileName(ext) {
      return (D.day ? "navratri-2026-day-" + D.day : "navratri-2026") + "." + (ext || "png");
    }
    function toBlob() { return new Promise(function (res) { canvas.toBlob(res, "image/png"); }); }
    var fbBtn = document.getElementById("btn-fb");
    var igBtn = document.getElementById("btn-ig");
    function refreshShare() {
      if (!state.mine) return;
      waBtn.href = "https://wa.me/?text=" + encodeURIComponent(shareMessage(state.name));
      fbBtn.href = "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent(shareLink(state.name));
    }

    segs.forEach(function (b) {
      b.setAttribute("aria-pressed", b.getAttribute("data-design") === state.design ? "true" : "false");
      b.addEventListener("click", function () {
        state.design = b.getAttribute("data-design");
        segs.forEach(function (x) { x.setAttribute("aria-pressed", x === b ? "true" : "false"); });
        redraw(); refreshShare();
      });
    });
    wishSel.addEventListener("change", function () {
      state.wish = parseInt(wishSel.value, 10) || 0;
      redraw(); refreshShare();
    });

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = cleanName(input.value);
      if (!name) { err.textContent = U.name_error; input.focus(); return; }
      err.textContent = "";
      state.name = name;
      state.mine = true;
      shareBox.hidden = false;
      status.textContent = "";
      refreshShare();
      redraw();
    });
    input.addEventListener("input", function () { if (err.textContent) err.textContent = ""; });

    dlBtn.addEventListener("click", function () {
      toBlob().then(function (blob) { if (blob) saveBlob(blob, fileName("png")); });
    });
    function saveBlob(blob, fname) {
      var url = URL.createObjectURL(blob);
      var a = document.createElement("a");
      a.href = url; a.download = fname;
      document.body.appendChild(a); a.click(); a.remove();
      setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
    }

    var canShareFiles = false;
    try {
      canShareFiles = !!(navigator.canShare && window.File &&
        navigator.canShare({ files: [new File([new Blob(["x"], { type: "image/png" })], "t.png", { type: "image/png" })] }));
    } catch (e) {}
    if (canShareFiles) {
      spBtn.hidden = false;
      spBtn.addEventListener("click", function () {
        toBlob().then(function (blob) {
          return navigator.share({ files: [new File([blob], fileName("png"), { type: "image/png" })], text: shareMessage(state.name) });
        }).catch(function () {});
      });
    }
    igBtn.addEventListener("click", function () {
      toBlob().then(function (blob) {
        var file = new File([blob], fileName("png"), { type: "image/png" });
        if (canShareFiles) {
          return navigator.share({ files: [file] }).catch(function () {});
        }
        saveBlob(blob, fileName("png"));
        status.textContent = U.insta_hint;
      });
    });
    clBtn.addEventListener("click", function () {
      copyText(shareLink(state.name)).then(function () { status.textContent = U.copied_link; });
    });

    if (incoming) {
      heading.textContent = U.card_heading_received;
      received.textContent = U.card_now_yours;
    }
    redraw();

    /* ---------- Reel (video) ---------- */
    var reelBtn = document.getElementById("btn-reel");
    if (reelBtn) initReel();

    function initReel() {
      var rc = document.getElementById("reel-canvas");
      var rctx = rc.getContext("2d");
      var RW = rc.width, RH = rc.height;
      var rStatus = document.getElementById("reel-status");
      var out = document.getElementById("reel-out");
      var video = document.getElementById("reel-video");
      var dl = document.getElementById("reel-download");
      var voiceBox = document.getElementById("reel-voice");
      var lastBlob = null, lastExt = "webm", busy = false;
      var audioBuf = null;
      var slides = D.slides || [];

      function pickType(withAudio) {
        if (!window.MediaRecorder || !rc.captureStream) return null;
        var list = withAudio
          ? ["video/mp4;codecs=avc1.42E01E,mp4a.40.2", "video/mp4;codecs=avc1,mp4a.40.2", "video/mp4",
             "video/webm;codecs=vp9,opus", "video/webm;codecs=vp8,opus", "video/webm"]
          : ["video/mp4;codecs=avc1.42E01E", "video/mp4;codecs=avc1", "video/mp4",
             "video/webm;codecs=vp9", "video/webm;codecs=vp8", "video/webm"];
        for (var i = 0; i < list.length; i++) if (MediaRecorder.isTypeSupported(list[i])) return list[i];
        return "";
      }

      function loadAudio(ac) {
        if (!D.audio) return Promise.resolve(null);
        if (audioBuf) return Promise.resolve(audioBuf);
        return fetch(D.audio.src).then(function (r) {
          if (!r.ok) throw new Error("audio");
          return r.arrayBuffer();
        }).then(function (ab) {
          return new Promise(function (res, rej) { ac.decodeAudioData(ab, res, rej); });
        }).then(function (buf) { audioBuf = buf; return buf; }).catch(function () { return null; });
      }

      // Build the timeline. Slide length follows the narration when there is one.
      function timeline(withVoice) {
        var seg = (withVoice && D.audio && D.audio.seg) || {};
        function len(key, min, pad) { return seg[key] ? Math.max(min, seg[key][1] + pad) : min; }
        var parts = [], t = 0;
        function add(kind, idx, dur, key) { parts.push({ kind: kind, idx: idx, start: t, dur: dur, key: key }); t += dur; }
        add("intro", 0, len("intro", 3, 0.9), "intro");
        slides.forEach(function (_, k) { add("story", k, len("s" + k, 3.4, 0.7), "s" + k); });
        add("bhog", 0, len("bhog", 2.8, 0.8), "bhog");
        add("end", 0, len("w" + state.wish, 4.5, 1.8), "w" + state.wish);
        return { parts: parts, total: t };
      }

      function ease(p) { return 1 - Math.pow(1 - Math.min(1, Math.max(0, p)), 3); }

      function bg() {
        rctx.globalAlpha = 1;
        rctx.fillStyle = D.color; rctx.fillRect(0, 0, RW, RH);
        var g = rctx.createRadialGradient(RW / 2, RH / 2, 60, RW / 2, RH / 2, 1000);
        g.addColorStop(0, "rgba(255,255,255,0.18)"); g.addColorStop(1, "rgba(0,0,0,0.12)");
        rctx.fillStyle = g; rctx.fillRect(0, 0, RW, RH);
        bandhani(rctx, RW, RH, 40, 30, D.ink, D.accent);
        drawLines(rctx, [U.card_top + (D.dayLabel ? "  |  " + D.dayLabel : "")], 600, 40, rgba(D.ink, 0.85), RW / 2, 120, 0);
        drawLines(rctx, [location.host || U.site_name], 600, 32, rgba(D.ink, 0.75), RW / 2, RH - 150, 0);
      }

      function frame(tl, tt) {
        bg();
        var part = tl.parts[tl.parts.length - 1];
        for (var i = 0; i < tl.parts.length; i++) {
          if (tt < tl.parts[i].start + tl.parts[i].dur) { part = tl.parts[i]; break; }
        }
        var lt = tt - part.start, p, y;
        if (part.kind === "intro") {
          p = ease(lt / 0.8);
          rctx.globalAlpha = p;
          mandala(rctx, RW / 2, 720, 300, tt * 0.25, true);
          y = 1150 + (1 - p) * 60;
          y = drawLines(rctx, [D.dayLabel], 600, 60, D.ink, RW / 2, y, 0) + 30;
          var tf = fitLines(rctx, D.cardTitle, 800, 120, 70, RW - 180, 1);
          drawLines(rctx, tf.lines, 800, tf.size, D.ink, RW / 2, y, 0);
        } else if (part.kind === "story") {
          p = ease(lt / 0.6);
          rctx.globalAlpha = 0.25;
          mandala(rctx, RW / 2, RH / 2, 420, tt * 0.15, false);
          rctx.globalAlpha = p;
          y = 420 + (1 - p) * 50;
          y = drawLines(rctx, [U.reel_story + "  " + (part.idx + 1) + "/" + slides.length], 700, 54, D.ink, RW / 2, y, 0) + 70;
          var st = fitLines(rctx, slides[part.idx], 600, 60, 40, RW - 200, 11);
          drawLines(rctx, st.lines, 600, st.size, D.ink, RW / 2, y, st.size * 0.45);
        } else if (part.kind === "bhog") {
          p = ease(lt / 0.6);
          rctx.globalAlpha = p;
          y = 720;
          diya(rctx, RW / 2, y, 110, D.ink, D.accent);
          flame(rctx, RW / 2, y - 120, 60, D.accent);
          y = drawLines(rctx, [U.bhog_label], 600, 60, rgba(D.ink, 0.85), RW / 2, y + 200, 0) + 40;
          var bf = fitLines(rctx, D.bhog, 800, 96, 50, RW - 200, 2);
          drawLines(rctx, bf.lines, 800, bf.size, D.ink, RW / 2, y, 24);
        } else {
          p = ease(lt / 0.7);
          rctx.globalAlpha = p;
          mandala(rctx, RW / 2, 520, 200, tt * 0.25, true);
          y = 820 + (1 - p) * 40;
          var tf2 = fitLines(rctx, D.cardTitle, 800, 100, 60, RW - 200, 1);
          y = drawLines(rctx, tf2.lines, 800, tf2.size, D.ink, RW / 2, y, 0) + 50;
          var wf = fitLines(rctx, D.wishes[state.wish] || "", 600, 60, 36, RW - 220, 5);
          y = drawLines(rctx, wf.lines, 600, wf.size, D.ink, RW / 2, y, wf.size * 0.4) + 80;
          if (state.name) senderBox(rctx, RW / 2, Math.max(y, 1380), RW - 180, D.ink, D.color, state.name);
        }
        rctx.globalAlpha = 1;
      }

      function record(withVoice, ac, buf) {
        var tl = timeline(withVoice && !!buf);
        var type = pickType(!!buf);
        var vstream = rc.captureStream(30);
        var tracks = vstream.getVideoTracks();
        var sources = [];
        if (buf) {
          var dest = ac.createMediaStreamDestination();
          tracks = tracks.concat(dest.stream.getAudioTracks());
          var t0 = ac.currentTime + 0.25;
          tl.parts.forEach(function (pt) {
            var sg = D.audio.seg[pt.key];
            if (!sg) return;
            var src = ac.createBufferSource();
            src.buffer = buf;
            src.connect(dest);
            src.start(t0 + pt.start + 0.25, sg[0], sg[1]);
            sources.push(src);
          });
        }
        var stream = new MediaStream(tracks);
        var rec;
        try {
          rec = type ? new MediaRecorder(stream, { mimeType: type, videoBitsPerSecond: 5000000 }) : new MediaRecorder(stream);
        } catch (e) {
          rStatus.textContent = U.reel_unsupported; done(); return;
        }
        var chunks = [];
        rec.ondataavailable = function (ev) { if (ev.data && ev.data.size) chunks.push(ev.data); };
        rec.onstop = function () {
          sources.forEach(function (sN) { try { sN.stop(); } catch (e) {} });
          if (ac) ac.close();
          var mime = rec.mimeType || type || "video/webm";
          lastExt = mime.indexOf("mp4") >= 0 ? "mp4" : "webm";
          lastBlob = new Blob(chunks, { type: mime.split(";")[0] });
          var url = URL.createObjectURL(lastBlob);
          video.src = url;
          dl.href = url;
          dl.download = fileName(lastExt);
          out.hidden = false;
          rStatus.textContent = U.reel_ready + (lastExt === "webm" ? " " + U.reel_webm_note : "");
          done();
        };
        frame(tl, 0);
        var start = performance.now() + 250;
        rec.start(500);
        var tick = function () {
          var tt = Math.max(0, (performance.now() - start) / 1000);
          if (tt >= tl.total) { frame(tl, tl.total - 0.01); setTimeout(function () { rec.stop(); }, 200); return; }
          frame(tl, tt);
          rStatus.textContent = fmt(U.reel_making, { p: Math.round((tt / tl.total) * 100) });
          requestAnimationFrame(tick);
        };
        requestAnimationFrame(tick);
      }
      function done() { busy = false; reelBtn.disabled = false; }

      reelBtn.addEventListener("click", function () {
        if (busy) return;
        if (pickType(false) === null) { rStatus.textContent = U.reel_unsupported; return; }
        busy = true;
        reelBtn.disabled = true;
        out.hidden = true;
        var withVoice = voiceBox ? voiceBox.checked : false;
        var AC = window.AudioContext || window.webkitAudioContext;
        var ac = withVoice && AC ? new AC() : null;
        rStatus.textContent = fmt(U.reel_making, { p: 0 });
        Promise.all([fontsReady(), ac ? loadAudio(ac) : Promise.resolve(null)]).then(function (r) {
          record(withVoice, ac, r[1]);
        });
      });

      // Share the finished reel
      document.querySelectorAll("[data-reel-share]").forEach(function (btn) {
        btn.addEventListener("click", function () {
          if (!lastBlob) return;
          var app = btn.getAttribute("data-reel-share");
          var file = new File([lastBlob], fileName(lastExt), { type: lastBlob.type });
          var canFile = false;
          try { canFile = !!(navigator.canShare && navigator.canShare({ files: [file] })); } catch (e) {}
          if (canFile) {
            navigator.share({ files: [file], text: state.name ? shareMessage(state.name) : "" }).catch(function () {});
            return;
          }
          saveBlob(lastBlob, fileName(lastExt));
          rStatus.textContent = fmt(U.reel_saved_hint, { app: app });
          if (app === "WhatsApp" && state.name) {
            window.open("https://wa.me/?text=" + encodeURIComponent(shareMessage(state.name)), "_blank", "noopener");
          }
        });
      });
    }
  }

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
