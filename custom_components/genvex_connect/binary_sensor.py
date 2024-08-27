"""Platform for Binary Sensor integration."""

import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
)
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoDatapointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.BYPASS_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.BYPASS_ACTIVE,
                "mdi:valve",
                type=BinarySensorDeviceClass.OPENING,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DEFROST_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.DEFROST_ACTIVE,
                "mdi:snowflake-melt",
                type=BinarySensorDeviceClass.RUNNING,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.SUMMER_MODE):
        new_entities.append(
            GenvexConnectBinarySensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.SUMMER_MODE,
                "mdi:sun-snowflake-variant",
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.SACRIFICIAL_ANODE):
        new_entities.append(
            GenvexConnectBinarySensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.SACRIFICIAL_ANODE,
                "mdi:water-opacity",
                type=BinarySensorDeviceClass.PROBLEM,
                inverted=True,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_ACTIVE):
        new_entities.append(
            GenvexConnectBinarySensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.ALARM_ACTIVE,
                "mdi:alarm-light",
                type=BinarySensorDeviceClass.PROBLEM,
            )
        )

    async_add_entities(new_entities)


class GenvexConnectBinarySensorGeneric(GenvexConnectEntityBase, BinarySensorEntity):
    def __init__(self, genvexNabto, valueKey, icon, type=None, inverted=False):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_device_class = type
        self._inverted = inverted

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def is_on(self) -> None:
        """Fetch new state data for the sensor."""
        if self._inverted:
            return not self.genvexNabto.getValue(self._valueKey)
        return self.genvexNabto.getValue(self._valueKey)
