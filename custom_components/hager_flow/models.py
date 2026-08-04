"""Data models for Hager Flow."""

from dataclasses import dataclass, field
from datetime import datetime

from mashumaro import DataClassDictMixin
from mashumaro.config import BaseConfig


# 1. Unter-Objekt: Die Adresse
@dataclass
class HagerAddress:
    country_code: str = field(metadata={"alias": "countryCode"})
    city: str
    zip: str
    street_name: str = field(metadata={"alias": "streetName"})
    street_number: str = field(metadata={"alias": "streetNumber"})
    latitude: float | None = None
    longitude: float | None = None


@dataclass(slots=True, frozen=True)
class Installation(DataClassDictMixin):
    """A Hager installation."""

    id: int
    name: str
    brand: str
    status: str
    installation_date: datetime = field(metadata={"alias": "installationDate"})
    updated_at: datetime = field(metadata={"alias": "updatedAt"})
    owner_id: int | None = field(default=None, metadata={"alias": "ownerId"})
    address: HagerAddress | None = None
    timezone: str | None = None

    class Config(BaseConfig):
        # Ignoriert Felder im JSON, die wir nicht im Code deklariert haben (z.B. "_links")
        ignore_unknown_fields = True


@dataclass(slots=True, frozen=True)
class CurrentEnergy(DataClassDictMixin):
    """Current energy values."""

    id: int
    time: datetime
    pv_production: int = field(metadata={"alias": "pvProduction"})
    direct_consumption: int = field(metadata={"alias": "directConsumption"})
    consumption: int
    grid_power: int = field(metadata={"alias": "gridPower"})
    battery_charge_power: int = field(metadata={"alias": "batteryChargePower"})
    battery_state_of_charge: int = field(metadata={"alias": "batteryStateOfCharge"})
    production: int
    external_production: int | None = field(
        default=None, metadata={"alias": "externalProduction"}
    )


@dataclass(slots=True, frozen=True)
class DailyEnergy(DataClassDictMixin):
    """Daily energy statistics."""

    pv_production: int = field(metadata={"alias": "pvProduction"})
    direct_consumption: int = field(metadata={"alias": "directConsumption"})
    consumption: int
    grid_consumption: int = field(metadata={"alias": "gridConsumption"})
    grid_feed_in: int = field(metadata={"alias": "gridFeedIn"})
    battery_charge: int | None = field(metadata={"alias": "batteryCharge"})
    battery_discharge: int = field(metadata={"alias": "batteryDischarge"})
    production: int
    external_production: int | None = field(
        default=None, metadata={"alias": "externalProduction"}
    )


@dataclass(slots=True, frozen=True)
class MonthlyEnergy(DataClassDictMixin):
    """Monthly energy statistics."""

    pv_production: int = field(metadata={"alias": "pvProduction"})
    direct_consumption: int = field(metadata={"alias": "directConsumption"})
    consumption: int
    grid_consumption: int = field(metadata={"alias": "gridConsumption"})
    grid_feed_in: int = field(metadata={"alias": "gridFeedIn"})
    battery_charge: int | None = field(metadata={"alias": "batteryCharge"})
    battery_discharge: int = field(metadata={"alias": "batteryDischarge"})
    production: int
    external_production: int | None = field(
        default=None, metadata={"alias": "externalProduction"}
    )


@dataclass(slots=True, frozen=True)
class YearlyEnergy(DataClassDictMixin):
    """Yearly energy statistics."""

    pv_production: int = field(metadata={"alias": "pvProduction"})
    direct_consumption: int = field(metadata={"alias": "directConsumption"})
    consumption: int
    grid_consumption: int = field(metadata={"alias": "gridConsumption"})
    grid_feed_in: int = field(metadata={"alias": "gridFeedIn"})
    battery_charge: int | None = field(metadata={"alias": "batteryCharge"})
    battery_discharge: int = field(metadata={"alias": "batteryDischarge"})
    production: int
    external_production: int | None = field(
        default=None, metadata={"alias": "externalProduction"}
    )


@dataclass(slots=True, frozen=True)
class TotalEnergy(DataClassDictMixin):
    """Total energy statistics."""

    pv_production: int = field(metadata={"alias": "pvProduction"})
    direct_consumption: int = field(metadata={"alias": "directConsumption"})
    consumption: int
    grid_consumption: int = field(metadata={"alias": "gridConsumption"})
    grid_feed_in: int = field(metadata={"alias": "gridFeedIn"})
    battery_charge: int | None = field(metadata={"alias": "batteryCharge"})
    battery_discharge: int = field(metadata={"alias": "batteryDischarge"})
    production: int
    external_production: int | None = field(
        default=None, metadata={"alias": "externalProduction"}
    )


@dataclass(slots=True, frozen=True)
class Battery(DataClassDictMixin):
    """Battery information."""

    state_of_charge: float | None = field(
        default=None, metadata={"alias": "batteryStateOfCharge"}
    )
    power: float | None = field(default=None, metadata={"alias": "batteryChargePower"})


@dataclass(slots=True, frozen=True)
class HagerFlowInstallationData:
    """Container to bundle all data belonging to a single installation."""

    installation: Installation
    current: CurrentEnergy
    daily: DailyEnergy
    total: TotalEnergy
