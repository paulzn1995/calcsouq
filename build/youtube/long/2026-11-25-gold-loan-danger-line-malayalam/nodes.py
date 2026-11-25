import json
IMG="""PELOD7sGnblMSwFWFdmJ nmC9pWzYvI15wUq5FTQs sVZsJDfXa9ubvwFzX2Kj zdhw31lzMXebtCpM3ZGh cpAOJcSJJaMSWd63rC9r ZixJezyrMPHj43GoW9NV hIsofwfw0vRfUJ0OjBuQ PqYKuuVKDAMlaWH7tQEo 8GtonYfE4WasB3ot91op 0jb1kuQTISrnIdPoCoDC de6ORMOwE7GwWqGdr6so QsZ2xvTWAJedBmAnzJCL OCIFnWSoTfSjpFQcbxue QQJ1IUJEV2lCGGK0KFIX UKKhdonTBX9CwJl4BlnB AF0EqXvl7QNPzC24KEIh GL3MsaOChobNm23JwHlR pASC1Z9jKNOaruDUQCe9 VgB1kdVUNg2HOrBq8ph8 WLKsAy9bDgQFCXAFeCCY aa53F6pWvmuWSKIVYAY9 UiBKayRV6hHGWzZZwTrQ YaCtHjCC4rp6IEKmPoMa ATITc0zg7lS7a7H4ln7y 9T9W4HzlEwIPuMYvuWAx Lft95VZgFocIRjbpzifv dD3ZirqlV3zykSST18tc I3KlM5zeVJ9lcc9SslTP ZWR9BC3dlV52JDqoHYWW iNmnDbcw43JNiYSHb25t KouZnVcNve0xDT0yKgr3 pWFb7JJPCfg3fCqtTkJJ HdoKA2JfOiBODG3r2Pxa CEAo91J9O9zMi5a2A3V7 P5PzdAAOsPbnHd8ICkJM P2oKSPVIjy5otrn6Yvsv nNy4E70Xu3JBOqQ2DCGs 1Mb9RpdkutVMWZSy4rE7 FVLQezKfuUJsi7DVHDKI fSkMEM01BfZkFa2Xa9RZ zosEPpok5SPT1YqIS7Aa nWizcg7Svul2RPl3QWXh B4aES8cJOkQ1eUvP9DW2 UcMDrFlksZlg0o60rm1Y TuuXAWn3Lu08VEjOc7Y4 n3NVGhOK3KHAip5mz9Nn""".split()
TTS="""aRzHuaMaBrkVSFl584FX Q79XMfHUvrdI97cbsx2P eeZtybD9DraclAIYHSrm DX34BxSDWrOMWNcU9Wrq kIGDt4gOQKFRDw2I2ksr m5HXmrkZDHQh9FldEhAd ZRQCcxHTAixHnY1hyT54 rTpaCFlRa8w2auHEH3Vw 26BSQnjVw8je0NTvfNpY vinwPzhm9bT6ZvUYRpuC fLpH8fobu0g4YEK8nSkp C0E8U6638LVkNfQEPM1G g6SPj81wZFGdW5bHZjMH RkmjTSFeRvgbNkdr1LaC BuZJryPHXa8aAxbhcfyU A4Q0FPumqq6EnbIQqRb1 Sckx4sjh95KfgPcv3qAT twqrhBKaI3UO7jXimkQn HHn1EAfS4JpRlxV8CBxA vYFN5b1jJT7yykR65Qx5 p2qgBhxpygpqDBdt4QwK 2o6dzc4QyYJJMJK9N38O zDVg3kGePoE2OuaYBDg2 NQGMdFfUDwZQgNpbdkQo Etnk25eL7KuutZOJbBU8""".split()
SC=json.load(open("scenes.json"))
imgs=[(s+k,SC[s][k]) for s in SC for k in "AB" if k in SC[s]]
assert len(imgs)==len(IMG)==46 and len(TTS)==len(SC)==25
def tts_text(s):
    t=" ".join(m for m,*_ in SC[s]["s"])
    return t.replace("NBFCകളും","എൻ ബി എഫ് സി കളും").replace("CalcSouq","കാൽക്സൂക്ക്")
nodes={"img":{k:i for (k,_),i in zip(imgs,IMG)},"tts":{s:i for s,i in zip(SC,TTS)}}
json.dump(nodes,open("nodes.json","w"),indent=1)
json.dump([{"node_id":i,"label":"I "+k,"prompt":p} for (k,p),i in zip(imgs,IMG)],open("/tmp/upd_img.json","w"),ensure_ascii=False)
json.dump([{"node_id":i,"label":"N "+s,"prompt":tts_text(s)} for s,i in zip(SC,TTS)],open("/tmp/upd_tts.json","w"),ensure_ascii=False)
print(sum(len(tts_text(s)) for s in SC))
