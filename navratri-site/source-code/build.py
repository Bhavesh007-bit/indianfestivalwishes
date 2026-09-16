"""
Indian Festival Wishes: Navratri 2026 site builder.
Edit CONFIG below, then run:  python build.py
Output goes to the  site/  folder. Upload everything inside site/ to GitHub.
"""
import datetime as dt
import html
import json
import os
import shutil

import content_en
import content_gu
import content_hi

# ------------------------------------------------------------------
CONFIG = {
    "domain": "https://www.indianfestivalwishes.com",   # apna domain yahan (end me / nahi)
    "email": "contact@indianfestivalwishes.com",        # apna email yahan
    "adsense_client": "",                     # jaise "ca-pub-1234567890123456" (approval ke baad)
    "updated": {"hi": "16 सितंबर 2026", "gu": "16 સપ્ટેમ્બર 2026", "en": "16 September 2026"},
}
START = dt.date(2026, 10, 11)       # Navratri day 1 (Ghatasthapana)
DUSSEHRA = dt.date(2026, 10, 20)
OUT = "site"
# ------------------------------------------------------------------

LANGS = {"hi": content_hi, "gu": content_gu, "en": content_en}
PREFIX = {"hi": "", "gu": "gu/", "en": "en/"}
LANG_SHORT = {"hi": "हिं", "gu": "ગુ", "en": "EN"}
LANG_NAME = {"hi": "हिन्दी", "gu": "ગુજરાતી", "en": "English"}
FONT_CSS = {
    "hi": "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Hind:wght@400;600&display=swap",
    "en": "https://fonts.googleapis.com/css2?family=Baloo+2:wght@600;700;800&family=Hind:wght@400;600&display=swap",
    "gu": "https://fonts.googleapis.com/css2?family=Baloo+Bhai+2:wght@600;700;800&family=Hind+Vadodara:wght@400;600&display=swap",
}
CANVAS_FONT = {"hi": "'Baloo 2', sans-serif", "en": "'Baloo 2', sans-serif", "gu": "'Baloo Bhai 2', sans-serif"}
EXTRA_UI = {
    "hi": {"btn_share_photo": "फ़ोटो शेयर करें", "today_short": "आज"},
    "gu": {"btn_share_photo": "ફોટો શેર કરો", "today_short": "આજે"},
    "en": {"btn_share_photo": "Share photo", "today_short": "Today"},
}

# Day colours: background, text colour, accent
COLORS = [
    ("#F07C12", "#2B1B14", "#7E0B20"),
    ("#F7F3EE", "#2B1B14", "#B3122E"),
    ("#C4122F", "#FFFFFF", "#F2A007"),
    ("#2748A8", "#FFFFFF", "#F2A007"),
    ("#F5C518", "#2B1B14", "#B3122E"),
    ("#267A35", "#FFFFFF", "#F2A007"),
    ("#6E7179", "#FFFFFF", "#F2A007"),
    ("#6B2FA0", "#FFFFFF", "#F2A007"),
    ("#0F7C7A", "#FFFFFF", "#F2A007"),
]
HOME_COLOR = ("#B3122E", "#FFFFFF", "#F2A007")

MANTRA_STEMS = [
    ("शैलपुत्र्यै", "શૈલપુત્ર્યૈ", "Shailaputryai"),
    ("ब्रह्मचारिण्यै", "બ્રહ્મચારિણ્યૈ", "Brahmacharinyai"),
    ("चन्द्रघण्टायै", "ચન્દ્રઘણ્ટાયૈ", "Chandraghantayai"),
    ("कूष्माण्डायै", "કૂષ્માણ્ડાયૈ", "Kushmandayai"),
    ("स्कन्दमातायै", "સ્કન્દમાતાયૈ", "Skandamatayai"),
    ("कात्यायन्यै", "કાત્યાયન્યૈ", "Katyayanyai"),
    ("कालरात्र्यै", "કાલરાત્ર્યૈ", "Kalaratryai"),
    ("महागौर्यै", "મહાગૌર્યૈ", "Mahagauryai"),
    ("सिद्धिदात्र्यै", "સિદ્ધિદાત્ર્યૈ", "Siddhidatryai"),
]

