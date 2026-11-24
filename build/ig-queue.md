# Instagram queue (@calcsouq)

Planner (Sunday) adds items with status `awaiting approval`. Only Paulson can approve, by replying in the planner's chat; that session changes the status to `approved`.
Auto-approval (Paulson, 21 Nov 2026): if Paulson does not reply within 15 minutes of an approval request, the items are approved automatically. This covers every item from every task or chat: daily reels and stories, news reels, the Sunday carousel and anything else. Whoever sends the request writes the status as `awaiting approval (auto at YYYY-MM-DD HH:MM)` (Dubai time = send time + 15 min). If Paulson replies before then, his answer replaces the status (`approved`, `rejected`, edits). Once that time has passed, the poster treats the row as approved and records `posted (auto-approved)`.
Daily poster publishes the item for today only if its status is `approved` or its auto-approval time has passed, then sets `posted` with the media id.
Media files live in build/static/media/ig/ and are served at https://www.calcsouq.com/media/ig/<file>.

| Date | Type | Media | Topic / page | Status | Media id |
|---|---|---|---|---|---|
| 2026-11-20 | reel | 2026-11-20-final-settlement.mp4 | /uae-final-settlement-calculator/ | posted manually by Paulson | — |
| 2026-11-20 | carousel (test) | 2026-11-21-welcome-1..4.jpg | / | posted 17:35 Dubai (approved by Paulson in chat) | 18077928467771333 |
| 2026-11-21 00:30 | reel | photo-rejected | — | rejected by Paulson | — |
| 2026-11-21 00:30 | reel | jpg-to-pdf | — | rejected by Paulson | — |
| 2026-11-21 00:21 | reel | 2026-11-21-sip-quiz.mp4 | /sip-calculator/ | replaced (silent version deleted by Paulson) | 18111084173365562 |
| 2026-11-21 00:22 | reel | 2026-11-21-1000-traders.mp4 | /trading-strategy-simulator/ | replaced (silent version deleted by Paulson) | 18123070780988329 |
| 2026-11-21 00:29 | reel | 2026-11-21-sip-quiz-audio.mp4 | /sip-calculator/ | posted with soundtrack (approved) | 18117462449174214 |
| 2026-11-21 00:29 | reel | 2026-11-21-1000-traders-audio.mp4 | /trading-strategy-simulator/ | posted with soundtrack (approved) | 18116309174128547 |
| 2026-11-21 00:43 | reel | 2026-11-21-emi-hidden-cost.mp4 | /loan-emi-calculator/ | posted (approved by Paulson in chat) | 18063848429798439 |

## Learnings
- 2026-11-24 PAULSON (13:54): content must be NEW information that people watch out of curiosity and SHARE so others learn. Daily creator: make the 19:00 reel a cinematic 3D curiosity reel per build/CONTENT_STRATEGY.md (Format A, template build/reels_2026_11_24_emotion.py) whenever ElevenLabs has 900+ credits; otherwise draw it in code and say 3D is waiting for credits. Every reel: curiosity gap in second 1, answer inside, share/comment prompt at the end.
- 2026-11-24 data (last 3 days): the Hormuz teaser (one huge counting number on frame 1) is still the best skip rate (51%), then Life at 30 (56%) and working days (65%); the jargon hook "10% flat" was the worst ever (97% skip, 1.6 s) and 10,000 days old did 71% / 4.7 s. Today: every reel opens on one big counting number in plain words (1,000,000,000 seconds, ₹118, 5 days off, 31.1 g, 100 traders) with the A/B/C pills arriving after it.
- 2026-11-23 EOD data: big animated number + one object on frame 1 won today: Hormuz ML teaser (39 km counting up, barrels) 51.5% skip, 4.6 s avg watch, our best skip rate yet; EMI/RBI ML teaser 66%, 1 save. Static-headline A/B/C quizzes lost: flat-rate trap 89% skip / 1.8 s, ₹100 a day 83% / 2.2 s, down 50 up 50 75%. Do more: open on one huge counting number (new reel_fx.hook_number) and move the A/B/C pills after it, or drop them.
- 2026-11-23 EOD hooks: jargon in the hook ("10% flat") was skipped fastest (89%); say the money result in plain words on frame 1 (e.g. "₹1 lakh loan, ₹30,000 interest") and keep the term for the reveal.
- 2026-11-23 EOD pace: the hold that gets cut is the last reveal before the end card (onion teaser "+₹140" was on screen 1.6 s; re-rendered to 3.2 s). Before rendering, run reel_fx.pace_report(timeline, DUR); after rendering, `python3 build/reel_fx.py sheet in.mp4 out.jpg` makes a 1 fps contact sheet to check every line.
- 2026-11-24 PAULSON'S DIRECTION (shown a viral 3D metaphor reel: 2.4M likes, 255K shares): stop posting only numbers. Mix in emotional story reels that people tag, share and comment on: an AI-generated 3D still or two of original characters (sacrifice, patience, family, the effort behind the result), a slow camera move and crossfade reveal, at most 3 short lines, and an end prompt to tag someone or answer 'which one are you?'. No brand logos in images (check bags and signs). Template: build/reels_2026_11_24_emotion.py. Images cost ~206 ElevenLabs credits each (gemini-3.1-flash-lite-image 1K); with credits low, reuse build/reel_assets/ images or draw scenes in code. Aim for about 1 story reel for every 2 number reels.
- 2026-11-22 EOD QA (toolkit bug, fixed): reel_fx.back() returned ~1e-16 instead of 0 at its start, so every `if p > 0` element (cards, pills, kinetic words) appeared early in its offset/half-drawn state, e.g. all 3 Hormuz cards popped in at once and the end-card title words showed before their beat. Fixed in reel_fx.py; before queueing, check `python3 <reel>.py --frame <t0-0.1>` shows nothing for the next item.
- 2026-11-22 EOD data: the slower 23–25 s reading-pace reels held people longer (avg watch 3.4–5.2 s: working days 5.2 s/64% skip, gold-loan ML teaser 4.8 s with 1 save, FD vs SIP 4.0 s) than the old 13.5 s news cuts (gold off record 2.1 s, 87% skip). Keep the pace rule; the personal-number hook still wins, UAE labour maths is weakest (gratuity: 39 reach, 76% skip).
- 2026-11-22 EOD legibility: secondary lines at 40 px or less ("barrels · 1979 crisis", phone mock-up field labels, "Each loss = that % of the current balance") are too small to read on a phone. Keep any text a viewer must read at 44 px or more; if a phone mock-up holds the key number, repeat it in a pill beside the phone (as position-size did with 0.40 lots).
- 2026-11-22 WEEKLY (16–22 Nov, Windsor): 14 reels + 1 carousel, ~1,300 views, ~1,100 reach (summed), 3,679 non-follower views; followers 0 → 11. Top 5: Bitcoin −51% needs +106% (69% skip, 18.4 s avg watch: loss maths keeps people), Life at 30 (55%, 5.6 s), Working days left (63%, 5.7 s), F&O margin (70%, 4.4 s, 1 save), SIP ₹68 lakh gap (139 views, most). Bottom 5: Fed hike mortgage (90% skip, 2.8 s), First follower meme (88%), Rupee 93 remittance (84%, 2.6 s), Gold making + GST (83%), UAE final settlement (80%).
- Wins: personal time/age numbers and "the maths most people get wrong" (loss recovery, % traps) with one question on frame 1. Loses: rate/FX/market-news hooks and long text lists; milestone memes. Topic-wise: life/date > trading maths > SIP > news.
- Slots: the 11:00 Dubai reels had the best watch time (working days, Bitcoin); late-night posts (00:30–02:00 Dubai) got good views early but higher skip. Sample is small; keep 11:00 for the strongest idea.
- Trial vs normal: Instagram still refuses trial reels (11 followers), so all were normal; keep one trial attempt a week. Auto-approved vs hand-approved: only one auto-approved reel so far (working days: 63% skip, 5.7 s, above average); no sign the approval route matters.
- 2026-11-23 data (last 3 days): personal time/age numbers and loss/% maths still win (Life at 30 56% skip 5.5 s, Rule of 72 60% 5.4 s, working days 65% 5.2 s, Bitcoin −51% 66% 15 s avg); news/rate hooks lose (Fed 89%, gold off record 87%, rupee 84%). Today: all 5 are 'maths most people get wrong' quizzes with a personal number, answer shown by ~5 s.
- Rules for 23–29 Nov: (1) every reel opens on a personal number or a "most people get this wrong" maths question, no news-rate hooks; (2) no reel without a reveal by ~9 s (reading pace still 18–25 s); (3) one save-bait cheat-sheet slide per week (carousel Wed 13:30) to grow saves, which are near zero.
- 2026-11-22 (Paulson, standing rule): reels were too fast to read. READING PACE for every reel: 18–25 s total; every line of text and every number stays fully visible for at least 3 s after it finishes animating in; no more than 2 new text items per beat; slower entrances (about 0.6 s); the reveal number holds 3–4 s; end card holds 4 s. Simple way: write the scene timings as before, then multiply time by SLOW = 1.75 (see build/reel_fed_hike.py) and scale the audio cues by the same factor.
- 2026-11-22 data (last 3 days): 'Life in numbers at 30' won clearly (51% skip, 5.8 s avg watch) vs 69–89% skip for everything else; the news/rate reels did worst (85–87% skip). Personal 'your life/your time' hooks beat market news. Today: lead with a personal-number quiz (working days left) and keep the question visible on frame 1.
- 2026-11-21 Paulson: prefers broad, intriguing content built on the site's complex calculations (quiz/guess formats, simulations) over single-tool demos.
- 2026-11-21 data (last 3 days): lowest skip (48%) and longest watch (5.4 s) = EMI reel with one concrete money question on frame 1; A/B/C quiz and long-text hooks were skipped 73–81%. Lead with a big number + question, show options after ~1 s, reveal by 9 s.
- 2026-11-21 Trial Reels are refused by Instagram: account has too few followers. Post every reel as a normal reel until followers grow; retry trial once a week (if refused, post the same reel normally).

