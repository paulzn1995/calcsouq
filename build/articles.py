# Guide articles. Each links to a calculator via "tool" (slug).
ARTICLES = []

def A(**k):
    ARTICLES.append(k)

def grat(b, y):
    return min(b / 30 * (21 * min(y, 5) + 30 * max(y - 5, 0)), b * 24)

rows = "".join(f"<tr><td>{y} year{'s' if y > 1 else ''}</td>" + "".join(f'<td class="n">AED {grat(b, y):,.0f}</td>' for b in (5000, 10000, 15000)) + "</tr>" for y in (1, 2, 3, 4, 5, 6, 7, 8, 10, 15, 20))
GRAT_TABLE = f'<div class="scroll"><table><thead><tr><th>Service</th><th class="n">Basic AED 5,000</th><th class="n">Basic AED 10,000</th><th class="n">Basic AED 15,000</th></tr></thead><tbody>{rows}</tbody></table></div>'

# ---------------- UAE ----------------
A(group="uae", slug="gratuity-after-5-years-uae", tool="uae-gratuity-calculator",
  title="Gratuity After 5 Years in UAE (2026): How Much You Get, With Table",
  h1="How much gratuity do you get after 5 years in the UAE?",
  desc="Gratuity after 1, 3, 5, 7, 10 and 20 years in the UAE, with a ready table for AED 5,000, 10,000 and 15,000 basic salaries under the new labour law.",
  keywords="gratuity after 5 years uae, gratuity after 10 years uae, gratuity after 3 years uae, how much gratuity uae, gratuity table uae, end of service after 7 years dubai",
  lede="Five years is the point where the UAE gratuity rate jumps from 21 to 30 days of basic salary a year. Here is what that means in dirhams.",
  body=f"""
<h2>The short answer</h2>
<p>After exactly five years you receive <strong>105 days of basic salary</strong> (21 days × 5 years). From year six onwards, every extra year adds <strong>30 days</strong>. The total is capped at two years' basic salary.</p>
<h2>Gratuity table by years of service</h2>
{GRAT_TABLE}
<p class="hint">Daily wage = basic salary ÷ 30. Amounts rounded to the nearest dirham. Part years are paid pro rata.</p>
<h2>Why year six matters</h2>
<p>Staying a sixth year earns you 30 days' pay for that year instead of 21, which is about 43% more per year. If you are deciding when to leave, finishing year five and then working part of year six both raise your payout.</p>
<h2>When you hit the cap</h2>
<p>Because the total cannot exceed 24 months of basic salary, the cap of 720 days' basic pay is reached after about 25½ years of service (105 days for the first 5 years plus 30 days for each later year).</p>
""",
  faqs=[("How much gratuity is paid after 5 years in UAE?", "105 days of basic salary: 21 days for each of the 5 years. With AED 10,000 basic, that is AED 35,000."),
        ("How much gratuity after 10 years in UAE?", "105 days for the first 5 years plus 150 days for the next 5, a total of 255 days of basic pay. With AED 10,000 basic, that is AED 85,000."),
        ("Is gratuity paid for part of a year?", "Yes. Once you complete one year, extra months and days are paid pro rata.")])

A(group="uae", slug="gratuity-after-resignation-uae", tool="uae-gratuity-calculator",
  title="Gratuity After Resignation in UAE: Do You Lose Any? (New Labour Law)",
  h1="Do you get full gratuity if you resign in the UAE?",
  desc="Under the new UAE labour law you get full gratuity whether you resign or are terminated. What changed from the old law, notice periods and when gratuity must be paid.",
  keywords="gratuity after resignation uae, resignation gratuity new labour law, gratuity if i resign dubai, gratuity unlimited contract resignation, gratuity reduction resignation uae",
  lede="Under the old law, resigning early could cut your gratuity by a third or two thirds. That rule is gone.",
  body="""
<h2>The rule today</h2>
<p>Under Federal Decree-Law No. 33 of 2021, private-sector employees receive the <strong>same gratuity whether they resign or are terminated</strong>: 21 days' basic pay per year for the first five years and 30 days per year after that, provided they completed at least one year of service.</p>
<h2>What the old law did</h2>
<p>On the old unlimited contracts, resigning after 1–3 years earned only one third of the gratuity, and 3–5 years earned two thirds. Those reductions do not appear in the new law.</p>
<h2>Dismissal without notice</h2>
<p>The new law also changed summary dismissal. Under Article 44 an employer can dismiss without notice in ten specific cases, but the end-of-service gratuity is still payable. Under the old Article 120 it could be forfeited. Your employer may deduct amounts you genuinely owe.</p>
<h2>What you still need to do</h2>
<ul><li>Serve the notice period in your contract, between 30 and 90 days.</li><li>Your employer must pay all dues within 14 days of the end of the contract.</li><li>Keep your offer letter and payslips showing your basic salary.</li></ul>
<p>If dues are not paid, you can file a complaint with MOHRE through its app or website.</p>
""",
  faqs=[("Is gratuity reduced if I resign in UAE?", "No. Under the new labour law there is no reduction for resigning."),
        ("Do I get gratuity if I am fired without notice?", "Yes. Under the new law, gratuity is payable even after a dismissal under Article 44, though proven amounts owed to the employer can be deducted."),
        ("How long does the employer have to pay gratuity?", "All end-of-service dues must be paid within 14 days of the end of the employment contract.")])

A(group="uae", slug="gratuity-basic-or-gross-salary", tool="uae-gratuity-calculator",
  title="Is UAE Gratuity Calculated on Basic or Gross Salary?",
  h1="Is gratuity calculated on basic or gross salary?",
  desc="UAE gratuity is calculated on your last basic salary, not your gross package. See how much the split between basic and allowances changes your payout.",
  keywords="gratuity basic salary uae, gratuity gross salary, gratuity calculated on basic or total salary, basic salary percentage uae, housing allowance gratuity",
  lede="Your gratuity is calculated on your last basic salary only. Housing, transport and other allowances don't count.",
  body="""
<h2>Why it matters</h2>
<p>Many UAE packages put only 50–60% of total pay into basic salary. Two people with the same total pay can therefore get very different gratuity.</p>
<div class="scroll"><table><thead><tr><th>Total package</th><th class="n">Basic</th><th class="n">Gratuity after 5 years</th></tr></thead><tbody>
<tr><td>AED 15,000 (basic 50%)</td><td class="n">AED 7,500</td><td class="n">AED 26,250</td></tr>
<tr><td>AED 15,000 (basic 60%)</td><td class="n">AED 9,000</td><td class="n">AED 31,500</td></tr>
<tr><td>AED 15,000 (basic 100%)</td><td class="n">AED 15,000</td><td class="n">AED 52,500</td></tr></tbody></table></div>
<h2>What counts as basic</h2>
<p>Basic salary is the figure stated as "basic" in your contract and MOHRE offer letter. Commission, overtime and allowances are excluded unless the contract says otherwise.</p>
<h2>Tip when negotiating</h2>
<p>When you compare job offers, look at the basic salary as well as the total. A higher basic raises your gratuity and often your leave encashment.</p>
""",
  faqs=[("Does housing allowance count for gratuity?", "No. Gratuity is calculated on the last basic salary only, unless your contract explicitly includes allowances."),
        ("Which salary is used, first or last?", "Your last basic salary at the end of employment.")])