PAGES = [  # slug, content attribute, nav key
    ("garba-dandiya.html", "GARBA", "nav_garba"),
    ("navratri-vrat-food.html", "VRAT", "nav_vrat"),
    ("about.html", "ABOUT", "nav_about"),
    ("contact.html", "CONTACT", "nav_contact"),
    ("privacy-policy.html", "PRIVACY", "nav_privacy"),
    ("disclaimer.html", "DISCLAIMER", "nav_disclaimer"),
]
ALL_SLUGS = ["index.html"] + [f"day-{i}.html" for i in range(1, 10)] + [p[0] for p in PAGES]

DIYA = ('<svg viewBox="0 0 32 32" aria-hidden="true"><path d="M16 2.5c3.2 4.3 4.2 7.6 0 11.5-4.2-3.9-3.2-7.2 0-11.5z" '
        'fill="#F2A007"/><path d="M3.5 16.5h25c-1 6.6-6.1 11-12.5 11S4.5 23.1 3.5 16.5z" fill="{bowl}"/></svg>')
WA_ICON = ('<svg viewBox="0 0 24 24" aria-hidden="true" fill="currentColor"><path d="M12 2a10 10 0 0 0-8.6 15.1L2 22l5-1.3A10 10 0 1 0 12 2zm0 18.2'
           'a8.2 8.2 0 0 1-4.2-1.2l-.3-.2-3 .8.8-2.9-.2-.3A8.2 8.2 0 1 1 12 20.2zm4.5-6.1c-.2-.1-1.5-.7-1.7-.8s-.4-.1-.6.1-.6.8-.8 1-.3.2-.5.1'
           'a6.7 6.7 0 0 1-3.3-2.9c-.2-.4.2-.4.7-1.3a.4.4 0 0 0 0-.4l-.8-1.9c-.2-.5-.4-.4-.6-.4h-.5a1 1 0 0 0-.7.3 3 3 0 0 0-.9 2.2 5.2 5.2 0 0 0 1.1 2.8'
           ' 11.9 11.9 0 0 0 4.6 4c1.7.7 2.4.8 3.2.7a2.8 2.8 0 0 0 1.8-1.3 2.3 2.3 0 0 0 .2-1.3c-.1-.1-.3-.2-.5-.3z"/></svg>')

e = html.escape


def url_for(lang, slug):
    path = PREFIX[lang] + ("" if slug == "index.html" else slug)
    return f"{CONFIG['domain']}/{path}"


def link_for(from_lang, to_lang, slug):
    """Relative link from a page in from_lang to slug in to_lang."""
    up = "../" if PREFIX[from_lang] else ""
    target = PREFIX[to_lang] + ("" if slug == "index.html" else slug)
    return (up + target) or "./"


def fmt_date(lang, d, with_weekday=True):
    U = LANGS[lang].UI
    wd = U["weekdays"][d.weekday()]
    if lang == "en":
        return f"{wd}, {d.day} {U['months'][d.month]} {d.year}" if with_weekday else f"{d.day} {U['months'][d.month]}"
    base = f"{d.day} {U['months'][d.month]}"
    return f"{base} {d.year}, {wd}" if with_weekday else base


def devi_full(lang, i):
    C = LANGS[lang]
    return f"{C.UI['maa']} {C.DAY_META[i]['devi']}"


def head(lang, slug, title, desc, og_image, colors, extra=""):
    rel = "../" if PREFIX[lang] else ""
    alts = "\n".join(
        f'<link rel="alternate" hreflang="{l}" href="{url_for(l, slug)}">' for l in LANGS
    ) + f'\n<link rel="alternate" hreflang="x-default" href="{url_for("hi", slug)}">'
    ads = ""
    if CONFIG["adsense_client"]:
        ads = (f'<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client='
               f'{CONFIG["adsense_client"]}" crossorigin="anonymous"></script>')
    return f"""<!doctype html>
<html lang="{lang}">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(title)}</title>
<meta name="description" content="{e(desc)}">
<link rel="canonical" href="{url_for(lang, slug)}">
{alts}
<meta property="og:type" content="website">
<meta property="og:site_name" content="{e(LANGS[lang].UI['site_name'])}">
<meta property="og:title" content="{e(title)}">
<meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{url_for(lang, slug)}">
<meta property="og:image" content="{CONFIG['domain']}/static/og/{og_image}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<meta name="theme-color" content="#B3122E">
<link rel="icon" href="{rel}static/favicon.svg" type="image/svg+xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="{FONT_CSS[lang]}">
<link rel="stylesheet" href="{rel}static/style.css">
<style>:root{{--day:{colors[0]};--day-ink:{colors[1]};}}</style>
{ads}
<script src="{rel}static/config.js"></script>
<script src="{rel}static/app.js" defer></script>
{extra}
</head>
"""


