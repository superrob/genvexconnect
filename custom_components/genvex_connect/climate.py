"""Platform for Climate integration."""

import logging
from homeassistant.helpers.entity import Entity
from homeassistant.components.climate import ClimateEntity
from homeassistant.components.climate.const import (
    ClimateEntityFeature,
    HVACMode,
    FAN_OFF,
    FAN_LOW,
    FAN_MIDDLE,
    FAN_MEDIUM,
    FAN_HIGH,
    HVACAction,
)
from homeassistant.const import UnitOfTemperature
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if (
        genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_SPEED)
        and genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SETPOINT)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.HUMIDITY)
    ):
        new_entities.append(
            GenvexConnectClimate(
                genvexNabto,
                "ventilation",
                fanSetKey=GenvexNabtoSetpointKey.FAN_SPEED,
                tempSetKey=GenvexNabtoSetpointKey.TEMP_SETPOINT,
                extractAirKey=GenvexNabtoDatapointKey.TEMP_EXTRACT,
                humidityKey=GenvexNabtoDatapointKey.HUMIDITY,
            )
        )
    async_add_entities(new_entities)


class GenvexConnectClimate(GenvexConnectEntityBase, ClimateEntity):

    def __init__(
        self, genvexNabto, name, fanSetKey, tempSetKey, extractAirKey, humidityKey
    ):
        super().__init__(genvexNabto, name, fanSetKey, False)
        self._fanSetKey = fanSetKey
        self._tempSetKey = tempSetKey
        self._extractAirKey = extractAirKey
        self._humidityKey = humidityKey
        genvexNabto.registerUpdateHandler(fanSetKey, self._on_change)
        genvexNabto.registerUpdateHandler(tempSetKey, self._on_change)
        genvexNabto.registerUpdateHandler(extractAirKey, self._on_change)
        genvexNabto.registerUpdateHandler(humidityKey, self._on_change)

    @property
    def supported_features(self):
        """Return the list of supported features."""
        features = (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.FAN_MODE
        )

        return features

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:hvac"

    @property
    def hvac_modes(self):
        return [HVACMode.AUTO]

    @property
    def hvac_mode(self):
        return HVACMode.AUTO

    def set_hvac_mode(self, _hvac_mode):
        pass

    @property
    def hvac_action(self):
        if self.genvexNabto.getValue(self._fanSetKey) == 0:
            return HVACAction.OFF
        return HVACAction.FAN

    @property
    def hvac_mode(self):
        return HVACMode.AUTO

    @property
    def fan_modes(self):
        return [FAN_OFF, FAN_LOW, FAN_MIDDLE, FAN_MEDIUM, FAN_HIGH]

    @property
    def fan_mode(self):
        fanValue = self.genvexNabto.getValue(self._fanSetKey)
        if fanValue == 0:
            return FAN_OFF
        elif fanValue == 1:
            return FAN_LOW
        elif fanValue == 2:
            return FAN_MIDDLE
        elif fanValue == 3:
            return FAN_MEDIUM
        elif fanValue == 4:
            return FAN_HIGH

    async def async_set_fan_mode(self, fan_mode: str) -> None:
        _LOGGER.info(f"Wanted to set fan mode to {fan_mode}")
        speed = 2
        if fan_mode == FAN_OFF:
            speed = 0
        elif fan_mode == FAN_LOW:
            speed = 1
        elif fan_mode == FAN_MIDDLE:
            speed = 2
        elif fan_mode == FAN_MEDIUM:
            speed = 3
        elif fan_mode == FAN_HIGH:
            speed = 4
        self.genvexNabto.setSetpoint(GenvexNabtoSetpointKey.FAN_SPEED, speed)

    @property
    def temperature_unit(self):
        return UnitOfTemperature.CELSIUS

    @property
    def current_temperature(self):
        return self.genvexNabto.getValue(self._extractAirKey)

    @property
    def target_temperature(self):
        return self.genvexNabto.getValue(self._tempSetKey)

    @property
    def min_temp(self):
        return 10

    @property
    def max_temp(self):
        return 30

    async def async_set_temperature(self, **kwargs) -> None:
        """Set the target temperature"""
        self.genvexNabto.setSetpoint(
            GenvexNabtoSetpointKey.TEMP_SETPOINT, kwargs["temperature"]
        )