- 2026-11-21 Paulson: wants reels with viral potential built on the latest news or rule changes, including international/global stories (markets, crypto, gold, oil, Fed) as well as UAE/India money, visas, tax and rupee,, packed with facts most people don't know; cite the source/date in the caption and verify every figure before queueing.

| 2026-11-21 | Reel | F&O margin calculator: futures, calendar spread, iron condor vs strangle, lot sizes | build/static/media/ig/2026-11-21-margin-calculator.mp4 | posted 2026-11-21, media 18143848828618251 |

## Topic calendar
Week 23–29 Nov 2026 (Sunday planner, 22 Nov). Slots are Dubai time: 11:00, 13:30, 16:00, 19:00, 21:30 (Wed: 11:00, 14:30, 16:00, 19:00, 21:30; carousel at 13:30). Rows marked VERIFY contain facts that change: check a current official source the morning you render, or drop the figure.
Timely: JEE Main 2027 S1 late registration 23–26 Nov (₹500 late fee), correction 27–29 Nov, exam 20–28 Jan 2027 (NTA via Testbook); CAT 2026 on Sun 29 Nov; UAE Eid Al Etihad: private sector Wed 2–Thu 3 Dec, public sector 2–4 Dec (MoHRE, Gulf News/Khaleej Times 13 Nov); India advance tax 3rd instalment 15 Dec (75%); belated ITR and GSTR-9 31 Dec; Black Friday/White Friday 27 Nov; UAE salary days ~25–30 Nov.