A(group="uae", slug="how-to-calculate-vat-uae", tool="uae-vat-calculator",
  title="How to Calculate 5% VAT in UAE: Add, Remove and Reverse VAT (Examples)",
  h1="How to calculate 5% VAT in the UAE",
  desc="Simple formulas to add 5% VAT, remove VAT from a total, and avoid the most common mistake. Worked AED examples for invoices and receipts.",
  keywords="how to calculate vat in uae, 5 percent vat formula, remove vat from total uae, reverse vat calculation, vat inclusive price formula, vat on invoice uae",
  lede="Two formulas cover almost every VAT sum in the UAE.",
  body="""
<h2>Adding VAT</h2>
<p><strong>Total = net price × 1.05</strong><br>AED 2,400 × 1.05 = AED 2,520, of which VAT is AED 120.</p>
<h2>Removing VAT from a total</h2>
<p><strong>Net price = total ÷ 1.05</strong><br>AED 2,520 ÷ 1.05 = AED 2,400. VAT = 2,520 − 2,400 = AED 120.</p>
<p>A quick shortcut: the VAT inside a VAT-inclusive price is <strong>total × 5 ÷ 105</strong>, or about 4.76% of the total.</p>
<h2>The common mistake</h2>
<p>Taking 5% off the total (2,520 × 0.95 = 2,394) gives the wrong answer. VAT was added to the net price, so you must divide by 1.05, not subtract 5%.</p>
<h2>Quick reference</h2>
<div class="scroll"><table><thead><tr><th>Net</th><th class="n">VAT 5%</th><th class="n">Total</th></tr></thead><tbody>
""" + "".join(f'<tr><td>AED {n:,}</td><td class="n">AED {n*0.05:,.2f}</td><td class="n">AED {n*1.05:,.2f}</td></tr>' for n in (100, 500, 1000, 5000, 10000, 50000)) + """</tbody></table></div>
""",
  faqs=[("What is 5% VAT on AED 1,000?", "AED 50, making the total AED 1,050."),
        ("How do I find the VAT in a VAT-inclusive price?", "Multiply the total by 5 and divide by 105. For AED 1,050 that is AED 50.")])

A(group="uae", slug="22k-vs-24k-gold", tool="gold-price-calculator",
  title="22K vs 24K vs 21K vs 18K Gold: Purity, Price and Which to Buy in Dubai",
  h1="22K vs 24K gold: what's the difference?",
  desc="Purity, price per gram and best uses for 24K, 22K, 21K and 18K gold. What Dubai and Kerala buyers should choose for jewellery, coins and investment.",
  keywords="22k vs 24k gold, 21k gold dubai, 18k vs 22k gold, gold purity karat, which gold is best for investment, 916 gold meaning, gold karat chart",
  lede="Karat measures how much of a piece is pure gold. More karats means purer, softer and more expensive gold.",
  body="""
<div class="scroll"><table><thead><tr><th>Karat</th><th class="n">Gold content</th><th>Typical use</th></tr></thead><tbody>
<tr><td>24K</td><td class="n">99.9%</td><td>Coins, bars, investment</td></tr>
<tr><td>22K (916)</td><td class="n">91.6%</td><td>Indian and Kerala jewellery</td></tr>
<tr><td>21K</td><td class="n">87.5%</td><td>Gulf and Arabic jewellery</td></tr>
<tr><td>18K (750)</td><td class="n">75%</td><td>Diamond and stone-set jewellery</td></tr></tbody></table></div>
<h2>Which should you buy?</h2>
<ul><li><strong>For investment:</strong> 24K coins or bars. Making charges are low, and in the UAE investment gold of 99% purity or more is zero-rated for VAT.</li>
<li><strong>For traditional jewellery:</strong> 22K is the Indian standard and holds value well, but it is soft.</li>
<li><strong>For everyday wear or stones:</strong> 18K is harder and holds settings securely, but less of what you pay for is gold.</li></ul>
<h2>Converting rates between karats</h2>
<p>Multiply the 24K rate by the purity. If 24K is AED 340 a gram, 22K is about 340 × 0.916 = AED 311. Published shop rates may differ slightly.</p>
<h2>What "916" means</h2>
<p>916 is the hallmark for 22K: 916 parts pure gold per 1,000. In India, look for the BIS hallmark with a 6-digit HUID code.</p>
""",
  faqs=[("Is 22K or 24K better for jewellery?", "22K. 24K is too soft for most jewellery and bends and scratches easily."),
        ("What does 916 gold mean?", "It means 91.6% pure gold, the same as 22 karat.")])

A(group="uae", slug="gold-making-charges-explained", tool="gold-price-calculator",
  title="Gold Making Charges Explained: Dubai vs India, VAT/GST and How to Negotiate",
  h1="Gold making charges explained",
  desc="What jewellery making charges are, typical ranges, how VAT and GST apply to them in the UAE and India, and how to bring them down.",
  keywords="gold making charges, making charges dubai, making charges kerala, how to negotiate making charges, vat on making charges uae, gst on gold making charges",
  lede="The making charge is often the biggest negotiable part of a jewellery bill.",
  body="""
<h2>What is a making charge?</h2>
<p>It is the jeweller's fee for designing and crafting the piece, on top of the gold value. It is quoted as a <strong>percentage of the gold value</strong> or as a <strong>fixed amount per gram</strong>.</p>
<h2>Typical ranges</h2>
<ul><li>Plain chains and bangles: low, often a few percent or a small amount per gram.</li><li>Machine-made designs: moderate.</li><li>Handcrafted, antique or temple designs: highest, sometimes 20% or more.</li></ul>
<h2>Tax on making charges</h2>
<p><strong>UAE:</strong> 5% VAT is charged on the full price, gold value plus making charge. Tourists can reclaim it on departure.<br><strong>India:</strong> 3% GST is charged on the jewellery value including making charges.</p>
<h2>How to pay less</h2>
<ul><li>Ask for the making charge as a separate line, then compare two or three shops.</li><li>Choose simpler designs for investment-type purchases.</li><li>Watch for festival offers (Akshaya Tritiya, Dhanteras, Dubai Shopping Festival) that discount making charges.</li><li>Check the exchange or buyback terms, because making charges are usually not refunded when you sell.</li></ul>
""",
  faqs=[("Is VAT charged on making charges in Dubai?", "Yes. 5% VAT is charged on the full retail price, including making charges."),
        ("Are making charges refunded when selling gold?", "Usually not. Jewellers generally pay only for the gold content, often minus a deduction.")])

A(group="uae", slug="compare-remittance-aed-to-inr", tool="aed-to-inr-calculator",
  title="Sending Money from UAE to India: How to Compare Exchange Rates and Fees",
  h1="How to get the most rupees when sending money from the UAE",
  desc="Why the best exchange rate isn't always the best deal. How to compare exchange houses and apps using the effective rate, with AED to INR examples.",
  keywords="best way to send money uae to india, aed to inr best rate, exchange house vs app uae, remittance fees uae, effective exchange rate, send money kerala from dubai",
  lede="Compare providers on how many rupees arrive in India, not on the headline rate.",
  body="""
<h2>Two costs, not one</h2>
<p>Every transfer has an <strong>exchange-rate margin</strong> (the difference from the market rate) and usually a <strong>fixed fee</strong>. A provider can advertise "zero fee" and still be expensive through a weaker rate.</p>
<h2>The effective rate</h2>
<p><strong>Effective rate = rupees received ÷ total dirhams paid (amount + fee)</strong></p>
<p>Example: sending AED 2,000.<br>Provider A: rate 24.10, fee AED 22 → ₹48,200 for AED 2,022 → effective 23.84.<br>Provider B: rate 24.00, fee 0 → ₹48,000 for AED 2,000 → effective 24.00.<br>Provider B wins even though its headline rate is lower.</p>
<h2>Tips</h2>
<ul><li>Send fewer, larger transfers so the fixed fee matters less.</li><li>Compare at the same time of day, because rates change through the day.</li><li>Use an NRE account if you may want to move the money back out of India.</li></ul>
""",
  faqs=[("What is the cheapest way to send money from UAE to India?", "Whichever provider gives the highest effective rate for your amount on the day. Compare by rupees received, not the advertised rate."),
        ("Do zero-fee transfers cost nothing?", "Not necessarily. The cost is often built into a weaker exchange rate.")])

