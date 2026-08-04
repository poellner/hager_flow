"""API client for Hager Flow."""

import asyncio
from datetime import datetime, timedelta
import logging

import aiohttp

from homeassistant.util import dt as dt_util

from .const import (
    API_BASE_URL,
    CURRENT_ENERGY_ENDPOINT,
    DAILY_ENERGY_ENDPOINT,
    TOTAL_ENERGY_ENDPOINT,
    GRANT_TYPE,
    INSTALLATIONS_ENDPOINT,
    MAX_RETRIES,
    REQUEST_TIMEOUT,
    RETRY_DELAY,
    TOKEN_REFRESH_MARGIN,
    TOKEN_URL,
)
from .models import CurrentEnergy, DailyEnergy, Installation, TotalEnergy

_LOGGER = logging.getLogger(__name__)


class AuthenticationError(Exception):
    """Authentication failed."""


class ApiError(Exception):
    """API error."""


class NoInstallationsError(ApiError):
    """No installations found in the account."""


class OAuthClient:
    """OAuth2 Client Credentials implementation."""

    def __init__(
        self, session: aiohttp.ClientSession, client_id: str, client_secret: str
    ) -> None:
        """Initialize the OAuth client."""
        self._session = session
        self._client_id = client_id
        self._client_secret = client_secret
        self._token: str | None = None
        self._expires_at: datetime | None = None

    async def get_access_token(self) -> str:
        """Return a valid access token."""

        if (
            self._token
            and self._expires_at
            and dt_util.utcnow() < self._expires_at - TOKEN_REFRESH_MARGIN
        ):
            return self._token
        await self._refresh_token()
        if self._token is None:
            raise AuthenticationError("No access token received.")
        return self._token

    async def _refresh_token(self) -> None:
        """Request a new access token."""

        _LOGGER.debug("Requesting OAuth token")

        data = {
            "grant_type": GRANT_TYPE,
            "client_id": self._client_id,
            "client_secret": self._client_secret,
        }
        async with self._session.post(
            TOKEN_URL, data=data, timeout=REQUEST_TIMEOUT
        ) as response:
            if response.status != 200:
                raise AuthenticationError(f"OAuth failed ({response.status})")
            payload = await response.json()
        self._token = payload["access_token"]
        expires = int(payload.get("expires_in", 300))
        self._expires_at = dt_util.utcnow() + timedelta(seconds=expires)

        _LOGGER.debug(
            "Token valid until %s",
            self._expires_at.isoformat(),
        )


class HagerFlowApi:
    """Hager API."""

    def __init__(self, session: aiohttp.ClientSession, oauth: OAuthClient) -> None:
        """Initialize the Hager API client."""
        self._session = session
        self._oauth = oauth

    async def get_installations(self) -> list[Installation]:
        """Fetch all installations and parse them via Mashumaro."""
        payload = await self._get(INSTALLATIONS_ENDPOINT)
        if not payload.get("data"):
            raise NoInstallationsError("No installations found in this account.")
        return [Installation.from_dict(inst) for inst in payload["data"]]

    async def get_current_energy(self, installation_id: str) -> CurrentEnergy:
        """Fetch current energy values."""
        endpoint = CURRENT_ENERGY_ENDPOINT.format(installation_id=installation_id)
        raw_data = await self._get(endpoint)
        return CurrentEnergy.from_dict(raw_data.get("data", {}))

    async def get_daily_energy(self, installation_id: str) -> DailyEnergy:
        """Fetch daily energy statistics (for the Energy Dashboard)."""
        # Hinweis: Endpunkt-Pfad ggf. an deine API-Doku anpassen
        # endpoint = f"/v1/installations/{installation_id}/energy/daily"
        endpoint = DAILY_ENERGY_ENDPOINT.format(
            installation_id=installation_id, day=dt_util.utcnow().strftime("%Y-%m-%d")
        )
        raw_data = await self._get(endpoint)
        return DailyEnergy.from_dict(raw_data["data"]["totals"])

    async def get_total_energy(self, installation_id: str) -> TotalEnergy:
        """Fetch total energy statistics (for the Energy Dashboard)."""
        endpoint = TOTAL_ENERGY_ENDPOINT.format(installation_id=installation_id)
        raw_data = await self._get(endpoint)
        return TotalEnergy.from_dict(raw_data["data"]["totals"])

    async def _get(self, endpoint: str) -> dict:
        """Robust GET request with retries and 401 auto-recovery."""
        token = await self._oauth.get_access_token()
        headers = {"Authorization": f"Bearer {token}", "Accept": "application/json"}
        url = API_BASE_URL + endpoint

        for retry in range(MAX_RETRIES):
            try:
                async with self._session.get(
                    url, headers=headers, timeout=REQUEST_TIMEOUT
                ) as response:
                    if response.status == 401:
                        token = await self._oauth.get_access_token()
                        headers["Authorization"] = f"Bearer {token}"
                        continue
                    response.raise_for_status()
                    response_json = await response.json()
                    _LOGGER.debug("GET %s -> %s", url, response_json)
                    return response_json
            except (TimeoutError, aiohttp.ClientError) as err:
                if retry == MAX_RETRIES - 1:
                    raise ApiError(err) from err
                await asyncio.sleep(RETRY_DELAY * (retry + 1))
        raise ApiError("Unknown API error.")
