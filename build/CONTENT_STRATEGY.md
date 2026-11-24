# CalcSouq content strategy: curiosity first (Paulson, 24 Nov 2026)

Every agent that makes Instagram reels, YouTube Shorts or videos reads this first.

## What Paulson wants
- Posts people watch **out of curiosity**, learn something **new**, and **share** so their friends learn it too.
- Cinematic **3D** visuals (like the viral 3D metaphor reels: 2.4M likes, 255K shares), not plain number cards.
- Goal: the best money-and-knowledge channel in the world. Brand idea: **"The money behind everything."**
  Every post explains how money, markets, prices or everyday things *really* work, and why.

## Why people share (use at least 3 in every post)
1. **Curiosity gap.** Open a question in second 1 that the viewer cannot answer. Close it only at the end.
   ("Why did Nvidia jump 29% before anyone woke up?" "Where does your old ₹10 coin go?")
2. **Surprise / aha.** One fact that flips what people assumed. If it doesn't surprise you, it won't surprise them.
3. **Social currency.** People share what makes *them* look smart or caring. End with
   "Send this to the friend who…" / "Tag someone who…".
4. **Emotion.** Awe, pride, worry or warmth beats neutral. Family, sacrifice, luck, risk and the future are strong.
5. **Practical value.** One thing they can use today (a rule, a check, a number to remember).
6. **Story.** A character, a problem, a turn. A 3D character on a journey beats a list.
7. **Identity.** "Which one are you?" "Are you the 1 in 10?" Gets comments.

## Format A: 3D curiosity reel (daily, when ElevenLabs credits allow)
- 15–25 s, 1080x1920, 3–4 AI 3D scenes of original characters/objects. Model: gemini-3.1-flash-lite-image, 9:16, 1K,
  ~206 credits per image (estimate_only first). When credits are plentiful, one Veo 3.1 Lite 4 s clip (~1,212 credits)
  for the hook scene.
- Beat 1 (0–4 s): the question + the most striking image. No logo, no intro.
- Beats 2–3: the answer revealed step by step, one idea per scene, with a slow camera move or crossfade
  (template: build/reels_2026_11_24_emotion.py).
- Last beat: the aha line + share prompt. CalcSouq tool link in the caption only if it truly fits.
- Max 3 short lines on screen at once, reading pace from AGENTS.md (each line ≥3 s). English on screen; for
  Kerala/India stories add a Malayalam line (Manjari font).
- Images: no real people, no brand logos or names (check bags, signs, screens; paint them out with OpenCV inpaint),
  no copyrighted characters. Getting images: the sandbox cannot download elevenlabsusercontent.com, so open each
  content_url in the cloud browser at 554x992 and use the saved screenshot (see the 24 Nov session notes in ig-queue.md).

## Format B: emotional story reel (2 a week)
Metaphor stories about money and life (father's shoes, the road to the house, two friends). Same template.

## Format C: number / quiz reels (the rest)
Keep the best performers (loss maths, life in numbers), but always wrap the number in a question or story.

## Topic sources (verify every fact with 2 current sources; never invent)
- Today's news with one jaw-dropping number (markets, AI, oil, gold, rupee, big companies, space, tech).
- Evergreen "how does that work?" money mysteries. Starter bank (research and verify before use):
  - Why does a stock jump before the market even opens?
  - What does it really cost to print a ₹500 note, and who pays?
  - Where does the gold go when you sell it to a jeweller?
  - Why do countries keep buying gold?
  - What happens to your money when a bank fails?
  - How do airlines make money (hint: often not from tickets)?
  - Why do petrol prices change at night?
  - How does a credit card company earn when you pay on time?
  - Why is ₹1 crore today not what it was in 2000?
  - What does 1 billion seconds look like?
  - How one 1% fee eats a pension over 30 years.
  - Why a 50% loss needs a 100% gain.
- Learn from data: Windsor.ai media_shares, media_saved and media_reel_avg_watch_time. Shares per 1,000 views
  is the main score. Every week, write which topics and hooks won in ig-queue.md "## Learnings" and do more of them.

## Hard rules (unchanged)
True hooks only, answered inside the post. Education only, no investment advice. No real people's photos,
copyrighted music/characters or brand logos. Worldwide positioning (never describe CalcSouq as for expats/NRIs/Gulf,
never say where it is made). Never log in anywhere.