A(group="india", slug="nre-vs-nro-account", tool="aed-to-inr-calculator",
  title="NRE vs NRO Account: Differences, Tax and Which One Gulf NRIs Should Use",
  h1="NRE vs NRO account: which should you use?",
  desc="NRE vs NRO explained for NRIs in the UAE: repatriation, tax on interest, joint holders and which account to send your salary to.",
  keywords="nre vs nro account, nre account meaning, nro account tax, nri account for uae salary, nre interest tax free, nro repatriation limit",
  lede="Both are Indian bank accounts for NRIs. The difference is where the money comes from and whether it can go back out.",
  body="""
<div class="scroll"><table class="stack"><thead><tr><th>Feature</th><th>NRE</th><th>NRO</th></tr></thead><tbody>
<tr><td>Money that goes in</td><td>Foreign earnings sent from abroad</td><td>Income earned in India (rent, dividends, pension), plus foreign money</td></tr>
<tr><td>Currency</td><td>Held in rupees</td><td>Held in rupees</td></tr>
<tr><td>Repatriation</td><td>Fully repatriable, principal and interest</td><td>Limited: up to USD 1 million per financial year, with paperwork</td></tr>
<tr><td>Tax on interest in India</td><td>Tax-free</td><td>Taxable, with TDS deducted</td></tr>
<tr><td>Joint holder</td><td>Another NRI</td><td>A resident Indian can be a joint holder</td></tr></tbody></table></div>
<h2>Which to use</h2>
<ul><li>Send your <strong>UAE salary to an NRE account</strong>: the interest is tax-free in India and the money can always go back out.</li>
<li>Use an <strong>NRO account</strong> for income that arises in India, such as rent from your Kerala house.</li></ul>
<p>Rules and tax treatment can change, and the UAE has no personal income tax. Check with your bank or a chartered accountant for your situation.</p>
""",
  faqs=[("Is NRE interest taxable in India?", "No. Interest on NRE deposits is exempt from Indian income tax while you remain an NRI."),
        ("Can I deposit rent from India into an NRE account?", "No. Indian income such as rent must go into an NRO account.")])

# ---------------- Trading ----------------
A(group="trading", slug="what-is-a-pip-forex", tool="forex-pip-value-calculator",
  title="What Is a Pip in Forex? Pip Size, Pip Value and Examples",
  h1="What is a pip in forex?",
  desc="A pip is the standard unit of price movement in forex. Pip size for EUR/USD, JPY pairs and gold, and how to work out what one pip is worth.",
  keywords="what is a pip, pip meaning forex, pip size, pipette, pip in jpy pairs, how much is a pip worth, pip vs point",
  lede="A pip is the unit traders use to measure price moves. For most pairs it is the fourth decimal place.",
  body="""
<h2>Pip size</h2>
<ul><li>Most pairs (EUR/USD, GBP/USD, AUD/USD): <strong>1 pip = 0.0001</strong>. EUR/USD moving from 1.0850 to 1.0875 is 25 pips.</li>
<li>JPY pairs (USD/JPY, GBP/JPY): <strong>1 pip = 0.01</strong>.</li>
<li>Many brokers quote one more digit, called a <strong>pipette</strong> or point, which is a tenth of a pip.</li></ul>
<h2>Pip value</h2>
<p><strong>Pip value = pip size × position size</strong>, in the quote currency.</p>
<div class="scroll"><table><thead><tr><th>Lot</th><th class="n">Units</th><th class="n">EUR/USD pip value</th></tr></thead><tbody>
<tr><td>Standard (1.00)</td><td class="n">100,000</td><td class="n">$10.00</td></tr>
<tr><td>Mini (0.10)</td><td class="n">10,000</td><td class="n">$1.00</td></tr>
<tr><td>Micro (0.01)</td><td class="n">1,000</td><td class="n">$0.10</td></tr></tbody></table></div>
<p>For a USD-based account, any pair ending in USD has a $10-per-lot pip. For other pairs the value changes with the exchange rate.</p>
""",
  faqs=[("How much is 1 pip in dollars?", "On EUR/USD, $10 per standard lot, $1 per mini lot and $0.10 per micro lot."),
        ("What is the difference between a pip and a point?", "On MT4/MT5 a point is usually the last quoted digit, so 10 points equal 1 pip on most forex pairs.")])

A(group="trading", slug="gold-pip-value-xauusd", tool="forex-pip-value-calculator",
  title="XAU/USD Pip Value: How Much Is 1 Pip in Gold per Lot?",
  h1="How much is 1 pip in gold (XAU/USD)?",
  desc="Gold pip value explained: $0.01, $0.10 and $1 moves on XAU/USD per standard, mini and micro lot, and why brokers define a gold pip differently.",
  keywords="gold pip value, xauusd pip value, how much is 1 pip in gold, gold lot size, 1 lot gold profit per dollar, xauusd points to pips",
  lede="One standard lot of gold is usually 100 troy ounces, so every $1 move in price is worth $100 per lot.",
  body="""
<h2>Gold moves in dollars per ounce</h2>
<div class="scroll"><table><thead><tr><th>Price move</th><th class="n">1.00 lot (100 oz)</th><th class="n">0.10 lot</th><th class="n">0.01 lot</th></tr></thead><tbody>
<tr><td>$0.01</td><td class="n">$1</td><td class="n">$0.10</td><td class="n">$0.01</td></tr>
<tr><td>$0.10</td><td class="n">$10</td><td class="n">$1</td><td class="n">$0.10</td></tr>
<tr><td>$1.00</td><td class="n">$100</td><td class="n">$10</td><td class="n">$1</td></tr>
<tr><td>$10.00</td><td class="n">$1,000</td><td class="n">$100</td><td class="n">$10</td></tr></tbody></table></div>
<h2>Why "pip" is confusing for gold</h2>
<p>Brokers define a gold pip differently: some use $0.01, many use $0.10, and some traders call $1 a pip. Rather than relying on the word, check the <strong>contract size</strong> and <strong>tick size</strong> in MT5 (right-click the symbol, then Specification).</p>
<h2>Risk example</h2>
<p>With a $1,000 account and 1% risk ($10), a $5 stop on gold allows 10 ÷ (5 × 100) = <strong>0.02 lots</strong>.</p>
""",
  faqs=[("How much is a $1 move in gold per lot?", "$100 per standard lot of 100 oz."),
        ("What lot size should I use for gold with $1,000?", "With 1% risk and a $5 stop, about 0.02 lots. Use the position size calculator for your exact numbers.")])

A(group="trading", slug="lot-size-explained", tool="position-size-calculator",
  title="Standard, Mini and Micro Lots Explained: Forex Lot Sizes for Beginners",
  h1="Forex lot sizes explained",
  desc="What a standard, mini, micro and nano lot is, how many units each contains, pip value per lot, and how to choose your lot size.",
  keywords="lot size forex, standard lot mini lot micro lot, what is 0.01 lot, how much is 1 lot in forex, lot size meaning mt5",
  lede="A lot is the trade size. On MT4 and MT5 you type it as a decimal: 1.00, 0.10 or 0.01.",
  body="""
<div class="scroll"><table><thead><tr><th>Name</th><th class="n">MT5 size</th><th class="n">Units</th><th class="n">EUR/USD pip</th></tr></thead><tbody>
<tr><td>Standard</td><td class="n">1.00</td><td class="n">100,000</td><td class="n">$10</td></tr>
<tr><td>Mini</td><td class="n">0.10</td><td class="n">10,000</td><td class="n">$1</td></tr>
<tr><td>Micro</td><td class="n">0.01</td><td class="n">1,000</td><td class="n">$0.10</td></tr></tbody></table></div>
<h2>How to choose a lot size</h2>
<p>Don't choose a lot size first. Decide <strong>how much you are willing to lose</strong> (for example 1% of the account) and <strong>where your stop loss goes</strong>, then work out the lot size:</p>
<p><strong>Lots = risk amount ÷ (stop in pips × pip value per lot)</strong></p>
<p>Example: $5,000 account, 1% risk = $50, 20-pip stop on EUR/USD → 50 ÷ (20 × 10) = 0.25 lots.</p>
<h2>Lots on other products</h2>
<p>CFDs on indices, oil and gold have their own contract sizes (gold is usually 100 oz per lot). Always check the symbol specification before trading.</p>
""",
  faqs=[("What is 0.01 lot?", "A micro lot: 1,000 units of the base currency, worth about $0.10 per pip on EUR/USD."),
        ("How much money do I need for 1 lot?", "That depends on leverage. At 1:100, one lot of EUR/USD needs about 1% of its value, around $1,085 at 1.0850.")])

