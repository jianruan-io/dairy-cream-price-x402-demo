# 🐮 Dairy Price API with X402

**Turn a ▼ cost center into ▲ revenue streams.**

Pay-per-call dairy commodity intelligence for AI agents — metered via [x402](https://x402.org) on Base. No API key. No onboarding. Just USDC per call.

Built for the **Coinbase × AWS Agentic Hackathon — Consensus Miami 2026**.

---

## The Problem

Meet Sneehee. She runs **Gallivant Ice Cream** in Houston — sells to Walmart and Kroger. Dairy is 40% of her COGS.

She uses AI daily. But when she asks her agent *"Can I hold my ice cream prices through Q3 or do I need to raise them?"* — the agent goes... **em...**

Why? USDA does have an API — technically. But you need a login.gov account to access it, there's zero schema documentation, the UI looks like it was built decades ago, and even humans get lost clicking through randomly placed links. No MCP server. No structured output.

So her agent can't really help. And even if it could parse the raw data, the modeling work to turn it into an actual forecast requires a data engineer + data scientist + ML engineer.

Most SMBs have none.

---

## The Solution

Make it **easier for AI agents to help Sneehee** :)

We built internal data pipelines to ingest USDA cream price data and run deterministic time-series forecasts — originally as infrastructure for our own invoice factoring underwriting. A cost center.

Now we're opening it up as an API. Any AI agent can call it, pay pennies in USDC, and get clean structured data + forecasts in under 2 seconds.

> 📹 Demo video coming soon

---

## Available APIs

Now AI agents can provide much better answers with **high quality data** :)

| Endpoint | Price | What you get |
|----------|-------|--------------|
| `GET /dairy/cream/price` | **$0.01** | Spot price for current week |
| `GET /dairy/cream/history` | **$0.10** | Weekly USDA cream prices from 1996 to April 2026 — clean, structured, ready to use |
| `GET /dairy/cream/forecast` | **$0.25** | ARIMA model to forecast most likely outcome |
| `GET /dairy/cream/simulation` | **$0.50** | 10k Monte Carlo simulations for possible outcomes |

Sample forecast response:
```json
{
  "commodity": "cream",
  "current_price": 2.13,
  "price_unit": "USD/lb",
  "as_of": "2026-04-27",
  "forecast": [
    { "horizon_days": 30, "arima_price": 2.26, "arima_change_pct": 6.1,
      "mc_p10": 2.01, "mc_p50": 2.26, "mc_p90": 2.54, "prob_increase": 0.71 },
    { "horizon_days": 60, "arima_price": 2.31, "arima_change_pct": 8.5,
      "mc_p10": 1.94, "mc_p50": 2.31, "mc_p90": 2.71, "prob_increase": 0.68 },
    { "horizon_days": 90, "arima_price": 2.38, "arima_change_pct": 11.7,
      "mc_p10": 1.89, "mc_p50": 2.38, "mc_p90": 2.89, "prob_increase": 0.65 }
  ]
}
```

---

## But Everyone Can Just Grab Public Data...

That's why we focus on the **unique data analysis and modeling** that are typically done by data engineers / data scientists / ML engineers etc.

| | Orbbit API | Hire an engineer |
|---|---|---|
| Cost | **$0.01 ~ $0.50 / call** | **$10K+ / year** |
| Setup | Zero | Months |
| Agent-ready | Yes | lol |

The data is public. The **clean, structured, model-ready version** is not.

---

## How X402 Works

All API calls are metered via the **x402 protocol** on **Base** (Coinbase L2):

1. Agent hits the endpoint → gets a `402 Payment Required` with USDC amount + Base chain details
2. Agent signs and broadcasts a USDC micropayment to the x402 Facilitator contract
3. Facilitator confirms on-chain → API runs the model
4. Clean data returned. Payment settled on-chain. Immutable record.

No API key. No contract. No KYC. Any agent with a wallet can call this.

---

## Inspired by AWS...

We can turn a **cost center** into **revenue streams** using X402.

Orbbit underwrites CPG SMB invoices — which requires data analysis and modeling on commodity prices. We built that infrastructure for ourselves. Now we're monetizing it as an API, the same way Amazon built AWS for Amazon first.

The broader flywheel:

```
Source capital from investors
Source invoices from SMBs
    → Underwrite SMBs & invoices (data analysis / modeling)
    → Deploy capital to SMBs
    → Collect payment from SMBs
    → Generate return for investors
    → (repeat)
```

The API sits at the top of that loop — generating revenue from the intelligence layer we'd be running anyway.

---

## And It Can Become Top of Funnel

We're moving from **SEO → AEO** (Answer Engine Optimization).

When an agent asks *"What's the cream price outlook?"* and Orbbit's API gives the best answer — that's discovery. When the forecast signals a working-capital gap, one click starts the factoring process.

- *Olala, Orbbit API gives useful data with insight!*
- *Em... What actions can I take for my finances?*
- *Oh! Orbbit also does invoice factoring!*

---

## Architecture

```
USDA AMS website (weekly cream prices, fetched 1996–April 2026)
    ↓
Normalized CSV/JSON (30 years of weekly data, committed to repo)
    ↓
ARIMA + Monte Carlo forecast models (Python)
    ↓
FastAPI on AWS Lambda + x402 payment middleware
    ↓
Anonymous agent pays USDC → gets forecast
    ↓
(optional) Signed handoff token → Orbbit factoring onboarding
```

> **Demo note:** This version demonstrates cream pricing. Production roadmap: full ETL pipeline for automated ingestion + scheduled model refresh, richer modeling features, and coverage well beyond dairy — other commodities, other data sources, other industries.

---

## Repo Structure

```
api/
  config.py        # environment + pricing config
  data.py          # USDA data loading + normalization
  x402.py          # x402 payment middleware
  main.py          # FastAPI app + endpoint handlers
data/              # normalized USDA cream price series
notebooks/         # EDA and model development
```

---

## Stack

| Layer | Technology |
|-------|-----------|
| API framework | FastAPI |
| Deployment | AWS Lambda |
| Payments | x402 Facilitator on Base · USDC |
| Data | USDA AMS weekly cream prices · 1996–April 2026 |
| Forecast models | Python · ARIMA · Monte Carlo GBM |
| Dev tooling | Claude Code · Kiro|

---

## Running Locally

```bash
pip install -r requirements.txt
cp .env.example .env  # add your keys
uvicorn api.main:app --reload
```

---

## About Orbbit

**Accelerate business prosperity through better capital.**

Orbbit is an invoice factoring platform built on stablecoin — connecting CPG SMBs that need fast working capital with investors seeking real-world yield. Settlement is instant in USDC on Base.

[orbbit.co](https://orbbit.co)
