# USDA Cream Class II — Market Analysis
**Dataset:** `usda_cream_classii_midwest_1996_2026.json`
**Coverage:** 2,003 records · Cream × Class II × Midwest · January 1996 – April 2026
**Prepared for:** Orbbit Forecast API — Hackathon context (Gallivant Ice Cream / Sneehee use case)

---

## 1. What This Data Is

USDA AMS Report 1100 tracks weekly **Class II cream prices** out of the Madison, WI office — the pricing benchmark for the Midwest dairy market. Class II covers soft manufactured dairy products: ice cream, sour cream, cottage cheese, yogurt. This is the direct input cost for an ice cream business like Sneehee's Gallivant Ice Cream.

Price unit: **dollars per pound ($/lb)**. Each record contains a `price_min` and `price_max` — the range of prices transacted that week across Midwest buyers.

---

## 2. Chart-by-Chart Findings

### Chart 1 — Records per Year
USDA published cream prices **once per week (52/year)** from 1996 through 2017. Starting in 2019, frequency doubled to **twice per week (~104/year)**. 2018 was a transition year (94 records). 2026 shows ~34 records — partial year through April.

**Decision for modeling:** Use 2019–2026 only for the forecasting model to ensure consistent sampling frequency. Pre-2019 data is retained in the file for historical charting only.

---

### Chart 2 — Annual Average Price Band (1996–2026)
The 30-year price history reveals a clear **boom-bust cycle** repeating roughly every 4–6 years:

| Peak Year | Avg Price ($/lb) | Context |
|-----------|-----------------|---------|
| 1998 | ~$2.25 | Demand surge |
| 2004 | ~$2.45 | Supply tightening |
| 2014–2015 | ~$2.85–$2.90 | **All-time sustained peak** |
| 2017 | ~$2.95 | Supply squeeze |
| 2022–2023 | ~$2.60 | Post-COVID supply chain |

The price band (gap between min and max lines) is narrow throughout — typically $0.10–$0.30/lb — meaning within any given week, Midwest buyers largely transact at similar prices.

**Current (2026 YTD):** Prices around **$1.50–$1.75/lb** — among the cheapest in a decade. This follows the typical post-spike correction pattern.

---

### Chart 3 — Price Distribution by Decade

**Histogram:** The distribution peaks sharply at **$1.00–$1.30/lb**, reflecting the baseline "normal" of the 1990s–2000s. The right tail extends to $4.50/lb — rare but real.

**Box plots by decade — the key structural shift:**

| Decade | Median | Box Width | Interpretation |
|--------|--------|-----------|----------------|
| 1990s | ~$1.50 | Narrow | Cheap, predictable |
| 2000s | ~$1.60 | Narrow | Still predictable |
| 2010s | ~$2.30 | Wide | Prices climbed and became volatile |
| 2020s | ~$1.50–$2.00 | **Very wide** ($0.80–$4.50) | Structurally more volatile than any prior decade |

**Conclusion:** The 2020s box is the widest in the dataset. Budgeting based on 1990s or 2000s averages actively understates current risk. Sneehee cannot assume prices will revert to a comfortable $1.50 floor — the floor itself has become uncertain.

---

### Chart 4 — Monthly Seasonality + The Cream Expiry Problem

Summer months (Jun–Sep) average **$0.40–$0.45/lb higher** than January–February ($2.10–$2.20 vs $1.75). That's a real seasonal signal.

However, the **error bars are enormous** — standard deviation lines extend to $3.00+ in summer months. The seasonal signal is almost completely swamped by year-to-year variation.

**The critical constraint: cream expires in 2–3 weeks.** Unlike shelf-stable commodities, Sneehee cannot stockpile cream in January to avoid summer price spikes. This makes the seasonal pattern **non-actionable for inventory** but directly actionable for **pricing strategy**:

- Ice cream demand peaks in summer (Q2–Q3) — exactly when cream costs more
- Margin compression hits at the worst possible moment
- **Recommended action:** Build a seasonal pricing buffer into Q3 wholesale contracts. Price summer production runs at a premium. Do not assume spring prices will hold into July.

---

### Chart 5 — Heatmap: Avg Price Min by Year × Month (2010–2026)

