"""The Hager Flow integration."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import UpdateFailed

from .const import CONF_CLIENT_ID, CONF_CLIENT_SECRET, PLATFORMS
from .coordinator import HagerFlowCoordinator
from .hub import HagerFlowApi, OAuthClient


type HagerFlowConfigEntry = ConfigEntry[HagerFlowCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: HagerFlowConfigEntry) -> bool:
    """Set up Hager Flow from a config entry."""
    session = async_get_clientsession(hass)

    oauth = OAuthClient(
        session, entry.data[CONF_CLIENT_ID], entry.data[CONF_CLIENT_SECRET]
    )
    api = HagerFlowApi(session, oauth)

    try:
        installations = await api.get_installations()
    except (OSError, ConnectionError) as err:
        raise UpdateFailed(
            f"Failed to fetch installations during setup: {err}"
        ) from err

    coordinator = HagerFlowCoordinator(hass, api, installations)
    await coordinator.async_config_entry_first_refresh()

    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: HagerFlowConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
