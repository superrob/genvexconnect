"""Platform for sensor integration."""
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities= []
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_SUPPLY):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_SUPPLY))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_EXTRACT))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_OUTSIDE):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_OUTSIDE))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXHAUST):
        new_entities.append(GenvexConnectSensorTemperature(genvexNabto, GenvexNabtoDatapointKey.TEMP_EXHAUST))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HUMIDITY):
        new_entities.append(GenvexConnectSensorHumidity(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY):
        new_entities.append(GenvexConnectSensorDutycycle(genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT):
        new_entities.append(GenvexConnectSensorDutycycle(genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT)) 
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_DAYS):
        new_entities.append(GenvexConnectSensorFilterdays(genvexNabto, GenvexNabtoSetpointKey.FILTER_DAYS, "d"))    
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_MONTHS):
        new_entities.append(GenvexConnectSensorFilterdays(genvexNabto, GenvexNabtoSetpointKey.FILTER_MONTHS, "m"))    
    async_add_entities(new_entities)
        

class GenvexConnectSensorTemperature(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._genvexNabto.getValue(self._valueKey)

class GenvexConnectSensorHumidity(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._genvexNabto.getValue(self._valueKey)

class GenvexConnectSensorDutycycle(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"{self._genvexNabto.getValue(self._valueKey)}"

class GenvexConnectSensorFilterdays(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey, unit):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._genvexNabto = genvexNabto
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:air-filter"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"{self._genvexNabto.getValue(self._valueKey)}"