A(group="trading", slug="1-percent-risk-rule", tool="position-size-calculator",
  title="The 1% Risk Rule in Trading: How It Works and Why It Matters",
  h1="The 1% risk rule",
  desc="Why many traders risk only 1% of their account per trade, how drawdowns grow at higher risk, and how to size positions to stick to it.",
  keywords="1 percent rule trading, risk per trade, how much to risk per trade, risk management forex, drawdown losing streak, money management trading",
  lede="The 1% rule says a single losing trade should cost no more than 1% of your account.",
  body="""
<h2>Why it works</h2>
<p>Every strategy has losing streaks. Small risk per trade means a streak hurts but doesn't end your trading.</p>
<div class="scroll"><table><thead><tr><th>Losses in a row</th><th class="n">1% risk</th><th class="n">2% risk</th><th class="n">5% risk</th><th class="n">10% risk</th></tr></thead><tbody>
""" + "".join(f'<tr><td>{n}</td>' + "".join(f'<td class="n">−{(1-(1-r)**n)*100:.0f}%</td>' for r in (0.01, 0.02, 0.05, 0.10)) + "</tr>" for n in (5, 10, 15, 20)) + """</tbody></table></div>
<p>After 10 straight losses, a 1% trader is down about 10%; a 10% trader has lost about two thirds of the account and needs nearly a 200% gain just to get back to the start.</p>
<h2>Applying it</h2>
<ol><li>Risk amount = account × 1%.</li><li>Place your stop where the trade idea is proven wrong.</li><li>Lot size = risk amount ÷ (stop distance × value per pip or point).</li></ol>
<p>Spreads, commission and slippage can make actual losses slightly larger, so some traders use 0.5–1%.</p>
""",
  faqs=[("Is 2% risk per trade too much?", "Many professionals use 0.5–2%. At 2%, ten straight losses cost about 18% of the account."),
        ("Does the 1% rule mean a 1% stop loss?", "No. It limits the money lost, not the price distance. The stop distance decides the position size.")])

A(group="trading", slug="margin-level-margin-call", tool="forex-margin-calculator",
  title="Margin, Free Margin, Margin Level and Stop Out Explained (MT5)",
  h1="Margin level, margin call and stop out explained",
  desc="How used margin, free margin and margin level work in MT4/MT5, what triggers a margin call and a stop out, with a worked example.",
  keywords="margin level explained, margin call forex, stop out level, free margin meaning, used margin mt5, equity margin level formula",
  lede="Four numbers in your MT5 terminal decide whether your positions stay open.",
  body="""
<ul><li><strong>Balance:</strong> account cash, excluding open trades.</li>
<li><strong>Equity:</strong> balance plus or minus open profit and loss.</li>
<li><strong>Margin (used):</strong> the deposit locked by open positions.</li>
<li><strong>Free margin:</strong> equity − used margin, the amount available for new trades.</li>
<li><strong>Margin level:</strong> equity ÷ used margin × 100%.</li></ul>
<h2>Worked example</h2>
<p>Balance $2,000. You open 1 lot of EUR/USD at 1.0850 with 1:100 leverage, so used margin is $1,085. If the trade is down $600, equity is $1,400 and margin level = 1,400 ÷ 1,085 = <strong>129%</strong>.</p>
<p>If the loss grows to $1,500, equity is $500 and margin level is 46%. With a 50% stop-out level, the broker starts closing positions.</p>
<h2>Margin call vs stop out</h2>
<p>A <strong>margin call</strong> is a warning level (often 100%). The <strong>stop out</strong> is where positions are closed automatically, largest loser first. Both levels are set by your broker.</p>
""",
  faqs=[("What is a good margin level?", "Many traders try to stay well above 300–500% so normal price swings never approach the stop-out level."),
        ("What happens at stop out?", "The broker automatically closes positions, usually the biggest loser first, until the margin level is back above the limit.")])

A(group="trading", slug="triple-swap-wednesday", tool="swap-calculator",
  title="Why Is Swap Charged 3 Times on Wednesday? Triple Swap Explained",
  h1="Why is there a triple swap on Wednesday?",
  desc="Forex rollover settles T+2, so Wednesday's rollover covers the weekend. Why indices and CFDs often charge triple swap on Friday instead, with examples.",
  keywords="triple swap wednesday, why swap is triple on wednesday, rollover forex, swap fee mt5, swap friday indices, overnight financing",
  lede="Hold a forex position past Wednesday's rollover and you pay (or earn) three days of swap at once.",
  body="""
<h2>The reason: T+2 settlement</h2>
<p>Spot forex settles two business days after the trade date. A position held over Wednesday's 5 pm New York rollover moves its value date from Friday to Monday, which covers Saturday and Sunday. So three days of interest are applied at once.</p>
<h2>Indices and CFDs</h2>
<p>Many index, commodity and stock CFDs charge the triple financing on <strong>Friday</strong> instead, because they don't follow forex settlement. Check your broker's specification.</p>
<h2>Example</h2>
<p>Swap long on a pair is −$7.50 per lot per night. Holding 2 lots from Monday to the following Monday: 5 rollovers, one of them triple → 7 nights × 2 lots × −7.50 = <strong>−$105</strong>.</p>
<h2>Positive swap</h2>
<p>If you hold the higher-interest currency, swap can be a credit, and Wednesday then pays you three times.</p>
""",
  faqs=[("What time is the forex rollover?", "Usually 5 pm New York time, which is 2 am in the UAE in winter and 1 am during US daylight saving time."),
        ("Do swap-free accounts pay triple swap?", "Islamic (swap-free) accounts don't charge swap, but some brokers charge a fixed admin fee after a set number of days.")])

A(group="trading", slug="best-time-to-trade-forex-uae", tool="market-hours",
  title="Best Time to Trade Forex in UAE: Session Times in Dubai Time (GST)",
  h1="Best time to trade forex from the UAE",
  desc="Forex session times converted to UAE time: Sydney, Tokyo, London and New York, the London–New York overlap and the quietest hours.",
  keywords="best time to trade forex in uae, forex session times dubai, london session time uae, new york session time dubai, forex market hours gst, gold trading time uae",
  lede="The best hours in Dubai are roughly 4 pm to 9 pm, when London and New York are both open.",
  body="""
<h2>Session times in UAE time</h2>
<div class="scroll"><table><thead><tr><th>Session</th><th>Winter (Nov–Mar)</th><th>Summer</th></tr></thead><tbody>
<tr><td>Sydney</td><td>00:00–09:00</td><td>01:00–10:00</td></tr>
<tr><td>Tokyo</td><td>04:00–13:00</td><td>04:00–13:00</td></tr>
<tr><td>London</td><td>12:00–21:00</td><td>11:00–20:00</td></tr>
<tr><td>New York</td><td>17:00–02:00</td><td>16:00–01:00</td></tr></tbody></table></div>
<p class="hint">The UAE has no daylight saving; times shift when the UK, US and Australia change clocks. Session boundaries are approximate.</p>
<h2>The best window</h2>
<p>The <strong>London–New York overlap</strong> (about 17:00–21:00 in winter, 16:00–20:00 in summer) has the most volume in EUR/USD, GBP/USD and gold, with tight spreads and big moves. US data such as non-farm payrolls arrives at 17:30 UAE time in winter.</p>
<h2>Quiet times</h2>
<p>Late evening to early morning in the UAE (after the New York close until Tokyo opens) is thin. Spreads widen around the daily rollover.</p>
""",
  faqs=[("What time does the London session open in UAE?", "12:00 noon UAE time in winter and 11:00 during UK summer time."),
        ("What time does the New York session open in Dubai?", "Around 17:00 in winter and 16:00 during US daylight saving time.")])

