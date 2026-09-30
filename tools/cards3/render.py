"""Shared renderer: turn 1080x1350 HTML/SVG card art into webp images.

Usage from an event script:
    from render import render_cards
    render_cards({"E-diwali-1": "<svg ...>...</svg>" or full html, ...})
Writes out/<id>.webp (1080x1350) and out/thumb/<id>.webp (432x540),
and saves the source to src/<id>.html so it can be inspected.
"""
import asyncio, io, os
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")
W, H = 1080, 1350

def _page(markup):
    if markup.lstrip().lower().startswith("<!doctype") or markup.lstrip().lower().startswith("<html"):
        return markup
    return ("<!doctype html><html><head><meta charset='utf-8'><style>html,body{margin:0;padding:0;"
            "width:%dpx;height:%dpx;overflow:hidden;background:#fff}svg{display:block}</style></head>"
            "<body>%s</body></html>") % (W, H, markup)

async def _run(cards):
    from playwright.async_api import async_playwright
    os.makedirs(os.path.join(OUT, "thumb"), exist_ok=True)
    os.makedirs(os.path.join(HERE, "src"), exist_ok=True)
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": W, "height": H})
        for cid, markup in cards.items():
            html = _page(markup)
            open(os.path.join(HERE, "src", cid + ".html"), "w").write(html)
            await pg.set_content(html, wait_until="load")
            await pg.wait_for_timeout(150)
            png = await pg.screenshot(clip={"x": 0, "y": 0, "width": W, "height": H})
            im = Image.open(io.BytesIO(png)).convert("RGB")
            im.save(os.path.join(OUT, cid + ".webp"), "WEBP", quality=86, method=5)
            im.resize((432, 540), Image.LANCZOS).save(os.path.join(OUT, "thumb", cid + ".webp"), "WEBP", quality=82)
            print("rendered", cid)
        await b.close()

def render_cards(cards):
    asyncio.run(_run(cards))
