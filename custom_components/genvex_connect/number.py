import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.number import (
    NumberDeviceClass,
    NumberEntity
)
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase
from homeassistant.const import EntityCategory
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities= []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BYPASS_OPENOFFSET))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL1):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL1))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL2):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL2))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL3):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL3))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL4):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL4))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL1):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL1))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL2):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL2))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL3):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL3))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL4):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL4))

    async_add_entities(new_entities)
        

class GenvexConnectNumber(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_device_class = NumberDeviceClass.TEMPERATURE
        self._attr_native_min_value = genvexNabto.getSetpointMinValue(valueKey)
        self._attr_native_max_value = genvexNabto.getSetpointMaxValue(valueKey)
        self._attr_native_step = genvexNabto.getSetpointStep(valueKey)
        self._attr_entity_category = EntityCategory.CONFIG
 
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvexNabto.setSetpoint(self._valueKey, value)
    
    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = f"{self._genvexNabto.getValue(self._valueKey)}"