A(group="trading", slug="es-vs-mes-futures", tool="futures-tick-value-calculator",
  title="ES vs MES Futures: E-mini vs Micro E-mini S&P 500 Compared",
  h1="ES vs MES: E-mini vs Micro E-mini S&P 500",
  desc="Tick size, tick value and point value of ES and MES futures, how to choose between them, and the same comparison for NQ vs MNQ and GC vs MGC.",
  keywords="es vs mes, micro e-mini s&p, mes tick value, es point value, nq vs mnq, gc vs mgc, micro futures explained",
  lede="MES is one tenth the size of ES. The price is the same; only the dollar value of each move differs.",
  body="""
<div class="scroll"><table><thead><tr><th>Contract</th><th class="n">Tick</th><th class="n">Tick value</th><th class="n">Per point</th></tr></thead><tbody>
<tr><td>ES (E-mini S&amp;P 500)</td><td class="n">0.25</td><td class="n">$12.50</td><td class="n">$50</td></tr>
<tr><td>MES (Micro)</td><td class="n">0.25</td><td class="n">$1.25</td><td class="n">$5</td></tr>
<tr><td>NQ (E-mini Nasdaq-100)</td><td class="n">0.25</td><td class="n">$5.00</td><td class="n">$20</td></tr>
<tr><td>MNQ (Micro)</td><td class="n">0.25</td><td class="n">$0.50</td><td class="n">$2</td></tr>
<tr><td>GC (Gold)</td><td class="n">0.10</td><td class="n">$10</td><td class="n">$100</td></tr>
<tr><td>MGC (Micro gold)</td><td class="n">0.10</td><td class="n">$1</td><td class="n">$10</td></tr></tbody></table></div>
<h2>Which to trade</h2>
<ul><li><strong>Micros</strong> let you size precisely and keep risk small. 10 MES equal 1 ES.</li><li><strong>Full-size</strong> contracts cost less in commission per dollar of exposure once your account is large.</li></ul>
<p>Example: a 10-point move in the S&amp;P is $500 on one ES and $50 on one MES. Margin requirements are set by CME and your broker and change with volatility.</p>
""",
  faqs=[("How many MES equal one ES?", "Ten. MES is one tenth the size of ES."),
        ("What is the point value of MES?", "$5 per index point, or $1.25 per 0.25 tick.")])

A(group="trading", slug="what-is-gift-nifty", tool="market-hours",
  title="What Is GIFT Nifty? SGX Nifty Replacement, Timings and How It Predicts Nifty",
  h1="What is GIFT Nifty?",
  desc="GIFT Nifty explained: the US-dollar Nifty 50 futures on NSE IX that replaced SGX Nifty in July 2023, trading hours in IST and UAE time, and how to read it.",
  keywords="what is gift nifty, gift nifty vs sgx nifty, gift nifty timings, gift nifty meaning, sgx nifty replaced, nse ix gift city, gift nifty uae time",
  lede="GIFT Nifty is a dollar-denominated Nifty 50 futures contract traded at NSE International Exchange in GIFT City, Gujarat.",
  body="""
<h2>From SGX Nifty to GIFT Nifty</h2>
<p>For years, offshore investors traded Nifty futures on the Singapore Exchange as SGX Nifty. From <strong>3 July 2023</strong> that trading moved to NSE IX in GIFT City and was renamed GIFT Nifty. SGX members can still route orders to it.</p>
<h2>Trading hours</h2>
<div class="scroll"><table><thead><tr><th>Session</th><th>India (IST)</th><th>UAE (GST)</th></tr></thead><tbody>
<tr><td>Session 1</td><td>06:30–15:40</td><td>05:00–14:10</td></tr>
<tr><td>Session 2</td><td>16:35–02:45</td><td>15:05–01:15</td></tr></tbody></table></div>
<h2>How traders use it</h2>
<p>Because GIFT Nifty trades before the NSE opens at 09:15 IST, its level compared with the previous Nifty 50 close hints at a <strong>gap-up or gap-down open</strong>. It reflects overnight US markets, Asian markets, crude oil and news.</p>
<p>It is a futures price, so it includes a small premium over the spot index. The actual opening gap is often a little smaller than GIFT Nifty suggests.</p>
""",
  faqs=[("Is SGX Nifty the same as GIFT Nifty?", "GIFT Nifty is the successor. SGX Nifty trading moved to NSE IX in GIFT City in July 2023."),
        ("What time does GIFT Nifty open in UAE?", "05:00 UAE time for the first session and 15:05 for the second.")])

# ---------------- India / Kerala ----------------
cent_rows = "".join(f'<tr><td>{c:g} cent{"s" if c != 1 else ""}</td><td class="n">{c*435.6:,.1f}</td><td class="n">{c*40.4686:,.2f}</td></tr>' for c in (1, 2, 3, 5, 8, 10, 15, 20, 25, 50, 100))
A(group="india", slug="cent-to-square-feet-kerala", tool="kerala-land-converter",
  title="1 Cent in Square Feet (Kerala): Cent to Sq Ft Table and Conversions",
  h1="How many square feet are in 1 cent?",
  desc="1 cent = 435.6 square feet = 40.47 square metres. A cent to square feet table for 1 to 100 cents, plus acre, are and hectare conversions used in Kerala.",
  keywords="1 cent in sq ft, cent to square feet, how many sq ft in 1 cent kerala, 5 cents in sq ft, 10 cents in sq ft, cent to square meter, 1 acre how many cents",
  lede="One cent is 435.6 square feet, or one hundredth of an acre.",
  body=f"""
<h2>Cent to square feet table</h2>
<div class="scroll"><table><thead><tr><th>Cents</th><th class="n">Square feet</th><th class="n">Square metres</th></tr></thead><tbody>{cent_rows}</tbody></table></div>
<h2>Other Kerala land units</h2>
<ul><li>1 acre = 100 cents = 43,560 sq ft</li><li>1 are = 100 m² = 1,076.39 sq ft ≈ 2.47 cents</li><li>1 hectare = 100 ares ≈ 247.1 cents ≈ 2.47 acres</li></ul>
<p>Sale deeds and brokers in Kerala usually quote <strong>cents</strong>, while village and revenue records often use <strong>ares</strong>. Convert one to the other before you compare prices or check a document.</p>
<h2>Price per cent to price per sq ft</h2>
<p>Divide the price per cent by 435.6. Land at ₹5 lakh per cent works out to about ₹1,148 per sq ft.</p>
""",
  faqs=[("How many sq ft is 5 cents?", "2,178 square feet."),
        ("How many cents are in one acre?", "100 cents.")])

