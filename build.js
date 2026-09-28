/* Indian Festival Wishes — static site builder.
   Reads content/*.json and writes the whole site into ./public.
   Run: node build.js   (Railway runs it as the build step) */
"use strict";
const fs = require("fs");
const path = require("path");

const ROOT = __dirname;
const OUT = path.join(ROOT, "public");
const SITE = "https://www.indianfestivalwishes.com";
const LANGS = ["hi", "gu", "en"];
const TODAY = new Date().toISOString().slice(0, 10);
const ADSENSE_PUB = "ca-pub-1833153255842443";

const read = (f) => JSON.parse(fs.readFileSync(path.join(ROOT, "content", f), "utf8"));
const UI = read("ui.json");
const HUB = read("hub.json");
const NAV = read("navratri.json");
const REC = read("recipes.json");
const PAGES = read("pages.json");
const OCC = read("occasions.json");
const ART = read("articles.json");
const FEST = read("festivals.json");
const MW = {}, NP = {};
["hi", "gu", "en"].forEach((L) => { MW[L] = read(`more_wishes_${L}.json`); NP[L] = read(`newpages_${L}.json`); });
const INVITES = ["wedding", "engagement", "birthday-party", "griha-pravesh", "baby-shower", "naming-ceremony", "puja", "shop-opening"];

const ASSET_V = String(Date.now()).slice(-8);

