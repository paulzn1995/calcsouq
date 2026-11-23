# CalcSouq weekly plan (shared by all scheduled agents)

The Monday strategist rewrites the "This week" section. Other agents take their item, do it, and tick it ([x]) with the page URL in the same commit.

## North star
Become the go-to free tools site: many single-purpose tools, each answering one search exactly, fast, private (processed in the browser), no sign-up.
Revenue: (1) AdSense on every page now; (2) later, a premium tier (ad-free, batch processing, extra limits) once traffic justifies it — owner decision; (3) paid templates on Gumroad.
Priorities when choosing work: search demand × ability to rank (specific long-tail first) × ad value of the topic (finance, tax, loans, insurance, education pay more per view than generic tools) × can be built fully client-side.

## Revenue target (owner, Nov 2026)
Owner goal: USD 10,000–50,000 from the site within 2–4 years. Plan as if it means per year early on and per month as the stretch goal.
Ad income ≈ monthly pageviews ÷ 1,000 × RPM. Working assumption: blended RPM USD 3–8 (lower for India-heavy traffic, higher for US/UK/UAE and for finance, tax and education topics). Record the real RPM from AdSense when available and replace this assumption.

| Milestone | Monthly pageviews | Ad income / month (RPM 3–8) | Add on top |
|---|---|---|---|
| M1 (by mid-2027) | 100k | ~USD 300–800 | AdSense approved, templates on Gumroad |
| M2 (by end-2027) | 500k | ~USD 1.5k–4k | Higher-paying ad network once eligible; direct sponsors on top pages |
| M3 (2028) | 2M | ~USD 6k–16k | "CalcSouq Pro": ad-free, batch PDF/photo, saved results (owner decision) |
| M4 (2029–30) | 5M | ~USD 15k–40k | Pro subscriptions + API/business plans |

## AI-proof rules (search is shifting to AI answers)
- Simple facts and one-line sums get answered by AI and by Google itself. Prioritise tools that DO something people cannot get from an AI answer: process files (PDF, images, signatures), take personal inputs and produce a statement/plan/file, run simulations, or match a specific official format (exam photos, forms).
- At least 70% of new work = interactive tools and their focused landing pages; at most 30% = articles, and articles must support a tool.
- Build return visits: installable app (PWA), tools people reuse (journal, PDF, photo, EMI), clear brand. Grow YouTube/Instagram as a second traffic source.
- Win markets competitors serve badly: regional languages (Malayalam now; Hindi, Arabic and Tamil next), country-specific official formats (exam/visa photos, local taxes), privacy (files never uploaded).
- Every Monday the strategist checks progress against the current milestone and shifts the mix (more high-RPM finance/tax tools if RPM is low; more high-traffic file tools if traffic is low).

## Weekly rhythm
- Mon — Strategist: research demand and competitors, rank backlog, write this week's plan, send owner a short brief (and any decisions only he can make).
- Tue — Tool builder: build tool #1 from this week's plan.
- Wed — SEO & content: focused landing pages for the week's tools, internal links, 1–2 guides, 1 Malayalam page.
- Thu — Tool builder: build tool #2 from this week's plan.
- Fri — QA, fact-check & weekly report (morning); Shorts video for the week's best new page (afternoon).
- 1st of month — Growth kit: accuracy review of changeable facts + share posts.

