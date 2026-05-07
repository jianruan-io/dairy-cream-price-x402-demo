"""x402 payment middleware — official Coinbase x402 Python SDK."""

from cdp.auth.utils.jwt import JwtOptions, generate_jwt
from x402 import x402ResourceServer
from x402.extensions.eip2612_gas_sponsoring import declare_eip2612_gas_sponsoring_extension
from x402.http import AuthHeaders, CreateHeadersAuthProvider, FacilitatorConfig, HTTPFacilitatorClient, PaymentOption, RouteConfig
from x402.mechanisms.evm.exact import ExactEvmServerScheme

from api.config import settings

_CDP_HOST = "api.cdp.coinbase.com"
_CDP_BASE = "/platform/v2/x402"


def _make_cdp_auth_provider() -> CreateHeadersAuthProvider | None:
    if not (settings.cdp_api_key_id and settings.cdp_api_key_secret):
        return None

    def _jwt(method: str, path: str) -> str:
        return generate_jwt(JwtOptions(
            api_key_id=settings.cdp_api_key_id,
            api_key_secret=settings.cdp_api_key_secret,
            request_method=method,
            request_host=_CDP_HOST,
            request_path=path,
            expires_in=120,
        ))

    def create_headers() -> dict[str, dict[str, str]]:
        return {
            "verify":    {"Authorization": f"Bearer {_jwt('POST', f'{_CDP_BASE}/verify')}"},
            "settle":    {"Authorization": f"Bearer {_jwt('POST', f'{_CDP_BASE}/settle')}"},
            "supported": {"Authorization": f"Bearer {_jwt('GET',  f'{_CDP_BASE}/supported')}"},
        }

    return CreateHeadersAuthProvider(create_headers)


def build_x402_server() -> x402ResourceServer:
    auth_provider = _make_cdp_auth_provider()
    facilitator = HTTPFacilitatorClient(FacilitatorConfig(
        url=settings.x402_facilitator_url,
        auth_provider=auth_provider,
    ))
    server = x402ResourceServer(facilitator)
    server.register("eip155:*", ExactEvmServerScheme())
    return server


def build_routes() -> dict[str, RouteConfig]:
    network = settings.x402_network
    pay_to = settings.x402_pay_to_address

    def _option(price: str) -> PaymentOption:
        return PaymentOption(
            scheme="exact",
            pay_to=pay_to,
            price=price,
            network=network,
            extra={"assetTransferMethod": "permit2"},
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
                },
                **declare_eip2612_gas_sponsoring_extension(),
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
                },
                **declare_eip2612_gas_sponsoring_extension(),
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
                },
                **declare_eip2612_gas_sponsoring_extension(),
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
                },
                **declare_eip2612_gas_sponsoring_extension(),
            },
        ),
    }
