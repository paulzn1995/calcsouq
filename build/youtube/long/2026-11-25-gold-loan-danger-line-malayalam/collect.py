# usage: python3 collect.py <status-json-file>...  -> updates audio.json (durations) and gens.json (session -> gen id, url)
import json, sys, re, os
S = json.load(open("sessions.json")); SC = list(json.load(open("scenes.json")))
imgs = [s + k for s in SC for k in "AB" if k in json.load(open("scenes.json"))[s]]
imgs_s = [k for k in imgs if k != "S23A"]
smap = {sid: ("tts", SC[i]) for i, sid in enumerate(S["tts"])}
smap.update({sid: ("img", imgs_s[i]) for i, sid in enumerate(S["img"])})
smap.update(S.get("extra", {}) and {sid: tuple(v) for sid, v in S["extra"].items()})
audio = json.load(open("audio.json")) if os.path.exists("audio.json") else {}
gens = json.load(open("gens.json")) if os.path.exists("gens.json") else {}
for f in sys.argv[1:]:
    raw = json.load(open(f)); d = json.loads("".join(x["text"] for x in raw)) if isinstance(raw, list) else raw
    for g in d["generations"]:
        u = g.get("content_url") or ""
        m = re.search(r"content_generation/(\w+)/", u)
        if not m or g["status"] != "completed": continue
        kind, key = smap[m.group(1)]
        gens[key] = {"id": g["id"], "url": u}
        if kind == "tts": audio[key] = g["duration_secs"]
json.dump(audio, open("audio.json", "w"), indent=1); json.dump(gens, open("gens.json", "w"), indent=1)
print("audio", len(audio), "/25  gens", len(gens), "missing tts", [s for s in SC if s not in audio])
print("missing img", [k for k in imgs if k not in gens])
