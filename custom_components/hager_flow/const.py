"""Constants for the Hager Flow integration."""

from datetime import timedelta
import logging
from typing import Final

from homeassistant.const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, Platform

DOMAIN: Final = "hager_flow"
LOGGER: Final = logging.getLogger(__package__)

# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------

# CONF_CLIENT_ID = "client_id"
# CONF_CLIENT_SECRET = "client_secret"
CONF_INSTALLATION_ID: Final = "installation_id"

# -----------------------------------------------------------------------------
# OAuth
# -----------------------------------------------------------------------------

AUTH_BASE_URL: Final = "https://auth.hagerenergy.com"

TOKEN_URL: Final = f"{AUTH_BASE_URL}/realms/customer/protocol/openid-connect/token"

GRANT_TYPE: Final = "client_credentials"

TOKEN_REFRESH_MARGIN: Final = timedelta(seconds=30)

# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------

API_BASE_URL: Final = "https://api.hagerenergy.com/v1"

INSTALLATIONS_ENDPOINT: Final = "/installations"

CURRENT_ENERGY_ENDPOINT: Final = "/installations/{installation_id}/energy/current"

TOTAL_ENERGY_ENDPOINT: Final = "/installations/{installation_id}/energy/total"

DAILY_ENERGY_ENDPOINT: Final = "/installations/{installation_id}/energy/daily/{day}"

MONTHLY_ENERGY_ENDPOINT: Final = (
    "/installations/{installation_id}/energy/monthly/{month}"
)

YEARLY_ENERGY_ENDPOINT: Final = "/installations/{installation_id}/energy/yearly/{year}"

# -----------------------------------------------------------------------------
# Update
# -----------------------------------------------------------------------------

DEFAULT_SCAN_INTERVAL: Final = timedelta(seconds=30)

REQUEST_TIMEOUT: Final = 20

# -----------------------------------------------------------------------------
# Device Information
# -----------------------------------------------------------------------------

MANUFACTURER: Final = "Hager Energy"

MODEL: Final = "FLOW"

# -----------------------------------------------------------------------------
# Platforms
# -----------------------------------------------------------------------------

PLATFORMS: Final = [Platform.SENSOR]

# -----------------------------------------------------------------------------
# Sensor Keys
# -----------------------------------------------------------------------------

ATTR_PV_PRODUCTION = "pvProduction"
ATTR_CONSUMPTION = "consumption"
ATTR_GRID_POWER = "gridPower"
ATTR_BATTERY_POWER = "batteryChargePower"
ATTR_BATTERY_SOC = "batteryStateOfCharge"

# -----------------------------------------------------------------------------
# Retry
# -----------------------------------------------------------------------------

MAX_RETRIES: Final = 3

RETRY_DELAY: Final = 2
