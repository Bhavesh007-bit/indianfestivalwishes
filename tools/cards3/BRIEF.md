# Card art brief: v3, full redesign

## Why this exists
indianfestivalwishes.com is an Indian greeting-card and invitation site in Hindi, Gujarati and English. Users pick a background design and the site's canvas engine (`static/cards.js`) writes their text on top of it: title, wish, names, date, venue and so on.

The owner rejected the previous designs, and he was right to. They had three problems:
1. **Too plain.** Most cards were a flat gradient with one tiny icon.
2. **Same layouts everywhere.** The big circle, the scallop split, the side stripe and the polaroid appeared in every event, only recoloured.
3. **Motifs leaked across events.** Wedding, engagement and anniversary all used the same rings and roses.

He wants each event to have its own designs that look like premium Canva / Adobe Express templates. No layout or motif should repeat from one event to another.

## Canvas and output
- Each card is 1080 × 1350 px. You author it as inline SVG, or as HTML/CSS with SVG. Chromium renders it through `tools/cards3/render.py`:
  ```python
  import sys; sys.path.insert(0, "tools/cards3")
  from render import render_cards
  render_cards({"E-<cat>-1": svg_or_html, ...})
  ```
- The render writes `tools/cards3/out/E-<cat>-N.webp` and a thumbnail. The source is saved to `src/`.
- Write the generator to `tools/cards3/gen_<cat>.py`. Shared helpers go in `tools/cards3/lib_<yourname>.py`. Don't edit other agents' files.
- No network, no external images, no web fonts.
- **The art contains no text or letters in any language.** The engine writes all text.
  - Religious symbols drawn as graphics are fine where they belong (swastik, om, shubh-labh-style kalash, shankh).

## Quality bar (every single card)
1. **Hero illustration.** A large illustration or scene that belongs only to this event, taking roughly 25–45% of the card. It must be detailed: many shapes, gradients, highlights and shadows. Not a 60 px icon.
   - Examples: a 10-headed Ravan effigy with a flaming arrow hitting it; a woman's silhouette holding a channi up to the full moon; a decorated mandap with draped fabric and marigold strings; a two-storey house with toran and kalash at the door.
2. **Finished edge treatment.** For example: an ornamental border, corner ornaments, a patterned band, a hanging garland, a jharokha frame, or a lace/paper-cut edge.
3. **Background with depth.** Use a pattern, texture, bokeh, soft light rays or layered gradients. Avoid big flat empty areas, except the calm text area.
4. **Calm text area.** The text zone must sit on something calm and contrasting: a parchment panel, silk plaque, glass card, cloth banner, or a clean low-detail region.
   - Keep the zone at least 40 px inside that calm area. No illustration detail may sit under the text.
   - Text colours must be strongly readable, with contrast of 4.5:1 or better.
   - The title may be `"gold"` only when `tone` is `"dark"`.
5. **Distinct compositions.** Your 10 cards are 10 different compositions, not recolours.
   - Vary the hero position (top, bottom, side, corner, full scene), the panel shape and the palette.
   - Banned generic layouts: plain gradient plus small corner icon; big empty circle in the middle; top colour band with scalloped cream bottom; thin vertical side stripe with icons; polaroid; thin double-line frame on a flat colour.
6. **Watermark space.** Keep the bottom-centre strip (x 330–750, y 1275–1350) low-detail. The engine draws a dark watermark pill there.

## Spec: `tools/cards3/out/<cat>.json`
This is a JSON list of 10 objects, in the order they should appear. Example:

```json
{"id":"E-diwali-1","tpl":true,"zone":[x0,y0,x1,y1],
 "colors":{"title":"#8C1C00" | "gold","text":"#3A2330","accent":"#B7791F"},
 "tone":"light" | "dark",
 "title":"deco" | "script" | "classic",
 "align":"center" | "left",
 "photo":{"shape":"arch|rounded|pill|rect|oval|heart","x":..,"y":..,"w":..,"h":..} or {"shape":"circle","x":cx,"y":cy,"r":r},
 "slot":true}
```

**Field notes:**
- `zone` is the box the engine stacks text into, vertically centred. The text auto-shrinks to fit.
  - Wishes (festival, birthday, couple, morning): the zone should be at least 760 × 460.
  - Invitations and shraddhanjali: the zone should be at least 780 × 700. These carry title, names, wording, date/time, venue and host.
- `tone`: use `"dark"` if the text sits on a dark area. In that case `text` should be light.
- `accent` colours the small divider line and the date line.
- `title` picks the font style:
  - `deco`: Yatra One / Shrikhand / Cinzel, festive.
  - `script`: Kalam / Mogra / Great Vibes, romantic or soft.
  - `classic`: Rozha One / Rasa, formal or sober.
- `photo` and `slot` are optional:
  - With `slot:true`, your art draws the frame (garland, border, shadow) around the given shape, and the user's photo is clipped into that shape.
  - When no photo is added, the slot area shows your art, so paint a soft placeholder there: light fill, subtle pattern or faint silhouette.
  - The zone must not overlap the slot.
  - Without `slot`, the engine draws its own frame and pushes the zone down. Prefer `slot:true`.

## Proofing (mandatory)
Run the proof, then **look at the image with the Read tool**:

```
python3 tools/cards3/proof.py <cat> hi
python3 tools/cards3/proof.py <cat> gu
python3 tools/cards3/proof.py <cat> en
python3 tools/cards3/proof.py <cat> hi --photo    # when any spec has a photo
```

The proof shows the real engine text on your art (`tools/cards3/proof/<cat>-<lang>.jpg`). Fix and repeat until **every card** passes all of these:
- All text is clearly readable.
- Nothing overlaps the hero or the watermark.
- The text is not tiny because of a cramped zone.
- The card looks like a premium template.

Also view a few full-size renders from `out/` to check illustration quality up close. Be self-critical. If a hero illustration looks crude, redraw it with more care: layered shapes, gradients, highlights.

**Rules for the shared environment:**
- The local server runs on :8765. **Never run `node build.js`**, and never kill that server or any other process.
- If `curl localhost:8765/healthz` fails, tell the orchestrator in your final report; don't restart it.
- Don't touch `static/`, `content/`, `build.js`, `server.js` or `admin/`.

## Motif ownership (use only your event's motifs; never another event's)
| Category | Motifs |
|---|---|
| navratri | Garba/dandiya dancers, dandiya sticks, garbo (pierced pot with a flame), trishul, bandhani / leheriya patterns, mirror-work (abhla) and cowrie embroidery borders, chaniya-choli colour blocks, Maa Amba's chunri. |
| dussehra | 10-headed Ravan effigy, bow and flaming arrow, Ram's silhouette with a drawn bow, effigy burning with sparks, apta/shami leaves, chariot, victory flag (dhwaj), evening sky with fire glow. |
| karva-chauth | Full moon, channi (sieve), karwa pot, puja thali with diya and sindoor, mehendi hands and patterns, red-and-gold chunri, bangles, woman silhouette looking at the moon, starry night. |
| diwali | Diyas (clusters, rows), rangoli (large, detailed), akash kandil lanterns, fireworks/phuljhadi, Lakshmi footprints, string lights, sweets box/mithai. |
| shraddhanjali | Sober only: white/cream/grey/muted sage/muted gold. Jasmine or rajnigandha garland around the photo, white lilies, white lotus, a single calm diya, incense smoke curls, soft light rays, a quiet dove. **No** bright festive colours, marigold, bells, mandala, fireworks, balloons, hearts or rings. Every card has a photo slot. |
| good-morning | Sunrise over hills or sea, tea/coffee cup with steam, birds, dewy leaves, sunflowers, morning flowers, sun rays, window with sunlight. |
| inv-wedding | Decorated mandap, elephant pair with raised trunks, jharokha/palace arches, kalash with coconut, shehnai, doli, marigold strings, paisley and mehendi ornament, stylised Ganesh symbol (abstract/geometric, respectful). |
| wedding (wishes) | Varmala exchange (couple silhouettes), gathbandhan knot, pheras around the sacred fire (agni), rose-petal shower, bride's hands with mehendi, doli with flowers. No mandap and no elephants (those belong to the invite). |
| anniversary | Two swans forming a heart, candle-lit table, clock/infinity, lock and key, twin coffee cups, bouquet with ribbon, photo-collage slots, anniversary cake with two figures on top. |
| inv-engagement | Ring box / rings on a decorated thal, floral jharokha photo frame, couple-photo slots (arch / rounded / heart / pill / rect, never a circle), roka/sagai thal with sweets and chunri, save-the-date style modern layouts. |
| engagement (wishes) | Interlocked rings as hero with sparkle, lovebirds, heart-shaped floral wreath, bouquet, couple silhouette under string lights. Photo slots never circle. Must look different from inv-engagement. |
| birthday (wishes) | Big cake with candles as hero, balloon bouquets, cupcakes, gift boxes, sparklers, confetti. |
| inv-birthday-party | Party bunting, party poppers, marquee/ticket style, disco ball, kids' themes (space rocket, jungle animals, under the sea, circus tent), photo slot of the birthday child. Do **not** reuse the cake-hero or balloon-bouquet layouts from birthday wishes. |
| inv-naming-ceremony | Decorated palna/cradle, baby footprints, sleeping baby in the cradle, lullaby moon and stars, peacock feather, toys (rattle, wooden toys), soft pastels. Photo slot of the baby. |
| inv-baby-shower | Godh bharai: expecting-mother silhouette, bangles stack, fruit basket and coconut for the lap ritual, flower jewellery, baby clothes on a line, soft clouds, pastel florals. No cradle (naming owns it). |
| inv-griha-pravesh | House with open door, toran of mango leaves and marigold, kalash with coconut at the door, key with ribbon, milk pot boiling over, rangoli at the entrance, Lakshmi footprints entering, nameplate door. |
| inv-puja | Satyanarayan/puja: kalash, puja thali, temple bell, shankh, banana leaves/plants, havan kund with flames, lotus, incense, temple silhouette, om symbol. |
| inv-shop-opening | Storefront with awning, ribbon-cutting with scissors, gold coins and money pot, open-sign-style shape (no text), grand-opening starburst, confetti in gold, shubh-labh style kalash, keys. |

## Palettes
Each event gets its own palette family. Vary the palette across its 10 cards. Keep colours rich and harmonious, not garish: use gradients, a gold foil feel (linear gradients with highlights) and soft shadows (SVG filters).

## Final report (keep it short)
For each category, give:
- one line per card: concept and whether it has a photo slot;
- the proof image paths;
- anything that is still weak.