CUR = ' aria-current="true"'


def header(lang, slug):
    U = LANGS[lang].UI
    switch = "".join(
        f'<a href="{link_for(lang, l, slug)}" lang="{l}" hreflang="{l}" title="{LANG_NAME[l]}"'
        f'{CUR if l == lang else ""}>{LANG_SHORT[l]}</a>'
        for l in LANGS
    )
    nav_items = [("index.html", "nav_home"), ("garba-dandiya.html", "nav_garba"), ("navratri-vrat-food.html", "nav_vrat")]
    nav = "".join(f'<li><a href="{link_for(lang, lang, s)}">{e(U[k])}</a></li>' for s, k in nav_items)
    return f"""<body>
<header class="site-header">
  <div class="wrap">
    <a class="brand" href="{link_for(lang, lang, 'index.html')}">{DIYA.format(bowl='#fff')}<span>{e(U['site_name'])}</span></a>
    <nav class="lang-switch" aria-label="{e(U['lang_label'])}">{switch}</nav>
  </div>
</header>
<div class="bandhani" aria-hidden="true" style="background-color:var(--sindoor)"></div>
<nav class="site-nav" aria-label="Menu"><ul class="wrap">{nav}</ul></nav>
<main>
"""


def footer(lang):
    U = LANGS[lang].UI
    items = [("index.html", "nav_home")] + [(p[0], p[2]) for p in PAGES]
    links = "".join(f'<li><a href="{link_for(lang, lang, s)}">{e(U[k])}</a></li>' for s, k in items)
    year = START.year
    return f"""</main>
<footer class="site-footer">
  <div class="bandhani" aria-hidden="true"></div>
  <div class="wrap">
    <ul>{links}</ul>
    <p class="note">{e(U['footer_note'])}</p>
    <p>© {year} {e(U['site_name'])}</p>
  </div>
</footer>
</body>
</html>
"""


def page_data(lang, day, card_title, card_line, day_label, colors):
    ui_keys = ["site_name", "today_is", "starts_in", "dussehra_today", "over", "open_today",
               "card_heading_received", "card_now_yours", "name_error", "card_top", "from_line",
               "share_msg", "share_msg_home", "copied_link", "copy", "copied"]
    ui = {k: LANGS[lang].UI[k] for k in ui_keys}
    ui.update(EXTRA_UI[lang])
    data = {
        "lang": lang, "day": day,
        "dates": [(START + dt.timedelta(days=i)).isoformat() for i in range(9)],
        "dussehra": DUSSEHRA.isoformat(),
        "cardTitle": card_title, "cardLine": card_line, "dayLabel": day_label,
        "color": colors[0], "ink": colors[1], "accent": colors[2],
        "font": CANVAS_FONT[lang], "ui": ui,
    }
    txt = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
    return f'<script id="page-data" type="application/json">{txt}</script>\n'


def card_maker(lang, day, colors):
    U = LANGS[lang].UI
    X = EXTRA_UI[lang]
    return f"""
<section class="card-maker" aria-labelledby="card-heading">
  <div class="card-preview">
    <canvas id="card" width="1080" height="1350" role="img" aria-label="{e(U['card_heading'])}"></canvas>
  </div>
  <div>
    <h2 id="card-heading">{e(U['card_heading'])}</h2>
    <p class="received-note" id="received-note"></p>
    <form id="card-form" novalidate>
      <div class="field">
        <label for="card-name">{e(U['name_label'])}</label>
        <input id="card-name" name="name" type="text" maxlength="30" autocomplete="name" placeholder="{e(U['name_placeholder'])}">
      </div>
      <p class="form-error" id="card-error" role="alert"></p>
      <button class="btn btn-primary" type="submit">{e(U['btn_make'])}</button>
    </form>
    <div class="share-actions actions" id="share-actions" hidden>
      <a class="btn btn-wa" id="btn-wa" href="#" target="_blank" rel="noopener">{WA_ICON}{e(U['btn_whatsapp'])}</a>
      <button class="btn btn-ghost" id="btn-share-photo" type="button" hidden>{e(X['btn_share_photo'])}</button>
      <button class="btn btn-ghost" id="btn-download" type="button">{e(U['btn_download'])}</button>
      <button class="btn btn-ghost" id="btn-copy-link" type="button">{e(U['btn_copy_link'])}</button>
    </div>
    <p class="status" id="card-status" role="status"></p>
  </div>
</section>
"""