| Day | Slot | Tool page | Hook (frame 1) | Angle | Trial |
|---|---|---|---|---|---|
| Mon 23 | 11:00 | /age-calculator/ | When do you turn 10,000 days old? | 10,000 days ≈ 27 y 4 m; example birth date → exact date; "most people pass it without noticing" | no |
| Mon 23 | 13:30 | /photo-resizer/ | JEE Main form: late window closes 26 Nov. Photo rejected? | Resize photo/signature to exact KB on your phone, files never uploaded. VERIFY sizes in the NTA bulletin | no |
| Mon 23 | 16:00 | /percentage-calculator/ | Down 50%, then up 50%. Are you back to even? | ₹1,000 → ₹500 → ₹750; order doesn't matter (up then down also ₹750) | no |
| Mon 23 | 19:00 | /compound-interest-calculator/ | ₹100 a day for 30 years becomes…? | ₹36,500 a year at 0% / 7% / 12% (illustrative rates) | no |
| Mon 23 | 21:30 | /risk-reward-calculator/ | What win rate do you need at 1:3? | Break-even win rate: 1:1 50%, 1:2 33%, 1:3 25% (before costs) | no |
| Tue 24 | 11:00 | /date-calculator/ | UAE National Day: 1 day of leave = 5 days off | Private sector off Wed 2–Thu 3 Dec; take Fri 4 → Wed–Sun. VERIFY no change since 13 Nov | no |
| Tue 24 | 13:30 | /gst-calculator/ | ₹118 bill incl. 18% GST: how much is GST? | ₹18, not ₹21.24 (reverse-GST trap: divide by 1.18) | no |
| Tue 24 | 16:00 | /age-calculator/ | You turn 1 billion seconds old at…? | 31 y 8 m (≈ 11,574 days); example birth date → date and weekday | no |
| Tue 24 | 19:00 | /gold-tola-pavan-converter/ | 1 pavan, 1 tola, 1 troy ounce: which is heaviest? | 8 g < 11.66 g < 31.10 g; quiz then reveal | no |
| Tue 24 | 21:30 | /trading-strategy-simulator/ | 100 traders, same coin-flip strategy. How many end up? | 50% win rate, 1:1.5 RR, 1% risk: spread of results (run the simulator, quote its output) | no |
| Wed 25 | 11:00 | /age-calculator/ | The UAE turns 55 on 2 Dec. How many days old is it? | 2 Dec 1971 (Thu) → 2 Dec 2026 (Wed) = 20,089 days; "how many days old are you?" | no |
| Wed 25 | 14:30 | /kerala-land-converter/ | How many sq ft is a 5-cent plot? | 1 cent = 435.6 sq ft → 2,178 sq ft; 100 cents = 1 acre | no |
| Wed 25 | 16:00 | /percentage-calculator/ | 8% raise, 6% inflation. What's your real raise? | 1.08 ÷ 1.06 − 1 = 1.89%, not 2% (illustrative rates) | yes (weekly retry; if refused, post normally) |
| Wed 25 | 19:00 | /bmi-calculator/ | Same BMI 24.9: 160 cm vs 185 cm | 63.7 kg vs 85.2 kg; BMI is a screening number only | no |
| Wed 25 | 21:30 | /forex-pip-value-calculator/ | 1 pip on a standard lot: EUR/USD vs USD/JPY vs gold | $10 vs ~$6–7 vs $10 per $0.10 on 100 oz. VERIFY USD/JPY rate and contract size that day | no |
| Thu 26 | 11:00 | /date-calculator/ | CAT is on Sunday. How many hours are left? | Countdown from Thu 11:00 to Sun 29 Nov; hours of sleep vs revision split | no |
| Thu 26 | 13:30 | /uae-leave-encashment-calculator/ | 10 unused leave days on AED 8,000 basic = ? | Basic ÷ 30 × days = AED 2,667. VERIFY basis (basic pay, Decree-Law 33/2021) | no |
| Thu 26 | 16:00 | /percentage-calculator/ | 437 out of 500: what percentage? | 87.4%; and the CGPA × 9.5 rule. VERIFY board rule before using CGPA | no |
| Thu 26 | 19:00 | /compound-interest-calculator/ | Pay only the minimum due on ₹50,000? | Card interest ~3–4% a month compounds to 40%+ a year. VERIFY a current bank rate | no |
| Thu 26 | 21:30 | /futures-tick-value-calculator/ | 1 tick on Nifty vs crude vs gold futures | Lot × tick size. VERIFY current lot sizes and tick sizes | no |
| Fri 27 | 11:00 | /percentage-calculator/ | 50% off + extra 20% off = 70% off? | No: 60% off (₹1,000 → ₹500 → ₹400). Black/White Friday | no |
| Fri 27 | 13:30 | /signature-resizer/ | JEE correction window is open. Signature too big? | Resize to exact KB in the browser. VERIFY sizes in the NTA bulletin | no |
| Fri 27 | 16:00 | /age-calculator/ | Exact age on 1 Jan 2027? Exams check this, not your birthday | "Age as on date" with an example cut-off; one day can make you ineligible | no |
| Fri 27 | 19:00 | /gulf-savings-return-planner/ | Payday: save 20% of AED 6,000 for 5 years = ? | AED 1,200 × 60 at 0% vs 5% (illustrative) | no |
| Fri 27 | 21:30 | /risk-reward-calculator/ | 70% win rate and still losing money? | Avg win $50, avg loss $150 → expectancy −$10 a trade | no |
| Sat 28 | 11:00 | /age-calculator/ | What day of the week were you born? | Quiz with three famous dates, then "check yours" | no |
| Sat 28 | 13:30 | /kerala-stamp-duty-calculator/ | ₹50 lakh plot in Kerala: cash on top? | Stamp duty + registration fee. VERIFY current Kerala rates (8% + 2%?) | no |
| Sat 28 | 16:00 | /image-to-pdf/ | 5 phone photos → 1 PDF under 1 MB? | Quiz on size, then the demo (offline, no upload) | no |
| Sat 28 | 19:00 | /compound-interest-calculator/ | ₹150 coffee a day for 20 years = ? | ₹54,750 a year invested at 10% (illustrative) | no |
| Sat 28 | 21:30 | /market-hours/ | London–New York overlap: what time in Dubai and India? | US winter time from 1 Nov. VERIFY session times | no |
| Sun 29 | 11:00 | /age-calculator/ | Born on 29 Feb? How many real birthdays have you had? | Born 29 Feb 2000 → 6 (2004…2024); next 2028 | no |
| Sun 29 | 13:30 | /mortgage-calculator/ | Equal EMI vs equal principal: which costs less? | Same loan, two schedules: interest difference and first-month payment | no |
| Sun 29 | 16:00 | /percentage-calculator/ | CAT done. 99 percentile = 99% marks? | Percentile is rank-based, not marks; simple 10-person example | no |
| Sun 29 | 19:00 | /date-calculator/ | Resign today with 30 days' notice: last working day? | Calendar days vs working days; date reveal | no |
| Sun 29 | 21:30 | /forex-margin-calculator/ | 1 lot of gold at 1:100 leverage needs how much margin? | Price × 100 oz ÷ 100. VERIFY spot price that morning | no |

Used so far (avoid repeating within 2 weeks): SIP flat vs step-up, 1,000 traders, EMI 10 vs 20 years, F&O margin, UAE final settlement (20–21 Nov); gold making + GST, Dubai property fees, life in numbers at 30, SIP at 25 vs 30, ₹1 crore savings planner, rupee 93, RBI EMI tenure (21 Nov).
Used 23 Nov: 10,000 days old, flat vs reducing rate (10% flat = 17.9%), down 50% up 50%, ₹100 a day for 30 years, break-even win rate at 1:3.
Used 24 Nov: 1 billion seconds old, GST inside ₹118 (reverse GST), UAE National Day 1 leave = 5 days off, 1 ounce = 3.9 pavan, 100 traders same strategy.
Used 22 Nov: working days left in 2026, FD vs SIP 15 yrs, UAE gratuity 10 yrs (21 vs 30 days), Rule of 72 doubling, position size / 10 losses in a row, Bitcoin −51% loss maths, gold off record, Fed hike mortgage, Nvidia teaser, gold loan (ML) teaser.
Planned 25 Nov carousel: EMI on ₹10 lakh at 5 rates (5/10/20 years, per-₹1-lakh shortcut).

## 2026-11-21 daily set (made by the daily Reels creator; slots are Dubai time)
Renders: build/reels_2026_11_21.py (reels), build/stories_2026_11_21.py (stories). Soundtrack: build/reel_audio.py, seed = 2026112N.

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-21 | 11:00 | reel | no | 2000 | desi | 2026-11-21-gold-hidden-cost.mp4 | /gold-price-calculator/ | posted 11:10 Dubai (approved by Paulson in chat), media 18102444311090136 |
| 2026-11-21 | 12:00 | story | — | — | — | 2026-11-21-story-gold-quiz.jpg | /gold-price-calculator/ | posted 12:03 Dubai (approved by Paulson in chat), media 18080585141724366 |
| 2026-11-21 | 13:30 | reel | no | 2000 | cinematic | 2026-11-21-dubai-property-costs.mp4 | /property-buying-cost-calculator/ | posted 16:06 Dubai (approved; late, slot was missed), media 18501931339100504 |
| 2026-11-21 | 16:00 | reel | yes | 1800 | pop | 2026-11-21-life-in-numbers.mp4 | /age-calculator/ | posted 16:06 Dubai (approved; trial refused: too few followers, posted as normal reel), media 17882995719553346 |
| 2026-11-21 | 18:00 | story | — | — | — | 2026-11-21-story-sip-gap.jpg | /sip-calculator/ | posted 18:03 Dubai (approved), media 18119707631107659 |
| 2026-11-21 | 19:00 | reel | no | 1600 | funk | 2026-11-21-sip-25-vs-30.mp4 | /sip-calculator/ | posted 19:03 Dubai (approved), media 18162405319502269 |
| 2026-11-21 | 21:30 | reel | yes | 2000 | lofi | 2026-11-21-one-crore-planner.mp4 | /gulf-savings-return-planner/ | approved |
| 2026-11-21 | 20:00 | reel | no | 1000 | electro | 2026-11-21-rupee-93.mp4 | /compare-remittance-aed-to-inr/ | posted 21:03 Dubai (approved by Paulson 21 Nov 12:33; late, slot was missed), media 18117491987329290 |
| 2026-11-21 | 22:30 | reel | no | 1000 | cinematic | 2026-11-21-rbi-emi-tenure.mp4 | /loan-emi-calculator/ | approved (Paulson 21 Nov 12:33) |
| 2026-11-21 | 16:30 | reel | no | 0 | funk | 2026-11-21-first-follower.mp4 | / | posted 16:34 Dubai (Paulson asked in chat to create and post it), media 18119711036153466 |

