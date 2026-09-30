"""Copy rendered art from tools/cards3/out into static/cards and rebuild content/templates.json."""
import json, glob, os, shutil
R = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
old = json.load(open(os.path.join(R, "content/templates.json")))
new = {}
for k in old:
    s = json.load(open(os.path.join(R, "tools/cards3/out", k + ".json")))
    for d in s:
        d.pop("url", None); d["tpl"] = True
    new[k] = s
json.dump(new, open(os.path.join(R, "content/templates.json"), "w"), ensure_ascii=False, indent=1)
for f in glob.glob(os.path.join(R, "tools/cards3/out/E-*.webp")): shutil.copy(f, os.path.join(R, "static/cards/"))
for f in glob.glob(os.path.join(R, "tools/cards3/out/thumb/E-*.webp")): shutil.copy(f, os.path.join(R, "static/cards/thumb/"))
print("installed", sum(len(v) for v in new.values()))