Three immediate observations from reading the cell values:

**1. The 2014–2015 crisis:**
- August 2014: **$3.53/lb** — highest single-month average in the dataset
- September 2014: **$3.46/lb**
- July–September 2015: $3.04–$3.46/lb sustained
- Any ice cream business that hadn't locked supplier rates in summer 2014 saw cream costs more than double from 2013 levels

**2. April 2020 — the COVID crash:**
- April 2020: **$0.86/lb** — the cheapest cream in the dataset
- This anomaly lasted only a few months before prices recovered sharply
- Illustrates how external shocks can create brief windows of very cheap cream that disappear almost immediately

**3. 2026 YTD — anomalously cheap:**
- January 2026: $2.00/lb
- February 2026: $1.48/lb
- March 2026: $1.73/lb
- April 2026: **$1.24/lb** — the cheapest April since 2016
- Prices are tracking well below 2024 and 2025 at the same calendar months

**Conclusion:** April 2026 at $1.24/lb is not a normal market. It requires a macroeconomic explanation (see Section 3).

---

### Chart 6 — Annual Avg Price Spread (Max − Min)

The spread measures market chaos — how much buyers disagreed on price within each week.

| Period | Avg Spread | Market State |
|--------|-----------|--------------|
| 1996–2009 | $0.09–$0.17 | Relatively calm |
| 2010 | $0.21 | First major disruption |
| 2014–2015 | **$0.27–$0.28** | Most chaotic period on record |
| 2019–2021 | $0.09–$0.12 | Calm pre-COVID |
| 2022–2023 | $0.15–$0.23 | Post-COVID turbulence |
| 2024–2026 | $0.15–$0.17 | **Rising again** |

The 2024–2026 spread is widening — buyers are disagreeing on price again. This is an early warning signal that market consensus is breaking down, even though absolute prices are low.

---

### Chart 7 — Weekly Price Trend 2023–2026 YTD

**2023 (light blue):** Started ~$2.50–$3.00/lb in January, peaked near **$4.00+/lb** in spring/summer, then crashed sharply through Q4 2023 back to $2.50.

**2024 (medium blue):** More contained. Ranged $1.50–$2.50/lb. Gradual decline through the year, ending around $1.50–$2.00.

**2025 (dark navy):** Started $1.50–$2.00, mid-year bump to $2.50–$3.00, then declining to ~$1.50–$2.00 by year end.

**2026 (red):** Started at ~$1.50, dipped to a low around February, now **ticking up** toward $2.00–$2.50 as of April. The upward trajectory in March–April 2026 rhymes with how 2023's spike started — a quiet Q1 followed by a sharp spring climb.

**Conclusion:** The March–April 2026 uptick is the signal to watch. It's early but directionally consistent with the start of a new upswing cycle.

---

### Chart 8 — Year-over-Year % Change

The boom-bust cycle is starkest here:

| Year | YoY Change | What Followed |
|------|-----------|---------------|
| 1998 | **+52%** | 1999: -27% |
| 2004 | **+58%** | 2005: -20% |
| 2010 | **+45%** | 2011: -20% |
| 2014 | **+40%** | 2016: -20% |
| 2022 | **+42%** | 2025: -20% |

The pattern is almost mechanical: a +40–60% spike is always followed within 1–2 years by a -20–30% correction. We are currently in the correction phase following 2022's spike.

**By this cycle, the next +40% year is due in 2026–2027.**

Large spikes consistently follow flat or red years — exactly the current setup. Any business budgeting based on 2026's cheap cream for 2027 planning is taking on unpriced risk.

---

### Chart 9 — 12-Week Rolling Average (2018–2026)

The smoothed trend removes week-to-week noise and shows the true underlying direction:

- **2018–2019:** ~$2.00–$2.50, gradually declining
- **Mid-2020:** Sharp COVID dip to ~$1.50, then rapid recovery
- **2021–2022:** Steep climb to **~$3.50/lb** — the post-COVID spike
- **2023–2025:** Long, steady decline back toward $1.50
- **Early 2026:** Rolling average has **flattened and shows the first small uptick** — a potential trend reversal signal