def ad(slot):
    return f'<div class="ad-slot" data-slot="{slot}"></div>\n'


def build_home(lang):
    C = LANGS[lang]
    U = C.UI
    tiles = []
    for i in range(9):
        d = START + dt.timedelta(days=i)
        bg, ink, _ = COLORS[i]
        cls = ' class="is-white"' if i == 1 else ""
        tiles.append(
            f'<li><a href="day-{i+1}.html" data-day="{i+1}"{cls} style="--c:{bg};--ci:{ink}">'
            f'<span class="num">{i+1}</span>'
            f'<span><span class="devi">{e(devi_full(lang, i))}</span>'
            f'<span class="meta">{e(fmt_date(lang, d, False))}, {e(C.DAY_META[i]["color"])}</span></span></a></li>'
        )
    ld = json.dumps({"@context": "https://schema.org", "@type": "WebSite", "name": U["site_name"],
                     "url": url_for(lang, "index.html"), "inLanguage": lang}, ensure_ascii=False)
    out = head(lang, "index.html", U["home_title"], U["home_desc"], "home.png", HOME_COLOR,
               f'<script type="application/ld+json">{ld}</script>')
    out += header(lang, "index.html")
    out += f"""
<section class="home-hero wrap">
  <h1>{e(U['hero_title'])}</h1>
  <p class="sub">{e(U['hero_sub'])}</p>
  <p class="today-note" id="today-note" aria-live="polite"></p>
  <p class="pick-hint">{e(U['hero_pick'])}</p>
  <ol class="days-grid">{''.join(tiles)}</ol>
</section>
<div class="wrap">
{ad('top')}
{card_maker(lang, 0, HOME_COLOR)}
<article class="article prose">
{C.HOME_ARTICLE}
</article>
{ad('middle')}
<div class="more-links">
  <a class="btn btn-ghost" href="garba-dandiya.html">{e(U['nav_garba'])}</a>
  <a class="btn btn-ghost" href="navratri-vrat-food.html">{e(U['nav_vrat'])}</a>
</div>
</div>
"""
    out += page_data(lang, 0, U["home_card_title"], U["home_card_line"], "", HOME_COLOR)
    out += footer(lang)
    return out


