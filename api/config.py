from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # CDP facilitator required for Bazaar discovery indexing
    x402_facilitator_url: str = "https://api.cdp.coinbase.com/platform/v2/x402"
    x402_pay_to_address: str = ""
    # CAIP-2 format — see .env.example for options
    x402_network: str = "eip155:8453"

    # CDP API keys — required for authenticated CDP facilitator requests
    cdp_api_key_id: str = ""
    cdp_api_key_secret: str = ""  # EC P-256 private key PEM; use \n for newlines in .env

    # Set to true to skip x402 payment checks locally
    dev_bypass_x402: bool = False

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


settings = Settings()