A(group="india", slug="kerala-land-registration-cost", tool="kerala-stamp-duty-calculator",
  title="Land Registration Cost in Kerala 2026: Stamp Duty 8% + Fee 2%, With Examples",
  h1="How much does land registration cost in Kerala?",
  desc="Total cost of registering land in Kerala: 8% stamp duty and 2% registration fee on the higher of fair value and sale price, with worked examples and other costs.",
  keywords="land registration cost kerala, kerala registration charges 2026, stamp duty kerala land, fair value kerala registration, how much to register land in kerala, document writer fee kerala",
  lede="Budget about 10% of the property value for government charges, plus a little for the document writer and other costs.",
  body="""
<h2>The two government charges</h2>
<ul><li><strong>Stamp duty: 8%</strong></li><li><strong>Registration fee: 2%</strong></li></ul>
<p>Both are calculated on the <strong>higher</strong> of the government fair value and the sale consideration in the deed. The same rates apply to men, women and joint buyers.</p>
<h2>Examples</h2>
<div class="scroll"><table><thead><tr><th>Value used</th><th class="n">Stamp duty</th><th class="n">Registration</th><th class="n">Total</th></tr></thead><tbody>
""" + "".join(f'<tr><td>₹{v/1e5:g} lakh</td><td class="n">₹{v*0.08:,.0f}</td><td class="n">₹{v*0.02:,.0f}</td><td class="n">₹{v*0.10:,.0f}</td></tr>' for v in (1000000, 2500000, 5000000, 10000000)) + """</tbody></table></div>
<h2>Other costs to budget</h2>
<ul><li>Document writer's or advocate's fee</li><li>Encumbrance certificate and copies of records</li><li>Mutation (pokkuvaravu) at the village office after registration</li></ul>
<p>Gift and settlement deeds between close family have much lower duty. Confirm the current rates at keralaregistration.gov.in or your sub-registrar office.</p>
""",
  faqs=[("What is the total registration cost in Kerala?", "About 10% of the higher of fair value and sale price: 8% stamp duty plus a 2% registration fee."),
        ("Is the fair value or the sale price used?", "Whichever is higher.")])

A(group="india", slug="can-nri-buy-land-in-kerala", tool="kerala-stamp-duty-calculator",
  title="Can an NRI Buy Land in Kerala? Rules, Documents and Power of Attorney",
  h1="Can an NRI buy land in Kerala?",
  desc="What NRIs and OCIs can and cannot buy in India under FEMA, how to pay for property from the UAE, and how to register using a power of attorney.",
  keywords="can nri buy land in kerala, nri buy agricultural land india, nri property purchase rules, power of attorney nri kerala, nri land registration from uae, oci buy property india",
  lede="Yes: NRIs can buy residential and commercial property in Kerala. Agricultural land, plantations and farmhouses are the exception.",
  body="""
<h2>What NRIs and OCIs can buy</h2>
<ul><li><strong>Allowed:</strong> residential and commercial property, with no limit on the number of properties.</li>
<li><strong>Not allowed by purchase:</strong> agricultural land, plantation property and farmhouses. They can be received by inheritance.</li></ul>
<h2>How to pay</h2>
<p>Pay through normal banking channels: from an NRE, NRO or FCNR account, or by inward remittance from the UAE. Cash and payment in foreign currency are not allowed.</p>
<h2>Registering while you are in the Gulf</h2>
<p>You can sign at the sub-registrar office on a visit, or give a relative a <strong>power of attorney</strong>. Execute it at the Indian embassy or consulate (or before a notary and attest it there), then have it adjudicated for stamp duty in Kerala before use.</p>
<h2>Checks before buying</h2>
<ul><li>Encumbrance certificate (at least 13–30 years)</li><li>Title deeds and prior deeds</li><li>Land tax receipt and possession certificate</li><li>Classification in revenue records: <strong>wetland (nilam) and paddy land have strict conversion rules</strong></li></ul>
""",
  faqs=[("Can NRIs buy agricultural land in Kerala?", "No. NRIs and OCIs cannot buy agricultural land, plantations or farmhouses, though they can inherit them."),
        ("Can I register property in Kerala while living in the UAE?", "Yes, through a power of attorney executed at the Indian embassy or consulate and given to someone in Kerala.")])

A(group="india", slug="are-to-cent-conversion", tool="kerala-land-converter",
  title="Are to Cent Conversion: 1 Are = 2.47 Cents (Kerala Land Records)",
  h1="Are to cent conversion",
  desc="Convert ares (used in Kerala village and revenue records) to cents, square feet and acres. 1 are = 2.471 cents = 1,076.39 sq ft.",
  keywords="are to cent, 1 are in cents, are to sq ft, kerala land record ares, hectare are cent conversion, thandaper area conversion",
  lede="Revenue records in Kerala often list land in ares and hectares. Sellers quote cents. Here's how to convert.",
  body="""
<h2>Key conversions</h2>
<ul><li>1 are = 100 m² = 1,076.39 sq ft = <strong>2.471 cents</strong></li><li>1 cent = 0.4047 ares</li><li>1 hectare = 100 ares = 247.1 cents</li></ul>
<div class="scroll"><table><thead><tr><th>Ares</th><th class="n">Cents</th><th class="n">Square feet</th></tr></thead><tbody>
""" + "".join(f'<tr><td>{a:g}</td><td class="n">{a*2.47105:,.2f}</td><td class="n">{a*1076.39:,.0f}</td></tr>' for a in (0.5, 1, 2, 4, 5, 8, 10, 20, 40)) + """</tbody></table></div>
<h2>Why it matters</h2>
<p>If a deed says 10 cents but the record shows 3.5 ares (8.65 cents), the land is smaller than described. Check the survey number and area on the government land records before paying an advance.</p>
""",
  faqs=[("How many cents are in 1 are?", "About 2.471 cents."),
        ("How many ares are in 10 cents?", "About 4.05 ares.")])

# ---------------- Loans: rate rises (answer pages, 24 Nov 2026) ----------------
import math as _m

def _emi(P, a, n):
    r = a / 1200
    return P * r * (1 + r) ** n / ((1 + r) ** n - 1)

def _months(P, a, E):
    r = a / 1200
    return _m.log(E / (E - P * r)) / _m.log(1 + r)

def _inr(x):
    return f"₹{x:,.0f}"

def _ym(m):
    m = _m.ceil(m - 1e-9); y, mo = divmod(m, 12)
    return f"{y} yr {mo} mo" if mo else f"{y} yr"

_P, _N, _A0 = 5_000_000, 240, 8.5
_E0 = _emi(_P, _A0, _N)
_I0 = _E0 * _N - _P
_ROWS = []
for _a in (8.75, 9.0, 9.25):
    _e = _emi(_P, _a, _N); _mo = _months(_P, _a, _E0)
    _ROWS.append(dict(a=_a, emi=_e, emi_up=_e - _E0, int_emi=_e * _N - _P, mo=_mo, int_ten=_E0 * _mo - _P))
_R1 = _ROWS[0]
def _lakh(x):
    return f"₹{x/1e5:.2f} L"

EMI_VS_TENURE_TABLE = ('<div class="scroll"><table><thead><tr><th>Rate</th><th class="n">A: EMI</th><th class="n">A: interest</th>'
    '<th class="n">B: tenure</th><th class="n">B: interest</th><th class="n">B costs more</th></tr></thead><tbody>'
    + "".join(f'<tr><td>{r["a"]:.2f}%</td><td class="n">{_inr(r["emi"])}</td><td class="n">{_lakh(r["int_emi"])}</td>'
              f'<td class="n">{_ym(r["mo"])}</td><td class="n">{_lakh(r["int_ten"])}</td><td class="n">{_lakh(r["int_ten"] - r["int_emi"])}</td></tr>' for r in _ROWS)
    + "</tbody></table></div>")

