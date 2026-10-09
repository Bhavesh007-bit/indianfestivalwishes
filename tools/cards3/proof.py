"""Proof the NEW card designs with the REAL card engine (static/cards.js).

    python3 tools/cards3/proof.py <category> [hi|gu|en] [--photo]

Reads out/<category>.json (list of 10 specs) + out/E-<category>-N.webp,
opens the real page on the local server (http://localhost:8765), swaps the
page's design list for the new specs, renders every design with sample text
and saves a contact sheet to proof/<category>-<lang>[-photo].jpg.
Look at that sheet: every word must be clearly readable and nothing may
overlap the art's key illustration or the bottom watermark pill.
Needs the local server on :8765 (do NOT run node build.js).
"""
import asyncio, base64, io, json, os, re, sys, time
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
BASE = "http://localhost:8765"

PAGES = {
    "navratri": "navratri/", "navratri-d1": "navratri/day-1.html", "dussehra": "dussehra/", "karva-chauth": "karva-chauth/", "diwali": "diwali/",
    "birthday": "wishes/birthday.html", "anniversary": "wishes/anniversary.html", "wedding": "wishes/wedding.html",
    "engagement": "wishes/engagement.html", "good-morning": "wishes/good-morning.html",
    "shraddhanjali": "shraddhanjali/",
}
for k in ["wedding", "engagement", "birthday-party", "griha-pravesh", "baby-shower", "naming-ceremony", "puja", "shop-opening"]:
    PAGES["inv-" + k] = "invitations/%s.html" % k

NAMES = {
    "hi": dict(name="भावेश सोनगरा", n1="राहुल", n2="प्रिया", to="प्रिया",
               f_name1="चि. आकाश", f_name2="चि. पूजा", f_date="शनिवार, 12 दिसंबर 2026", f_time="शाम 7 बजे",
               f_venue="श्रीजी पार्टी प्लॉट, वराछा रोड, सूरत", f_host="पटेल परिवार", f_dates="जन्म: 12-03-1950 | निधन: 20-10-2026"),
    "gu": dict(name="ભાવેશ સોનગરા", n1="રાહુલ", n2="પ્રિયા", to="પ્રિયા",
               f_name1="ચિ. આકાશ", f_name2="ચિ. પૂજા", f_date="શનિવાર, 12 ડિસેમ્બર 2026", f_time="સાંજે 7 વાગ્યે",
               f_venue="શ્રીજી પાર્ટી પ્લોટ, વરાછા રોડ, સુરત", f_host="પટેલ પરિવાર", f_dates="જન્મ: 12-03-1950 | અવસાન: 20-10-2026"),
    "en": dict(name="Bhavesh Sonagara", n1="Rahul", n2="Priya", to="Priya",
               f_name1="Aakash", f_name2="Pooja", f_date="Saturday, 12 December 2026", f_time="7:00 PM",
               f_venue="Shreeji Party Plot, Varachha Road, Surat", f_host="The Patel Family", f_dates="Born: 12-03-1950 | Passed: 20-10-2026"),
}
TRIBUTE_NAME = {"hi": "स्व. श्री रमेशभाई पटेल", "gu": "સ્વ. શ્રી રમેશભાઈ પટેલ", "en": "Late Shri Rameshbhai Patel"}


def query(cat, lang):
    n = dict(NAMES[lang])
    if cat == "shraddhanjali":
        n["f_name1"] = TRIBUTE_NAME[lang]; n.pop("f_name2")
    if cat.startswith("inv-") and cat not in ("inv-wedding", "inv-engagement"):
        n.pop("f_name2")
        if cat in ("inv-birthday-party", "inv-baby-shower", "inv-naming-ceremony"):
            pass
    n["fs"] = "family"
    from urllib.parse import urlencode
    return urlencode(n)


async def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    cat = args[0]
    lang = args[1] if len(args) > 1 else "hi"
    photo = "--photo" in sys.argv
    specs = json.load(open(os.path.join(HERE, "out", cat + ".json")))
    stamp = str(int(time.time()))
    for s in specs:
        s["url"] = "/__proof/%s.webp?t=%s" % (s["id"], stamp)
    prefix = "" if lang == "hi" else lang + "/"
    page_url = "%s/%s%s" % (BASE, prefix, PAGES[cat])
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1280, "height": 900})
        errs = []
        pg.on("pageerror", lambda e: errs.append(str(e)))

        async def page_route(route):
            resp = await route.fetch()
            html = await resp.text()
            m = re.search(r'(<script id="page-data" type="application/json">)(.*?)(</script>)', html, re.S)
            data = json.loads(m.group(2))
            data["card"]["designs"] = specs
            new = json.dumps(data, ensure_ascii=False).replace("</", "<\\/")
            html = html[:m.start(2)] + new + html[m.end(2):]
            await route.fulfill(status=200, body=html, headers={"content-type": "text/html; charset=utf-8"})

        async def img_route(route):
            name = route.request.url.split("/__proof/")[1].split("?")[0]
            p = os.path.join(HERE, "out", name)
            await route.fulfill(status=200, body=open(p, "rb").read(), headers={"content-type": "image/webp"})

        await pg.route("**/__proof/**", img_route)
        await pg.route(lambda u: u.split("?")[0] == page_url, page_route)
        await pg.route("**/static/site-settings.json*", lambda r: r.fulfill(status=200, body="{}", headers={"content-type": "application/json"}))
        tiles = []
        q = query(cat, lang)
        for i in range(len(specs)):
            await pg.goto("%s?%s&s=%d" % (page_url, q, i), wait_until="networkidle")
            if photo:
                btn = await pg.query_selector('[data-photo-mode="with"]')
                if btn and await btn.is_visible():
                    await btn.click()
                inp = await pg.query_selector("#card-photo")
                if inp:
                    await inp.set_input_files(os.path.join(HERE, "testphoto.jpg"))
            await pg.wait_for_timeout(600)
            d = await pg.evaluate('document.getElementById("card").toDataURL("image/jpeg",0.88)')
            tiles.append(Image.open(io.BytesIO(base64.b64decode(d.split(",")[1]))).convert("RGB").resize((432, 540), Image.LANCZOS))
        await b.close()
    cols = 5
    rows = (len(tiles) + cols - 1) // cols
    G = Image.new("RGB", (432 * cols, 540 * rows), "white")
    for i, t in enumerate(tiles):
        G.paste(t, ((i % cols) * 432, (i // cols) * 540))
    os.makedirs(os.path.join(HERE, "proof"), exist_ok=True)
    out = os.path.join(HERE, "proof", "%s-%s%s.jpg" % (cat, lang, "-photo" if photo else ""))
    G.save(out, quality=84)
    print("saved", out, "errors:", errs[:3])

if __name__ == "__main__":
    asyncio.run(main())
