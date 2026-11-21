# Daily long YouTube video: playbook (agent follows this exactly)

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
  - Thumbnail: `python3 yt_thumb.py youtube/long/<folder>/thumbnail.jpg "LINE ONE" "LINE TWO" --hl WORD --tag "..." --stat "..." --prop ...`. Use big words and one honest number. Then look at it.

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

## 9. Tell Paulson (he is often on his phone)
Send ONE message, plus a push notification, containing:
1. The video link to watch and download: the composition's `generation_url`.
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
