import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
load_dotenv()  # ensure CDP_API_KEY_ID / CDP_API_KEY_SECRET are in os.environ

import base64, json, logging as _logging  # noqa: E402
from fastapi import Depends, FastAPI, HTTPException, Query, Request  # noqa: E402
from starlette.middleware.base import BaseHTTPMiddleware  # noqa: E402
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware  # noqa: E402
from x402.http.middleware import PaymentMiddlewareASGI  # noqa: E402

from api.config import settings  # noqa: E402
from api.data import get_df, get_prices  # noqa: E402
from api.models import get_model_summary, point_forecast, risk_simulation, warm_up  # noqa: E402
from api.schemas import CreamForecastResponse, CreamHistoryResponse, CreamPriceResponse, CreamSimulationResponse  # noqa: E402
from api.x402 import build_routes, build_x402_server  # noqa: E402


@asynccontextmanager
async def lifespan(app: FastAPI):
    import logging
    log = logging.getLogger("uvicorn.error")
    log.info("CDP_API_KEY_ID set: %s", bool(os.getenv("CDP_API_KEY_ID")))
    log.info("CDP_API_KEY_SECRET set: %s", bool(os.getenv("CDP_API_KEY_SECRET")))
    warm_up(get_prices())
    log.info("Docs: http://localhost:8000/docs")
    yield


app = FastAPI(
    title="Dairy Cream Price API",
    description=(
        "CPG dairy commodity intelligence for AI agents. Pay per call via x402 on Base.\n\n"
        "## Endpoints\n\n"
        "| Route | Cost | Description |\n"
        "|---|---|---|\n"
        "| `GET /dairy/cream/price` | $0.01 | Latest spot price (this week) |\n"
        "| `GET /dairy/cream/history` | $0.05 | Weekly price series — up to 1,560 weeks (~30 yrs) |\n"
        "| `GET /dairy/cream/forecast` | $0.10 | ARIMA point forecast at custom horizons |\n"
        "| `GET /dairy/cream/simulation` | $0.15 | Monte Carlo risk envelope (10k paths) |\n\n"
        "## Query Parameters\n\n"
        "**`/dairy/cream/history`**\n"
        "- `weeks` *(int, default 52, min 4, max 1560)* — number of trailing weeks to return.\n"
        "  - 1 year ≈ 52 weeks · 5 years ≈ 260 · 10 years ≈ 520 · 25 years ≈ 1300 · 30 years = 1560\n\n"
        "**`/dairy/cream/forecast`** and **`/dairy/cream/simulation`**\n"
        "- `horizons` *(str, default \"30,60,90\")* — comma-separated forecast horizons in **days** (max 730 per horizon).\n"
        "  - Examples: `30` · `90,180` · `30,60,90,180,365`"
    ),
    version="0.1.0",
    lifespan=lifespan,
)

# Trust X-Forwarded-Proto / X-Forwarded-Host from any upstream proxy (ngrok, etc.)
# so request.url reflects the public HTTPS URL rather than http://localhost
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

_dbg = _logging.getLogger("uvicorn.error")

class _X402DebugMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        for name, value in request.headers.items():
            if "payment" in name.lower() or "x402" in name.lower() or "signature" in name.lower():
                try:
                    decoded = json.loads(base64.b64decode(value + "=="))
                    _dbg.info(">> %s: %s", name, json.dumps(decoded, indent=2))
                except Exception:
                    _dbg.info(">> %s (raw): %s", name, value[:500])
        return await call_next(request)

if not settings.dev_bypass_x402 and settings.x402_pay_to_address:
    app.add_middleware(  # type: ignore[arg-type]
        PaymentMiddlewareASGI,
        routes=build_routes(),
        server=build_x402_server(),
    )
    app.add_middleware(_X402DebugMiddleware)  # outermost — logs before PaymentMiddleware sees it


# ---------------------------------------------------------------------------
# Shared dependencies
# ---------------------------------------------------------------------------

def df_dep():
    return get_df()

def prices_dep():
    return get_prices()


# ---------------------------------------------------------------------------
# GET /dairy/cream/price  —  $0.01  —  this week's spot price
# ---------------------------------------------------------------------------

@app.get(
    "/dairy/cream/price",
    response_model=CreamPriceResponse,
    summary="Latest spot price",
    description="Returns the most recent weekly spot price for Class II cream (Central U.S.). No parameters required. Cost: $0.01.",
)
async def cream_price(df=Depends(df_dep)) -> CreamPriceResponse:
    row = df.iloc[-1]
    return CreamPriceResponse(**{
        "commodity": "cream",
        "class": "Class II",
        "region": "Central U.S.",
        "as_of": str(df.index[-1].date()),
        "price": round(float(row["price"]), 4),
        "price_min": round(float(row["price_min"]), 4),
        "price_max": round(float(row["price_max"]), 4),
        "price_unit": "USD/lb",
        "source": "USDA AMS 1100 — Fluid Milk and Cream",
        "x402_cost_usd": 0.01,
    })


# ---------------------------------------------------------------------------
# GET /dairy/cream/history  —  $0.05  —  normalized weekly series
# ---------------------------------------------------------------------------

