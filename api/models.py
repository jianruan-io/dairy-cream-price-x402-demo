import math
from functools import lru_cache
from typing import Any

import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

ARIMA_ORDER = (1, 1, 1)
ARIMA_SEASONAL_ORDER = (1, 0, 1, 52)
AIC = -2420.19
MAX_WEEKS = 105  # ceil(730 / 7)
N_MC_PATHS = 10_000
MC_SEED = 42


@lru_cache(maxsize=1)
def _fit(prices_tuple: tuple) -> Any:
    prices = np.array(prices_tuple)
    return SARIMAX(prices, order=ARIMA_ORDER, seasonal_order=ARIMA_SEASONAL_ORDER).fit(disp=False)


@lru_cache(maxsize=1)
def _arima_weeks(prices_tuple: tuple) -> list[float]:
    return _fit(prices_tuple).forecast(steps=MAX_WEEKS).tolist()


def warm_up(prices: np.ndarray) -> None:
    t = tuple(prices.tolist())
    _fit(t)
    _arima_weeks(t)


def get_model_summary(_prices: np.ndarray) -> dict:
    return {"order": list(ARIMA_ORDER), "seasonal_order": list(ARIMA_SEASONAL_ORDER), "aic": AIC}


def point_forecast(prices: np.ndarray, horizons_days: list[int]) -> list[dict]:
    weeks = _arima_weeks(tuple(prices.tolist()))
    current = float(prices[-1])
    return [
        {
            "horizon_days": h,
            "arima_price": round(weeks[math.ceil(h / 7) - 1], 4),
            "arima_change_pct": round((weeks[math.ceil(h / 7) - 1] - current) / current * 100, 2),
        }
        for h in horizons_days
    ]


def risk_simulation(prices: np.ndarray, horizons_days: list[int]) -> dict:
    current = float(prices[-1])
    n_weeks = math.ceil(max(horizons_days) / 7)

    log_returns = np.diff(np.log(prices))
    mu = float(np.mean(log_returns))
    sigma = float(np.std(log_returns))

    rng = np.random.default_rng(MC_SEED)
    shocks = rng.standard_normal((N_MC_PATHS, n_weeks))
    paths = current * np.exp(np.cumsum((mu - 0.5 * sigma**2) + sigma * shocks, axis=1))

    path_bands = [
        {
            "week": w + 1,
            "p10": round(float(np.percentile(paths[:, w], 10)), 4),
            "p25": round(float(np.percentile(paths[:, w], 25)), 4),
            "p50": round(float(np.percentile(paths[:, w], 50)), 4),
            "p75": round(float(np.percentile(paths[:, w], 75)), 4),
            "p90": round(float(np.percentile(paths[:, w], 90)), 4),
        }
        for w in range(n_weeks)
    ]

    snapshots = [
        {
            "horizon_days": h,
            "p10": round(float(np.percentile(paths[:, math.ceil(h / 7) - 1], 10)), 4),
            "p25": round(float(np.percentile(paths[:, math.ceil(h / 7) - 1], 25)), 4),
            "p50": round(float(np.percentile(paths[:, math.ceil(h / 7) - 1], 50)), 4),
            "p75": round(float(np.percentile(paths[:, math.ceil(h / 7) - 1], 75)), 4),
            "p90": round(float(np.percentile(paths[:, math.ceil(h / 7) - 1], 90)), 4),
            "prob_increase": round(float(np.mean(paths[:, math.ceil(h / 7) - 1] > current)), 4),
        }
        for h in horizons_days
    ]

    return {"paths": path_bands, "snapshots": snapshots}
