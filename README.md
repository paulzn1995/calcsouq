# CalcSouq: free calculators for UAE & India

A static site with 11 calculators, a GIFT Nifty page and the pages AdSense needs, built for Vercel.

## Pages
- UAE: `/uae-gratuity-calculator/`, `/uae-vat-calculator/`, `/gold-price-calculator/`, `/aed-to-inr-calculator/`
- Trading: `/forex-pip-value-calculator/`, `/position-size-calculator/`, `/forex-margin-calculator/`, `/swap-calculator/`, `/futures-tick-value-calculator/`, `/market-hours/`
- India: `/kerala-land-converter/`, `/kerala-stamp-duty-calculator/`
- `/gift-nifty/`: delayed GIFT Nifty page. It shows sample data until `api/quote.js` is given a licensed vendor feed.
- `/about/`, `/privacy/` (includes the AdSense cookie wording), `/terms/`, `/contact/`, `404.html`

## Search engine work already done
- Every page has a keyword-led `<title>`, a meta description, keywords, a canonical URL, Open Graph tags and an H1.
- Structured data: WebApplication, FAQPage (eligible for FAQ rich results) and BreadcrumbList on every tool, plus WebSite on the home page.
- Each tool has a 300–500 word explainer, a worked example, FAQs and related-tool links for internal linking.
- `sitemap.xml`, `robots.txt`, fast static pages and a mobile-first layout.

## Go live
1. **Domain:** buy one (calcsouq.com).
2. **Rebuild with your domain and AdSense ID.** Send both to Claude, or run:
   `python3 build/build.py site https://www.calcsouq.com ca-pub-XXXXXXXXXXXXXXXX GSC_CODE`
   This bakes the domain into canonical URLs and the sitemap, adds the AdSense code to every page, fills `ads.txt` and hides the grey placeholders.
3. **GitHub:** create an empty repo and push the site folder.
4. **Vercel:** Add New, then Project, then import the repo. Set **Root Directory** to `site`, then Deploy and add your domain.
5. **Google Search Console:** add the domain, verify it, then submit `https://yourdomain/sitemap.xml`. Without this, Google can take weeks to find the site.
6. **AdSense:** apply at adsense.google.com with the live domain. The site uses **Auto ads**, so once you're approved, Google places the ads; no slot IDs are needed.
7. **Payout:** AdSense pays UAE publishers by EFT or wire to a UAE bank account. PayPal (Hyperwallet) is not offered in the UAE.
