# CalcSouq: working rules for agents

Live site: https://www.calcsouq.com (Vercel project `calcsouq-site`, root directory `site/`, deploys automatically on every push to `main`).
Owner: Paulson Jose (paulznjoz@gmail.com). Contact address on the site: contact@calcsouq.com.

## Build
- Everything in `site/` is generated. Never hand-edit `site/`; edit `build/` and rebuild:
  `python3 build/build.py site`  (settings come from `build/config.json`: url, adsense, slot, gsc)
- Calculators: `build/tools_uae.py`, `build/tools_trading.py`, `build/tools_india.py`, `build/tools_extra.py`, `build/tools_unique.py` (combined "Only on CalcSouq" tools; set `unique=True`, optional `sources=[(name, url)]`), `build/tools_photo.py` (photo resizer + preset landing pages), `build/tools_more.py` (everyday tools: image to PDF, age, percentage, SIP, compound interest, GST, dates, word counter, BMI). Translated pages: `build/i18n.py` (Hindi `hi`, Chinese `zh`, Russian `ru`; Malayalam `ml` lives in `build/ml.py`). To translate a tool, add its English label list to `KEYS` and an entry under the language with name/title/desc/keywords/h1/lede/card/body/faqs/tr. The build prints `<lang> miss:` for any label not found. Worldwide property cost tool: `build/tools_property.py` (country presets; India by state).
- Make tools international: where a rule differs by country, add a country selector (and state/region where it matters) with each rate editable, and default the country from the page language (hi/ml→India, zh→China, ru→Russia) or the visitor's time zone.
- Guides: `build/articles.py` (one `A(...)` call per article; `tool` must be an existing calculator slug)
- Layout, theme, ads, search, share bar: `build/base.py`. Site search index is generated automatically from tools and guides.
- Design: clean product style (Inter, gold #f5c300 used sparingly). Keep copy plain and specific; avoid hype, slogans and generic marketing phrases.
- Topic ideas waiting to be written: `build/backlog.md`

## Content rules
- Positioning: CalcSouq is a general, worldwide site of free calculators and tools. In site-wide text (home, about, footer, descriptions, social posts) do not describe it as a site for expats, NRIs or Gulf/UAE residents, and do not say where it is made. Country-specific tools (UAE gratuity, Kerala land, NRI accounts) may name their country on their own pages.
- Facts that can change (laws, tax rates, fees, contract specs, session times) must be checked against a current source with web search before writing. If unsure, leave it out.
- Original writing only. No copied text, no fake reviews or testimonials, no invented statistics.
- Each guide: clear H1 that matches a real search question, 300–600 words, at least one worked example or table, 2–4 FAQs, links to its calculator.
- British spelling, plain English, short paragraphs.
- Never add content about gambling, adult topics, or anything against Google AdSense policies. Never write "click the ads" or place ads to look like content.
- No personalised investment advice; keep the existing disclaimers.

## Before every push
1. `python3 build/build.py site` must succeed.
2. Every page script must pass `node --check` and every page must load in headless Chrome without console errors or horizontal overflow at 375px.
3. Commit with a clear message and push to `main`.