/* ------------------------------------------------------------------ helpers */
const esc = (s) => String(s == null ? "" : s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
const fmt = (s, o) => String(s).replace(/\{(\w+)\}/g, (_, k) => (o[k] != null ? o[k] : ""));
const pre = (L) => (L === "hi" ? "" : "/" + L);
const url = (L, p) => pre(L) + "/" + (p || "");
const abs = (L, p) => SITE + url(L, p);
const jsonScript = (o) => JSON.stringify(o).replace(/</g, "\\u003c");
function write(rel, html) {
  const f = path.join(OUT, rel);
  fs.mkdirSync(path.dirname(f), { recursive: true });
  fs.writeFileSync(f, html);
}
function outPath(L, p) {
  let r = (L === "hi" ? "" : L + "/") + p;
  if (r === "" || r.endsWith("/")) r += "index.html";
  return r;
}
function copyDir(src, dst, skip) {
  if (!fs.existsSync(src)) return;
  fs.mkdirSync(dst, { recursive: true });
  for (const n of fs.readdirSync(src)) {
    if (skip && skip(n)) continue;
    const s = path.join(src, n), d = path.join(dst, n);
    if (fs.statSync(s).isDirectory()) copyDir(s, d, skip); else fs.copyFileSync(s, d);
  }
}
const REL_LABELS = {};
LANGS.forEach((L) => { REL_LABELS[L] = OCC[L].birthday.rels; });

/* ------------------------------------------------------------------ festivals calendar */
const NAVRATRI_DATES = ["2026-10-11", "2026-10-12", "2026-10-13", "2026-10-14", "2026-10-15", "2026-10-16", "2026-10-17", "2026-10-18", "2026-10-19"];
const DUSSEHRA = "2026-10-20";
const CAL = [
  { key: "navratri", path: "navratri/", start: "2026-10-11", end: "2026-10-19", img: "N1",
    when: { hi: "11–19 अक्टूबर", gu: "11–19 ઓક્ટોબર", en: "11–19 Oct" } },
  { key: "dussehra", path: "dussehra/", start: "2026-10-20", end: "2026-10-20", img: "S1",
    when: { hi: "20 अक्टूबर", gu: "20 ઓક્ટોબર", en: "20 Oct" } },
  { key: "karva-chauth", path: "karva-chauth/", start: "2026-10-29", end: "2026-10-29", img: "K1",
    when: { hi: "29 अक्टूबर", gu: "29 ઓક્ટોબર", en: "29 Oct" } },
  { key: "diwali", path: "diwali/", start: "2026-11-08", end: "2026-11-08", img: "D1",
    when: { hi: "8 नवंबर", gu: "8 નવેમ્બર", en: "8 Nov" } }
];
const LATER = [
  { name: { hi: "भाई दूज", gu: "ભાઈબીજ", en: "Bhai Dooj" }, when: { hi: "11 नवंबर", gu: "11 નવેમ્બર", en: "11 Nov" } },
  { name: { hi: "उत्तरायण", gu: "ઉત્તરાયણ", en: "Uttarayan" }, when: { hi: "14 जनवरी 2027", gu: "14 જાન્યુઆરી 2027", en: "14 Jan 2027" } }
];

/* ------------------------------------------------------------------ card designs */
// zone = [top, bottom] of the text area on a 1080x1350 card; w = max text width
const DESIGNS = {
  N1: { tone: "dark", zone: [210, 990], w: 820, scrim: 0.5 },
  N2: { tone: "dark", zone: [170, 930], w: 820, scrim: 0.55 },
  N3: { tone: "dark", zone: [140, 800], w: 820, scrim: 0.5 },
  N4: { tone: "light", zone: [300, 960], w: 640, ink: "#9A1B4B" },
  U1: { tone: "dark", zone: [210, 1140], w: 780, scrim: 0.25 },
  U2: { tone: "dark", zone: [200, 1150], w: 820, scrim: 0.1 },
  U3: { tone: "light", zone: [230, 1120], w: 800, ink: "#5B2A86" },
  U4: { tone: "light", zone: [330, 1030], w: 820, ink: "#8C2F4B" },
  U5: { tone: "dark", zone: [200, 1150], w: 800, scrim: 0.3 },
  U6: { tone: "dark", zone: [170, 1180], w: 860, scrim: 0.3 },
  D1: { tone: "dark", zone: [150, 900], w: 880, scrim: 0.25 },
  D2: { tone: "dark", zone: [330, 1080], w: 880, scrim: 0.35 },
  D3: { tone: "dark", zone: [430, 1060], w: 820, scrim: 0.35 },
  D4: { tone: "light", zone: [240, 1090], w: 760, ink: "#7A4A12" },
  S1: { tone: "dark", zone: [260, 960], w: 860, scrim: 0.55 },
  S2: { tone: "dark", zone: [260, 1110], w: 860, scrim: 0.3 },
  K1: { tone: "dark", zone: [300, 900], w: 820, scrim: 0.6 },
  K2: { tone: "light", zone: [340, 1000], w: 660, ink: "#1F2A5C" },
  B1: { tone: "light", zone: [280, 1010], w: 720, ink: "#C2185B" },
  B2: { tone: "light", zone: [300, 1030], w: 780, ink: "#7B2CBF" },
  B3: { tone: "dark", zone: [260, 1100], w: 760, scrim: 0.2 },
  B4: { tone: "light", zone: [190, 1170], w: 700, ink: "#8E2C6B" },
  C1: { tone: "light", zone: [190, 900], w: 760, ink: "#8B1030" },
  C2: { tone: "light", zone: [270, 1050], w: 620, ink: "#8B1030", scrim: 0.5 },
  C3: { tone: "light", zone: [330, 1060], w: 800, ink: "#C2185B" },
  C4: { tone: "light", zone: [230, 1120], w: 760, ink: "#7A5A12" },
  M1: { tone: "light", zone: [130, 640], w: 900, ink: "#5A2A0C", scrim: 0.55 },
  M2: { tone: "light", zone: [120, 620], w: 900, ink: "#4A2C12", scrim: 0.45 },
  M3: { tone: "light", zone: [330, 1000], w: 820, ink: "#1F5AA6" },
  M4: { tone: "light", zone: [120, 700], w: 900, ink: "#8C2F5B", scrim: 0.45 },
  P1: { tone: "light", zone: [150, 1200], w: 820, ink: "#7A4A12" },
  P2: { tone: "light", zone: [150, 1200], w: 820, ink: "#3F3F4A" },
  P3: { tone: "dark", zone: [150, 1200], w: 820 }
};
const SETS = {
  shraddhanjali: ["P2", "M4", "C4", "M1", "P1", "U2", "U4", "U5"],
  "inv-wedding": ["C2", "U1", "U5", "N1", "C4", "U2", "P1", "P3", "D4", "U4"],
  "inv-engagement": ["C4", "C3", "C1", "U4", "U2", "B4", "U3", "P1", "U6", "C2"],
  "inv-birthday-party": ["B2", "B1", "B3", "B4", "U6", "U3", "M3", "D3", "U2", "C3"],
  "inv-griha-pravesh": ["N3", "D1", "N1", "D4", "U1", "U5", "P1", "P3", "S1", "U4"],
  "inv-baby-shower": ["M3", "C3", "U3", "B4", "B2", "U4", "K2", "M4", "P1", "C4"],
  "inv-naming-ceremony": ["K2", "M3", "C3", "U3", "B4", "U4", "M4", "B2", "P1", "C4"],
  "inv-puja": ["N3", "N1", "D1", "S1", "U1", "U5", "P3", "M4", "N2", "P1"],
  "inv-shop-opening": ["D2", "S2", "U2", "B3", "U5", "U1", "N1", "D4", "P3", "U6"],
  navratri: ["N1", "N2", "N3", "N4", "U1", "U5", "U2", "U6", "U3", "U4"],
  dussehra: ["S1", "S2", "N1", "N3", "U1", "U5", "U2", "U6", "D2", "U3"],
  "karva-chauth": ["K1", "K2", "U1", "U2", "C1", "C4", "U4", "U6", "D4", "U5"],
  diwali: ["D1", "D2", "D3", "D4", "N1", "U1", "U2", "U5", "U6", "U3"],
  birthday: ["B1", "B2", "B3", "B4", "U3", "U6", "U2", "U4", "C3", "M3"],
  anniversary: ["C1", "C3", "C4", "C2", "U1", "U2", "U4", "U5", "B3", "U3"],
  wedding: ["C2", "C1", "C4", "U1", "U5", "U2", "C3", "U4", "N1", "U6"],
  engagement: ["C4", "C3", "C1", "C2", "U4", "U2", "U3", "U1", "B4", "U6"],
  "good-morning": ["M1", "M2", "M3", "M4", "U3", "U4", "B4", "U6", "C4", "U5"]
};
const LIGHT_DAY = ["#F7F3EE", "#F5C518"];
const tileCls = (c) => "day-tile" + (LIGHT_DAY.indexOf(c) >= 0 ? " is-light" : "");
const designList = (set) => SETS[set].map((id) => Object.assign({ id }, DESIGNS[id]));

/* ------------------------------------------------------------------ icons */
const I = {
  menu: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 7h16M4 12h16M4 17h10" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>',
  close: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 6l12 12M18 6L6 18" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>',
  globe: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M3 12h18M12 3c2.6 2.5 3.9 5.5 3.9 9s-1.3 6.5-3.9 9c-2.6-2.5-3.9-5.5-3.9-9S9.4 5.5 12 3z" fill="none" stroke="currentColor" stroke-width="1.8"/></svg>',
  arrow: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 12h13M13 6l6 6-6 6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
  chevron: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 9l6 6 6-6" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
  wa: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2a10 10 0 00-8.6 15.1L2 22l5-1.3A10 10 0 1012 2zm0 18.2a8.2 8.2 0 01-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1112 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.7.8-.8 1-.3.2-.5.1a6.7 6.7 0 01-3.3-2.9c-.3-.4.3-.4.8-1.3.1-.2 0-.3 0-.4l-.8-1.8c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 00-.7.3 3 3 0 00-.9 2.2 5.2 5.2 0 001.1 2.7 11.8 11.8 0 004.5 4c1.7.7 2.3.8 3.2.6a2.7 2.7 0 001.8-1.2 2.2 2.2 0 00.1-1.3c0-.1-.2-.2-.4-.3z"/></svg>',
  fb: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M13.5 21v-7.5H16l.4-3h-2.9V8.6c0-.9.3-1.5 1.5-1.5h1.5V4.4a20 20 0 00-2.2-.1c-2.2 0-3.7 1.3-3.7 3.8v2.4H8v3h2.6V21z"/></svg>',
  ig: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="3" width="18" height="18" rx="5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="12" cy="12" r="4" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="17.3" cy="6.7" r="1.2" fill="currentColor"/></svg>',
  download: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 4v11M7 10l5 5 5-5M5 20h14" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
  link: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M10 14a4 4 0 005.7 0l3-3a4 4 0 00-5.7-5.7l-1 1M14 10a4 4 0 00-5.7 0l-3 3a4 4 0 005.7 5.7l1-1" stroke="currentColor" stroke-width="2" stroke-linecap="round" fill="none"/></svg>',
  share: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="18" cy="5" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="6" cy="12" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="18" cy="19" r="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M8.2 10.8l7.6-4.4M8.2 13.2l7.6 4.4" stroke="currentColor" stroke-width="2" fill="none"/></svg>',
  image: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="4" width="18" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><circle cx="9" cy="10" r="2" fill="currentColor"/><path d="M4 18l5-5 4 4 3-3 4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/></svg>',
  refresh: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 12a8 8 0 11-2.3-5.7M20 4v5h-5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" fill="none"/></svg>',
  copy: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="8" y="8" width="12" height="12" rx="2.5" fill="none" stroke="currentColor" stroke-width="2"/><path d="M16 8V6a2 2 0 00-2-2H6a2 2 0 00-2 2v8a2 2 0 002 2h2" fill="none" stroke="currentColor" stroke-width="2"/></svg>',
  calendar: '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="3" y="5" width="18" height="16" rx="3" fill="none" stroke="currentColor" stroke-width="2"/><path d="M3 10h18M8 3v4M16 3v4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/></svg>',
  sparkle: '<svg viewBox="0 0 24 24" aria-hidden="true"><path fill="currentColor" d="M12 2l1.8 6.2L20 10l-6.2 1.8L12 18l-1.8-6.2L4 10l6.2-1.8zM19 15l.9 2.1L22 18l-2.1.9L19 21l-.9-2.1L16 18l2.1-.9z"/></svg>',
  cake: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 21h16v-7a2 2 0 00-2-2H6a2 2 0 00-2 2zM4 16c1.3 0 1.3 1 2.7 1s1.3-1 2.6-1 1.4 1 2.7 1 1.3-1 2.6-1 1.4 1 2.7 1 1.4-1 2.7-1M12 12V8M12 5.5c.8 0 1.2-.7 1.2-1.3S12 2 12 2s-1.2 1.6-1.2 2.2.4 1.3 1.2 1.3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  rings: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="9" cy="14" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><circle cx="15" cy="14" r="5.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M13 3l2 3 2-3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
  heart: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 20s-7.5-4.6-9.2-9.3C1.6 7.3 4 4 7.3 4c2 0 3.6 1.1 4.7 2.7C13.1 5.1 14.7 4 16.7 4 20 4 22.4 7.3 21.2 10.7 19.5 15.4 12 20 12 20z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
  mandap: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 9c3-1 6-3 9-6 3 3 6 5 9 6M5 9v12M19 9v12M3 21h18M9 21v-6a3 3 0 016 0v6" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
  sun: '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="4.5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 2v2.5M12 19.5V22M2 12h2.5M19.5 12H22M4.9 4.9l1.8 1.8M17.3 17.3l1.8 1.8M4.9 19.1l1.8-1.8M17.3 6.7l1.8-1.8" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
  diya: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M2.5 13.5h19c-.8 4-4.6 6.5-9.5 6.5s-8.7-2.5-9.5-6.5z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/><path d="M12 3c1.8 2.3 2.6 4 2.6 5.4A2.6 2.6 0 0112 11a2.6 2.6 0 01-2.6-2.6C9.4 7 10.2 5.3 12 3z" fill="currentColor"/></svg>',
  bowl: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M3 11h18a9 9 0 01-18 0zM8 7c0-1.5 1-2 1-3.5M12 7c0-1.5 1-2 1-3.5M16 7c0-1.5 1-2 1-3.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
  sticks: '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20L16 4M8 20L20 4" stroke="currentColor" stroke-width="2" stroke-linecap="round"/><circle cx="16" cy="4" r="1.6" fill="currentColor"/><circle cx="20" cy="4" r="1.6" fill="currentColor"/></svg>'
};
const LOGO = '<svg class="logo-mark" viewBox="0 0 48 48" aria-hidden="true"><defs><linearGradient id="lg-a" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#FF3D7F"/><stop offset=".55" stop-color="#E0115F"/><stop offset="1" stop-color="#FF9F1C"/></linearGradient><linearGradient id="lg-b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#FFF6D6"/><stop offset="1" stop-color="#FFC94A"/></linearGradient></defs><rect width="48" height="48" rx="14" fill="url(#lg-a)"/><path d="M9 28.5h30c-1.3 6.3-7.3 10-15 10s-13.7-3.7-15-10z" fill="#fff"/><path d="M24 8.5c3.4 4.3 5 7.6 5 10.2a5 5 0 01-10 0c0-2.6 1.6-5.9 5-10.2z" fill="url(#lg-b)"/><circle cx="36.5" cy="12" r="2.2" fill="#FFF3C4"/><circle cx="11" cy="15" r="1.5" fill="#FFF3C4" opacity=".8"/></svg>';

/* ------------------------------------------------------------------ fonts */
const FONT_CSS = (() => {
  const dv = "U+0900-097F,U+1CD0-1CF9,U+200C-200D,U+20A8,U+20B9,U+20F0,U+25CC,U+A830-A839,U+A8E0-A8FF";
  const gu = "U+0951-0952,U+0964-0965,U+0A80-0AFF,U+200C-200D,U+20B9,U+25CC,U+A830-A839";
  const la = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+0304,U+0308,U+0329,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215,U+FEFF,U+FFFD";
  const ff = (fam, file, w, range) => `@font-face{font-family:'${fam}';font-style:normal;font-weight:${w};font-display:swap;src:url(/static/fonts/${file}.woff2) format('woff2');unicode-range:${range}}`;
  let css = "";
  css += ff("Rozha One", "rozha-one-devanagari-400-normal", 400, dv) + ff("Rozha One", "rozha-one-latin-400-normal", 400, la);
  [600, 700].forEach((w) => { css += ff("Rasa", `rasa-gujarati-${w}-normal`, w, gu) + ff("Rasa", `rasa-latin-${w}-normal`, w, la); });
  [400, 500, 600, 700].forEach((w) => {
    css += ff("Hind", `hind-devanagari-${w}-normal`, w, dv) + ff("Hind", `hind-latin-${w}-normal`, w, la);
    css += ff("Hind Vadodara", `hind-vadodara-gujarati-${w}-normal`, w, gu) + ff("Hind Vadodara", `hind-vadodara-latin-${w}-normal`, w, la);
  });
  return css;
})();
const FONTS = {
  hi: { display: "'Rozha One', serif", body: "'Hind', system-ui, sans-serif", preload: ["rozha-one-devanagari-400-normal", "hind-devanagari-500-normal"] },
  gu: { display: "'Rasa', serif", body: "'Hind Vadodara', system-ui, sans-serif", preload: ["rasa-gujarati-700-normal", "hind-vadodara-gujarati-500-normal"] },
  en: { display: "'Rozha One', serif", body: "'Hind', system-ui, sans-serif", preload: ["rozha-one-latin-400-normal", "hind-latin-500-normal"] }
};

/* ------------------------------------------------------------------ layout */
function navItems(L) {
  const n = UI[L].nav;
  return {
    festivals: [["navratri", "navratri/"], ["dussehra", "dussehra/"], ["karva-chauth", "karva-chauth/"], ["diwali", "diwali/"]].map(([k, p]) => ({ k, p, t: n[k] })),
    invites: [["invitations", "invitations/"]].concat(INVITES.map((k) => [k, "invitations/" + k + ".html"])).map(([k, p]) => ({ k, p, t: k === "invitations" ? NP[L].invitations.nav : NP[L].invites[k].nav })),
    tribute: { k: "shraddhanjali", p: "shraddhanjali/", t: NP[L].shraddhanjali.nav },
    occasions: [["birthday", "wishes/birthday.html"], ["anniversary", "wishes/anniversary.html"], ["wedding", "wishes/wedding.html"], ["engagement", "wishes/engagement.html"], ["good-morning", "wishes/good-morning.html"]].map(([k, p]) => ({ k, p, t: n[k] })),
    more: [["recipes", "navratri/vrat-recipes.html"], ["garba", "navratri/garba-dandiya.html"], ["about", "about.html"], ["contact", "contact.html"]].map(([k, p]) => ({ k, p, t: n[k] }))
  };
}
const OCC_ICON = { invitations: "mandap", shraddhanjali: "diya", "birthday-party": "cake", "griha-pravesh": "mandap", "baby-shower": "heart", "naming-ceremony": "heart", puja: "diya", "shop-opening": "sparkle", birthday: "cake", anniversary: "heart", wedding: "mandap", engagement: "rings", "good-morning": "sun", navratri: "sticks", dussehra: "sparkle", "karva-chauth": "sparkle", diwali: "diya", recipes: "bowl", garba: "sticks", about: "sparkle", contact: "sparkle" };

function header(L, p, active) {
  const u = UI[L], N = navItems(L);
  const link = (it, cls) => `<a class="${cls}" href="${url(L, it.p)}"${active === it.k ? ' aria-current="page"' : ""}>${esc(it.t)}</a>`;
  const langs = LANGS.map((x) => `<a href="${url(x, p)}" lang="${x}" hreflang="${x}"${x === L ? ' aria-current="true"' : ""}>${esc(UI[x].lang_short)}</a>`).join("");
  const occList = N.occasions.concat([N.tribute], N.more);
  const occActive = occList.some((i) => i.k === active);
  const invActive = N.invites.some((i) => i.k === active);
  const invLink = N.invites[0];
  const drawerGroup = (key, list) => `<div class="drawer-group"><p class="drawer-h">${esc(u.nav_groups[key])}</p><ul>${list.map((it) => `<li><a href="${url(L, it.p)}"${active === it.k ? ' aria-current="page"' : ""}><span class="ico">${I[OCC_ICON[it.k]] || I.sparkle}</span>${esc(it.t)}</a></li>`).join("")}</ul></div>`;
  return `<a class="skip" href="#main">${esc(u.skip)}</a>
<header class="hdr" id="top">
  <div class="wrap hdr-in">
    <a class="logo" href="${url(L, "")}" aria-label="Indian Festival Wishes">${LOGO}<span class="logo-t">Indian Festival <b>Wishes</b></span></a>
    <nav class="nav-desk" aria-label="${esc(u.menu)}">
      <a class="nav-link" href="${url(L, "")}"${active === "home" ? ' aria-current="page"' : ""}>${esc(u.nav.home)}</a>
      ${N.festivals.map((it) => link(it, "nav-link")).join("")}
      <a class="nav-link" href="${url(L, invLink.p)}"${invActive ? ' aria-current="page"' : ""}>${esc(invLink.t)}</a>
      <div class="nav-more">
        <button class="nav-link nav-more-btn" type="button" aria-expanded="false" aria-controls="nav-occ"${occActive ? ' data-active="1"' : ""}>${esc(u.nav_groups.occasions)}${I.chevron}</button>
        <div class="nav-pop" id="nav-occ" hidden>${occList.map((it) => `<a href="${url(L, it.p)}"${active === it.k ? ' aria-current="page"' : ""}><span class="ico">${I[OCC_ICON[it.k]] || I.sparkle}</span>${esc(it.t)}</a>`).join("")}</div>
      </div>
    </nav>
    <div class="lang-pill" role="group" aria-label="${esc(u.language)}">${I.globe}${langs}</div>
    <button class="burger" id="menu-btn" type="button" aria-expanded="false" aria-controls="drawer" aria-label="${esc(u.menu)}">${I.menu}</button>
  </div>
  <nav class="chips-nav" aria-label="${esc(u.nav_groups.festivals)}"><div class="chips-row">${N.festivals.map((it) => link(it, "chip")).join("")}<a class="chip chip-hot" href="${url(L, invLink.p)}"${invActive ? ' aria-current="page"' : ""}>${esc(invLink.t)}</a>${N.occasions.concat([N.tribute]).map((it) => link(it, "chip")).join("")}</div></nav>
</header>
<div class="drawer" id="drawer" hidden>
  <div class="drawer-scrim" data-close></div>
  <div class="drawer-panel" role="dialog" aria-modal="true" aria-label="${esc(u.menu)}">
    <div class="drawer-top"><span class="logo">${LOGO}<span class="logo-t">Indian Festival <b>Wishes</b></span></span><button class="icon-btn" type="button" data-close aria-label="${esc(u.close)}">${I.close}</button></div>
    ${drawerGroup("festivals", N.festivals)}${drawerGroup("invites", N.invites)}${drawerGroup("occasions", N.occasions.concat([N.tribute]))}${drawerGroup("more", N.more)}
    <div class="drawer-lang">${LANGS.map((x) => `<a href="${url(x, p)}" lang="${x}"${x === L ? ' aria-current="true"' : ""}>${esc(UI[x].lang_name)}</a>`).join("")}</div>
  </div>
</div>`;
}

function footer(L) {
  const u = UI[L], N = navItems(L);
  const col = (h, list) => `<div class="f-col"><p class="f-h">${esc(h)}</p><ul>${list.map((it) => `<li><a href="${url(L, it.p)}">${esc(it.t)}</a></li>`).join("")}</ul></div>`;
  const legal = [["about", "about.html"], ["contact", "contact.html"], ["privacy", "privacy-policy.html"], ["disclaimer", "disclaimer.html"]].map(([k, p]) => ({ k, p, t: u.nav[k] }));
  return `<footer class="ftr">
  <div class="ftr-wave" aria-hidden="true"></div>
  <div class="wrap ftr-grid">
    <div class="f-brand"><span class="logo">${LOGO}<span class="logo-t">Indian Festival <b>Wishes</b></span></span><p>${esc(u.footer_about)}</p></div>
    ${col(u.nav_groups.festivals, N.festivals)}
    ${col(u.nav_groups.occasions, N.occasions.concat([N.tribute, N.invites[0]]))}
    ${col(u.nav_groups.more, [N.more[0], N.more[1]].concat(legal))}
  </div>
  <div class="wrap ftr-bottom"><p class="f-note">${esc(u.footer_note)}</p><p>${esc(u.rights)} · <a href="mailto:contact@indianfestivalwishes.com">contact@indianfestivalwishes.com</a></p></div>
</footer>
<a class="to-top" href="#top" aria-label="${esc(u.back_top)}">${I.arrow}</a>`;
}

function page(o) {
  // o: {L, p, title, desc, active, body, data, og, ld, noindex, cards}
  const L = o.L, F = FONTS[L];
  const alts = o.noAlt ? "" : LANGS.map((x) => `<link rel="alternate" hreflang="${x}" href="${abs(x, o.p)}">`).join("\n") + `\n<link rel="alternate" hreflang="x-default" href="${abs("hi", o.p)}">`;
  const data = Object.assign({ lang: L, page: o.pageTag || "info", dates: NAVRATRI_DATES, dussehra: DUSSEHRA, fonts: { display: F.display, body: F.body }, ui: UI[L] }, o.data || {});
  const ld = [{ "@context": "https://schema.org", "@type": "WebPage", name: o.title, description: o.desc, inLanguage: L, url: abs(L, o.p) }].concat(o.ld || []);
  return `<!doctype html>
<html lang="${L}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>${esc(o.title)}</title>
<meta name="description" content="${esc(o.desc)}">
${o.noindex ? '<meta name="robots" content="noindex, follow">' : ""}
<link rel="canonical" href="${abs(L, o.p)}">
${alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="Indian Festival Wishes">
<meta property="og:title" content="${esc(o.title)}">
<meta property="og:description" content="${esc(o.desc)}">
<meta property="og:url" content="${abs(L, o.p)}">
<meta property="og:image" content="${SITE}/static/og/${o.og || "hub.png"}">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#E0115F">
<meta name="google-adsense-account" content="${ADSENSE_PUB}">
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
${F.preload.map((f) => `<link rel="preload" href="/static/fonts/${f}.woff2" as="font" type="font/woff2" crossorigin>`).join("\n")}
<style>${FONT_CSS}:root{--f-display:${F.display};--f-body:${F.body}}</style>
<link rel="stylesheet" href="/static/style.css?v=${ASSET_V}">
<script src="/static/app.js?v=${ASSET_V}" defer></script>
${o.cards ? `<script src="/static/cards.js?v=${ASSET_V}" defer></script>` : ""}
<script type="application/ld+json">${jsonScript(ld.length === 1 ? ld[0] : ld)}</script>
</head>
<body class="lang-${L} pg-${o.pageTag || "info"}">
${header(L, o.p, o.active)}
<main id="main">
${o.body}
</main>
${footer(L)}
<script id="page-data" type="application/json">${jsonScript(data)}</script>
</body>
</html>
`;
}

/* ------------------------------------------------------------------ shared blocks */
const slots = (L, aff) => `<div class="tg-slot"></div>
<div class="ad-slot" data-slot="top"></div>`;
const affSlot = (L, key) => `<div class="aff-slot" data-aff="${key}" data-title="${esc(UI[L].shop_h)}" data-note="${esc(UI[L].aff_note)}"></div>`;

function pageHead(L, o) {
  // o: {kicker, h1, sub, crumbs:[[t,href]], img, color}
  const crumbs = o.crumbs ? `<ol class="crumbs">${o.crumbs.map(([t, h]) => h ? `<li><a href="${h}">${esc(t)}</a></li>` : `<li aria-current="page">${esc(t)}</li>`).join("")}</ol>` : "";
  return `<section class="phead${o.img ? " has-img" : ""}"${o.color ? ` style="--accent:${o.color}"` : ""}>
  ${o.img ? `<div class="phead-bg" aria-hidden="true" style="background-image:url(/static/cards/thumb/${o.img}.webp)"></div>` : ""}
  <div class="phead-blobs" aria-hidden="true"><span></span><span></span><span></span></div>
  <div class="wrap phead-in">
    ${crumbs}
    ${o.kicker ? `<p class="kicker">${I.sparkle}<span>${esc(o.kicker)}</span></p>` : ""}
    <h1 class="phead-h1">${esc(o.h1)}</h1>
    ${o.sub ? `<p class="phead-sub">${esc(o.sub)}</p>` : ""}
    ${o.extra || ""}
  </div>
</section>`;
}

function cardMaker(L, K) {
  // K = card config; returns html. Fields depend on kind.
  const u = UI[L];
  const kind = K.kind;
  const invite = kind === "invite";
  const rels = invite ? "" : K.rels.map(([k, t]) => `<option value="${esc(k)}">${esc(t)}</option>`).join("");
  let names = "";
  if (invite) {
    const long = { venue: 90, host: 90, note: 90 };
    names = Object.keys(K.fieldDefs).map((k) => `<div class="field"><label for="f-${k}">${esc(K.fieldDefs[k].label)}</label><input id="f-${k}" type="text" maxlength="${long[k] || 50}" placeholder="${esc(K.fieldDefs[k].ph)}"></div>`).join("");
  } else if (kind === "couple") {
    names = `<div class="row2"><div class="field"><label for="in-n1">${esc(u.n1_label)}</label><input id="in-n1" type="text" maxlength="30" placeholder="${esc(u.n1_ph)}"></div><div class="field"><label for="in-n2">${esc(u.n2_label)}</label><input id="in-n2" type="text" maxlength="30" placeholder="${esc(u.n2_ph)}"></div></div>`;
  } else if (kind === "person") {
    names = `<div class="field"><label for="in-to">${esc(K.toLabel || u.to_label)}</label><input id="in-to" type="text" maxlength="30" placeholder="${esc(u.to_ph)}"></div>`;
  }
  const fromReq = kind === "festival";
  if (!invite) names += `<div class="field"><label for="in-from">${esc(fromReq ? u.from_label : u.from_label_opt)}</label><input id="in-from" type="text" maxlength="30" autocomplete="name" placeholder="${esc(u.from_ph)}"></div>`;
  const thought = kind === "morning" ? `<div class="field thought-box"><span class="label" id="thought-label">${esc(u.thought_label)}</span><p class="thought" id="thought-text" aria-labelledby="thought-label"></p><button class="btn btn-soft btn-sm" id="next-thought" type="button">${I.refresh}${esc(u.next_thought)}</button></div>` : "";
  const photo = kind !== "festival" || true ? `<fieldset class="field" id="photo-box"><legend>${esc(u.photo_label)}</legend>
        <div class="segs"><button type="button" class="seg" data-photo-mode="without" aria-pressed="true">${esc(u.without_photo)}</button><button type="button" class="seg" data-photo-mode="with" aria-pressed="false">${esc(u.with_photo)}</button></div>
        <div id="photo-pick" hidden><label class="btn btn-soft file-btn">${I.image}${esc(u.choose_photo)}<input id="card-photo" type="file" accept="image/*"></label><p class="hint">${esc(u.photo_hint)}</p></div>
      </fieldset>` : "";
  const designs = K.designs.map((d, i) => `<button type="button" class="dz" data-i="${i}" aria-pressed="${i === 0}" aria-label="${esc(u.step_design)} ${i + 1}"><img src="/static/cards/thumb/${d.id}.webp" alt="" width="108" height="135" loading="lazy" decoding="async"></button>`).join("");
  return `<section class="maker reveal" id="card-maker" aria-labelledby="card-heading">
  <div class="maker-preview">
    <div class="canvas-frame"><canvas id="card" width="1080" height="1350" role="img" aria-label="${esc(u.card_heading)}"></canvas><div class="canvas-loading" id="canvas-loading">${esc(u.loading_design)}</div></div>
  </div>
  <div class="maker-form">
    <h2 id="card-heading" class="maker-h">${esc(u.card_heading)}</h2>
    <p class="received-note" id="received-note"></p>
    <form id="card-form" novalidate>
      <fieldset class="field"><legend><span class="step-n">1</span>${esc(u.step_design)} <span class="muted">· ${esc(fmt(u.designs_count, { n: K.designs.length }))}</span></legend>
        <div class="dz-row" id="design-row">${designs}</div>
      </fieldset>
      ${invite ? (K.types ? `<div class="field"><label for="card-type"><span class="step-n">2</span>${esc(u.type_label)}</label><select id="card-type">${K.types.map((t, i) => `<option value="${i}">${esc(t.label)}</option>`).join("")}</select></div>` : "")
        : `<div class="field"><label for="card-rel"><span class="step-n">2</span>${esc(u.rel_label)}</label><select id="card-rel">${rels}</select></div>`}
      <div class="field"><label for="card-wish">${invite && !K.types ? '<span class="step-n">2</span>' : ""}${esc(invite ? u.wording_label : u.wish_label)}</label><select id="card-wish"></select></div>
      <div class="field" id="custom-box" hidden><label for="card-custom">${esc(u.custom_label)}</label><textarea id="card-custom" rows="3" maxlength="180" placeholder="${esc(u.custom_ph)}"></textarea></div>
      ${thought}
      ${invite ? names + photo : photo + names}
      <p class="form-error" id="card-error" role="alert"></p>
      <button class="btn btn-primary btn-wide shine" type="submit">${I.sparkle}${esc(u.make_card)}</button>
    </form>
    <div class="share" id="share-actions" hidden>
      <div class="share-main">
        <a class="btn btn-wa" id="btn-wa" href="#" target="_blank" rel="noopener">${I.wa}${esc(u.send_wa)}</a>
        <button class="btn btn-soft" id="btn-share-photo" type="button" hidden>${I.share}${esc(u.share_photo)}</button>
      </div>
      <div class="share-row">
        <a class="icon-chip fb" id="btn-fb" href="#" target="_blank" rel="noopener" aria-label="Facebook">${I.fb}</a>
        <button class="icon-chip ig" id="btn-ig" type="button" aria-label="Instagram">${I.ig}</button>
        <button class="btn btn-soft" id="btn-download" type="button">${I.download}${esc(u.download)}</button>
        <button class="btn btn-soft" id="btn-copy-link" type="button">${I.link}${esc(u.copy_link)}</button>
      </div>
    </div>
    <p class="status" id="card-status" role="status"></p>
  </div>
</section>`;
}

function wishList(L, list, idp) {
  const u = UI[L];
  return `<ul class="wish-list">${list.map((w, i) => `<li class="wish reveal"><p id="${idp}-${i}">${esc(w)}</p><button class="copy-btn" type="button" data-copy="${idp}-${i}">${I.copy}<span>${esc(u.copy)}</span></button></li>`).join("")}</ul>`;
}

function faqBlock(L, faq) {
  if (!faq || !faq.length) return "";
  return `<section class="faq reveal"><h2 class="sec-h">${esc(UI[L].faq_h)}</h2>${faq.map((f, i) => `<details class="faq-item"${i === 0 ? " open" : ""}><summary>${esc(f.q)}<span class="faq-ico" aria-hidden="true">${I.chevron}</span></summary><p>${esc(f.a)}</p></details>`).join("")}</section>`;
}
const faqLd = (faq) => (faq && faq.length ? [{ "@context": "https://schema.org", "@type": "FAQPage", mainEntity: faq.map((f) => ({ "@type": "Question", name: f.q, acceptedAnswer: { "@type": "Answer", text: f.a } })) }] : []);
const crumbLd = (L, list) => ({ "@context": "https://schema.org", "@type": "BreadcrumbList", itemListElement: list.map(([t, p], i) => ({ "@type": "ListItem", position: i + 1, name: t, item: abs(L, p) })) });

function mergeWishes(base, extra) {
  const out = {};
  Object.keys(base).forEach((k) => { out[k] = base[k].slice(); });
  return out;
}

/* ------------------------------------------------------------------ pages */
const SITEMAP = [];
function emit(L, p, html, inSitemap = true) {
  write(outPath(L, p), html);
  if (inSitemap && L === "hi") SITEMAP.push(p);
}

function countdownData() {
  return CAL.map((c) => ({ key: c.key, start: c.start, end: c.end }));
}

function buildHome(L) {
  const u = UI[L], H = HUB[L], p = "";
  const festCards = CAL.map((c, i) => {
    const t = u.nav[c.key];
    return `<li class="reveal" style="--d:${i * 70}ms"><a class="fest" href="${url(L, c.path)}" data-start="${c.start}" data-end="${c.end}">
      <img src="/static/cards/thumb/${c.img}.webp" alt="" loading="lazy" width="432" height="540">
      <span class="fest-shade"></span>
      <span class="fest-date">${I.calendar}${esc(c.when[L])}</span>
      <span class="fest-body"><span class="fest-name">${esc(t)}</span><span class="fest-count" data-count></span></span>
      <span class="fest-go">${I.arrow}</span>
    </a></li>`;
  }).join("") + LATER.map((c) => `<li class="reveal"><div class="fest fest-soon"><span class="fest-date">${I.calendar}${esc(c.when[L])}</span><span class="fest-body"><span class="fest-name">${esc(c.name[L])}</span><span class="fest-count">${esc(u.soon)}</span></span></div></li>`).join("");
  const occ = navItems(L).occasions.map((it, i) => `<li class="reveal" style="--d:${i * 60}ms"><a class="occ occ-${it.k}" href="${url(L, it.p)}"><span class="occ-ico">${I[OCC_ICON[it.k]]}</span><span class="occ-name">${esc(it.t)}</span><span class="occ-go">${I.arrow}</span></a></li>`).join("");
  const days = NAV[L].days.map((d, i) => `<li class="reveal" style="--d:${i * 40}ms"><a class="${tileCls(d.theme.primary)}" href="${url(L, "navratri/day-" + (i + 1) + ".html")}" data-day="${i + 1}" style="--c:${d.theme.primary}"><span class="day-n">${i + 1}</span><span class="day-devi">${esc(d.devi)}</span><span class="day-col">${esc(d.color)}</span></a></li>`).join("");
  const stack = ["N1", "D3", "B1"].map((id, i) => `<div class="stack-card s${i + 1}"><img src="/static/cards/thumb/${id}.webp" alt="" width="432" height="540"></div>`).join("");
  const body = `
<section class="hero">
  <div class="hero-bg" aria-hidden="true"><span class="orb o1"></span><span class="orb o2"></span><span class="orb o3"></span><span class="grain"></span></div>
  <div class="wrap hero-in">
    <div class="hero-copy">
      <p class="kicker live" id="next-fest">${I.sparkle}<span>${esc(u.hero_kicker)}</span></p>
      <h1 class="hero-h1">${esc(H.h1)}</h1>
      <p class="hero-sub">${esc(u.hero_sub)}</p>
      <div class="hero-cta"><a class="btn btn-primary btn-lg shine" href="${url(L, "navratri/")}">${I.sparkle}${esc(u.hero_cta)}</a><a class="btn btn-ghost btn-lg" href="#festivals">${esc(u.hero_cta2)}${I.arrow}</a></div>
      <ul class="hero-stats">${u.hero_stats.map((s) => `<li>${esc(s)}</li>`).join("")}</ul>
    </div>
    <div class="hero-art" aria-hidden="true">${stack}<span class="spark sp1"></span><span class="spark sp2"></span><span class="spark sp3"></span></div>
  </div>
</section>
<div class="wrap">
  <section class="sec" id="festivals"><div class="sec-top"><h2 class="sec-h">${esc(u.upcoming_h)}</h2><p class="sec-sub">${esc(u.upcoming_sub)}</p></div><ul class="fest-grid">${festCards}</ul></section>
  ${slots(L)}
  <section class="sec"><div class="sec-top"><h2 class="sec-h">${esc(u.occasions_h)}</h2><p class="sec-sub">${esc(u.occasions_sub)}</p></div><ul class="occ-grid">${occ}</ul></section>
  <section class="sec"><div class="sec-top"><h2 class="sec-h">${esc(u.invites_h)}</h2><p class="sec-sub">${esc(u.invites_sub)}</p></div><ul class="inv-grid">${inviteTiles(L)}</ul></section>
  <a class="tribute-band reveal" href="${url(L, "shraddhanjali/")}"><span class="ico">${I.diya}</span><span><b>${esc(u.tribute_tile)}</b><small>${esc(u.tribute_sub)}</small></span>${I.arrow}</a>
  <section class="sec how reveal"><h2 class="sec-h">${esc(u.how_h)}</h2><ol class="how-list">${u.how.map((t, i) => `<li><span class="how-n">${i + 1}</span><span>${esc(t)}</span></li>`).join("")}</ol></section>
  <section class="sec"><div class="sec-top"><h2 class="sec-h">${esc(u.days_h)}</h2><p class="sec-sub">${esc(u.days_sub)}</p></div><ol class="days-grid">${days}</ol></section>
  ${affSlot(L, "home")}
  <article class="prose reveal">${H.article}</article>
  <div class="ad-slot" data-slot="middle"></div>
</div>`;
  emit(L, p, page({ L, p, title: H.title, desc: H.desc, active: "home", pageTag: "home", body, og: "home.png", data: { cal: countdownData() },
    ld: [{ "@context": "https://schema.org", "@type": "WebSite", name: "Indian Festival Wishes", url: SITE + "/", inLanguage: L }] }));
}

function navCard(L, o) {
  return Object.assign({ occasion: "navratri", kind: "festival", rels: REL_LABELS[L], designs: designList("navratri") }, o);
}

function buildNavratri(L) {
  const u = UI[L], N = NAV[L], p = "navratri/";
  const days = N.days.map((d, i) => `<li class="reveal" style="--d:${i * 40}ms"><a class="${tileCls(d.theme.primary)}" href="${url(L, "navratri/day-" + (i + 1) + ".html")}" data-day="${i + 1}" style="--c:${d.theme.primary}"><span class="day-n">${i + 1}</span><span class="day-devi">${esc(d.devi)}</span><span class="day-col">${esc(d.date)}</span></a></li>`).join("");
  const K = navCard(L, { title: N.card_title, topLabel: N.card_top, wishes: MW[L].navratri.card, fromTpl: N.from_home, slug: "navratri-2026", theme: N.days[0].theme });
  const body = `${pageHead(L, { kicker: N.hero_sub, h1: N.hero_title, sub: N.pick, img: "N1", crumbs: [[u.nav.home, url(L, "")], [u.nav.navratri]], extra: '<p class="today-note" id="today-note"></p>' })}
<div class="wrap">
  <ol class="days-grid days-lg">${days}</ol>
  ${cardMaker(L, K)}
  ${slots(L)}
  <section class="sec"><h2 class="sec-h">${esc(u.wishes_h)}</h2>${wishList(L, MW[L].navratri.list, "w")}</section>
  <article class="prose reveal">${N.article}</article>
  <div class="ad-slot" data-slot="middle"></div>
  ${affSlot(L, "navratri")}
</div>`;
  emit(L, p, page({ L, p, title: N.title, desc: N.desc, active: "navratri", pageTag: "navratri", body, og: "home.png", cards: true, data: { card: K },
    ld: [crumbLd(L, [[u.nav.home, ""], [u.nav.navratri, p]])] }));
}

function buildNavDay(L, i) {
  const u = UI[L], N = NAV[L], d = N.days[i], n = i + 1, p = `navratri/day-${n}.html`;
  const K = navCard(L, { title: d.devi, topLabel: d.card_top, wishes: MW[L]["navratri-day-" + n].card, fromTpl: d.from, slug: "navratri-2026-day-" + n, theme: d.theme, dayNum: String(n) });
  const facts = [[u.date_label, d.date], [u.color_label, d.color], [u.bhog_label, d.bhog]];
  const prevNext = `<nav class="pn" aria-label="${esc(u.nav.navratri)}">${n > 1 ? `<a class="pn-a" href="${url(L, `navratri/day-${n - 1}.html`)}"><span>${esc(u.prev)}</span><b>${esc(N.days[i - 1].devi)}</b></a>` : "<span></span>"}${n < 9 ? `<a class="pn-a next" href="${url(L, `navratri/day-${n + 1}.html`)}"><span>${esc(u.next)}</span><b>${esc(N.days[i + 1].devi)}</b></a>` : `<a class="pn-a next" href="${url(L, "dussehra/")}"><span>${esc(u.next)}</span><b>${esc(u.nav.dussehra)}</b></a>`}</nav>`;
  const light = ["#F7F3EE", "#F5C518"].indexOf(d.theme.primary) >= 0;
  const body = `${pageHead(L, { kicker: fmt(u.day_n, { n }) + " · " + d.date, h1: d.devi, sub: d.intro, color: d.theme.primary, crumbs: [[u.nav.home, url(L, "")], [u.nav.navratri, url(L, "navratri/")], [fmt(u.day_n, { n })]],
    extra: `<ul class="facts">${facts.map(([k, v], j) => `<li${j === 1 ? ` class="fact-color" style="--c:${d.theme.primary}"` : ""}><span>${esc(k)}</span><b>${esc(v)}</b></li>`).join("")}</ul>` })}
<div class="wrap">
  ${cardMaker(L, K)}
  ${slots(L)}
  <div class="two-col">
    <article class="prose reveal">
      <h2>${esc(u.story_h)}</h2><p>${esc(d.story)}</p>
      <h2>${esc(u.puja_h)}</h2><p>${esc(d.puja)}</p>
      <h2>${esc(u.mantra_h)}</h2><blockquote class="mantra"><p>${esc(d.mantra)}</p>${d.mantra_translit ? `<p class="translit">${esc(d.mantra_translit)}</p>` : ""}</blockquote>
    </article>
    <aside class="side reveal"><a class="side-card${light ? " is-light" : ""}" href="${url(L, `navratri/vrat-recipes-day-${n}.html`)}" style="--c:${d.theme.primary}"><span class="ico">${I.bowl}</span><span><b>${esc(u.day_recipes)}</b><small>${esc(REC[L].days[i].desc || "")}</small></span>${I.arrow}</a></aside>
  </div>
  <section class="sec"><h2 class="sec-h">${esc(u.wishes_h)}</h2>${wishList(L, d.wishes.concat(MW[L]["navratri-day-" + n].list), "w")}</section>
  <div class="ad-slot" data-slot="middle"></div>
  ${prevNext}
  ${affSlot(L, "navratri-day")}
</div>`;
  emit(L, p, page({ L, p, title: d.title, desc: d.desc, active: "navratri", pageTag: "navratri-day", body, og: `day-${n}.png`, cards: true, data: { card: K, day: n },
    ld: [crumbLd(L, [[u.nav.home, ""], [u.nav.navratri, "navratri/"], [d.devi, p]])] }));
}

function buildRecipesIndex(L) {
  const u = UI[L], R = REC[L], N = NAV[L], p = "navratri/vrat-recipes.html";
  const list = R.days.map((d, i) => `<li class="reveal" style="--d:${i * 40}ms"><a class="rec-tile${LIGHT_DAY.indexOf(N.days[i].theme.primary) >= 0 ? " is-light" : ""}" href="${url(L, `navratri/vrat-recipes-day-${i + 1}.html`)}" style="--c:${N.days[i].theme.primary}"><span class="day-n">${i + 1}</span><span><b>${esc(fmt(u.day_n, { n: i + 1 }))}: ${esc(N.days[i].devi)}</b><small>${esc(d.recipes.map((r) => r.name).join(", "))}</small></span>${I.arrow}</a></li>`).join("");
  const body = `${pageHead(L, { h1: R.title, sub: R.intro, crumbs: [[u.nav.home, url(L, "")], [u.nav.navratri, url(L, "navratri/")], [u.nav.recipes]] })}
<div class="wrap"><ol class="rec-list">${list}</ol>${slots(L)}<article class="prose reveal">${R.article}</article><div class="ad-slot" data-slot="middle"></div>${affSlot(L, "recipes")}</div>`;
  emit(L, p, page({ L, p, title: R.doc_title || R.title, desc: R.desc, active: "recipes", pageTag: "recipes", body }));
}

function qty(q, u) {
  if (u === "g" || u === "ml") return String(q >= 50 ? Math.round(q / 5) * 5 : Math.round(q));
  if (u === "pinch") return String(Math.max(1, Math.round(q)));
  const whole = Math.floor(q + 1e-9); let quarters = Math.round((q - whole) * 4); let w = whole;
  if (quarters === 4) { w += 1; quarters = 0; }
  return ((w ? String(w) : "") + ["", "¼", "½", "¾"][quarters]) || "0";
}
function buildRecipeDay(L, i) {
  const u = UI[L], R = REC[L], d = R.days[i], nd = NAV[L].days[i], n = i + 1, p = `navratri/vrat-recipes-day-${n}.html`;
  const recipes = d.recipes.map((r, j) => `<article class="recipe reveal" id="${esc(r.id)}">
    <header class="recipe-h"><span class="recipe-n">${j + 1}</span><div><h2>${esc(r.name)}</h2><p class="muted">${esc(r.meta)}</p></div></header>
    <div class="recipe-grid">
      <div><h3>${esc(u.ingredients)}</h3><ul class="ing">${r.ingredients.map((g) => g.text != null ? `<li><span>${esc(g.name)}</span><b>${esc(g.text)}</b></li>` : `<li><span>${esc(g.name)}</span><b><span class="qty" data-q="${g.q}" data-u="${esc(g.u)}">${qty(g.q, g.u)}</span> ${esc(g.unit)}</b></li>`).join("")}</ul></div>
      <div><h3>${esc(u.method)}</h3><ol class="steps">${r.steps.map((s) => `<li>${esc(s)}</li>`).join("")}</ol>${r.note ? `<p class="note">${esc(r.note)}</p>` : ""}</div>
    </div>
  </article>`).join("");
  const body = `${pageHead(L, { kicker: fmt(u.day_n, { n }) + " · " + nd.devi, h1: d.title, sub: d.desc, color: nd.theme.primary, crumbs: [[u.nav.home, url(L, "")], [u.nav.recipes, url(L, "navratri/vrat-recipes.html")], [fmt(u.day_n, { n })]] })}
<div class="wrap">
  <div class="servings reveal"><label for="servings">${esc(u.servings)}</label><div class="stepper"><button class="step-btn" type="button" data-step="-1" aria-label="-1">−</button><input id="servings" type="number" min="1" max="30" value="1" inputmode="numeric"><button class="step-btn" type="button" data-step="1" aria-label="+1">+</button></div></div>
  ${recipes}
  ${slots(L)}
  <nav class="pn">${n > 1 ? `<a class="pn-a" href="${url(L, `navratri/vrat-recipes-day-${n - 1}.html`)}"><span>${esc(u.prev)}</span><b>${esc(fmt(u.day_n, { n: n - 1 }))}</b></a>` : `<span></span>`}<a class="pn-a next" href="${url(L, n < 9 ? `navratri/vrat-recipes-day-${n + 1}.html` : "navratri/vrat-recipes.html")}"><span>${esc(u.next)}</span><b>${esc(n < 9 ? fmt(u.day_n, { n: n + 1 }) : u.all_recipes)}</b></a></nav>
  <div class="ad-slot" data-slot="middle"></div>
  ${affSlot(L, "recipes")}
</div>`;
  const ld = [{ "@context": "https://schema.org", "@type": "ItemList", itemListElement: d.recipes.map((r, j) => ({ "@type": "ListItem", position: j + 1, name: r.name })) }];
  emit(L, p, page({ L, p, title: d.title, desc: d.desc, active: "recipes", pageTag: "recipes", body, ld }));
}

function buildInfo(L, key, active, tag) {
  const u = UI[L], P = PAGES[L][key], p = key;
  const crumbs = key.startsWith("navratri/") ? [[u.nav.home, url(L, "")], [u.nav.navratri, url(L, "navratri/")], [P.title]] : [[u.nav.home, url(L, "")], [P.title]];
  const body = `${pageHead(L, { h1: P.title, crumbs })}<div class="wrap">${tag === "garba" ? slots(L) : ""}<article class="prose reveal">${P.body}</article>${tag === "garba" ? `<div class="ad-slot" data-slot="middle"></div>${affSlot(L, "garba")}` : ""}</div>`;
  emit(L, p, page({ L, p, title: P.doc_title || P.title, desc: P.desc, active, pageTag: tag || "info", body }));
}

function buildOccasion(L, occ) {
  const u = UI[L], O = OCC[L][occ], A = ART[L][occ], p = `wishes/${occ}.html`;
  const kind = { birthday: "person", "good-morning": "morning" }[occ] || "couple";
  const K = { occasion: occ, kind, title: O.card_title, topLabel: "", wishes: MW[L][occ].card, rels: O.rels, fromTpl: O.from, theme: O.theme, slug: occ, thoughts: O.thoughts || null, designs: designList(occ) };
  const allW = MW[L][occ].list;
  const body = `${pageHead(L, { h1: O.h1, sub: O.sub, img: SETS[occ][0], crumbs: [[u.nav.home, url(L, "")], [u.nav[occ]]] })}
<div class="wrap">
  ${cardMaker(L, K)}
  ${slots(L)}
  <section class="sec"><h2 class="sec-h">${esc(u.wishes_h)}</h2>${wishList(L, allW, "w")}</section>
  <article class="prose reveal">${A.article}</article>
  <div class="ad-slot" data-slot="middle"></div>
  ${faqBlock(L, A.faq)}
  ${affSlot(L, occ)}
</div>`;
  emit(L, p, page({ L, p, title: O.title, desc: O.desc, active: occ, pageTag: occ, body, cards: true, data: { card: K },
    ld: faqLd(A.faq).concat([crumbLd(L, [[u.nav.home, ""], [u.nav[occ], p]])]) }));
}

function buildFestival(L, key) {
  const u = UI[L], F = FEST[L][key], p = key + "/";
  const K = { occasion: key, kind: "festival", title: F.card_title, topLabel: F.card_top, wishes: MW[L][key].card, rels: F.rels, fromTpl: F.from, theme: F.theme, slug: key + "-2026", designs: designList(key) };
  const allW = MW[L][key].list;
  const cal = CAL.find((c) => c.key === key);
  const body = `${pageHead(L, { kicker: F.date_label, h1: F.h1, sub: F.sub, img: cal.img, crumbs: [[u.nav.home, url(L, "")], [u.nav[key]]],
    extra: `<p class="countdown" data-start="${cal.start}" data-end="${cal.end}"></p>` })}
<div class="wrap">
  <section class="facts-card reveal"><h2 class="sec-h sm">${esc(u.facts_h)}</h2><dl class="facts-grid">${F.facts.map((f) => `<div><dt>${esc(f.label)}</dt><dd>${esc(f.value)}</dd></div>`).join("")}</dl></section>
  ${cardMaker(L, K)}
  ${slots(L)}
  <section class="sec"><h2 class="sec-h">${esc(u.wishes_h)}</h2>${wishList(L, allW, "w")}</section>
  <article class="prose reveal">${F.article}</article>
  <div class="ad-slot" data-slot="middle"></div>
  ${faqBlock(L, F.faq)}
  ${affSlot(L, key)}
</div>`;
  const ev = { "@context": "https://schema.org", "@type": "Event", name: F.h1, startDate: F.date_iso, endDate: F.date_iso, eventAttendanceMode: "https://schema.org/MixedEventAttendanceMode", eventStatus: "https://schema.org/EventScheduled", location: { "@type": "Place", name: "India", address: { "@type": "PostalAddress", addressCountry: "IN" } }, description: F.desc };
  emit(L, p, page({ L, p, title: F.title, desc: F.desc, active: key, pageTag: key, body, cards: true, data: { card: K },
    ld: faqLd(F.faq).concat([crumbLd(L, [[u.nav.home, ""], [u.nav[key], p]]), ev]) }));
}

function inviteCard(L, key, C, set, extra) {
  return Object.assign({
    occasion: key, kind: "invite", title: C.title, topLabel: C.top || "", wordings: C.wordings, fieldDefs: C.fields, join: C.join || "",
    prefix: { host: C.host_prefix || "", date: C.date_prefix || "", time: C.time_prefix || "", venue: C.venue_prefix || "" },
    theme: { primary: "#7A0F35", secondary: "#B7791F" }, slug: key, designs: designList(set)
  }, extra || {});
}

function buildTribute(L) {
  const u = UI[L], T = NP[L].shraddhanjali, p = "shraddhanjali/";
  const K = inviteCard(L, "shraddhanjali", T.card, "shraddhanjali", { types: T.card.types, photoDefault: true, shareMsg: u.tribute_share });
  const body = `${pageHead(L, { h1: T.h1, sub: T.sub, crumbs: [[u.nav.home, url(L, "")], [T.nav]] })}
<div class="wrap">
  ${cardMaker(L, K)}
  <section class="sec"><h2 class="sec-h">${esc(u.tribute_h)}</h2>${wishList(L, T.list, "w")}</section>
  <article class="prose reveal">${T.article}</article>
  ${faqBlock(L, T.faq)}
</div>`;
  emit(L, p, page({ L, p, title: T.title, desc: T.desc, active: "shraddhanjali", pageTag: "shraddhanjali", body, cards: true, data: { card: K },
    ld: faqLd(T.faq).concat([crumbLd(L, [[u.nav.home, ""], [T.nav, p]])]) }));
}

function inviteTiles(L) {
  return INVITES.map((k, i) => {
    const V = NP[L].invites[k];
    return `<li class="reveal" style="--d:${i * 50}ms"><a class="inv-tile" href="${url(L, "invitations/" + k + ".html")}"><img src="/static/cards/thumb/${SETS["inv-" + k][0]}.webp" alt="" loading="lazy" width="432" height="540"><span class="inv-shade"></span><span class="inv-name">${esc(V.nav)}</span><span class="fest-go">${I.arrow}</span></a></li>`;
  }).join("");
}

function buildInvitesHub(L) {
  const u = UI[L], H = NP[L].invitations, p = "invitations/";
  const body = `${pageHead(L, { h1: H.h1, sub: H.sub, crumbs: [[u.nav.home, url(L, "")], [H.nav]] })}
<div class="wrap">
  <ul class="inv-grid">${inviteTiles(L)}</ul>
  ${slots(L)}
  <article class="prose reveal">${H.article}</article>
  ${faqBlock(L, H.faq)}
</div>`;
  emit(L, p, page({ L, p, title: H.title, desc: H.desc, active: "invitations", pageTag: "invitations", body,
    ld: faqLd(H.faq).concat([crumbLd(L, [[u.nav.home, ""], [H.nav, p]])]) }));
}

function buildInvite(L, k) {
  const u = UI[L], V = NP[L].invites[k], H = NP[L].invitations, p = "invitations/" + k + ".html";
  const K = inviteCard(L, k, V.card, "inv-" + k, { shareMsg: u.invite_share });
  const others = INVITES.filter((x) => x !== k).map((x) => `<a class="chip" href="${url(L, "invitations/" + x + ".html")}">${esc(NP[L].invites[x].nav)}</a>`).join("");
  const body = `${pageHead(L, { h1: V.h1, sub: V.sub, img: SETS["inv-" + k][0], crumbs: [[u.nav.home, url(L, "")], [H.nav, url(L, "invitations/")], [V.nav]] })}
<div class="wrap">
  ${cardMaker(L, K)}
  ${slots(L)}
  <section class="sec"><h2 class="sec-h">${esc(u.messages_h)}</h2>${wishList(L, V.list, "w")}</section>
  <article class="prose reveal">${V.article}</article>
  <div class="ad-slot" data-slot="middle"></div>
  ${faqBlock(L, V.faq)}
  <nav class="more-chips" aria-label="${esc(H.nav)}">${others}</nav>
  ${affSlot(L, "invite-" + k)}
</div>`;
  emit(L, p, page({ L, p, title: V.title, desc: V.desc, active: k, pageTag: "invite-" + k, body, cards: true, data: { card: K },
    ld: faqLd(V.faq).concat([crumbLd(L, [[u.nav.home, ""], [H.nav, "invitations/"], [V.nav, p]])]) }));
}

function buildStub(L, from, to) {
  const u = UI[L];
  const target = url(L, to);
  write(outPath(L, from), `<!doctype html>
<html lang="${L}"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>${esc(u.moved)}</title>
<meta name="robots" content="noindex, follow">
<link rel="canonical" href="${SITE + target}">
<meta http-equiv="refresh" content="0; url=${target}">
<script>location.replace(${JSON.stringify(target)} + location.search);</script>
</head><body><p>${esc(u.moved)} <a href="${target}">${esc(u.moved_link)}</a></p></body></html>
`);
}

function build404() {
  const L = "hi", u = UI[L];
  const body = `<section class="nf"><div class="wrap nf-in"><p class="nf-code">404</p><h1 class="phead-h1">${esc(u.nf_title)}</h1><p>${esc(u.nf_text)}</p><p class="nf-links">${LANGS.map((x) => `<a class="btn ${x === "hi" ? "btn-primary" : "btn-ghost"}" href="${url(x, "")}">${esc(UI[x].nf_home)} · ${esc(UI[x].lang_name)}</a>`).join("")}</p></div></section>`;
  write("404.html", page({ L, p: "404.html", title: u.nf_title + " | Indian Festival Wishes", desc: u.nf_text, body, noindex: true, noAlt: true }));
}

function buildSitemap() {
  const lines = SITEMAP.map((p) => `<url><loc>${abs("hi", p)}</loc>${LANGS.map((x) => `<xhtml:link rel="alternate" hreflang="${x}" href="${abs(x, p)}"/>`).join("")}<lastmod>${TODAY}</lastmod></url>` +
    LANGS.slice(1).map((x) => `\n<url><loc>${abs(x, p)}</loc>${LANGS.map((y) => `<xhtml:link rel="alternate" hreflang="${y}" href="${abs(y, p)}"/>`).join("")}<lastmod>${TODAY}</lastmod></url>`).join(""));
  write("sitemap.xml", `<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:xhtml="http://www.w3.org/1999/xhtml">\n${lines.join("\n")}\n</urlset>\n`);
}

/* ------------------------------------------------------------------ run */
function main() {
  fs.rmSync(OUT, { recursive: true, force: true });
  fs.mkdirSync(OUT, { recursive: true });
  copyDir(path.join(ROOT, "static"), path.join(OUT, "static"), (n) => n === "devi");
  ["ads.txt", "robots.txt"].forEach((f) => fs.copyFileSync(path.join(ROOT, f), path.join(OUT, f)));
  for (const L of LANGS) {
    buildHome(L);
    buildNavratri(L);
    for (let i = 0; i < 9; i++) buildNavDay(L, i);
    buildRecipesIndex(L);
    for (let i = 0; i < 9; i++) buildRecipeDay(L, i);
    ["dussehra", "karva-chauth", "diwali"].forEach((k) => buildFestival(L, k));
    ["birthday", "anniversary", "wedding", "engagement", "good-morning"].forEach((o) => buildOccasion(L, o));
    buildTribute(L);
    buildInvitesHub(L);
    INVITES.forEach((k) => buildInvite(L, k));
    buildInfo(L, "navratri/garba-dandiya.html", "garba", "garba");
    buildInfo(L, "about.html", "about");
    buildInfo(L, "contact.html", "contact");
    buildInfo(L, "privacy-policy.html", "privacy");
    buildInfo(L, "disclaimer.html", "disclaimer");
    for (let n = 1; n <= 9; n++) buildStub(L, `day-${n}.html`, `navratri/day-${n}.html`);
    buildStub(L, "garba-dandiya.html", "navratri/garba-dandiya.html");
    buildStub(L, "navratri-vrat-food.html", "navratri/vrat-recipes.html");
  }
  build404();
  buildSitemap();
  let count = 0;
  (function walk(d) { for (const n of fs.readdirSync(d)) { const f = path.join(d, n); if (fs.statSync(f).isDirectory()) walk(f); else if (n.endsWith(".html")) count++; } })(OUT);
  console.log(`Built ${count} HTML files into public/ (${SITEMAP.length * 3} in sitemap)`);
}
main();