A(group="uae", slug="higher-emi-or-longer-tenure-after-rate-hike", tool="loan-emi-calculator",
  title="Rate Hike on Your Home Loan: Higher EMI or Longer Tenure? (Worked Example)",
  h1="After a rate hike, should you pay a higher EMI or extend the tenure?",
  desc="When your loan rate goes up, the bank can raise your EMI or stretch the tenure. A worked ₹50 lakh example shows how much more interest a longer tenure costs.",
  keywords="higher emi or longer tenure, rate hike emi or tenure, increase emi or tenure home loan, bank increased tenure instead of emi, repo rate hike home loan tenure, home loan tenure extended after rate hike",
  lede="Keeping the same EMI feels painless, but every extra month of tenure is a month of interest. Paying the higher EMI almost always costs less in total.",
  body=f"""
<h2>The short answer</h2>
<p>If your budget can take it, choose the <strong>higher EMI</strong>. The loan ends on the original date and you pay less interest. Extending the tenure keeps the instalment the same, but the extra months are paid at the new, higher rate, so the total cost rises by much more than the EMI increase suggests.</p>
<p>Many banks extend the tenure by default on floating-rate loans, because it needs no change to your standing instruction. Check your latest loan statement for the remaining tenure, not only the EMI.</p>
<h2>Worked example: ₹50 lakh over 20 years</h2>
<p>Loan of {_inr(_P)} at {_A0}% for 20 years. EMI {_inr(_E0)}, total interest {_inr(_I0)}. Now the rate rises at the very start. You can either pay a higher EMI for the same 20 years (option A) or keep paying {_inr(_E0)} for longer (option B).</p>
{EMI_VS_TENURE_TABLE}
<p class="hint">A = pay a higher EMI for the original 20 years; B = keep the {_inr(_E0)} EMI and extend. L = lakh (₹1,00,000). Calculated with the standard reducing-balance EMI formula; the rate change is applied to the full balance from month one. Real loans part-way through will see smaller numbers, but the same pattern.</p>
<h2>What the table shows</h2>
<p>A 0.25 percentage point rise adds only {_inr(_R1["emi_up"])} a month to the EMI. Keeping the old EMI instead adds about {_m.ceil(_R1["mo"] - _N)} months to the loan and {_inr(_R1["int_ten"] - _R1["int_emi"])} more interest than option A. After three such rises the tenure grows by more than three years.</p>
<p>The reason is simple: with a fixed EMI, a larger share of each payment goes to interest, so the balance falls more slowly. Close to the point where the EMI only covers the interest, small rate rises push the tenure out sharply.</p>
<h2>When extending can make sense</h2>
<ul><li>Your monthly budget truly cannot absorb the higher EMI.</li>
<li>You expect a bonus or lump sum and plan to prepay soon, which shortens the tenure again.</li>
<li>You are young enough that a longer loan still ends well before retirement. Banks usually cap the loan at a maximum age.</li></ul>
<h2>A middle path</h2>
<p>Keep the old EMI but make a small part-prepayment once a year, or ask the bank to raise the EMI by a part of the increase. Use the calculator with your outstanding balance, new rate and remaining months to see both options before you call your lender.</p>
""",
  faqs=[("Why did my home loan tenure increase instead of my EMI?", "On floating-rate loans many lenders keep the EMI unchanged and extend the tenure when rates rise. You can usually ask them to raise the EMI instead; check your loan agreement and the lender's process."),
        ("Is a higher EMI or a longer tenure cheaper after a rate hike?", f"A higher EMI. In our ₹50 lakh, 20-year example, a 0.25 point rise costs {_inr(_R1['int_ten'] - _R1['int_emi'])} more in interest if you extend the tenure instead."),
        ("Can I switch back to a higher EMI later?", "Usually yes, by request to the lender or by making part-prepayments. In India, RBI rules bar prepayment charges on floating-rate loans taken by individuals for non-business purposes; elsewhere, check your loan terms."),
        ("Does this apply to loans outside India?", "Yes. The maths is the same for any reducing-balance loan in any currency; only the rates and lender rules differ.")])

_LOANS = (2_000_000, 3_000_000, 5_000_000, 7_500_000, 10_000_000)
_Q = []
for _L in _LOANS:
    _d = _emi(_L, 8.75, 240) - _emi(_L, 8.5, 240)
    _Q.append((_L, _emi(_L, 8.5, 240), _d, _d * 240))
QUARTER_TABLE = ('<div class="scroll"><table><thead><tr><th>Loan</th><th class="n">EMI at 8.50%</th><th class="n">Extra EMI at 8.75%</th><th class="n">Extra interest over 20 yrs</th></tr></thead><tbody>'
    + "".join(f'<tr><td>₹{L/1e5:g} lakh</td><td class="n">{_inr(e)}</td><td class="n">+{_inr(d)}</td><td class="n">{_inr(t)}</td></tr>' for L, e, d, t in _Q)
    + "</tbody></table></div>")
_Q50 = _Q[2]
_SIMPLE = _Q50[0] * 0.0025 / 12

A(group="uae", slug="how-much-does-a-quarter-point-rate-rise-cost", tool="loan-emi-calculator",
  title="How Much Does a 0.25% Rate Rise Cost on a Home Loan? (Table by Loan Size)",
  h1="How much does a 0.25% interest rate rise cost on a home loan?",
  desc="A 0.25 percentage point rate rise adds about ₹160 a month per ₹10 lakh on a 20-year loan at 8.5%. See the table for ₹20 lakh to ₹1 crore and how to work out your own loan.",
  keywords="0.25 rate hike emi impact, 25 bps repo hike home loan emi, how much will emi increase, repo rate hike emi calculator, 0.25 percent increase home loan cost, emi increase per lakh",
  lede="A quarter-point rise sounds tiny. On a long loan it adds a small amount each month and a surprisingly large amount in total.",
  body=f"""
<h2>The short answer</h2>
<p>On a 20-year loan, moving from 8.50% to 8.75% raises the EMI by about <strong>{_inr(_Q[0][2] / 2)} per ₹10 lakh borrowed</strong>. For a {_inr(_Q50[0])} loan that is {_inr(_Q50[2])} a month, or {_inr(_Q50[3])} extra over the full 20 years, if you keep the tenure unchanged.</p>
<h2>Table by loan size</h2>
{QUARTER_TABLE}
<p class="hint">20-year reducing-balance loans, rate change applied from month one. Figures rounded to the nearest rupee.</p>
<h2>Worked example</h2>
<p>A quick shortcut is 0.25% of the loan divided by 12: {_inr(_Q50[0])} × 0.25% ÷ 12 = {_inr(_SIMPLE)}. The true increase is lower, {_inr(_Q50[2])}, because the extra interest is spread over 240 payments while the balance falls. The shortcut is a fair upper bound for long loans.</p>
<p>The real figure for you depends on three things: your outstanding balance, the months left, and whether the lender raises the EMI or extends the tenure. Extending the tenure costs more in total; see our guide on <a href="/guides/higher-emi-or-longer-tenure-after-rate-hike/">higher EMI or longer tenure</a>.</p>
<h2>Why rates are in the news</h2>
<p>In India, the Reserve Bank raised the repo rate by 0.25 points to 5.50% in October 2026, and October retail inflation came in at 6.09%, above the 6% upper tolerance band. The next policy decision is due on 4 December 2026. Loans linked to an external benchmark such as the repo rate usually reset at the next reset date set in your loan agreement, not on the day of the announcement.</p>
<p>Elsewhere the same arithmetic applies to any floating-rate mortgage: put your balance, new rate and remaining term into the calculator.</p>
""",
  faqs=[("How much does EMI increase for a 0.25% rate rise on ₹50 lakh?", f"About {_inr(_Q50[2])} a month on a 20-year loan moving from 8.50% to 8.75%, if the tenure stays the same."),
        ("When will my EMI change after a repo rate rise?", "Repo-linked loans change on the reset date in your loan agreement, often the start of the next month or quarter. Your lender will confirm the new rate."),
        ("Does a 0.25% rise cost more on a longer loan?", "Yes. The longer the remaining term, the more months the higher rate applies to, so the total extra interest is larger.")])

