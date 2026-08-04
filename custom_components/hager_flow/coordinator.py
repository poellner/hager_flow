import asyncio

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import LOGGER, DEFAULT_SCAN_INTERVAL
from .hub import HagerFlowApi
from .models import HagerFlowInstallationData, Installation


class HagerFlowCoordinator(DataUpdateCoordinator[dict[str, HagerFlowInstallationData]]):
    """Class to manage fetching data from Hager Flow API."""

    def __init__(
        self, hass: HomeAssistant, api: HagerFlowApi, installations: list[Installation]
    ) -> None:
        """Initialize."""
        super().__init__(
            hass,
            LOGGER,
            name="hager_flow",
            update_interval=DEFAULT_SCAN_INTERVAL,
        )
        self.api = api
        self.installations = installations

    async def _async_update_data(self) -> dict[str, HagerFlowInstallationData]:
        """Fetch data from API for ALL installations."""
        data: dict[str, HagerFlowInstallationData] = {}

        try:
            for inst in self.installations:
                # Parallelisiertes Abrufen von Live- und Tagesdaten für maximale Performance
                current, daily, total = await asyncio.gather(
                    self.api.get_current_energy(inst.id),
                    self.api.get_daily_energy(inst.id),
                    self.api.get_total_energy(inst.id),
                )

                data[inst.id] = HagerFlowInstallationData(
                    installation=inst, current=current, daily=daily, total=total
                )
            return data
        except Exception as err:
            raise UpdateFailed(f"Error communicating with Hager Flow API: {err}")
