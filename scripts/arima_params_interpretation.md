Model: ARIMA(1,1,1)(1,0,1)[52]
Data:  usda_cream_classii_midwest_1996_2026.csv
AIC:   -2420.19 (lower = better; negative is normal for price series)

NON-SEASONAL — order: [1, 1, 1]
  p=1  Price depends on 1 lag (last week's price)
  d=1  Differenced once to remove long-run price trend and achieve stationarity
  q=1  1 moving average term — corrects for last week's forecast error

SEASONAL — seasonal_order: [1, 0, 1, 52]
  P=1  Price depends on the same week one year ago
  D=0  No seasonal differencing needed — annual pattern is stable
  Q=1  Corrects for the same week last year's forecast error
  m=52 One seasonal cycle = 52 weeks (annual)

PLAIN ENGLISH
  Cream prices are driven by last week's price plus the same week last year,
  with short-term and annual error correction built in.
  d=1 confirms prices follow a random-walk drift with no mean reversion.
  D=0 confirms seasonal swings are consistent enough to model directly.