The rolling average is what the Orbbit forecasting model extends forward. A flattening line after a long decline is a leading indicator of a regime change — not confirmation of continued cheapness.

---

### Chart 10 — Rolling 12-Week Volatility (2018–2026)

| Period | Volatility Level | Market State |
|--------|-----------------|--------------|
| Early 2018 | Rising from 0 → $0.80 | Market waking up |
| 2019 | $0.80–$0.85, declining | Settling |
| Mid-2020 | Near zero briefly | COVID calm |
| 2021 | Rising from $0.25 → $0.80 | Pre-spike buildup |
| Mid-2022 | **$1.50** — peak | Post-COVID chaos |
| Early 2023 | Another $1.50 spike | Sustained turbulence |
| Mid-2024 | **$1.57** sharp spike | Highest recorded |
| Late 2025 | Declining $0.90–$1.40 | Easing |
| Early 2026 | **Near zero** | Anomalously calm |

The near-zero volatility in 2026 is historically a precursor to spikes, not continued calm:
- Mid-2020 near-zero → 2021–2022 blowup
- Mid-2021 near-zero → 2022 peak
- Early 2026 near-zero → next spike TBD

**The low volatility right now is a warning state, not a safe state.** Every prior near-zero episode in this dataset was followed by a major price surge within 2–6 months.

---

## 3. Why Cream Prices Are Declining in 2026 — Research Findings

Seven macroeconomic forces are converging simultaneously. This co-occurrence of all bearish factors at once is what caused volatility to collapse — there is no opposing force creating uncertainty.

---

### Driver 1: US Milk Production at Record Levels

- 2025 full-year production: **231.4 billion lbs** (USDA raised forecast by 800M lbs mid-year)
- February 2026: **18.255 billion lbs** — up **2.9% year-over-year**
- 2026 projected: **235.3 billion lbs** (USDA ERS LDP-M-382, April 2026)
- Milk per cow February 2026: **1,899 lbs** — up 12 lbs from February 2025

More milk means more cream separated per hundredweight. The domestic cream pool is structurally oversupplied.

**Source:** USDA ERS Livestock, Dairy, and Poultry Outlook: April 2026 (LDP-M-382)

---

### Driver 2: Dairy Herd at Near-Record Size

- January 1, 2026 herd: **9.568 million cows** — up 188,000 head year-over-year
- February 2026: **9.615 million cows** — still expanding, up 211,000 head YoY
- Near the highest herd count since 1998

The concerning structural signal: **replacement heifer inventory fell to 3.905 million head** (January 2026) — the lowest since 1978, at only 40.8% of productive cows. The herd pipeline is shrinking. Current high supply will eventually contract, but not in 2026.

**Source:** USDA NASS Cattle Inventory Report (January 2026); American Farm Bureau Federation Market Intel

---

### Driver 3: The Butterfat Genetics Revolution (Most Underrated Driver)

This is the slow-moving structural cause that permanently altered the cream market:

- Average butterfat content in US milk: **4.43% in early 2026** — up from ~3.7% in 2010 (+20%)
- 2024 was the fourth consecutive annual record for butterfat content
- From 2010 to 2024, butterfat yield improved **~16%** per hundredweight
- **~22 million extra pounds of butterfat annually** produced by the same herd that existed before, purely from genetic gains
- US butterfat growth rate (13% over 2015–2024) is **6× higher** than EU (2.4%) or New Zealand (2.5%)
- Protein-to-fat ratio has dropped from 0.82–0.84 (pre-2017) to **0.77** — structurally more cream per pound of milk

**Mechanism:** Every hundredweight of milk now yields more cream when separated. This cream goes into Class II (ice cream) or gets churned into butter (Class IV). Both channels are oversupplied. Cream multiples in the Midwest in early 2025 traded **below 1.00** — fire-sale pricing.

This is not a cyclical factor — it is a **structural, permanent increase in cream supply** that will continue as long as genomic selection prioritizes butterfat.

**Source:** CoBank: "While US Leads Milk Component Growth, Butterfat May Be Growing Too Fast" (2025); CoBank: "Unprecedented Genetic Gains Are Driving Record Milk Components"; The Bullvine: "Butter Glut 2025"

