# YouTube (@calcsouq) — how it works
- Windsor.ai's YouTube connector cannot upload videos. Agents prepare Shorts + upload packs; Paulson uploads in the YouTube app; agents then optimise (titles, descriptions, tags, playlists), read analytics and hold obvious spam comments for review.
- Shorts must follow the READING PACE rule in AGENTS.md (18–25 s). Re-render older reels at reading pace with `python3 build/yt_pace.py <module> <reel> out.mp4` then add sound with build/reel_audio.py (cue times × 1.75).
- Channel art: banner.png (2560×1440), profile.png (800×800). First upload pack: CalcSouq-YouTube-upload-pack.md.
- Log uploaded videos in build/youtube/log.md (date, file, video id once known, title, playlist).