def build_day(lang, i):
    C = LANGS[lang]
    U = C.UI
    M = C.DAY_META[i]
    T = C.DAYS[i]
    n = i + 1
    colors = COLORS[i]
    d = START + dt.timedelta(days=i)
    devi = devi_full(lang, i)
    day_label = U["day"].format(n=n)
    title = f"{day_label}: {devi}, {M['color']}, {U['bhog_label']} | {U['hero_title']}"
    desc = T["intro"]
    white = " is-white" if i == 1 else ""

    stem = MANTRA_STEMS[i]
    if lang == "gu":
        mantra = f'<p>ૐ દેવી {stem[1]} નમઃ</p>'
    elif lang == "en":
        mantra = f'<p lang="sa">ॐ देवी {stem[0]} नमः</p><p class="translit">Om Devi {stem[2]} Namah</p>'
    else:
        mantra = f'<p lang="sa">ॐ देवी {stem[0]} नमः</p>'

    wishes = "".join(
        f'<li><p id="w{k}">{e(w)}</p><button class="btn btn-ghost btn-small" type="button" data-copy="w{k}">{e(U["copy"])}</button></li>'
        for k, w in enumerate(T["wishes"])
    )
    prev_link = f'<a class="btn btn-ghost" href="day-{n-1}.html">{e(U["prev"])}: {e(devi_full(lang, i-1))}</a>' if n > 1 else \
        f'<a class="btn btn-ghost" href="./">{e(U["all_days"])}</a>'
    next_link = f'<a class="btn btn-primary" href="day-{n+1}.html">{e(U["next"])}: {e(devi_full(lang, i+1))}</a>' if n < 9 else \
        f'<a class="btn btn-primary" href="./">{e(U["all_days"])}</a>'

    ld = json.dumps({"@context": "https://schema.org", "@type": "Article", "headline": title,
                     "description": desc, "inLanguage": lang,
                     "image": f"{CONFIG['domain']}/static/og/day-{n}.png",
                     "datePublished": "2026-09-16", "dateModified": "2026-09-16",
                     "author": {"@type": "Organization", "name": U["site_name"]}}, ensure_ascii=False)

    out = head(lang, f"day-{n}.html", title, desc, f"day-{n}.png", colors,
               f'<script type="application/ld+json">{ld}</script>')
    out += header(lang, f"day-{n}.html")
    out += f"""
<section class="day-hero{white}">
  <div class="wrap">
    <p class="big-num" aria-hidden="true">{n}</p>
    <div>
      <p style="margin:0;font-weight:600">{e(day_label)}</p>
      <h1>{e(devi)}</h1>
      <p class="intro">{e(T['intro'])}</p>
      <dl class="facts">
        <div><dt>{e(U['date_label'])}</dt><dd>{e(fmt_date(lang, d))}</dd></div>
        <div><dt>{e(U['color_label'])}</dt><dd>{e(M['color'])}</dd></div>
        <div><dt>{e(U['bhog_label'])}</dt><dd>{e(M['bhog'])}</dd></div>
      </dl>
    </div>
  </div>
</section>
<div class="wrap">
{ad('top')}
{card_maker(lang, n, colors)}
<article class="article prose">
  <h2>{e(U['story_label'])}</h2>
  <p>{e(T['story'])}</p>
  <h2>{e(U['puja_label'])}</h2>
  <p>{e(T['puja'])}</p>
  <div class="mantra{white}"><h3 class="visually-hidden">{e(U['mantra_label'])}</h3>{mantra}</div>
  {ad('middle')}
  <h2>{e(U['wishes_label'])}</h2>
  <ul class="wishes">{wishes}</ul>
</article>
<nav class="day-nav" aria-label="{e(U['all_days'])}">{prev_link}{next_link}</nav>
<div class="more-links">
  <a class="btn btn-ghost" href="garba-dandiya.html">{e(U['nav_garba'])}</a>
  <a class="btn btn-ghost" href="navratri-vrat-food.html">{e(U['nav_vrat'])}</a>
</div>
</div>
"""
    out += page_data(lang, n, devi, T["card_line"], day_label, colors)
    out += footer(lang)
    return out


def build_page(lang, slug, attr):
    C = LANGS[lang]
    P = getattr(C, attr)
    body = P["body"].replace("{email}", e(CONFIG["email"])) \
        .replace("{domain}", e(CONFIG["domain"].replace("https://", ""))) \
        .replace("{updated}", CONFIG["updated"][lang])
    out = head(lang, slug, f"{P['title']} | {C.UI['site_name']}", P["desc"], "home.png", HOME_COLOR)
    out += header(lang, slug)
    out += f"""
<div class="wrap">
  <header class="page-head"><h1>{e(P['title'])}</h1></header>
  <article class="article prose">{body}</article>
  {ad('middle') if attr in ('GARBA', 'VRAT') else ''}
  <div class="more-links"><a class="btn btn-primary" href="./">{e(C.UI['all_days'])}</a></div>
</div>
"""
    # page-data needed by app.js (no card on these pages)
    out += page_data(lang, 0, "", "", "", HOME_COLOR)
    out += footer(lang)
    return out


def build_404():
    U = content_hi.UI
    G = content_gu.UI
    N = content_en.UI
    return f"""<!doctype html>
<html lang="hi"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>404 | {e(U['site_name'])}</title><meta name="robots" content="noindex">
<link rel="icon" href="/static/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="{FONT_CSS['hi']}"><link rel="stylesheet" href="/static/style.css"></head>
<body><main class="wrap nf">
<h1>{e(U['notfound_title'])}</h1><p>{e(U['notfound_text'])}</p>
<p lang="gu">{e(G['notfound_text'])}</p><p lang="en">{e(N['notfound_text'])}</p>
<p class="actions" style="justify-content:center">
<a class="btn btn-primary" href="/">{e(U['notfound_btn'])}</a>
<a class="btn btn-ghost" href="/gu/">ગુજરાતી</a><a class="btn btn-ghost" href="/en/">English</a></p>
</main></body></html>
"""


