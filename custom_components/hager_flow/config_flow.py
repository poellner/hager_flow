"""Config flow for the Hager Flow integration."""

from typing import Any

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, DOMAIN, LOGGER
from .hub import (
    ApiError,
    AuthenticationError,
    HagerFlowApi,
    NoInstallationsError,
    OAuthClient,
)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_CLIENT_ID): str,
        vol.Required(CONF_CLIENT_SECRET): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    session = async_get_clientsession(hass)
    oauth = OAuthClient(session, data[CONF_CLIENT_ID], data[CONF_CLIENT_SECRET])
    api = HagerFlowApi(session, oauth)

    try:
        # 1. Schritt: Testen, ob die OAuth-Verbindung ein Token ausgibt
        await oauth.get_access_token()

        # 2. Schritt: Testen, ob wir mit dem Token auch Daten lesen dürfen
        installations = await api.get_installations()

    except AuthenticationError as err:
        # Falsche Client ID oder falsches Secret
        raise InvalidAuth from err
    except NoInstallationsError as err:
        # Keine Anlagen im Account gefunden
        raise NoInstallations from err
    except ApiError as err:
        # Netzwerk-Timeout, Cloud offline oder API-Fehler
        raise CannotConnect from err

    # Wir nehmen die ID der ersten Anlage als Unique ID
    primary_installation = installations[0]

    # Wenn beide Schritte klappen, wird dieser Name im HA-UI angezeigt
    return {
        "title": f"Hager Flow ({primary_installation.id})",
        "unique_id": str(primary_installation.id),
    }


class HagerFlowConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hager Flow."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> config_entries.ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                # Validierung über unsere ausgelagerte Funktion
                info = await validate_input(self.hass, user_input)

                # 1. Setze die Unique ID für diesen Config Entry
                await self.async_set_unique_id(info["unique_id"])

                # 2. Prüfe, ob diese ID bereits in Home Assistant existiert.
                # Falls ja, bricht HA hier ab und zeigt "already_configured" aus deiner strings.json.
                self._abort_if_unique_id_configured()
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except NoInstallations:
                errors["base"] = "no_installations"
            except Exception:  # pylint: disable=broad-except
                LOGGER.exception("Unexpected exception during config flow setup")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["title"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""


class NoInstallations(HomeAssistantError):
    """Error to indicate no installations were found."""