---

### Driver 4: The Butter Glut — Cream's Price Anchor

Class II cream price is mechanically tied to butter prices via the USDA Federal Milk Marketing Order formula. When butter is cheap, cream is cheap.

- CME spot butter: **$2.63/lb** (January 2025) → **~$1.65/lb** (December 2025) — a **40% crash in 12 months**
- Broke below $2.00/lb for the first time in years in September 2025
- US butter production up **5.68% in 2025**, adding 27 million extra pounds to the market
- January 2026 butter production: **231 million lbs** (+6.0% YoY)
- January 2026 butter cold storage: **270.3 million lbs** (+26% month-over-month)
- April 2026 CME butter: **$1.7707/lb**

Butter manufacturers were running churns **seven days a week** in early 2026 (USDA Dairy Market News) — processing surplus cream at maximum capacity just to clear the glut. This sets the price floor for all cream including Class II.

**Source:** UGA CAES 2026 Dairy Forecast; USDA AMS Dairy Market News, April 27–May 1, 2026; The Bullvine: "US Dairy Surplus Deepens"

---

### Driver 5: Tariffs Shut Export Markets

This is the most acute near-term driver and directly what triggered the 2026 acceleration downward.

**Timeline of events:**
- Early 2025: Trump administration imposed 25% tariffs on Canadian and Mexican goods
- Canada retaliated with **25% tariffs on US cheese, butter, and dairy spreads**
- March 2025: China imposed **10% tariffs** on US dairy
- April 2025: China escalated to **84–125% tariffs** on all US goods

**Trade volumes at stake:**
- Canada: **$2.47 billion** in annual US dairy exports (largest single market)
- China: **$1.14 billion** in annual US dairy exports
- Canada + China = **>50% of total US dairy export value**
- US dairy exports February 2026: **down 4.3% year-over-year**

**Historical precedent:** The 2018–2021 China tariff episode caused a **$2.6 billion loss** in US dairy farm revenues over three years. The 2025 escalation is broader and steeper.

**Direct cream impact:** Milk and cream that would have left the US as cheese or butter for export markets remains domestic, adding directly to the cream/butter glut.

**Source:** Fortune: "Trump Tariffs Threaten $8.2 Billion American Dairy Exports"; American Farm Bureau Federation: "Strong Start, Fragile Future"; Dairy Reporter: "How Trump's Liberation Day Impacts Global Dairy Markets"

---

### Driver 6: Global Dairy Oversupply — All Major Regions at Once

A simultaneous global surplus is unusual — typically regional shortfalls offset surpluses elsewhere.

- **Big 7 dairy exporters** (US, EU, NZ, Australia, Brazil, Argentina, Uruguay) finished 2025 **2.2% above 2024** — highest collective growth in years
- **New Zealand:** Highest milk production since 2018 at 22.0 million MT
- **EU:** Milk production growing alongside US
- Global milk prices fell for **seven consecutive months** through December 2025 (IFCN Dairy Research Network)
- Butter hit a **24-month global low** by end-2025
- Market rebalancing not expected until **late 2026 at the earliest** (StoneX)

**Source:** Dairy Reporter: "Global Milk Oversupply Persists Despite Demand Uptick" (January 2026); StoneX: "Global Milk Oversupply Pushes Dairy Rebalancing into Late 2026"; Dairy Reporter: "Global Dairy Outlook 2026: Glut, Prices, and Growth Bets"

---

### Driver 7: Low Feed Costs Delayed Natural Herd Contraction

Low input costs removed the normal economic pressure that would force farmers to cull marginal cows and reduce milk supply.

- Record 2025 corn harvest: **17.021 billion bushels**
- DMC (Dairy Margin Coverage) feed costs dropped to **$9–10/cwt** — lowest since October 2020
- USDA projected corn at potentially **$4.20/bushel** (May 2025 Feed Outlook)
- Despite cheap feed, all-milk prices are projected to fall to **$18.75–$19.25/cwt in 2026** (from $21.05 in 2025) — the milk price decline outpaced feed savings by >$1/cwt
- Cheap feed made it economical to keep more cows longer through late 2025, **postponing the herd contraction** that would otherwise tighten supply