## This week (week of 23 Nov 2026, set Mon 23 Nov)
Focus: traffic is near zero and search data is not connected, so build file tools that AI answers cannot replace, plus exam-season photo pages. Unit converter moved to the backlog (Google and AI answer conversions directly).
- [ ] Tue tool: QR code generator `/qr-code-generator` — inputs: type (URL, text, Wi-Fi SSID/password/security, WhatsApp number+message, email, phone, UPI-style payment text), size, colours, error-correction level; outputs: live preview, PNG and SVG download; edge cases: text too long for chosen level (show limit), low contrast colours (warn), Wi-Fi special characters escaped (\\ ; , : "), empty input. Encoder written in-page, no external library. Targets "qr code generator free" / "wifi qr code generator". Why: very high, steady worldwide demand; produces a file, so AI answers cannot replace it; reuse visits.
- [ ] Thu tool: Merge PDF `/merge-pdf` (with reorder and page delete) — inputs: several PDFs (drag to reorder, remove pages by thumbnail); output: one PDF download; edge cases: encrypted/password PDFs (clear message, skip), very large files (progress, memory warning on phones), mixed page sizes kept as is, 0 or 1 file. Runs in the browser; a MIT library such as pdf-lib may be self-hosted in `site/assets` (no CDN, no upload). Targets "merge pdf" / "combine pdf files free". Why: one of the largest tool searches; file processing + "files never uploaded" privacy angle; opens the PDF cluster (split, compress) for later weeks.
- [ ] Wed (no Search Console data yet, so no CTR fixes; first job: if GSC is connected by then, re-plan from it): landing pages on existing tools — (1) "JEE Main 2027 photo and signature size" → photo resizer + signature resizer presets (photo JPG 10–200 KB, signature JPG 10–100 KB; re-check on jeemain.nta.nic.in before publishing); (2) "age calculator as on date" (exam eligibility cut-off dates); (3) "step-up SIP calculator" (SIP reels are our best Instagram posts); (4) "JPG to PDF under 1 MB"; (5) "Wi-Fi QR code generator" once Tuesday's tool is live. Malayalam page: loan EMI calculator `/ml/loan-emi-calculator` (supports the new Malayalam EMI video). Guides: "How to calculate percentage of marks" (→ percentage calculator) and "How to make a QR code for your Wi-Fi" (→ QR tool).
- Next Tuesday (1 Dec), planned now because of the 15 Dec advance-tax deadline: India income tax calculator `/income-tax-calculator-india` — inputs: income by head (salary, other), age band, deductions for the old regime; outputs: tax under both regimes side by side, which is lower, monthly TDS, and advance-tax amounts due by 15 Dec (75%) and 15 Mar (100%); edge cases: rebate threshold, marginal relief, senior citizens. Targets "income tax calculator new vs old regime". If a builder has free time this week, start it after Merge PDF.
- [ ] Fri: QA new QR and Merge PDF pages at 375 px (downloads work on Android Chrome and iPhone Safari), fact-check JEE/PSC photo specs and GST rates, weekly report. Video: Short on the step-up SIP calculator ("₹10,000 a month, three choices") — SIP reels have the most Instagram views; English with Malayalam version if time.

## Metrics log
- 2026-11-23 (last 28 days, 26 Oct–22 Nov): Search Console, GA4 and YouTube are NOT connected in Windsor.ai, so no site traffic numbers. Instagram (@calcsouq, first posts 20 Nov): 21 posts, ~2,000 views, 11 followers, 0 shares, 3 saves; no previous period to compare. Best posts: SIP ₹10k/month three choices (141 views), age-30 life in numbers (125), SIP at 25 vs 30 (123); the launch carousel had 10 views. Top pages/queries and low-CTR queries: unknown until GSC is connected. Milestone M1 (100k pageviews/month by mid-2027): progress unmeasurable; treat as ~0. RPM: still the 3–8 USD assumption (no AdSense data).

## Owner decisions made
- 2026-11-23: Paulson approved the India income tax calculator (new vs old regime, FY 2026-27). Slabs, rebate, standard deduction, surcharge and cess must be checked on incometax.gov.in (and the Income Tax Act 2025 rules from 1 Apr 2026) before building; show the source and "checked on" date; every rate editable; no personal tax advice.

## Owner decisions pending
- Premium tier (ad-free + batch) and payments: not before steady traffic; needs Paulson's approval and a check with his employer's outside-business rules.
- Connect Google Search Console, GA4 and YouTube for calcsouq.com in Windsor.ai (only Instagram is connected), so the Monday plan can use real queries and pages.
- Gumroad links for the two templates (send to the agent to switch on the Buy buttons).
