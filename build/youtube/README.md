# YouTube (@calcsouq) — how it works
- Windsor.ai's YouTube connector cannot upload videos. Agents prepare Shorts + upload packs; Paulson uploads in the YouTube app; agents then optimise (titles, descriptions, tags, playlists), read analytics and hold obvious spam comments for review.
- Shorts must follow the READING PACE rule in AGENTS.md (18–25 s). Re-render older reels at reading pace with `python3 build/yt_pace.py <module> <reel> out.mp4` then add sound with build/reel_audio.py (cue times × 1.75).
- Channel art: banner.png (2560×1440), profile.png (800×800). First upload pack: CalcSouq-YouTube-upload-pack.md.
- Log uploaded videos in build/youtube/log.md (date, file, video id once known, title, playlist).

## Automatic upload (after Paulson approves)
- Approved videos go in build/youtube/uploads.json: {"id", "date" (YYYY-MM-DD), "title", "description", "tags": [...], "file" (in build/static/media/yt/), "bytes", "status"}.
- The build publishes ONLY status "approved" items at https://www.calcsouq.com/youtube/feed.xml (RSS with the video as enclosure).
- Paulson's Zapier automation (set up once): RSS by Zapier "New item in feed" → YouTube "Upload video" (video = enclosure URL, title, description, tags = category, privacy Public, made for kids = No). Zapier then uploads each newly approved item.
- Never add an item with status "approved" unless Paulson approved that video in chat, or it falls under a standing approval he has given in chat (recorded in this file with date).