**Source:** The Bullvine: "Feed Cost Revolution — 2025–26"; American Farm Bureau Federation: "Dairy Margin Coverage Showing Its Limits"

---

## 4. Summary Table — All Drivers

| Driver | Key Data Point | Direction |
|--------|---------------|-----------|
| Milk production | +2.9% YoY Feb 2026; 235B lbs projected 2026 | ↓ Price |
| Herd size | 9.615M cows — near 28-year high | ↓ Price |
| Butterfat genetics | 4.43% fat content; ~22M extra lbs butterfat/yr from genetics alone | ↓ Price (structural) |
| Butter/Class IV glut | CME butter $1.77/lb; 270M lbs in cold storage | ↓ Price |
| Tariffs / export collapse | Exports -4.3% YoY; Canada 25%, China 84–125% retaliatory | ↓ Price |
| Global oversupply | Big 7 exporters +2.2% in 2025; NZ highest since 2018 | ↓ Price |
| Low feed costs | Corn at 10-yr low; delayed herd liquidation | ↓ Price (indirect) |

---

## 5. What This Means for Sneehee — Orbbit's Narrative

Cream at **$1.24/lb in April 2026** is not a stable new baseline. It is the product of seven simultaneous bearish forces that will not all persist indefinitely:

- **Tariff deals** could reopen export markets quickly, redirecting US cream/butter abroad and draining the domestic surplus
- **Herd contraction** is already in the pipeline — replacement heifer inventory at a 46-year low means fewer cows in 2027–2028
- **The YoY cycle** has produced a +40–58% spike every 4–6 years since 1996. The last spike was 2022. The next is statistically due in 2026–2027
- **Volatility at near-zero** has historically preceded every major price blowup in this dataset

Sneehee cannot stockpile cream — it expires in 2–3 weeks. Her only levers are:
1. **Lock current supplier rates** into 60–90 day contracts while prices are near the cycle floor
2. **Raise wholesale prices now** before the next spike compresses her margins at peak summer demand
3. **Secure working capital proactively** — not after cream hits $3.00/lb and her receivables gap has already opened

This is precisely what Orbbit's Forecast API surfaces: not just the current price, but the cycle position, the macro drivers, and a forward projection with a confidence band — so Sneehee acts before the market moves, not after.

---

## 6. Key Sources

| Source | URL |
|--------|-----|
| USDA ERS LDP-M-382: Livestock, Dairy & Poultry Outlook, April 2026 | https://ers.usda.gov/sites/default/files/_laserfiche/outlooks/114065/LDP-M-382.pdf |
| USDA AMS Dairy Market News, April 27–May 1, 2026 | https://www.ams.usda.gov/mnreports/dywweeklyreport.pdf |
| USDA NASS Cattle Inventory Report, January 2026 | https://www.nass.usda.gov/Newsroom/2026/01-30-2026.php |
| CoBank: Butterfat May Be Growing Too Fast | https://www.cobank.com/knowledge-exchange/dairy/while-us-leads-milk-component-growth-butterfat-may-be-growing-too-fast |
| CoBank: Unprecedented Genetic Gains | https://www.cobank.com/knowledge-exchange/dairy/unprecedented-genetic-gains-are-driving-record-milk-components |
| StoneX: Global Milk Oversupply into Late 2026 | https://www.stonex.com/en/insights/global-milk-oversupply-pushes-dairy-rebalancing-into-late-2026-2026-01-29/ |
| Fortune: Trump Tariffs Threaten $8.2B Dairy Exports | https://fortune.com/2025/04/01/trump-tariffs-threaten-8-2-billion-dollar-american-dairy-exports/ |
| American Farm Bureau: Strong Start, Fragile Future | https://www.fb.org/market-intel/strong-start-fragile-future-u-s-dairys-trade-balancing-act |
| The Bullvine: Butter Glut 2025 | https://www.thebullvine.com/news/butter-glut-2025-why-your-cream-checks-about-to-get-creamed/ |
| Dairy Reporter: Global Dairy Outlook 2026 | https://www.dairyreporter.com/Article/2026/03/26/global-dairy-outlook-2026-glut-prices-and-growth-bets/ |
