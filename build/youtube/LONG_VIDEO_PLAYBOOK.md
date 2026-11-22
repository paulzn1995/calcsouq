# Long YouTube video (Mon, Wed, Fri): playbook (agent follows this exactly)

Paulson approved video #1 (`long/2026-11-22-rates-rising/`) as the standard. **Paulson uploads every video himself.** The agent never uploads or posts anything to YouTube or any other platform.

## 0. Budget check (do this first)
- Call ElevenLabs `account_get_usage`. One video uses about 3,000 narration characters and reuses the stock music for free.
- If fewer than 3,500 characters are left, stop. Tell Paulson the video is paused until credits reset (give the reset date) or he upgrades the plan. Still do step 1 and save the topic so it is ready.

## 1. Pick today's hot topic (trend watch)
- Search the web for what people are searching for and talking about worldwide today. Use Google Trends "trending now" (US, India, UK, worldwide), top news, and big market moves.
- Write the top 5 candidates to `youtube/trends.md`, newest first. For each, give the topic, why it is hot, and 3 phrases people actually type into search. Other agents (Shorts, reels, SEO) read this file.
- Pick ONE topic using all of these rules:
  1. Search interest is high right now and will last a few days, so an explainer can rank.
  2. You can explain it clearly with real numbers or a worked example.
  3. Prefer money, economy, prices, jobs, tech, science or world events that affect daily life. It is fine if it isn't about calculators, but link a CalcSouq tool when one fits.
  4. It hasn't been covered in the last 14 days (check `youtube/long/log.md`).
- Do NOT pick:
  - gambling, adult topics, or tragedies or violence as entertainment;
  - partisan politics (election news is OK only as a neutral explainer of how something works);
  - celebrity gossip or medical advice.
- Prefer a topic where search demand is rising and few good explainer videos exist yet. Being early matters more than being long.

## 2. Facts
- Every number, date and claim comes from at least 2 current sources found today. Save the source URLs in the video folder (`sources.md`).
- If something can't be verified, leave it out.
- Worked examples must be computed in Python, not by hand.
- No financial, legal or medical advice. Explain how things work and show example numbers.

## 3. Script (target 3:00–3:20 total, the length of the stock music)
- 7–8 scenes, 470–520 words total, plain English, British spelling.
- Scene 1 hooks with the news in the first sentence. The last scene is a recap plus "check your own numbers free at calc souq dot com" (only if a tool fits) plus "subscribe".
- Spell numbers out in the narration so the voice reads them correctly (e.g. "five point five percent").
- Save `script.md` and `scenes.json` ({"S1": text, ...}) in `youtube/long/<YYYY-MM-DD>-<slug>/`.

## 4. Voice (ElevenLabs)
- `creative_create_flow`, named "CalcSouq YouTube — <title>".
- Add one `tts` node per scene: model `eleven_v4`, voice Bella `hpp4J3VqNfWAUOO0d1Us`.
- Run all of them with `generations_count: 1`. Never re-run a node to retry, because that charges twice.
- Read each clip's `duration_secs` from `creative_get_flow_run_status`. Wait the poll time between calls, and only check status after a real wait.

## 5. Animation (16:9, 1920×1080, 30 fps)
- Copy `build/yt_long_rates.py` to `build/yt_long_<slug>.py`.
- Change `TEXT` (path to the new scenes.json), `AUDIO` (real durations) and the `S1…S8` scene functions. Keep the helpers, subtitles, brand tag and `PAD = 0.7`.
- **Characters and real examples:**
  - Souq the mascot appears in at least 3 scenes.
  - Each scene has moving illustrated objects (props from reel_fx and the helpers here; draw new simple ones when needed).
  - Numbers count up, and visuals appear when the narration reaches them (`at(scene, phrase)`).
