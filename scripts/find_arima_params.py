"""Run once to discover best ARIMA parameters, then hardcode in api/models.py for demo purpose"""

import sys
import warnings
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
warnings.filterwarnings("ignore")

import pmdarima as pm

from api.data import get_prices

print("Fitting auto_arima on full price history — takes ~60-90s...")
prices = get_prices()

model = pm.auto_arima(
    prices,
    seasonal=True,
    m=52,
    stepwise=True,
    information_criterion="aic",
    suppress_warnings=True,
    error_action="ignore",
)

print()
print("Best parameters found:")
print(f"  order          = {model.order}")
print(f"  seasonal_order = {model.seasonal_order}")
print(f"  aic            = {round(model.aic(), 2)}")
print()
print("Paste into api/models.py:")
print(f"  ARIMA_ORDER          = {model.order}")
print(f"  ARIMA_SEASONAL_ORDER = {model.seasonal_order}")
