"""Platform for Binary Sensor integration."""
import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity
)
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoDatapointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities= []
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.BYPASS_ACTIVE):
        new_entities.append(GenvexConnectSensorBypass(genvexNabto, GenvexNabtoDatapointKey.BYPASS_ACTIVE))

    async_add_entities(new_entities)
        

class GenvexConnectSensorBypass(GenvexConnectEntityBase, BinarySensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_device_class = BinarySensorDeviceClass.OPENING

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:valve"

    @property
    def is_on(self) -> None:
        """Fetch new state data for the sensor."""
        return self._genvexNabto.getValue(self._valueKey)