```captions
[2026-11-21 11:00]
₹1 lakh of gold jewellery: what's the real bill?
Gold value ₹1,00,000
+ making charge 12% = ₹12,000
+ GST 3% on gold AND making = ₹3,360
Bill: ₹1,15,360. At 20% making it's ₹1,23,600.
Link in bio → Gold price calculator (making charges + GST/VAT)
Did you guess A, B or C? 👇
Example: 22K, India, making 12%, GST 3%. Making charges vary by jeweller.
#goldprice #goldjewellery #makingcharges #gstongold #22kgold #calcsouq

[2026-11-21 13:30]
Buying a AED 1.5M flat in Dubai? Here's the cash on top.
DLD transfer fee 4%: AED 60,000
Agent 2% + VAT: AED 31,500
Trustee fee + VAT: AED 4,200 · admin & title deed: about AED 580
Total: AED 96,280 (6.4% on top of the price)
Link in bio → Property buying cost calculator
Which fee surprised you most? 👇
Cash purchase, before mortgage fees. Fees can change; check with the Dubai Land Department.
#dubaiproperty #dubairealestate #dldfees #buyingahome #propertycosts #calcsouq

[2026-11-21 16:00]
Your life in numbers at 30
30 years = 10,957 days = 262,968 hours
1,565 weekends lived
Weekdays left until 60: 7,826 (Mon–Fri, before holidays and leave)
Link in bio → Age calculator (exact age, days lived, next birthday)
What would you do with 1,565 more weekends? 👇
Example: born 21 Nov 1996, counted to 21 Nov 2026.
#agecalculator #lifeinnumbers #daysalive #timemanagement #motivation #calcsouq

[2026-11-21 19:00]
SIP at 25 vs 30: what 5 years of waiting costs
₹5,000 a month until 60, at an assumed 12% a year:
Start at 35 → about ₹95 lakh
Start at 30 → about ₹1.76 crore
Start at 25 → about ₹3.25 crore
Gap: ₹1.48 crore, for only ₹3 lakh more invested.
Link in bio → Step-up SIP calculator
At what age did you start? 👇
Illustration only. Returns are not guaranteed. Not investment advice.
#sipcalculator #mutualfunds #compounding #startearly #personalfinance #calcsouq

[2026-11-21 21:30]
How long to save ₹1 crore on AED 3,000 a month?
Just saving: 11 yrs 7 mo
With 7% growth: 8 yrs 7 mo
With 3% yearly raises + UAE gratuity too: 7 yrs 4 mo
Link in bio → Savings goal planner
What's your target number? 👇
Assumes ₹24 per AED, starting from zero, AED 8,000 basic for gratuity. Returns are not guaranteed. Not investment advice.
#savingsgoal #onecrore #financialplanning #moneygoals #gratuity #calcsouq

[2026-11-21 20:00]
The rupee just hit 93 per dollar: its strongest since April. Great news? Not if you send money home.
AED is pegged at 3.6725 per $, so a strong rupee means fewer rupees per dirham.
AED 5,000 at the late-May low (₹96.96/$): ₹1,32,008
AED 5,000 now (₹93.00/$): ₹1,26,617
That's ₹5,391 less per transfer, about ₹64,700 a year if you send monthly, before your exchange house's margin.
Link in bio → Compare remittance rates (AED to INR)
Are you sending now or waiting? 👇
Rates: rupee touched 92.995/$ on 20 Nov 2026 (Reuters); 2026 low 96.96 in late May (LKP Securities). Not financial advice.
#aedtoinr #rupee #forex #moneytransfer #remittance #calcsouq

[2026-11-21 22:30]
RBI raised the repo rate (5.25% → 5.50%, 7 Oct 2026). Your EMI didn't change? Check your tenure.
₹50 lakh home loan, 20 years, 8.00% → 8.25%:
A) EMI up ₹781 a month → about ₹1.88 lakh extra over the loan
B) Same EMI, 12 more months → about ₹4.96 lakh extra
A longer tenure costs about 2.6× more. You can ask your bank to raise the EMI instead (or do both).
Link in bio → Loan EMI calculator
Did your bank extend your tenure? 👇
Example: full 20-year loan repriced at 8.25%; your rate and bank's spread will differ. Not financial advice.
#homeloan #emi #rbi #reporate #interestrates #calcsouq

[2026-11-21 first-follower]
From 0 followers to 1 follower. Yipeeeeeeee 🎉
To our one follower: you are literally the whole fan club. 🙏
Want to be follower #2? We make free calculators for EMI, tax, gold, SIP, salary and more.
Link in bio → calcsouq.com
Tag someone who'd follow a calculator page 👇
#firstfollower #smallbeginnings #growthjourney #relatable #startuplife #calcsouq
```

## 2026-11-22 international news reels (made in Paulson's chat 21 Nov; slots are Dubai time)
Render: build/reels_2026_11_21_world.py. Sources in the script header.

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-22 | 10:30 | reel | no | 1000 | electro | 2026-11-21-bitcoin-half-off.mp4 | /percentage-calculator/ | posted 22 Nov 11:05 Dubai (approved by Paulson 21 Nov 12:33), media 17972236698198157 |
| 2026-11-22 | 14:30 | reel | no | 1000 | desi | 2026-11-21-gold-off-record.mp4 | /gold-price-calculator/ | posted 22 Nov 16:06 Dubai (approved by Paulson 21 Nov 12:33), media 18134154409892025 |

```captions
[2026-11-22 10:30]
Bitcoin is down 51% from its peak. How much does it need to get back?
Peak: $126,198 (6 Oct 2025). 20 Nov 2026: about $61,300.
$10,000 bought at the top is worth about $4,859 today.
To break even it needs +106%, not +51%.
The loss math: −20% needs +25%, −33% needs +50%, −50% needs +100%.
Link in bio → Percentage change calculator
Did you guess +51%? 👇
Prices: Fortune, 20 Nov 2026. Crypto is volatile. Not financial advice.
#bitcoin #crypto #btc #investing #lossmath #calcsouq

[2026-11-22 14:30]
Gold hit a record $5,590 an ounce on 28 Jan 2026. On 19 Nov it was about $3,715.
100 g of gold, spot value:
January peak: AED 66,003
19 Nov: AED 43,864
That's 34% down. To get back to the record, gold needs +50%.
Bought jewellery? Making charges usually aren't paid back when you sell. Coins and bars resell closest to spot.
Link in bio → Gold price calculator
Are you buying the dip or waiting? 👇
Prices: spot, 28 Jan and 19 Nov 2026 ($1 = AED 3.6725). Shop prices differ. Not financial advice.
#goldprice #dubaigold #gold #goldrate #investing #calcsouq
```

| 2026-11-22 | 00:20 | reel | no | 2800 | cinematic | 2026-11-22-fed-hike-mortgage.mp4 | /mortgage-calculator/ | posted 22 Nov 00:17 Dubai (Paulson asked in chat: "create and post"), media 18126261127933091 |
| 2026-11-22 | 00:27 | reel | no | 4900 | cinematic | 2026-11-22-fed-hike-mortgage-slow.mp4 | /mortgage-calculator/ | posted 22 Nov 00:27 Dubai (Paulson: "post now"; reading-pace version, 24.5 s), media 18136312300685864. The 14 s version (18126261127933091) is still live until Paulson deletes it in the app |

