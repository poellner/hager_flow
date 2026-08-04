"""Test the E3/DC & Hager Flow config flow."""

from unittest.mock import AsyncMock, patch

from custom_components.hager_flow.const import (
    CONF_CLIENT_ID,
    CONF_CLIENT_SECRET,
    DOMAIN,
)
from custom_components.hager_flow.hub import ApiError, AuthenticationError
import pytest

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import HomeAssistant

# Standard-Testdaten, die das Formular absendet
MOCK_USER_INPUT = {
    CONF_CLIENT_ID: "test-client-id",
    CONF_CLIENT_SECRET: "test-client-secret",
}


async def test_setup(hass: HomeAssistant):
    """Testet, ob die Domain korrekt definiert ist."""
    assert DOMAIN == "hager_flow"


async def test_show_form(hass: HomeAssistant) -> None:
    """Test that the setup form is served."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    assert result["type"] == data_entry_flow.FlowResultType.FORM
    assert result["step_id"] == "user"
    assert result["errors"] == {}


async def test_form_success(hass: HomeAssistant, mock_hager_flow_api) -> None:
    """Test a successful config flow."""
    # 1. Schritt: Den User-Flow starten (Formular anzeigen)
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # 2. Schritt: Formular ausfüllen und absenden.
    # Wir mocken die API-Aufrufe, damit sie Erfolg (keine Exception) signalisieren.
    with (
        patch(
            "custom_components.hager_flow.config_flow.OAuthClient.get_access_token",
            return_value="mock_valid_token",
        ),
        patch(
            "custom_components.hager_flow.async_setup_entry",
            return_value=True,
        ) as mock_setup_entry,
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            MOCK_USER_INPUT,
        )
        await hass.async_block_till_done()

    # Überprüfen, ob der Eintrag erfolgreich angelegt wurde
    assert result2["type"] == data_entry_flow.FlowResultType.CREATE_ENTRY
    assert result2["title"] == "Hager Flow (My Installation)"
    assert result2["data"] == MOCK_USER_INPUT

    # Sicherstellen, dass HA danach versucht, die Integration zu laden
    assert len(mock_setup_entry.mock_calls) == 1


async def test_form_invalid_auth(hass: HomeAssistant) -> None:
    """Test that invalid credentials throw the correct error in UI."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Wir simulieren, dass der OAuthClient einen AuthenticationError wirft (z.B. Secret falsch)
    with patch(
        "custom_components.hager_flow.config_flow.OAuthClient.get_access_token",
        side_effect=AuthenticationError("Invalid secret"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            MOCK_USER_INPUT,
        )

    # Der Flow darf nicht abbrechen, sondern muss das Formular erneut mit dem Fehler anzeigen
    assert result2["type"] == data_entry_flow.FlowResultType.FORM
    assert result2["errors"] == {"base": "invalid_auth"}


async def test_form_cannot_connect(hass: HomeAssistant) -> None:
    """Test that connection issues throw the correct error in UI."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Wir simulieren einen API- oder Netzwerkfehler (z.B. Cloud offline)
    with (
        patch(
            "custom_components.hager_flow.config_flow.OAuthClient.get_access_token",
            return_value="mock_token",
        ),
        patch(
            "custom_components.hager_flow.config_flow.HagerFlowApi.get_installations",
            side_effect=ApiError("Timeout"),
        ),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            MOCK_USER_INPUT,
        )

    assert result2["type"] == data_entry_flow.FlowResultType.FORM
    assert result2["errors"] == {"base": "cannot_connect"}


async def test_form_unknown_exception(hass: HomeAssistant) -> None:
    """Test that unexpected crashes throw a generic error in UI."""
    result = await hass.config_entries.flow.async_init(
        DOMAIN, context={"source": config_entries.SOURCE_USER}
    )

    # Wir simulieren einen unvorhergesehenen Programmierfehler oder Systemfehler
    with patch(
        "custom_components.hager_flow.config_flow.OAuthClient.get_access_token",
        side_effect=RuntimeError("Unexpected system failure"),
    ):
        result2 = await hass.config_entries.flow.async_configure(
            result["flow_id"],
            MOCK_USER_INPUT,
        )

    assert result2["type"] == data_entry_flow.FlowResultType.FORM
    assert result2["errors"] == {"base": "unknown"}
