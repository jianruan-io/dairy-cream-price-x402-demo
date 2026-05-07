variable "aws_region" {
  type    = string
  default = "us-east-1"
}

variable "app_name" {
  type    = string
  default = "dairy-cream-price-api"
}

variable "lambda_memory_size" {
  type    = number
  default = 1536
  # pmdarima/scipy/statsmodels are memory-hungry; 1536 MB is a safe floor
}

variable "lambda_timeout" {
  type    = number
  default = 30
  # API Gateway HTTP API v2 hard cap is 30s
}

# --- x402 / CDP config ---

variable "x402_facilitator_url" {
  type    = string
  default = "https://api.cdp.coinbase.com/platform/v2/x402"
}

variable "x402_pay_to_address" {
  type      = string
  sensitive = true
}

variable "x402_network" {
  type    = string
  default = "base"
}

variable "cdp_api_key_id" {
  type      = string
  sensitive = true
}

variable "cdp_api_key_secret" {
  type      = string
  sensitive = true
  description = "EC P-256 private key PEM. Use literal newlines or \\n escape in tfvars."
}

variable "dev_bypass_x402" {
  type    = bool
  default = false
}