# ---------------- Everyday / documents (25 Nov 2026) ----------------
A(group="everyday", slug="how-to-calculate-percentage-of-marks", tool="percentage-calculator",
  title="How to Calculate Percentage of Marks (With Examples for 5 and 6 Subjects)",
  h1="How to calculate percentage of marks",
  desc="Percentage of marks = marks obtained ÷ total marks × 100. Worked examples for 5 and 6 subjects, best of five, a single subject, and how to find the marks you need for a target percentage.",
  keywords="how to calculate percentage of marks, percentage of marks formula, marks percentage calculator, how to calculate percentage of 5 subjects, percentage of 6 subjects, best of five percentage, how to find percentage of marks out of 500",
  lede="One formula covers every case: add the marks you got, divide by the maximum marks, multiply by 100.",
  body="""
<h2>The formula</h2>
<p><strong>Percentage = (marks obtained ÷ total maximum marks) × 100</strong></p>
<p>Add your marks across all the subjects that count, add the maximum marks for the same subjects, divide the first total by the second and multiply by 100. Round only at the end.</p>
<h2>Worked example: 5 subjects out of 100 each</h2>
<div class="scroll"><table><thead><tr><th>Subject</th><th class="n">Marks</th><th class="n">Out of</th></tr></thead><tbody>
<tr><td>English</td><td class="n">78</td><td class="n">100</td></tr><tr><td>Mathematics</td><td class="n">91</td><td class="n">100</td></tr>
<tr><td>Science</td><td class="n">85</td><td class="n">100</td></tr><tr><td>Social science</td><td class="n">72</td><td class="n">100</td></tr>
<tr><td>Second language</td><td class="n">88</td><td class="n">100</td></tr>
<tr><td><b>Total</b></td><td class="n"><b>414</b></td><td class="n"><b>500</b></td></tr></tbody></table></div>
<p>414 ÷ 500 × 100 = <strong>82.8%</strong>.</p>
<h2>6 subjects, or papers with different maximum marks</h2>
<p>With six subjects out of 100, divide by 600. If the papers carry different maximum marks (for example 80 for theory and 20 for practical), do not average the separate percentages. Add the real marks and the real maximums: 65/80 and 18/20 make 83/100, which is 83%, while averaging 81.25% and 90% would give a wrong 85.6%.</p>
<h2>Best of five</h2>
<p>Some boards and admission forms ask for the percentage of your best five subjects. Drop the subject with the lowest marks, then use a total out of 500. If the example above had a sixth subject with 60 marks, best of five is still 414 out of 500, or 82.8%, while all six give 474 out of 600, or 79%. Always check which subjects your form says must be included; some insist on a language.</p>
<h2>Marks you need for a target percentage</h2>
<p>Turn the formula round: <strong>marks needed = target % × total marks ÷ 100</strong>. To reach 75% in a 500-mark exam you need 375 marks. If you already have 290 from four papers, the last 100-mark paper needs 85.</p>
<h2>CGPA and grades</h2>
<p>A CGPA or grade point is not a percentage. Universities and boards use their own conversion rules, so use the formula printed on your marksheet or in your university's regulations rather than a general multiplier.</p>
<p>The <a href="/percentage-calculator/">percentage calculator</a> does the division for you: enter the marks obtained as X and the total as Y in the "X is what % of Y" row.</p>
""",
  faqs=[("How do I calculate percentage of marks out of 500?", "Divide your total marks by 500 and multiply by 100. For example, 414 ÷ 500 × 100 = 82.8%."),
        ("Should I average the percentages of each subject?", "Only if every subject has the same maximum marks. Otherwise add the actual marks and the actual maximums first, then divide."),
        ("How do I calculate percentage for 6 subjects?", "Add the marks of all six subjects, divide by the total maximum (600 if each is out of 100) and multiply by 100."),
        ("Can I convert CGPA to percentage with this formula?", "No. CGPA conversion depends on the rule set by your board or university; check your marksheet or its regulations.")])

A(group="docs", slug="how-to-make-a-wifi-qr-code", tool="qr-code-generator",
  title="How to Make a QR Code for Your Wi-Fi (Free, Works on iPhone and Android)",
  h1="How to make a QR code for your Wi-Fi",
  desc="Make a Wi-Fi QR code that lets guests join your network by pointing their phone camera at it. Step by step, what to enter for security type and hidden networks, and what to do if it fails.",
  keywords="how to make a qr code for wifi, wifi qr code generator, wifi qr code, share wifi password qr code, qr code for wifi password, wifi qr code not working, guest wifi qr code",
  lede="A Wi-Fi QR code holds your network name, password and security type. Guests scan it with the phone camera and join without typing anything.",
  body="""
<h2>Step by step</h2>
<ol><li>Open the <a href="/qr-code-generator/">QR code generator</a> and choose <em>Wi-Fi network</em>.</li>
<li>Type the <strong>network name (SSID)</strong> exactly as it appears in your phone's Wi-Fi list. Capital letters and spaces count.</li>
<li>Type the <strong>password</strong> exactly. It is case-sensitive.</li>
<li>Pick the <strong>security type</strong>. Almost every home router today uses WPA2 or WPA3, so choose <em>WPA / WPA2 / WPA3</em>. Choose <em>None</em> only for an open network with no password.</li>
<li>Tick <em>Hidden network</em> only if your router does not broadcast its name.</li>
<li>Download the code as PNG to share on a phone, or SVG or the 2048 px PNG to print.</li>
<li>Test it: forget the network on one phone, then scan the code with its camera.</li></ol>
<h2>What the code contains</h2>
<p>A Wi-Fi QR code is plain text in a standard format that phone cameras recognise:</p>
<div class="scroll"><table><thead><tr><th>Network</th><th>Text inside the code</th></tr></thead><tbody>
<tr><td>Name <em>Home 5G</em>, password <em>blue;sky</em>, WPA2</td><td><code>WIFI:T:WPA;S:Home 5G;P:blue\\;sky;;</code></td></tr>
<tr><td>Open café network <em>Cafe Guest</em></td><td><code>WIFI:T:nopass;S:Cafe Guest;;</code></td></tr></tbody></table></div>
<p>Special characters such as <code>;</code> <code>,</code> <code>:</code> <code>\\</code> and <code>"</code> must be escaped with a backslash, as in the first row. The generator does this for you, which is the most common reason hand-made codes fail.</p>
<h2>If the code does not work</h2>
<ul><li><strong>Wrong name or password:</strong> one wrong capital letter or a trailing space is enough to fail. Copy them from the router label or settings.</li>
<li><strong>Wrong security type:</strong> an old router set to WEP needs <em>WEP</em>; a modern one needs <em>WPA</em>.</li>
<li><strong>Printed too small or low contrast:</strong> print it at least 3 cm wide, dark on a light background.</li>
<li><strong>You changed the password:</strong> the code stores the old one. Make and print a new code.</li></ul>
<h2>Is it safe?</h2>
<p>Anyone who scans the code, or photographs it, gets your password. For visitors, put the code on a separate guest network if your router offers one, and do not post a photo of it online. The CalcSouq generator builds the code in your browser and does not save the password.</p>
""",
  faqs=[("Do I need an app to scan a Wi-Fi QR code?", "Usually not. Current iPhone and Android camera apps recognise Wi-Fi QR codes and offer to join the network."),
        ("Which security type should I choose?", "WPA / WPA2 / WPA3 for nearly all home and office routers. Choose WEP only for very old routers and None for open networks."),
        ("Does a Wi-Fi QR code expire?", "No. It keeps working until you change the network name or password."),
        ("Can I print a Wi-Fi QR code?", "Yes. Download the SVG or the 2048 px PNG for sharp printing, and print it at least 3 cm wide.")])
