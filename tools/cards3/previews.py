"""Render invite/tribute preview tiles (static/cards/preview/<k>-<L>.webp) from the live local server."""
import asyncio, base64, io, os, sys
from urllib.parse import urlencode
from PIL import Image
sys.path.insert(0, os.path.dirname(__file__))
from proof import NAMES, TRIBUTE_NAME
KS = ["wedding", "engagement", "birthday-party", "griha-pravesh", "baby-shower", "naming-ceremony", "puja", "shop-opening", "shraddhanjali"]
OUT = os.path.join(os.path.dirname(__file__), "..", "..", "static", "cards", "preview")
async def main():
    from playwright.async_api import async_playwright
    async with async_playwright() as pw:
        b = await pw.chromium.launch(); pg = await b.new_page(viewport={"width": 1280, "height": 900})
        for L in ["hi", "gu", "en"]:
            for k in KS:
                n = {x: v for x, v in NAMES[L].items() if x.startswith("f_") and x != "f_dates"}
                if k == "shraddhanjali":
                    n["f_name1"] = TRIBUTE_NAME[L]; n.pop("f_name2"); n["f_dates"] = NAMES[L]["f_dates"]
                    path = "shraddhanjali/"
                else:
                    if k not in ("wedding", "engagement"): n.pop("f_name2")
                    path = "invitations/%s.html" % k
                url = "http://localhost:8765/%s%s?%s&s=0" % ("" if L == "hi" else L + "/", path, urlencode(n))
                await pg.goto(url, wait_until="networkidle"); await pg.wait_for_timeout(500)
                d = await pg.evaluate('document.getElementById("card").toDataURL("image/png")')
                im = Image.open(io.BytesIO(base64.b64decode(d.split(",")[1]))).convert("RGB").resize((432, 540), Image.LANCZOS)
                im.save(os.path.join(OUT, "%s-%s.webp" % (k, L)), "WEBP", quality=84); print(k, L)
        await b.close()
asyncio.run(main())
