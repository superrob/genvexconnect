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
    # Air supply level sliders
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
    # Boost time
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BOOST_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BOOST_TIME))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.HOTWATER_TEMP):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.HOTWATER_TEMP))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.HOTWATER_BOOSTTEMP):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.HOTWATER_BOOSTTEMP))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_DAYS_SETTING):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_DAYS_SETTING))

        
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLYAIR_MIN_TEMP_SUMMER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLYAIR_MIN_TEMP_SUMMER))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLYAIR_MAX_TEMP_SUMMER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLYAIR_MAX_TEMP_SUMMER))

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SETPOINT):
        new_entities.append(GenvexConnectNumberSetpointTemperature(genvexNabto, GenvexNabtoSetpointKey.TEMP_SETPOINT))

    async_add_entities(new_entities)
        

class GenvexConnectNumber(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
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
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"

class GenvexConnectNumberSetpointTemperature(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, f"{valueKey}_slider", valueKey)
        self._valueKey = valueKey
        self._attr_device_class = NumberDeviceClass.TEMPERATURE
        self._attr_native_min_value = genvexNabto.getSetpointMinValue(valueKey)
        self._attr_native_max_value = genvexNabto.getSetpointMaxValue(valueKey)
        self._attr_native_step = genvexNabto.getSetpointStep(valueKey)
 
    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvexNabto.setSetpoint(self._valueKey, value)
    
    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"