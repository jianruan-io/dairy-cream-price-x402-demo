import math
import warnings

import numpy as np
from pmdarima import ARIMA

warnings.filterwarnings("ignore")

# Best params from scripts/find_arima_params.py — AIC -2420.19
ARIMA_ORDER = (1, 1, 1)
ARIMA_SEASONAL_ORDER = (1, 0, 1, 52)

_arima_model = None


def _get_arima(prices: np.ndarray) -> ARIMA:
    global _arima_model
    if _arima_model is None:
        _arima_model = ARIMA(order=ARIMA_ORDER, seasonal_order=ARIMA_SEASONAL_ORDER)
        _arima_model.fit(prices)
    return _arima_model


def warm_up(prices: np.ndarray) -> None:
    _get_arima(prices)


def get_model_summary(prices: np.ndarray) -> dict:
    _get_arima(prices)
    return {
        "order": list(ARIMA_ORDER),
        "seasonal_order": list(ARIMA_SEASONAL_ORDER),
        "aic": -2420.19,
    }


def point_forecast(prices: np.ndarray, horizons_days: list[int]) -> list[dict]:
    model = _get_arima(prices)
    n_periods = math.ceil(max(horizons_days) / 7)
    forecast = model.predict(n_periods=n_periods)
    current = float(prices[-1])
    results = []
    for h in horizons_days:
        week_idx = math.ceil(h / 7) - 1
        price = round(float(forecast[week_idx]), 4)
        change_pct = round((price - current) / current * 100, 2)
        results.append({
            "horizon_days": h,
            "arima_price": price,
            "arima_change_pct": change_pct,
        })
    return results


def risk_simulation(
    prices: np.ndarray,
    horizons_days: list[int],
    n: int = 10000,
    seed: int = 42,
) -> dict:
    """Geometric Brownian Motion Monte Carlo.
    Returns weekly fan-chart bands (paths) + per-horizon snapshots.
    """
    log_returns = np.diff(np.log(prices))
    mu = float(np.mean(log_returns))
    sigma = float(np.std(log_returns))
    current = float(prices[-1])

    rng = np.random.default_rng(seed)
    n_weeks = math.ceil(max(horizons_days) / 7)

    shocks = rng.standard_normal((n, n_weeks))
    weekly_returns = (mu - 0.5 * sigma ** 2) + sigma * shocks
    sim_paths = current * np.exp(np.cumsum(weekly_returns, axis=1))

    paths = []
    for w in range(n_weeks):
        col = sim_paths[:, w]
        paths.append({
            "week": w + 1,
            "p10": round(float(np.percentile(col, 10)), 4),
            "p25": round(float(np.percentile(col, 25)), 4),
            "p50": round(float(np.percentile(col, 50)), 4),
            "p75": round(float(np.percentile(col, 75)), 4),
            "p90": round(float(np.percentile(col, 90)), 4),
        })

    snapshots = []
    for h in horizons_days:
        week_idx = math.ceil(h / 7) - 1
        col = sim_paths[:, week_idx]
        snapshots.append({
            "horizon_days": h,
            "p10": round(float(np.percentile(col, 10)), 4),
            "p25": round(float(np.percentile(col, 25)), 4),
            "p50": round(float(np.percentile(col, 50)), 4),
            "p75": round(float(np.percentile(col, 75)), 4),
            "p90": round(float(np.percentile(col, 90)), 4),
            "prob_increase": round(float(np.mean(col > current)), 4),
        })

    return {"paths": paths, "snapshots": snapshots}
