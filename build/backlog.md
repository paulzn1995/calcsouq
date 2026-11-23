# Guide backlog (remove a line once the guide is published)


## Ranked by expected revenue impact (strategist, 23 Nov 2026; re-ranked every Monday)
1. Merge PDF (+ reorder/delete pages) — Thu this week; huge search volume, file tool AI cannot replace.
2. QR code generator (URL, Wi-Fi, WhatsApp, UPI text; PNG/SVG) — Tue this week; high steady demand, makes a file.
3. Compress PDF to a target size (e.g. under 200 KB / 1 MB for forms) — exam and visa portals cap PDF size; pairs with merge PDF.
4. India income tax calculator, new vs old regime FY 2026-27 — APPROVED by owner 23 Nov; scheduled Tue 1 Dec; highest ad value we can build; verify slabs on incometax.gov.in.
5. Exam photo/signature presets: JEE Main, NEET, CUET, SSC, UPSC, IBPS — cheap landing pages on existing resizers; exam season Dec–Mar.
6. Split PDF / extract pages — same library as merge; long-tail "extract pages from pdf".
7. PDF to JPG (page images, in browser) — big volume; needed for portals that only take images.
8. Advance tax / tax instalment planner (India 15 Dec, 15 Mar; UK 31 Jan payment on account) — personal multi-step result, high RPM; verify rules.
9. Malayalam versions of EMI, SIP, age and percentage — regional-language gap; supports Malayalam YouTube. Then Arabic for UAE tools.
10. Loan comparison / prepayment calculator (any currency) — high-RPM loans topic; personal result AI answers handle poorly.
11. Image compressor / convert (JPG↔PNG↔WebP, HEIC to JPG) — high volume file tools, client-side.
12. CGPA to percentage (university-specific formulas) — strong India student demand; must cite each university's rule.
13. Retirement corpus / PPF / NPS calculators — high-RPM finance; personal plan output.
14. Time zone converter / meeting planner — steady global demand; multi-person result beats a one-line AI answer.
15. Unit converter — moved down: Google and AI answers absorb simple conversions; build only as a light hub for internal links.
16. Reel-to-tool prefill links (e.g. /compound-interest-calculator/?daily=100&years=30) — UX: viewers from a reel land on default numbers (₹1 lakh, 5 years) instead of the scenario they just watched; prefilled inputs answer them in one tap. (EOD QA 23 Nov)
17. Hindi state names in the property cost tool's state list (/hi/property-buying-cost-calculator/) — UX: "Tamil Nadu", "Uttar Pradesh" still show in English on the Hindi page. (EOD QA 23 Nov)
18. "Updated · Free · languages" meta line: move the language links into one compact "Also in: हिन्दी · 中文 · Русский" row — UX: on phones it wraps into two ragged lines above the tool. (EOD QA 23 Nov)

## UAE
- Annual leave encashment UAE: how unused leave is paid at end of service
- Notice period rules in UAE (new labour law)
- UAE overtime pay calculation
- How to check MOHRE labour contract and work permit online
- Dubai rent increase calculator rules (RERA index) – check current rules first
- Gold price per tola in Dubai (1 tola = 11.664 g) and tola to gram conversion
- How much gold can you carry from Dubai to India (customs allowance) – verify current CBIC rules
- UAE corporate tax basics for freelancers – verify current FTA rules
- DEWS savings scheme vs gratuity (DIFC)
- Emirates ID and visa renewal costs – only if an official current source exists

## Trading
- Pip value for USD/JPY explained with examples
- Leverage explained: 1:30 vs 1:100 vs 1:500 risk
- Spread and commission: true cost of a forex trade
- Stop loss vs take profit: risk–reward ratio
- Crude oil (CL) vs Brent CFD contract sizes
- Nasdaq (NQ/US100) lot size and point value on CFDs
- Gold lot size for beginners: 0.01 vs 0.1 vs 1 lot
- How to read an MT5 symbol specification
- What is slippage and when it happens
- Islamic (swap-free) accounts explained

## India / Kerala / NRI
- NRI tax on Indian rental income (TDS) – verify current rates
- Cents to ares to hectares quick table for village records
- Kerala fair value: how to check online
- Kerala building permit fee basics – verify
- Gold price per pavan (8 grams) Kerala, pavan to gram
- How to send money to India tax-free limits (NRI) – verify
- FCNR vs NRE fixed deposit
- GIFT Nifty vs Nifty futures: differences

## New calculator ideas (needs owner approval before building)
- UAE overtime pay calculator
- Dubai rent increase calculator (RERA index rules – verify current rules)
- NRI income tax estimator on Indian rent/interest (verify current slabs)
- Compound interest / SIP calculator (AED and ₹)

## High-demand tools to add next (need owner OK for anything with tax rules)
- Income tax calculator India (new vs old regime) — approved 23 Nov; rules change every Budget; verify on incometax.gov.in first
- QR code generator (needs a QR encoder written in-page)
- Unit converter (length, weight, temperature, area)
- CGPA to percentage converter (university-specific formulas)
- Compress PDF / merge PDF
- Mortgage calculator (generic, any currency) and loan comparison
- Retirement corpus calculator, PPF calculator, NPS calculator
- Time zone converter

## UX ideas from the end-of-day QA (22 Nov 2026)
- Malayalam gold price calculator opens on UAE (AED 320/g); AGENTS.md says ml→India. Default it to India with a verified current Kerala 22K gram rate (needs a fresh rate check, so not done in QA).
- Search aliases: add a short `a` (aliases) field to search-index entries ("20kb" → resize-photo-to-20kb, "housing loan" → mortgage/EMI) so exact-intent pages rank above the generic tool.
- Home hero on phones: the 6-line lede still pushes the search box to ~620 px; a one-sentence phone lede would put search inside the first 500 px.