- **Reading pace:** at most 2 new text items at once, every item stays on screen at least 3 s, and headings are 76 px.
- **No copyrighted material:** no characters, logos, flags of brands or photos of real people.
- **Before the full render:** render a frame at the busiest moment of each scene with `--frame`, put the frames on a contact sheet, look at it, and fix overlaps or clipped text.
- **Render:** run two background processes (`python3 yt_long_<slug>.py S1 S3 …`), then concat with `ffmpeg -f concat -c copy` into `<date>-<slug>-silent.mp4`.
- **Extra outputs:**
  - Captions: `python3 yt_long_<slug>.py --srt youtube/long/<folder>/captions.srt`
  - Thumbnail (premium, realistic style — Paulson rejected the cartoon/mascot look for thumbnails): `python3 yt_thumb_pro.py youtube/long/<folder>/thumbnail.jpg --top "SUBJECT" --big "−47%" --sub "THE SEARCH QUESTION?" --trend down|up --start <v0> --end <v1> --tag "SHORT LABEL"`. One honest number, dark trading-screen look, no mascot, no logos, no real people. Look at it before using it.

## 6. Host the files
- Copy the silent video, `thumbnail.jpg` and `captions.srt` to `build/static/media/yt/<date>-<slug>/`.
- Run `python3 build/build.py site`, then commit and push to main.
- Wait about 100 s for the Vercel deploy.

## 7. Assemble in ElevenLabs (on the same flow)
1. `creative_attach_reference_file` with url `https://www.calcsouq.com/media/yt/<date>-<slug>/<file>.mp4`.
2. Music: `creative_add_flow_asset_node` with modality audio and generation_id `1F1uylCu8eYwoCFakNud` (stock CalcSouq bed, 203 s, instrumental, made in ElevenLabs). Only generate new music if Paulson asks.
3. Add a `composition` node (`eleven_composition`) with connect_from = the TTS nodes in scene order, plus the video node, plus the music node.
4. Read it with `creative_get_flow_node`, then `creative_update_node` with the full `tracks` list:
   - each narration clip's `gap_before` = its scene start in seconds. A scene's start is the sum of the earlier scenes' `round((audio+0.7)*30)/30`.
   - the video clip at 0;
   - the music clip with `fade_in` 1.5, `fade_out` 3 and track `volume` 0.8;
   - `auto_mix` true.
5. Run with `estimate_only` first (it should be 0 credits), then run it. After about 45 s, check the status once.

## 8. Upload pack for Paulson
- Write `youtube/long/<folder>/upload.md` in the same format as video #1:
  - **Title** (≤ 70 characters): the main search phrase first, then the hook. No clickbait the video doesn't back up.
  - **Description:**
    - The first 2 lines use the main search phrase naturally.
    - Chapters (0:00 …) taken from the scene start times.
    - The CalcSouq tool link(s), plus "Figures checked on <date>. For education only, not financial advice." when the topic is about money.
    - End with 3 hashtags (YouTube shows the first 3 above the title).
  - **Tags:** 10–15 search phrases from trends.md, comma separated.
  - **Category:** Education. **Language:** English.
  - **Thumbnail URL:** https://www.calcsouq.com/media/yt/<folder>/thumbnail.jpg
  - **Captions URL:** https://www.calcsouq.com/media/yt/<folder>/captions.srt
- Add a row to `youtube/long/log.md` (date, topic, flow id, generation id, "ready for Paulson"). Commit and push.

