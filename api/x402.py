"""x402 payment middleware — official Coinbase x402 Python SDK."""

from x402 import x402ResourceServer
from x402.http import FacilitatorConfig, HTTPFacilitatorClient, PaymentOption, RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme

from api.config import settings

_NETWORK_CAIP2 = {
    "base": "eip155:8453",
    "base-sepolia": "eip155:84532",
}


def build_x402_server() -> x402ResourceServer:
    facilitator = HTTPFacilitatorClient(
        FacilitatorConfig(url=settings.x402_facilitator_url)
    )
    server = x402ResourceServer(facilitator)
    server.register("eip155:*", ExactEvmServerScheme())
    return server


def build_routes() -> dict[str, RouteConfig]:
    network = _NETWORK_CAIP2.get(settings.x402_network, settings.x402_network)
    pay_to = settings.x402_pay_to_address

    def _option(price: str) -> PaymentOption:
        return PaymentOption(
            scheme="exact",
            pay_to=pay_to,
            price=price,
            network=network,
            extra={"name": "Dairy Cream Price API", "version": "0.1.0"},
        )

    return {
        "GET /dairy/cream/price": RouteConfig(
            accepts=_option("$0.01"),
            description=(
                "Current spot price for Class II cream, Central U.S. (USDA AMS). "
                "Returns this week's price, min, and max in USD/lb."
            ),
            extensions={
                "bazaar": {
                    "discoverable": True,
                    "category": "financial-data",
                    "tags": ["dairy", "cream", "commodity", "spot-price", "usda", "cpg"],
                }
            },
        ),
        "GET /dairy/cream/history": RouteConfig(
            accepts=_option("$0.05"),
            description=(
                "Normalized weekly price series for Class II cream, Central U.S. (USDA AMS). "
                "Up to 30 years of history in a consistent schema — no scraping required."
            ),
            extensions={
                "bazaar": {
                    "discoverable": True,
                    "category": "financial-data",
                    "tags": ["dairy", "cream", "commodity", "time-series", "historical", "usda", "cpg"],
                }
            },
        ),
        "GET /dairy/cream/forecast": RouteConfig(
            accepts=_option("$0.10"),
            description=(
                "ARIMA point forecast for Class II cream, Central U.S. (USDA AMS). "
                "Returns a price estimate per configurable horizon (up to 730 days). "
                "Trained on 30 years of weekly USDA data."
            ),
            extensions={
                "bazaar": {
                    "discoverable": True,
                    "category": "financial-data",
                    "tags": ["dairy", "cream", "commodity", "forecast", "arima", "cpg"],
                }
            },
        ),
        "GET /dairy/cream/simulation": RouteConfig(
            accepts=_option("$0.15"),
            description=(
                "Monte Carlo GBM risk simulation (10k paths) for Class II cream, Central U.S. (USDA AMS). "
                "Returns p10/p25/p50/p75/p90 risk envelope and probability of price increase "
                "per configurable horizon (up to 730 days)."
            ),
            extensions={
                "bazaar": {
                    "discoverable": True,
                    "category": "financial-data",
                    "tags": ["dairy", "cream", "commodity", "simulation", "monte-carlo", "risk", "cpg"],
                }
            },
        ),
    }