## YouTube teaser reels (Paulson, 22 Nov 03:09: "whenever we create a YouTube video make its insta post also with youtube link and post it automatically")
Rule: every long YouTube video gets a 20–25 s vertical teaser reel (reading pace) that ends "Full explainer on YouTube · youtube.com/@calcsouq · link in bio". The teaser row is created with status exactly `approved` (Paulson's standing rule 22 Nov: YouTube teasers post automatically) and the poster publishes it at its slot. Slot: same day, 17:30 Dubai (or the next free slot).

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-22 | 17:30 | reel | no | 3500 | cinematic | 2026-11-22-nvidia-ai-crash-teaser.mp4 | /percentage-calculator/ | posted 22 Nov 18:05 Dubai (approved: YouTube teaser rule), media 18116533043132278 |
| 2026-11-22 | 17:45 | reel | no | 1500 | cinematic | 2026-11-22-gold-loan-ml-teaser.mp4 | /gold-price-calculator/ | posted 22 Nov 19:04 Dubai (approved: YouTube teaser rule), media 18129571402917476 |
| 2026-11-23 | 17:45 | reel | no | 1500 | cinematic | 2026-11-23-hormuz-ml-teaser.mp4 | /loan-emi-calculator/ | posted 23 Nov 18:05 Dubai (approved: YouTube teaser rule), media 17981614515172878 |
| 2026-11-23 | 18:00 | reel | no | 1500 | cinematic | 2026-11-23-emi-rbi-ml-teaser.mp4 | /loan-emi-calculator/ | posted 23 Nov 19:06 Dubai (approved: YouTube teaser rule), media 18018958883968828 |
| 2026-11-24 | 19:30 | reel | no | 1500 | cinematic | 2026-11-23-onion-ml-teaser.mp4 | /percentage-calculator/ | approved (quality re-render 23 Nov EOD: "+₹140" reveal now holds 3.2 s, 23.6 s; same facts and caption) |

[2026-11-22 17:30]
```
Nvidia just lost almost half its value 📉 Is the AI bubble bursting?

From a ~$239 record (6 Oct) to $125.53 (20 Nov): about −47% in seven weeks. 4 reasons:
1️⃣ Doubts that AI spending turns into profit fast enough
2️⃣ Fears of tighter AI rules and data-centre pushback after the US midterms
3️⃣ CEO Jensen Huang resigned on 12 Nov
4️⃣ A Fed rate hike expected in December

The maths: $1,000 at the record = about $525 now, and it needs +91% just to get back.

▶️ Full 3-minute explainer on our YouTube: youtube.com/@calcsouq (link in bio)
Work out any gain or loss: calcsouq.com/percentage-calculator

Sources: company filing, AP/Reuters market reports, 20–21 Nov 2026. Education only, not investment advice.

#nvidia #aibubble #stockmarket #nasdaq #calcsouq
```

[2026-11-22 17:45]
```
സ്വർണ്ണം പണയം വെച്ചവർ കുടുങ്ങിയോ? 😟 Gold loan holders, watch this.

ജനുവരിയിൽ ഒരു പവന് ₹1,31,000-ൽ അധികം. ഇന്ന് ഏകദേശം ₹92,000. പവന് ഏകദേശം ₹39,000 കുറവ്.
Same loan, cheaper gold → your LTV goes up → the bank may ask for margin.

എന്തുകൊണ്ട് സ്വർണ്ണം കുറയുന്നു?
1️⃣ US Fed: more rate hikes expected
2️⃣ Dollar near a 19-month high
3️⃣ Stock crash: investors sold gold for cash

▶️ ബാങ്ക് വിളിക്കും മുൻപ് മുഴുവൻ വീഡിയോ കാണുക: youtube.com/@calcsouq (link in bio). Malayalam, with English subtitles.
Pavan price calculator: calcsouq.com/gold-price-calculator

Kerala 22K rates 21 Nov 2026; RBI gold loan rules from 1 Apr 2026. Education only, not financial advice.

#goldrate #goldloan #keralagoldrate #സ്വർണ്ണവില #calcsouq
```

## 2026-11-23 daily set (made by the daily Reels creator; slots are Dubai time)
Renders: build/reels_2026_11_23.py (reels, reading pace SLOW = 1.75, 23.1 s each, answer revealed at ~4.5–6 s), build/stories_2026_11_23.py (stories). Soundtrack: build/reel_audio.py, seed = 2026112N. The calendar's 13:30 JEE photo-resizer demo was swapped for the flat-rate loan quiz (Paulson prefers complex-calculation quizzes over single-tool demos).

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | 11:00 | reel | no | 3500 | pop | 2026-11-23-10000-days-old.mp4 | /age-calculator/ | posted (auto-approved) 11:06 Dubai, media 18164753548500786 |
| 2026-11-23 | 12:00 | story | — | — | — | 2026-11-23-story-10000-days.jpg | /age-calculator/ | posted (auto-approved) 12:10 Dubai, media 18654865579053282 |
| 2026-11-23 | 13:30 | reel | no | 3500 | cinematic | 2026-11-23-flat-rate-trap.mp4 | /loan-emi-calculator/ | posted (auto-approved) 16:06 Dubai, media 18002230269031431 |
| 2026-11-23 | 16:00 | reel | yes | 3500 | funk | 2026-11-23-down-50-up-50.mp4 | /percentage-calculator/ | posted (auto-approved) 16:06 Dubai as normal reel (trial refused: too few followers), media 18648202270039938 |
| 2026-11-23 | 18:00 | story | — | — | — | 2026-11-23-story-flat-rate.jpg | /loan-emi-calculator/ | posted (auto-approved) 18:05 Dubai, media 18117285725156224 |
| 2026-11-23 | 19:00 | reel | yes | 3500 | desi | 2026-11-23-100-a-day-30-years.mp4 | /compound-interest-calculator/ | posted (auto-approved) 19:06 Dubai as normal reel (trial refused: too few followers), media 18024351173729091 |
| 2026-11-23 | 21:30 | reel | no | 3500 | electro | 2026-11-23-break-even-win-rate.mp4 | /risk-reward-calculator/ | awaiting approval (auto at 2026-11-23 09:47) |

```captions
[2026-11-23 11:00]
When do you turn 10,000 days old?
10,000 days = 27 years 4 months and a bit (about 27.4 years).
Born 15 July 1999? Your 10,000th day is Monday 30 Nov 2026.
20,000 days ≈ 54.8 years. 30,000 days ≈ 82.1 years.
Link in bio → Age calculator (exact age and total days lived)
How many days old are you today? 👇
Days counted from the birth date to the chosen date, as the age calculator does.
#agecalculator #10000days #lifeinnumbers #birthday #howoldami #calcsouq

[2026-11-23 13:30]
"10% flat" loan: what's the real interest rate?
₹1 lakh for 3 years at 10% flat: interest ₹30,000, EMI ₹3,611.
Flat interest is charged on the full loan for all 3 years, even as you repay it.
The same EMI on a reducing balance = about 17.9% a year.
A true 10% reducing-balance loan: EMI ₹3,227, interest ₹16,162.
Link in bio → Loan EMI calculator
Has a lender ever quoted you a "flat" rate? 👇
Example figures, before processing fees and insurance. Always ask for the reducing-balance rate (APR). Not financial advice.
#flatrate #personalloan #emicalculator #loantips #interestrate #calcsouq

[2026-11-23 16:00]
Down 50%, then up 50%: are you back to even?
No. ₹1,000 → ₹500 → ₹750. You're still 25% down.
Up 50% first? ₹1,000 → ₹1,500 → ₹750. Same result.
After a 50% fall you need +100% to get back.
Link in bio → Percentage change calculator
Did you guess A, B or C? 👇
Simple percentage maths, any currency or asset. Not investment advice.
#percentage #lossmath #investing101 #stockmarket #mathtricks #calcsouq

[2026-11-23 19:00]
₹100 a day for 30 years becomes…?
₹3,000 a month for 30 years = ₹10.8 lakh put in.
At 7% a year: about ₹36.6 lakh
At an assumed 12% a year: about ₹1.05 crore
Link in bio → Compound interest calculator (with monthly additions)
What would you skip to save ₹100 a day? 👇
Illustration only: ₹3,000 added at the end of each month, compounded monthly, before tax. Returns are not guaranteed. Not investment advice.
#compoundinterest #savemoney #sip #moneytips #personalfinance #calcsouq

[2026-11-23 21:30]
Risk 1 to make 3: what win rate breaks even?
Just 25%. Breakeven win rate = 1 ÷ (1 + R).
1:1 → 50% · 1:2 → 33% · 1:3 → 25%
3 wins in 10 trades at 1:3 = +2R (9R won − 7R lost).
Link in bio → Risk–reward calculator
What risk–reward do you trade? 👇
Before spreads, commission and slippage. Education only, not investment advice.
#riskreward #tradingtips #forextrading #riskmanagement #daytrading #calcsouq
```

## 2026-11-23 YouTube Shorts → Instagram (made by the daily Shorts agent; slots are Dubai time)
Best of the 3 world-news Shorts (build/yt_shorts_2026_11_23.py, pack build/youtube/2026-11-23-pack.md), posted automatically under Paulson's standing rule (YouTube teasers/shorts post automatically). 21:30 was already taken by the break-even win-rate reel, so this goes at 22:00.

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | 22:00 | reel | no | 4000 | cinematic | 2026-11-23-sensex-1484-crash-short.mp4 | /percentage-calculator/ | approved |

```captions
[2026-11-23 22:00]
ഷെയറിൽ ഇട്ടവർക്ക് ഇന്ന് എത്ര പോയി? 📉 Sensex −1,484 today.

Sensex closed at 82,436 (−1.77%) and Nifty 50 at 25,350 (−1.75%) on 23 Nov.
Why: the US AI-stock sell-off spread to Asia; banks and metals fell most.
Your money: ₹1 lakh in a Nifty index fund ≈ ₹1,750 less tonight (a paper loss until you sell).
Markets are shut on 24 Nov (Guru Nanak Jayanti) and reopen on Wednesday.

▶️ Daily world money news in Malayalam: youtube.com/@calcsouq (link in bio)
Work out any gain or loss: calcsouq.com/percentage-calculator

Sources: BSE/NSE close via Business Standard, NationPath, InCred, 23 Nov 2026. Education only, not investment advice.
#sensex #nifty #stockmarketcrash #sharemarket #calcsouq
```

## 2026-11-22 daily set (made by the daily Reels creator; slots are Dubai time)
Renders: build/reels_2026_11_22.py (reels, reading pace SLOW = 1.75, 23.4 s each), build/stories_2026_11_22.py (stories). Soundtrack: build/reel_audio.py, seed = 2026112N.

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-22 | 11:00 | reel | no | 500 | pop | 2026-11-22-working-days-left.mp4 | /date-calculator/ | posted (auto-approved) 22 Nov 11:05 Dubai, media 18124125247967161 |
| 2026-11-22 | 12:00 | story | — | — | — | 2026-11-22-story-days-quiz.jpg | /date-calculator/ | posted (auto-approved) 22 Nov 12:04 Dubai, media 18125095810940672 |
| 2026-11-22 | 13:30 | reel | yes | 500 | desi | 2026-11-22-fd-vs-sip.mp4 | /sip-calculator/ | posted (auto-approved) 22 Nov 16:05 Dubai as a normal reel (trial refused: too few followers), media 17920088349545514 |
| 2026-11-22 | 16:00 | reel | no | 500 | cinematic | 2026-11-22-uae-gratuity-10-years.mp4 | /uae-gratuity-calculator/ | posted (auto-approved) 22 Nov 18:05 Dubai, media 18175007167463653 |
| 2026-11-22 | 18:00 | story | — | — | — | 2026-11-22-story-rule-of-72.jpg | /compound-interest-calculator/ | posted (auto-approved) 22 Nov 19:04 Dubai, media 18072661472606429 |
| 2026-11-22 | 19:00 | reel | yes | 500 | funk | 2026-11-22-rule-of-72.mp4 | /compound-interest-calculator/ | posted (auto-approved) 22 Nov 21:04 Dubai as a normal reel (trial refused: too few followers), media 18119805218591886 |
| 2026-11-22 | 21:30 | reel | no | 500 | electro | 2026-11-22-position-size.mp4 | /position-size-calculator/ | awaiting approval (auto at 2026-11-22 09:52) |

```captions
[2026-11-22 11:00]
How many working days are left in 2026?
From 23 Nov to 31 Dec: 39 days left.
10 of them are weekend days.
That leaves 29 working days: about 232 hours at 8 a day.
89% of this year's 261 working days are already gone.
Link in bio → Days between dates calculator (working days included)
Which goal are you finishing before 31 Dec? 👇
Counted Monday to Friday, before public holidays and leave.
#workingdays #yearend #productivity #goals2026 #datecalculator #calcsouq

[2026-11-22 13:30]
FD vs SIP: ₹10,000 a month for 15 years
You put in: ₹18 lakh
FD/RD at 7%: about ₹31.6 lakh
SIP at an assumed 12%: about ₹50.5 lakh
Gap: about ₹18.9 lakh. The FD rate is fixed; SIP returns are market-linked and can be lower (or negative).
Link in bio → SIP calculator and compound interest calculator
What did you guess: A, B or C? 👇
Illustration only: RD at 7% compounded quarterly, SIP at 12% compounded monthly, before tax. Returns are not guaranteed. Not investment advice.
#fdvssip #sipcalculator #fixeddeposit #mutualfunds #personalfinance #calcsouq

[2026-11-22 16:00]
UAE gratuity after 10 years on AED 10,000 basic
Years 1–5: 21 days' basic a year = AED 7,000 a year → AED 35,000
Years 6–10: 30 days' basic a year = AED 10,000 a year → AED 50,000
Total: AED 85,000. Every year after year 5 pays 43% more.
Capped at 2 years' basic (AED 240,000).
Link in bio → UAE gratuity calculator
Did you guess B? 👇
Private sector, Federal Decree-Law 33 of 2021 (Art. 51); basic salary only, day rate = basic ÷ 30. General information, not legal advice.
#uaegratuity #endofservice #uaelabourlaw #dubaijobs #uaesalary #calcsouq

[2026-11-22 19:00]
How long does it take to double your money at 8%?
Rule of 72: 72 ÷ 8 = 9 years.
₹1 lakh at 8% a year → ₹1,99,900 after 9 years
Wait 27 years and it doubles 3 times: about ₹7.99 lakh
At 6% it takes about 12 years; at 12% about 6.
Link in bio → Compound interest calculator
What rate are you earning right now? 👇
Compounded yearly, before tax, example rates. Returns are not guaranteed. Not investment advice.
#ruleof72 #compoundinterest #doubleyourmoney #moneytips #investing101 #calcsouq

[2026-11-22 21:30]
$10,000 account, 1% risk: how many lots?
Risk $100 ÷ (25-pip stop × $10 a pip per lot) = 0.40 lots on EUR/USD
Trade 1 full lot with the same stop and one loss costs $250 (2.5%).
10 losses in a row: risking 1% a trade leaves $9,044; risking 5% leaves $5,987.
Link in bio → Position size calculator (forex and gold)
What do you risk per trade? 👇
Example: standard lot, $10 a pip, each loss a % of the current balance, before spread and commission. Education only, not investment advice.
#positionsizing #forextrading #riskmanagement #lotsize #tradingtips #calcsouq
```

## 2026-11-25 carousel (Sunday planner, 22 Nov)
Render: build/carousel_2026_11_25.py (7 slides, 1080x1350 JPEG). All figures are reducing-balance EMI maths, computed by two independent methods in the script (formula and amortisation bisection; it asserts they agree within ₹1).

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-25 | 13:30 | carousel | — | — | dark cheat sheet | 2026-11-25-emi-10-lakh-1..7.jpg | /loan-emi-calculator/ | awaiting approval (auto at 2026-11-22 15:58) |

```captions
[2026-11-25 13:30]
EMI on a ₹10 lakh loan at 8%, 9%, 10%, 11% and 12% 📌 Save this for your next loan quote.

5 years at 10%: EMI ₹21,247, interest ₹2.75 lakh
10 years at 10%: EMI ₹13,215, interest ₹5.86 lakh
20 years at 10%: EMI ₹9,650, interest ₹13.16 lakh

The longer loan cuts the EMI by ₹11,597 but adds ₹10.41 lakh of interest.
Shortcut on slide 6: EMI per ₹1 lakh. Multiply by your loan in lakh.

Link in bio → Loan EMI calculator (any amount, rate and tenure)
Which rate did your bank quote? 👇

Reducing-balance EMI, monthly rests, before processing fees and insurance. Rates shown are examples, not offers. Not financial advice.
#emi #homeloan #personalloan #carloan #loancalculator #calcsouq
```

[2026-11-23 17:45]
```
ഈ കടൽ അടഞ്ഞാൽ നമ്മൾ? 🌊 വെറും 39 കിലോമീറ്റർ — ഹോർമുസ് കടലിടുക്ക്.

യുദ്ധത്തിന് മുമ്പ് ലോകത്തിലെ എണ്ണയുടെയും ഗ്യാസിന്റെയും അഞ്ചിലൊന്ന് ഇതുവഴിയാണ് പോയിരുന്നത്. ചരിത്രത്തിലെ ഏറ്റവും വലിയ എണ്ണ-ഗ്യാസ് തടസ്സമെന്ന് IEA.
⛽ Petrol (Kochi): ≈₹106 → ≈₹114 in a year
🔥 Kitchen LPG: +₹89 since March
🏦 RBI repo: 5.5%

▶️ മുഴുവൻ വീഡിയോ (Malayalam, English subtitles): youtube.com/@calcsouq (link in bio)
EMI calculator: calcsouq.com/loan-emi-calculator

Figures checked 22 Nov 2026 (IEA, Kpler, PTI, Upstox). Education only, not financial advice.

#hormuz #petrolprice #lpg #malayalam #calcsouq
```

[2026-11-24 19:30]
```
ഉള്ളി വില ഇരട്ടിയായി! 🧅 ഒരു വർഷം കൊണ്ട് +116%.

പക്ഷേ ഉരുളക്കിഴങ്ങിന് വില കുറഞ്ഞു. എന്തുകൊണ്ട്?
🧄 Garlic +61% · Ginger +48%
🍲 Food inflation 8.94% · CPI 6.09% (above RBI's 6%)
🏠 Example: 4 kg a month, ₹120 → ₹260

▶️ മുഴുവൻ വീഡിയോ (Malayalam, English subtitles): youtube.com/@calcsouq (link in bio)
Percentage calculator: calcsouq.com/percentage-calculator

Figures checked 23 Nov 2026 (MoSPI/PIB, ThePrint). Kitchen figures are an example. Education only.
#OnionPrice #Inflation #Kerala #MalayalamNews #CalcSouq
```


[2026-11-23 18:00]
```
ഹോം ലോൺ EMI വീണ്ടും കൂടുമോ? 🏠 ഡിസംബർ 4-ന് റിസർവ് ബാങ്ക് തീരുമാനം.

₹30 ലക്ഷം ലോൺ, 20 വർഷം: റിപ്പോ 6% ആയാൽ EMI മാസം ≈ +₹1,382 (ഒക്ടോബറിന് മുമ്പുള്ളതിനേക്കാൾ).
📈 Inflation 6.09% in October (above the RBI's 6% limit)
🏦 Repo 5.25% → 5.50% on 7 Oct; most forecasters expect another 0.25% on 4 Dec
⚠️ Same EMI, longer loan: +39 months and ≈ ₹9.3 lakh more paid (raising the EMI instead ≈ ₹3.3 lakh)

▶️ മുഴുവൻ വീഡിയോ (Malayalam, English subtitles): youtube.com/@calcsouq (link in bio)
Check your own EMI: calcsouq.com/loan-emi-calculator

Figures checked 23 Nov 2026 (MoSPI CPI, RBI, SBI/PNB rate notices, Business Standard, ThePrint). Example assumes full pass-through. Education only, not financial advice.

#homeloan #emi #rbi #malayalam #calcsouq
```

## 2026-11-23 NVDA / AI premarket news (Paulson asked 18:17 Dubai: "push a few posts fast"). Render: build/reels_2026_11_23_nvda.py (sources in header)

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-23 | 18:30 | reel | no | 3000 | electro | 2026-11-23-nvda-29-premarket.mp4 | /percentage-calculator/ | posted 18:2x Dubai (Paulson asked), media 17941741677403756 |
| 2026-11-23 | 18:35 | reel | no | 3000 | pop | 2026-11-23-ai-stocks-premarket.mp4 | /percentage-calculator/ | posted (Paulson asked), media 18119208430829536 |
| 2026-11-23 | 18:40 | story | — | — | — | 2026-11-23-story-nvda-29.jpg | /percentage-calculator/ | posted (Paulson asked), media 18402889363203070 |

## 2026-11-24 daily set (made by the daily Reels creator; slots are Dubai time)
Renders: build/reels_2026_11_24.py (reels, reading pace SLOW = 1.75, 23.1 s each, frame 1 = one big counting number per the 23 Nov learning; answer revealed at ~6 s), build/stories_2026_11_24.py (stories). Soundtrack: build/reel_audio.py, seed = 2026112N. Calendar swap: the strongest idea by data (personal age number: 1 billion seconds) moved to 11:00; UAE National Day leave moved to 16:00. National Day dates re-checked 24 Nov (MoHRE via The National / Gulf News, 13 and 17 Nov: private sector paid holiday Wed 2–Thu 3 Dec 2026).

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 11:00 | reel | no | 4500 | cinematic | 2026-11-24-billion-seconds.mp4 | /age-calculator/ | posted (auto-approved) 11:04 Dubai, media 18136703135504650 |
| 2026-11-24 | 12:00 | story | — | — | — | 2026-11-24-story-billion-seconds.jpg | /age-calculator/ | posted (auto-approved) 12:04 Dubai, media 17983014477152833 |
| 2026-11-24 | 13:30 | reel | yes | 4500 | desi | 2026-11-24-gst-inside-118.mp4 | /gst-calculator/ | posted (auto-approved) 16:11 Dubai as normal reel (trial refused: too few followers), media 18399910276164819 |
| 2026-11-24 | 16:00 | reel | no | 4500 | funk | 2026-11-24-national-day-5-days.mp4 | /date-calculator/ | posted (auto-approved) 16:11 Dubai, media 18436323061146948 |
| 2026-11-24 | 18:00 | story | — | — | — | 2026-11-24-story-national-day.jpg | /date-calculator/ | posted (auto-approved) 18:04 Dubai, media 17909578710669753 |
| 2026-11-24 | 19:00 | reel | yes | 4500 | pop | 2026-11-24-ounce-in-pavan.mp4 | /gold-tola-pavan-converter/ | posted (auto-approved) 19:05 Dubai as normal reel (trial refused: too few followers), media 18233932927336896 |
| 2026-11-24 | 21:30 | reel | no | 4500 | electro | 2026-11-24-100-traders.mp4 | /trading-strategy-simulator/ | awaiting approval (auto at 2026-11-24 09:49) |

```captions
[2026-11-24 11:00]
When do you turn 1 billion seconds old?
1,000,000,000 seconds = 11,574 days = 31 years 8 months (about 31.7 years).
Born 1 Jan 1996? Your billion-second day is Thursday 9 Sep 2027.
2 billion seconds ≈ 63.4 years.
Link in bio → Age calculator (exact age and total days lived)
Have you passed your billion yet? 👇
Counted from midnight on the birth date; leap years included.
#agecalculator #billionseconds #lifeinnumbers #birthday #howoldami #calcsouq

[2026-11-24 12:00]
(story) Quiz: You turn 1,000,000,000 seconds old at…? A 21 years · B 31 years 8 months · C 41 years. Answer in today's reel. calcsouq.com

[2026-11-24 13:30]
₹118 bill with 18% GST: how much is the GST?
₹18, not ₹21.24.
The ₹118 already includes GST, so divide: 118 × 18 ÷ 118 = ₹18. Price before GST = ₹100.
Any rate: GST inside a bill = bill × rate ÷ (100 + rate).
Link in bio → GST calculator (add or remove GST)
Did you guess A, B or C? 👇
Simple arithmetic on an 18% slab; your item's GST rate may differ.
#gst #gstcalculator #gstindia #reversegst #mathtricks #calcsouq

[2026-11-24 16:00]
UAE National Day: 1 day of leave = 5 days off
Private sector paid holiday: Wed 2 and Thu 3 Dec.
Take Friday 4 Dec as leave → off from Wed 2 to Sun 6 Dec.
Link in bio → Date calculator (days between dates, working days)
Where are you spending the long weekend? 👇
For a Monday–Friday job with Sat–Sun off. Holiday dates as announced by MoHRE (13 Nov 2026); check your employer's notice.
#uaenationalday #eidaletihad #uaeholidays #longweekend #dubailife #calcsouq

[2026-11-24 18:00]
(story) UAE National Day: 1 day of leave = 5 days off. Take Fri 4 Dec · off Wed 2 → Sun 6. calcsouq.com

[2026-11-24 19:00]
1 ounce of gold = how many pavan?
Almost 4: 1 troy ounce = 31.10 g ÷ 8 g = 3.9 pavan.
Lightest to heaviest: 1 pavan (sovereign) 8 g · 1 tola 11.66 g · 1 troy ounce 31.10 g.
1 ounce ≈ 2.67 tola.
Link in bio → Gold tola and pavan converter
Do you buy gold in grams, pavan or tola? 👇
The international gold price is quoted per troy ounce, not the everyday 28.35 g ounce.
#gold #goldrate #pavan #tola #keralagold #calcsouq

[2026-11-24 21:30]
100 traders, same coin-flip strategy: how many end up?
In one run of our simulator, 90 finished in profit and 10 lost money, with the same rules.
Best +63%, worst −8%. Someone had 15 losses in a row.
Same edge (+0.2R a trade after costs), different luck.
Link in bio → Trading strategy simulator (1,000 runs, drawdowns, losing streaks)
What's your longest losing streak? 👇
Assumptions: 50% win rate, win 1.5R, lose 1R, risk 1% of balance, costs 0.05R, 100 trades each. Results change every run (89–97 of 100 in profit across 300 repeats). Education only, not investment advice.
#tradingsimulator #riskmanagement #tradingpsychology #forextrading #daytrading #calcsouq
## 2026-11-24 YouTube Shorts → Instagram (made by the daily Shorts agent; slots are Dubai time)
Best of the 3 world-news Shorts (build/yt_shorts_2026_11_24.py, pack build/youtube/2026-11-24-pack.md), posted automatically under Paulson's standing rule (YouTube teasers/shorts post automatically). 21:30 was already taken by the 100-traders reel, so this goes at 22:00.

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 22:00 | reel | no | 4000 | electro | 2026-11-24-nvidia-31pct-day-short.mp4 | /percentage-calculator/ | approved |

```captions
[2026-11-24 22:00]
Can a giant company jump 31% in ONE day? 🚀 Nvidia just did.

Mon 23 Nov: Nvidia shares +31.5% after its board brought back the CEO who had quit less than 2 weeks earlier. The Nasdaq Composite rose 6.51% the same day.
₹1 lakh in a Nasdaq-tracking fund: ₹94,720 after Friday's −5.28%, about ₹1,00,886 after Monday's +6.51%. Big swings go both ways.

Send this to the friend who checks the market every hour 👇
Sources: Saxo, 10 Things, IC Markets, Tickmill market reports, 23–24 Nov 2026. Education only, not investment advice.
#nvidia #nasdaq #stockmarket #aistocks #money #calcsouq
```

## 2026-11-24 emotional story reels (Paulson asked 13:34 Dubai: "posts should go viral … people share and like"). Render: build/reels_2026_11_24_emotion.py

| Date | Slot | Type | Trial | cover_ms | Style | Media | Page | Status |
|---|---|---|---|---|---|---|---|---|
| 2026-11-24 | 13:45 | reel | no | 9000 | cinematic | 2026-11-24-father-shoes.mp4 | / | posted 13:5x Dubai (Paulson asked), media 17928953472199454 |
| 2026-11-24 | 20:30 | reel | no | 9000 | cinematic | 2026-11-24-house-road.mp4 | / | approved |
| 2026-11-25 | 13:00 | reel | no | 10000 | lofi | 2026-11-24-two-friends.mp4 | /sip-calculator/ | approved |

```captions
[2026-11-24 13:45]
Everyone clapped for the degree. Nobody looked at the shoes that paid for it. ❤️

Some people wear old shoes for years so we can walk into rooms they never could.

Tag the person who did this for you. 👇
#father #parents #sacrifice #family #motivation #CalcSouq

[2026-11-24 20:30]
They clapped for the house. They never saw the road. 🏡

The old bike. The packed lunch. The holidays skipped. The small savings, every single month, for years.

Respect the walk, not just the house.
Share this with someone who's walking that road right now. 🙏
#home #dream #savings #hardwork #family #CalcSouq

[2026-11-25 13:00]
Age 25. Same salary. One spent it. One planted it. 🌱

Age 55. Which one are you becoming? Tell us in the comments 👇

₹5,000 a month from 25 to 55 at an assumed 12% a year ≈ ₹1.76 crore. Returns are not guaranteed; try your own numbers: calcsouq.com/sip-calculator
Education only, not investment advice.
#savings #sip #money #future #financialfreedom #CalcSouq
```
