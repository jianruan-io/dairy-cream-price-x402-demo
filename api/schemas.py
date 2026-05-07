from pydantic import BaseModel, Field


class CreamPriceResponse(BaseModel):
    commodity: str
    class_: str = Field(alias="class")
    region: str
    as_of: str
    price: float
    price_min: float
    price_max: float
    price_unit: str
    source: str
    x402_cost_usd: float

    model_config = {"populate_by_name": True}


class PricePoint(BaseModel):
    date: str
    price: float
    price_min: float
    price_max: float


class CreamHistoryResponse(BaseModel):
    commodity: str
    class_: str = Field(alias="class")
    region: str
    price_unit: str
    source: str
    weeks_returned: int
    series: list[PricePoint]
    x402_cost_usd: float

    model_config = {"populate_by_name": True}


class ARIMAModel(BaseModel):
    order: list[int]
    seasonal_order: list[int]
    aic: float


class ForecastHorizon(BaseModel):
    horizon_days: int
    price: float
    change_pct: float


class CreamForecastResponse(BaseModel):
    commodity: str
    class_: str = Field(alias="class")
    region: str
    current_price: float
    price_unit: str
    as_of: str
    model: ARIMAModel
    forecast: list[ForecastHorizon]
    x402_cost_usd: float

    model_config = {"populate_by_name": True}


class PathBand(BaseModel):
    week: int
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float


class SimulationSnapshot(BaseModel):
    horizon_days: int
    p10: float
    p25: float
    p50: float
    p75: float
    p90: float
    prob_increase: float


class CreamSimulationResponse(BaseModel):
    commodity: str
    class_: str = Field(alias="class")
    region: str
    current_price: float
    price_unit: str
    as_of: str
    model: str
    paths: list[PathBand]
    snapshots: list[SimulationSnapshot]
    x402_cost_usd: float

    model_config = {"populate_by_name": True}
