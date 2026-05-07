from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException, Query
from uvicorn.middleware.proxy_headers import ProxyHeadersMiddleware
from x402.http.middleware import PaymentMiddlewareASGI

from api.config import settings
from api.data import get_df, get_prices
from api.models import get_model_summary, point_forecast, risk_simulation, warm_up
from api.schemas import CreamForecastResponse, CreamHistoryResponse, CreamPriceResponse, CreamSimulationResponse
from api.x402 import build_routes, build_x402_server


@asynccontextmanager
async def lifespan(app: FastAPI):
    import asyncio
    import logging
    asyncio.get_event_loop().run_in_executor(None, warm_up, get_prices())
    logging.getLogger("uvicorn.error").info("Docs: http://localhost:8000/docs")
    yield


app = FastAPI(
    title="Dairy Cream Price API",
    description="CPG dairy commodity intelligence for AI agents. Pay per call via x402 on Base.",
    version="0.1.0",
    lifespan=lifespan,
)

# Trust X-Forwarded-Proto / X-Forwarded-Host from any upstream proxy (ngrok, etc.)
# so request.url reflects the public HTTPS URL rather than http://localhost
app.add_middleware(ProxyHeadersMiddleware, trusted_hosts="*")

if not settings.dev_bypass_x402 and settings.x402_pay_to_address:
    app.add_middleware(
        PaymentMiddlewareASGI,
        routes=build_routes(),
        server=build_x402_server(),
    )


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

@app.get("/dairy/cream/price", response_model=CreamPriceResponse)
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

@app.get("/dairy/cream/history", response_model=CreamHistoryResponse)
async def cream_history(
    weeks: int = Query(52, ge=4, le=1560, description="Number of weeks to return"),
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

@app.get("/dairy/cream/forecast", response_model=CreamForecastResponse)
async def cream_forecast(
    horizons: str = Query("30,60,90", description="Comma-separated forecast horizons in days"),
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

@app.get("/dairy/cream/simulation", response_model=CreamSimulationResponse)
async def cream_simulation(
    horizons: str = Query("30,60,90", description="Comma-separated forecast horizons in days"),
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