@app.get(
    "/dairy/cream/history",
    response_model=CreamHistoryResponse,
    summary="Weekly price history",
    description=(
        "Returns a weekly price series going back up to 1,560 weeks (~30 years). "
        "Cost: $0.05.\n\n"
        "**Parameter:** `weeks` (integer)\n"
        "- Default: `52` (one year)\n"
        "- Min: `4` · Max: `1560`\n"
        "- Quick reference: 52=1yr, 260=5yr, 520=10yr, 1300=25yr, 1560=30yr"
    ),
)
async def cream_history(
    weeks: int = Query(
        52,
        ge=4,
        le=1560,
        description=(
            "Trailing weeks of weekly price data to return. "
            "Min 4, max 1560 (~30 years). "
            "Examples: 52 = 1 yr, 260 = 5 yrs, 520 = 10 yrs, 1300 = 25 yrs."
        ),
    ),
    df=Depends(df_dep),
) -> CreamHistoryResponse:
    subset = df.tail(weeks)
    return CreamHistoryResponse(**{
        "commodity": "cream",
        "class": "Class II",
        "region": "Central U.S.",
        "price_unit": "USD/lb",
        "source": "USDA AMS 1100 — Fluid Milk and Cream",
        "weeks_returned": len(subset),
        "series": [
            {
                "date": str(idx.date()),
                "price": round(float(row["price"]), 4),
                "price_min": round(float(row["price_min"]), 4),
                "price_max": round(float(row["price_max"]), 4),
            }
            for idx, row in subset.iterrows()
        ],
        "x402_cost_usd": 0.05,
    })


# ---------------------------------------------------------------------------
# GET /dairy/cream/forecast  —  $0.10  —  ARIMA point forecast
# ---------------------------------------------------------------------------

@app.get(
    "/dairy/cream/forecast",
    response_model=CreamForecastResponse,
    summary="ARIMA point forecast",
    description=(
        "Returns ARIMA-based price forecasts for one or more forward horizons. "
        "Cost: $0.10.\n\n"
        "**Parameter:** `horizons` (string)\n"
        "- Comma-separated integers representing **days** ahead (each 1–730)\n"
        "- Default: `'30,60,90'`\n"
        "- Examples: `'30'` · `'90,180'` · `'30,60,90,180,365'`"
    ),
)
async def cream_forecast(
    horizons: str = Query(
        "30,60,90",
        description=(
            "Comma-separated forecast horizons in days (integers, each 1–730). "
            "Examples: '30' · '90,180' · '30,60,90,180,365'."
        ),
    ),
    prices=Depends(prices_dep),
    df=Depends(df_dep),
) -> CreamForecastResponse:
    try:
        horizon_list = [int(h.strip()) for h in horizons.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="horizons must be comma-separated integers e.g. 30,60,90")

    if not horizon_list or max(horizon_list) > 730:
        raise HTTPException(status_code=400, detail="each horizon must be between 1 and 730 days")

    arima = point_forecast(prices, horizon_list)

    return CreamForecastResponse(**{
        "commodity": "cream",
        "class": "Class II",
        "region": "Central U.S.",
        "current_price": round(float(prices[-1]), 4),
        "price_unit": "USD/lb",
        "as_of": str(df.index[-1].date()),
        "model": get_model_summary(prices),
        "forecast": [
            {"horizon_days": a["horizon_days"], "price": a["arima_price"], "change_pct": a["arima_change_pct"]}
            for a in arima
        ],
        "x402_cost_usd": 0.10,
    })


# ---------------------------------------------------------------------------
# GET /dairy/cream/simulation  —  $0.15  —  Monte Carlo risk envelope
# ---------------------------------------------------------------------------

@app.get(
    "/dairy/cream/simulation",
    response_model=CreamSimulationResponse,
    summary="Monte Carlo risk simulation",
    description=(
        "Runs a 10,000-path Monte Carlo GBM simulation and returns percentile bands (p10–p90) "
        "for each requested horizon. Cost: $0.15.\n\n"
        "**Parameter:** `horizons` (string)\n"
        "- Comma-separated integers representing **days** ahead (each 1–730)\n"
        "- Default: `'30,60,90'`\n"
        "- Examples: `'30'` · `'90,180'` · `'30,60,90,180,365'`"
    ),
)
async def cream_simulation(
    horizons: str = Query(
        "30,60,90",
        description=(
            "Comma-separated forecast horizons in days (integers, each 1–730). "
            "Examples: '30' · '90,180' · '30,60,90,180,365'."
        ),
    ),
    prices=Depends(prices_dep),
    df=Depends(df_dep),
) -> CreamSimulationResponse:
    try:
        horizon_list = [int(h.strip()) for h in horizons.split(",")]
    except ValueError:
        raise HTTPException(status_code=400, detail="horizons must be comma-separated integers e.g. 30,60,90")

    if not horizon_list or max(horizon_list) > 730:
        raise HTTPException(status_code=400, detail="each horizon must be between 1 and 730 days")

    mc = risk_simulation(prices, horizon_list)

    return CreamSimulationResponse(**{
        "commodity": "cream",
        "class": "Class II",
        "region": "Central U.S.",
        "current_price": round(float(prices[-1]), 4),
        "price_unit": "USD/lb",
        "as_of": str(df.index[-1].date()),
        "model": "Monte Carlo GBM — 10,000 paths, seed=42",
        "paths": mc["paths"],
        "snapshots": mc["snapshots"],
        "x402_cost_usd": 0.15,
    })
