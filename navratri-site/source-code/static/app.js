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
  // Keep names short and plain. The name is only ever drawn on canvas or set via textContent.
  function cleanName(v) {
    return String(v || "")
      .replace(/[\u0000-\u001F\u007F<>"`]/g, "")
      .replace(/\s+/g, " ")
      .trim()
      .slice(0, 30);
  }

  var params = new URLSearchParams(location.search);
  var incoming = cleanName(params.get("name"));

  try { localStorage.setItem("lang", D.lang); } catch (e) {}

  // Keep the sender's name when switching language
  if (incoming) {
    document.querySelectorAll(".lang-switch a").forEach(function (a) {
      var u = new URL(a.getAttribute("href"), location.href);
      u.searchParams.set("name", incoming);
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
    if (todayIdx >= 0) {
      span.textContent = fmt(U.today_is, { n: todayIdx + 1 });
      note.appendChild(span);
      if (D.day !== todayIdx + 1) {
        var a = document.createElement("a");
        a.className = "btn btn-primary btn-small";
        a.href = "day-" + (todayIdx + 1) + ".html";
        a.textContent = U.open_today;
        note.appendChild(a);
      }
    } else if (t < D.dates[0]) {
      var days = Math.round((Date.parse(D.dates[0]) - Date.parse(t)) / 86400000);
      span.textContent = fmt(U.starts_in, { d: days });
      note.appendChild(span);
    } else if (t === D.dussehra) {
      span.textContent = U.dussehra_today;
      note.appendChild(span);
    } else {
      span.textContent = U.over;
      note.appendChild(span);
    }
  }

  /* ---------- Copy buttons for wishes ---------- */
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

  /* ---------- Greeting card ---------- */
  var canvas = document.getElementById("card");
  if (canvas) initCard();

  function initCard() {
    var ctx = canvas.getContext("2d");
    var W = canvas.width, H = canvas.height;
    var F = D.font;
    var form = document.getElementById("card-form");
    var input = document.getElementById("card-name");
    var err = document.getElementById("card-error");
    var shareBox = document.getElementById("share-actions");
    var waBtn = document.getElementById("btn-wa");
    var dlBtn = document.getElementById("btn-download");
    var spBtn = document.getElementById("btn-share-photo");
    var clBtn = document.getElementById("btn-copy-link");
    var status = document.getElementById("card-status");
    var heading = document.getElementById("card-heading");
    var received = document.getElementById("received-note");
    var currentName = "";

    function fontsReady() {
      if (!document.fonts || !document.fonts.load) return Promise.resolve();
      var sample = D.cardTitle + D.cardLine + D.dayLabel + U.card_top;
      return Promise.all([
        document.fonts.load("800 100px " + F, sample),
        document.fonts.load("600 44px " + F, sample)
      ]).catch(function () {});
    }

    function fitFont(text, weight, size, maxW) {
      var s = size;
      do { ctx.font = weight + " " + s + "px " + F; s -= 4; } while (ctx.measureText(text).width > maxW && s > 28);
      return s + 4;
    }

    function wrap(text, maxW) {
      var words = text.split(" "), lines = [], line = "";
      words.forEach(function (w) {
        var test = line ? line + " " + w : w;
        if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = w; }
        else line = test;
      });
      if (line) lines.push(line);
      return lines;
    }

    function rgba(hex, a) {
      var n = parseInt(hex.slice(1), 16);
      return "rgba(" + (n >> 16) + "," + ((n >> 8) & 255) + "," + (n & 255) + "," + a + ")";
    }

    function roundRect(x, y, w, h, r) {
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
    }

    function bandhaniBorder() {
      var inset = 40, gap = 30;
      for (var x = inset; x <= W - inset; x += gap) {
        dot(x, inset, x / gap); dot(x, H - inset, x / gap);
      }
      for (var y = inset + gap; y < H - inset; y += gap) {
        dot(inset, y, y / gap); dot(W - inset, y, y / gap);
      }
      ctx.strokeStyle = rgba(D.ink, 0.35);
      ctx.lineWidth = 2;
      ctx.strokeRect(70, 70, W - 140, H - 140);
    }
    function dot(x, y, i) {
      ctx.beginPath();
      ctx.arc(x, y, Math.round(i) % 2 ? 5 : 7, 0, Math.PI * 2);
      ctx.fillStyle = Math.round(i) % 2 ? rgba(D.ink, 0.55) : D.accent;
      ctx.fill();
    }

    function mandala(cx, cy, r) {
      ctx.save();
      ctx.translate(cx, cy);
      var rings = [
        { n: 16, rx: r * 0.16, ry: r * 0.42, d: r * 0.58, fill: rgba(D.ink, 0.16) },
        { n: 12, rx: r * 0.13, ry: r * 0.32, d: r * 0.38, fill: rgba(D.ink, 0.28) }
      ];
      rings.forEach(function (ring) {
        for (var i = 0; i < ring.n; i++) {
          ctx.save();
          ctx.rotate((Math.PI * 2 * i) / ring.n);
          ctx.beginPath();
          ctx.ellipse(0, -ring.d, ring.rx, ring.ry, 0, 0, Math.PI * 2);
          ctx.fillStyle = ring.fill;
          ctx.fill();
          ctx.restore();
        }
      });
      // dotted ring
      for (var k = 0; k < 36; k++) {
        var ang = (Math.PI * 2 * k) / 36;
        ctx.beginPath();
        ctx.arc(Math.cos(ang) * r, Math.sin(ang) * r, 5, 0, Math.PI * 2);
        ctx.fillStyle = D.accent;
        ctx.fill();
      }
      // centre
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.3, 0, Math.PI * 2);
      ctx.fillStyle = D.accent;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(0, 0, r * 0.25, 0, Math.PI * 2);
      ctx.fillStyle = D.color;
      ctx.fill();
      if (D.day) {
        ctx.fillStyle = D.ink;
        ctx.textAlign = "center";
        ctx.textBaseline = "middle";
        ctx.font = "800 " + Math.round(r * 0.34) + "px " + F;
        ctx.fillText(String(D.day), 0, r * 0.03);
      } else {
        // diya flame
        ctx.beginPath();
        ctx.moveTo(0, -r * 0.18);
        ctx.quadraticCurveTo(r * 0.12, 0, 0, r * 0.12);
        ctx.quadraticCurveTo(-r * 0.12, 0, 0, -r * 0.18);
        ctx.fillStyle = D.accent;
        ctx.fill();
      }
      ctx.restore();
    }

    function draw(name) {
      ctx.setTransform(1, 0, 0, 1, 0, 0);
      ctx.fillStyle = D.color;
      ctx.fillRect(0, 0, W, H);
      var g = ctx.createRadialGradient(W / 2, 440, 40, W / 2, 440, 620);
      g.addColorStop(0, "rgba(255,255,255,0.22)");
      g.addColorStop(1, "rgba(255,255,255,0)");
      ctx.fillStyle = g;
      ctx.fillRect(0, 0, W, H);
      bandhaniBorder();

      ctx.textAlign = "center";
      ctx.textBaseline = "alphabetic";
      ctx.fillStyle = rgba(D.ink, 0.85);
      ctx.font = "600 40px " + F;
      ctx.fillText(U.card_top, W / 2, 150);

      mandala(W / 2, 440, 215);

      var y = 745;
      if (D.dayLabel) {
        ctx.fillStyle = rgba(D.ink, 0.85);
        ctx.font = "600 48px " + F;
        ctx.fillText(D.dayLabel, W / 2, y);
        y += 100;
      } else {
        y += 50;
      }
      ctx.fillStyle = D.ink;
      fitFont(D.cardTitle, 800, 104, W - 220);
      ctx.fillText(D.cardTitle, W / 2, y);

      ctx.font = "600 44px " + F;
      var lines = wrap(D.cardLine, W - 260).slice(0, 3);
      var ly = y + 85;
      lines.forEach(function (l) {
        ctx.fillStyle = rgba(D.ink, 0.92);
        ctx.fillText(l, W / 2, ly);
        ly += 62;
      });

      if (name) {
        var text = fmt(U.from_line, { name: name });
        var fs = fitFont(text, 700, 56, W - 300);
        ctx.font = "700 " + fs + "px " + F;
        var tw = ctx.measureText(text).width;
        var pw = tw + 90, ph = fs + 46, px = (W - pw) / 2, py = 1115;
        roundRect(px, py, pw, ph, ph / 2);
        ctx.fillStyle = D.ink;
        ctx.fill();
        ctx.fillStyle = D.color;
        ctx.textBaseline = "middle";
        ctx.fillText(text, W / 2, py + ph / 2 + 3);
        ctx.textBaseline = "alphabetic";
      }

      ctx.fillStyle = rgba(D.ink, 0.7);
      ctx.font = "600 30px " + F;
      ctx.fillText(location.host || U.site_name, W / 2, H - 92);

      canvas.classList.remove("is-new");
      void canvas.offsetWidth;
      canvas.classList.add("is-new");
    }

    function shareLink(name) {
      return location.origin + location.pathname + "?name=" + encodeURIComponent(name);
    }
    function shareMessage(name) {
      var tpl = D.day ? U.share_msg : U.share_msg_home;
      return fmt(tpl, { name: name, n: D.day }) + "\n" + shareLink(name);
    }
    function fileName() {
      return (D.day ? "navratri-2026-day-" + D.day : "navratri-2026") + ".png";
    }
    function toBlob() {
      return new Promise(function (res) { canvas.toBlob(res, "image/png"); });
    }

    function makeCard(name) {
      currentName = name;
      draw(name);
      waBtn.href = "https://wa.me/?text=" + encodeURIComponent(shareMessage(name));
      shareBox.hidden = false;
      status.textContent = "";
    }

    form.addEventListener("submit", function (e) {
      e.preventDefault();
      var name = cleanName(input.value);
      if (!name) {
        err.textContent = U.name_error;
        input.focus();
        return;
      }
      err.textContent = "";
      fontsReady().then(function () { makeCard(name); });
    });
    input.addEventListener("input", function () { if (err.textContent) err.textContent = ""; });

    dlBtn.addEventListener("click", function () {
      toBlob().then(function (blob) {
        if (!blob) return;
        var url = URL.createObjectURL(blob);
        var a = document.createElement("a");
        a.href = url; a.download = fileName();
        document.body.appendChild(a); a.click(); a.remove();
        setTimeout(function () { URL.revokeObjectURL(url); }, 4000);
      });
    });

    // Native share with the image file, where the phone supports it
    var canShareFiles = false;
    try {
      canShareFiles = !!(navigator.canShare && window.File &&
        navigator.canShare({ files: [new File([new Blob(["x"], { type: "image/png" })], "t.png", { type: "image/png" })] }));
    } catch (e) {}
    if (canShareFiles) {
      spBtn.hidden = false;
      spBtn.addEventListener("click", function () {
        toBlob().then(function (blob) {
          var file = new File([blob], fileName(), { type: "image/png" });
          return navigator.share({ files: [file], text: shareMessage(currentName) });
        }).catch(function () {});
      });
    }

    clBtn.addEventListener("click", function () {
      copyText(shareLink(currentName)).then(function () { status.textContent = U.copied_link; });
    });

    fontsReady().then(function () {
      if (incoming) {
        draw(incoming);
        heading.textContent = U.card_heading_received;
        received.textContent = U.card_now_yours;
      } else {
        draw("");
      }
    });
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
