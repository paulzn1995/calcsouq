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
- 2026-11-22 (Paulson, standing rule): reels were too fast to read. READING PACE for every reel: 18–25 s total; every line of text and every number stays fully visible for at least 3 s after it finishes animating in; no more than 2 new text items per beat; slower entrances (about 0.6 s); the reveal number holds 3–4 s; end card holds 4 s. Simple way: write the scene timings as before, then multiply time by SLOW = 1.75 (see build/reel_fed_hike.py) and scale the audio cues by the same factor.
- 2026-11-21 Paulson: prefers broad, intriguing content built on the site's complex calculations (quiz/guess formats, simulations) over single-tool demos.
- 2026-11-21 data (last 3 days): lowest skip (48%) and longest watch (5.4 s) = EMI reel with one concrete money question on frame 1; A/B/C quiz and long-text hooks were skipped 73–81%. Lead with a big number + question, show options after ~1 s, reveal by 9 s.
- 2026-11-21 Trial Reels are refused by Instagram: account has too few followers. Post every reel as a normal reel until followers grow; retry trial once a week (if refused, post the same reel normally).

- 2026-11-21 Paulson: wants reels with viral potential built on the latest news or rule changes, including international/global stories (markets, crypto, gold, oil, Fed) as well as UAE/India money, visas, tax and rupee,, packed with facts most people don't know; cite the source/date in the caption and verify every figure before queueing.

| 2026-11-21 | Reel | F&O margin calculator: futures, calendar spread, iron condor vs strangle, lot sizes | build/static/media/ig/2026-11-21-margin-calculator.mp4 | posted 2026-11-21, media 18143848828618251 |

## Topic calendar
Milestone/meme posts: 0 → 1 follower 'Yipeee' reel (21 Nov).
Used so far (avoid repeating within 2 weeks): SIP flat vs step-up, 1,000 traders, EMI 10 vs 20 years, F&O margin, UAE final settlement (20–21 Nov); gold making + GST, Dubai property fees, life in numbers at 30, SIP at 25 vs 30, ₹1 crore savings planner (21 Nov).
Ideas next: FD vs SIP, GST slabs, gratuity 21 vs 30 days, position sizing, compound interest doubling, BMI, working days to deadline.

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
| 2026-11-22 | 10:30 | reel | no | 1000 | electro | 2026-11-21-bitcoin-half-off.mp4 | /percentage-calculator/ | approved (Paulson 21 Nov 12:33) |
| 2026-11-22 | 14:30 | reel | no | 1000 | desi | 2026-11-21-gold-off-record.mp4 | /gold-price-calculator/ | approved (Paulson 21 Nov 12:33, with fixes: video re-rendered with verified $3,715 on 19 Nov) |

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
