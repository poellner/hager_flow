"""Common fixtures for the Hager Flow tests."""

from collections.abc import Generator
from datetime import datetime
from unittest.mock import AsyncMock, patch

import pytest

from custom_components.hager_flow.models import HagerAddress, Installation


@pytest.fixture
def mock_setup_entry() -> Generator[AsyncMock]:
    """Override async_setup_entry."""
    with patch(
        "homeassistant.components.hager_flow.async_setup_entry", return_value=True
    ) as mock_setup_entry:
        yield mock_setup_entry


@pytest.fixture(autouse=True)
def auto_enable_custom_integrations(enable_custom_integrations):
    """Schaltet das Schutzschild aus und erlaubt Custom Components in allen Tests."""
    yield


@pytest.fixture
def mock_hager_flow_api():
    """Mockt den Hager Flow API-Client für alle Tests."""
    # HINWEIS: Passe den Pfad unten an deine tatsächliche API-Klasse an.
    # Wenn deine Klasse z. B. "HagerFlowAPI" heißt und in config_flow.py importiert wird:
    with patch(
        "custom_components.hager_flow.config_flow.HagerFlowApi", autospec=True
    ) as mock_client:
        client = mock_client.return_value

        # 1. Wir mocken die Authentifizierung (falls vorhanden)
        client.authenticate = AsyncMock(return_value=True)

        # 2. Wir mocken deine "get_installations"-Methode
        # Falls get_installations asynchron ist (async def):
        # Wir bauen das Objekt exakt so nach, wie deine Library es tun würde:
        test_installation = Installation(
            id=123456,
            name="My Installation",
            brand="Hager",
            owner_id=123456,
            status="ok",
            address=HagerAddress(
                country_code="DEU",
                city="Osnabrück",
                zip="49090",
                street_name="Ursula-Flick-Straße",
                street_number="8a",
                latitude=52.2885,
                longitude=8.0157,
            ),
            timezone="Europe/Berlin",
            installation_date=datetime.now(),
            updated_at=datetime.now(),
        )

        # Wir geben die Liste mit unserem Test-Objekt zurück
        client.get_installations = AsyncMock(return_value=[test_installation])

        yield client
