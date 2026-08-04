"""Support for Hager Flow sensors."""

from collections.abc import Callable
from dataclasses import dataclass

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.const import PERCENTAGE, UnitOfEnergy, UnitOfPower
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

from . import HagerFlowConfigEntry
from .const import DOMAIN
from .coordinator import HagerFlowCoordinator
from .models import HagerFlowInstallationData


@dataclass(frozen=True, kw_only=True)
class HagerFlowSensorEntityDescription(SensorEntityDescription):
    """Describes Hager Flow sensor entity."""

    value_fn: Callable[[HagerFlowInstallationData], float | int | None]


# Definition aller Sensoren unter Nutzung deiner neuen Attribute
SENSOR_TYPES: tuple[HagerFlowSensorEntityDescription, ...] = (
    # --- LIVE DATEN (WATT) ---
    HagerFlowSensorEntityDescription(
        key="pv_production",
        name="PV Leistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.pv_production,
    ),
    HagerFlowSensorEntityDescription(
        key="grid_power",
        name="Netzleistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.grid_power,
    ),
    HagerFlowSensorEntityDescription(
        key="direct_consumption",
        name="Direkter Verbrauch",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.direct_consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="consumption",
        name="Gesamtverbrauch",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="battery_charge_power",
        name="Batterie Ladeleistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.battery_charge_power,
    ),
    HagerFlowSensorEntityDescription(
        key="battery_state_of_charge",
        name="Batterie Ladestand",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.battery_state_of_charge,
    ),
    HagerFlowSensorEntityDescription(
        key="production",
        name="Gesamtleistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.production,
    ),
    HagerFlowSensorEntityDescription(
        key="external_production",
        name="Externe Leistung",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda data: data.current.external_production,
    ),
    # --- STATISTIKEN FÜR ENERGIE DASHBOARD Totals (Wh) ---
    HagerFlowSensorEntityDescription(
        key="total_pv_production",
        name="PV Produktion Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,  # Wichtig fürs Energie-Dashboard!
        value_fn=lambda data: data.total.pv_production,
    ),
    HagerFlowSensorEntityDescription(
        key="total_production",
        name="Produktion Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,  # Wichtig fürs Energie-Dashboard!
        value_fn=lambda data: data.total.production,
    ),
    HagerFlowSensorEntityDescription(
        key="total_direct_consumption",
        name="Direktverbrauch Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.direct_consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="total_consumption",
        name="Verbrauch Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="total_grid_consumption",
        name="Netzbezug Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.grid_consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="total_grid_feed_in",
        name="Netzeinspeisung Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.grid_feed_in,
    ),
    HagerFlowSensorEntityDescription(
        key="total_battery_charge",
        name="Batterieladung Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.battery_charge,
    ),
    HagerFlowSensorEntityDescription(
        key="total_battery_discharge",
        name="Batterieentladung Gesamt",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.total.battery_discharge,
    ),
    # --- STATISTIKEN FÜR ENERGIE DASHBOARD (Wh) ---
    HagerFlowSensorEntityDescription(
        key="daily_pv_production",
        name="PV Produktion Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,  # Wichtig fürs Energie-Dashboard!
        value_fn=lambda data: data.daily.pv_production,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_production",
        name="Produktion Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,  # Wichtig fürs Energie-Dashboard!
        value_fn=lambda data: data.daily.production,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_direct_consumption",
        name="Direktverbrauch Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.direct_consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_consumption",
        name="Verbrauch Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_grid_consumption",
        name="Netzbezug Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.grid_consumption,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_grid_feed_in",
        name="Netzeinspeisung Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.grid_feed_in,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_battery_charge",
        name="Batterieladung Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.battery_charge,
    ),
    HagerFlowSensorEntityDescription(
        key="daily_battery_discharge",
        name="Batterieentladung Heute",
        native_unit_of_measurement=UnitOfEnergy.WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda data: data.daily.battery_discharge,
    ),
)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: HagerFlowConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up Hager Flow sensors based on a config entry."""
    coordinator = entry.runtime_data
    entities: list[HagerFlowSensor] = []

    # Dynamische Erstellung der Sensoren für jede gefundene Installation
    entities.extend(
        HagerFlowSensor(coordinator, inst_id, description)
        for inst_id in coordinator.data
        for description in SENSOR_TYPES
    )

    async_add_entities(entities)


class HagerFlowSensor(SensorEntity):
    """Representation of a Hager Flow sensor."""

    entity_description: HagerFlowSensorEntityDescription
    _attr_has_entity_name = (
        True  # Nutzt den Namen des Geräts als Präfix (Best Practice)
    )

    def __init__(
        self,
        coordinator: HagerFlowCoordinator,
        inst_id: str,
        description: HagerFlowSensorEntityDescription,
    ) -> None:
        """Initialize the sensor."""
        self.coordinator = coordinator
        self.inst_id = inst_id
        self.entity_description = description

        # Holen uns die spezifischen Anlagendaten aus dem Koordinator-Dict
        inst_info = coordinator.data[inst_id].installation

        self._attr_unique_id = f"hager_{inst_id}_{description.key}"

        # Nutzen den im UI vergebenen Namen der Anlage oder Fallback auf ID
        device_name = f"Hager Kraftwerk {inst_id}"

        self._attr_device_info = {
            "identifiers": {(DOMAIN, inst_id)},
            "name": device_name,
            "manufacturer": "Hager Energy",
            "model": "Hager Flow",
            "serial_number": str(inst_info.id),
        }

    @property
    def native_value(self) -> float | int | None:
        """Return the state of the sensor from coordinator data."""
        # Sicherstellen, dass Daten für diese Instanz existieren
        if not (data := self.coordinator.data.get(self.inst_id)):
            return None
        return self.entity_description.value_fn(data)

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return (
            self.coordinator.last_update_success
            and self.inst_id in self.coordinator.data
        )

    async def async_added_to_hass(self) -> None:
        """Connect to coordinator update signal."""
        self.async_on_remove(
            self.coordinator.async_add_listener(self.async_write_ha_state)
        )