def build_og_images(dest):
    from PIL import Image, ImageDraw, ImageFont
    bold = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    reg = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
    os.makedirs(dest, exist_ok=True)

    def make(fname, bg, ink, accent, big, mid, small):
        img = Image.new("RGB", (1200, 630), bg)
        dr = ImageDraw.Draw(img)
        for x in range(30, 1200, 28):
            for y in (24, 606):
                r = 6 if (x // 28) % 2 == 0 else 4
                dr.ellipse([x - r, y - r, x + r, y + r], fill=accent if r == 6 else ink)
        dr.text((80, 120), small, font=ImageFont.truetype(reg, 40), fill=ink)
        dr.text((80, 200), big, font=ImageFont.truetype(bold, 110), fill=ink)
        dr.text((80, 360), mid, font=ImageFont.truetype(bold, 64), fill=ink)
        dr.text((80, 500), "indianfestivalwishes.com  |  Hindi, Gujarati, English", font=ImageFont.truetype(reg, 30), fill=ink)
        cx, cy, R = 1010, 315, 120
        dr.ellipse([cx - R, cy - R, cx + R, cy + R], outline=accent, width=10)
        dr.ellipse([cx - 60, cy - 60, cx + 60, cy + 60], fill=accent)
        img.save(os.path.join(dest, fname), optimize=True)

    for i in range(9):
        bg, ink, accent = COLORS[i]
        make(f"day-{i+1}.png", bg, ink, accent, f"Day {i+1}",
             f"Maa {content_en.DAY_META[i]['devi']}", "Navratri 2026")
    make("home.png", *HOME_COLOR, "Navratri 2026", "9 days, 9 goddesses", "Make a greeting card with your name")


def main():
    base = os.path.dirname(os.path.abspath(__file__))
    out = os.path.join(base, OUT)
    if os.path.exists(out):
        shutil.rmtree(out)
    os.makedirs(out)
    shutil.copytree(os.path.join(base, "static"), os.path.join(out, "static"))

    for lang in LANGS:
        d = os.path.join(out, PREFIX[lang])
        os.makedirs(d, exist_ok=True)

        def write(name, txt):
            with open(os.path.join(d, name), "w", encoding="utf-8") as f:
                f.write(txt)

        write("index.html", build_home(lang))
        for i in range(9):
            write(f"day-{i+1}.html", build_day(lang, i))
        for slug, attr, _ in PAGES:
            write(slug, build_page(lang, slug, attr))

    with open(os.path.join(out, "404.html"), "w", encoding="utf-8") as f:
        f.write(build_404())

    # config.js (the one file to edit after AdSense approval)
    with open(os.path.join(out, "static", "config.js"), "w", encoding="utf-8") as f:
        f.write(
            "// AdSense approve hone ke baad yahan apni IDs daalein.\n"
            "window.SITE = {\n"
            f'  adsenseClient: "{CONFIG["adsense_client"]}",   // jaise "ca-pub-1234567890123456"\n'
            '  adSlots: { top: "", middle: "" },   // AdSense me banaye ad units ke slot IDs (optional)\n'
            '  gaId: ""                            // Google Analytics ID, jaise "G-XXXXXXXXXX" (optional)\n'
            "};\n"
        )
    with open(os.path.join(out, "static", "favicon.svg"), "w", encoding="utf-8") as f:
        f.write(DIYA.format(bowl="#B3122E").replace('aria-hidden="true"', 'xmlns="http://www.w3.org/2000/svg"'))

    build_og_images(os.path.join(out, "static", "og"))

    # sitemap
    rows = []
    for l in LANGS:
        for s in ALL_SLUGS:
            alts = "".join(f'<xhtml:link rel="alternate" hreflang="{a}" href="{url_for(a, s)}"/>' for a in LANGS)
            rows.append(f"<url><loc>{url_for(l, s)}</loc>{alts}<lastmod>2026-09-16</lastmod></url>")
    with open(os.path.join(out, "sitemap.xml"), "w", encoding="utf-8") as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" '
                'xmlns:xhtml="http://www.w3.org/1999/xhtml">\n' + "\n".join(rows) + "\n</urlset>\n")
    with open(os.path.join(out, "robots.txt"), "w") as f:
        f.write(f"User-agent: *\nAllow: /\n\nSitemap: {CONFIG['domain']}/sitemap.xml\n")
    with open(os.path.join(out, "ads.txt"), "w") as f:
        f.write("# AdSense approval ke baad neeche wali line ke aage se # hataayein aur pub ID badlein:\n"
                "# google.com, pub-0000000000000000, DIRECT, f08c47fec0942fa0\n")
    open(os.path.join(out, ".nojekyll"), "w").close()
    print("Built", sum(len(fs) for _, _, fs in os.walk(out)), "files into", out)


if __name__ == "__main__":
    main()