## 8b. Instagram teaser (automatic — Paulson's standing rule, 22 Nov 2026)
Every long video also gets an Instagram teaser reel that is posted automatically:
- 1080x1920, 20–25 s, reading pace (AGENTS.md rule), made with build/reel_fx.py + build/reel_audio.py (reference: build/reel_nvda_teaser.py). Hook number first, 3–4 key points, one worked example, end on "Full explainer on YouTube · youtube.com/@calcsouq · link in bio". Same verified facts as the video.
- Save to build/static/media/ig/<date>-<slug>-teaser.mp4 and add a row under "## YouTube teaser reels" in build/ig-queue.md, slot 17:30 Dubai the same day, status exactly `approved` (the poster only publishes that exact word; the rule is Paulson's standing approval of 22 Nov), with the caption block (hook, key numbers, "Full explainer on our YouTube: youtube.com/@calcsouq (link in bio)", tool link, sources/date, "Education only, not investment advice." when about money, 4–6 hashtags). The existing Instagram poster publishes it.
- Mention the teaser and its slot in the message to Paulson.

## 9. Tell Paulson (he is often on his phone)
Paulson wants to download the video inside Claude, not in ElevenLabs.
- Get a fresh `full_res_url` (the direct content.mp4) with `creative_get_generations`.
- Then try `curl -fL -o <folder>.mp4 "<full_res_url>"` in the shell.
  - If it works, check the file with ffprobe (it should have video and audio, about 3 min), then send it with **SendUserFile** (display: attach), named `<YYYY-MM-DD>-<slug>.mp4`.
  - If the proxy refuses (403), the host elevenlabsusercontent.com is not allowed for this session. Say so in one line and give the direct `full_res_url` instead. It opens and downloads straight in the phone browser with no ElevenLabs login, but it expires at about 04:00 Dubai, so tell him to download it soon. Also say that adding elevenlabsusercontent.com to Allowed domains (claude.ai → Settings → Capabilities) lets you attach the file in Claude.
- Also send thumbnail.jpg and captions.srt with SendUserFile.

Send ONE message, plus a push notification, containing:
1. The video, attached as described above. If attaching failed, give the direct link and its expiry.
2. The thumbnail and captions links.
3. The title, description, tags and hashtags in copy-ready blocks.
4. "Upload tip": the best time to publish is usually the agent's recommendation based on the topic's main audience (e.g. 6–8 pm in India = 4:30–6:30 pm Dubai; for US topics, 7–9 am Eastern = 4–6 pm Dubai).
5. Credits left this month.
6. End with the CalcSouq links: https://www.calcsouq.com · https://github.com/paulzn1995/calcsouq · https://search.google.com/search-console · https://adsense.google.com · https://vercel.com/dashboard · https://porkbun.com/account/domainsSpeedy

## Never
- Upload, post, comment or publish on YouTube or any social account.
- Type passwords, or change AdSense or config.json.
- Use expat/NRI/Gulf wording, or say where CalcSouq is made.
- Use copyrighted music, characters, logos or photos of real people.

## 3D B-roll (from 23 Nov 2026 — Paulson asked for real 3D visuals; plan upgraded)
Goal: each long video gets 3–5 short cinematic 3D clips that make it feel premium, without losing the clean explainer style.

**Where they go:** as 3–4 s chapter interstitials between scenes (music only, no narration), plus one 4–5 s clip right after the opening hook. Never over narration (the burnt-in subtitles would be hidden).

**What to generate:** objects and places only, photoreal 3D look, slow camera move, 16:9, 1080p, no text, no logos, no people or faces, no real brands or banks:
- gold bars falling / stacking on a dark reflective table; a bank vault door opening; gold coins pouring; a pawn ticket and gold chain on a counter (no shop names);
- a glowing price chart rising/falling in 3D; a dollar and rupee coin on a see-saw; a city skyline at dusk with a red arrow;
- one clip per chapter that matches it (e.g. Fed chapter: a columned government building silhouette, generic).

**How (inside ElevenLabs, because the sandbox cannot download ElevenLabs files):**
1. `creative_get_model_guide` for the video model, then pick a good-value model (e.g. veo-3.1-fast-generate-001, kling, seedance) and add one video-generation node per clip on the same flow. Ask for 4–5 s (shortest the model allows), no audio.
2. Run `creative_run_flow_nodes` with **estimate_only first**. Keep the clips under ~30% of the credits the narration needs; if they would push credits below what the next two videos need, make fewer clips (minimum 1 for the hook).
3. Host each rendered scene mp4 separately (build/static/media/yt/<folder>/S1.mp4 …) instead of only the joined file, attach each with `creative_attach_reference_file`.
4. Composition video track = scene clips and B-roll clips in order, sequential (gap_before 0, a 0.4 s fade_in/fade_out on B-roll). Shift each narration clip's gap_before by the total B-roll length placed before it. Music track covers the full new length.
5. Subtitles (.srt) must be shifted by the same amounts — regenerate them with the offsets.
6. After the composition finishes, check `duration_secs` matches your computed total.

**Local "3D" upgrades (free, in PIL):** shaded gold bars with highlights and reflections, slight perspective tilt, depth layers that move at different speeds (parallax), a slow camera push-in on key numbers, soft shadows and glow. Use these in every scene.

**YouTube "AI use" answer:** if a video contains generated photoreal B-roll, tell Paulson to choose **Yes** on the AI-use screen (it is a realistic generated scene). Without B-roll, **No**.
