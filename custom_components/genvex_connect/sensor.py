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

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_SUPPLY):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_SUPPLY
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_EXTRACT
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_OUTSIDE):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_OUTSIDE
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXHAUST):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_EXHAUST
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_ROOM):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_ROOM
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_CONDENSER):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_CONDENSER
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EVAPORATOR):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.TEMP_EVAPORATOR
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HOTWATER_TOP):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.HOTWATER_TOP
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HOTWATER_BOTTOM):
        new_entities.append(
            GenvexConnectSensorTemperature(
                genvexNabto, GenvexNabtoDatapointKey.HOTWATER_BOTTOM
            )
        )

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HUMIDITY):
        new_entities.append(
            GenvexConnectSensorHumidity(genvexNabto, GenvexNabtoDatapointKey.HUMIDITY)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY):
        new_entities.append(
            GenvexConnectSensorDutycycle(
                genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT):
        new_entities.append(
            GenvexConnectSensorDutycycle(
                genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.RPM_SUPPLY):
        new_entities.append(
            GenvexConnectSensorRPM(genvexNabto, GenvexNabtoDatapointKey.RPM_SUPPLY)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.RPM_EXTRACT):
        new_entities.append(
            GenvexConnectSensorRPM(genvexNabto, GenvexNabtoDatapointKey.RPM_EXTRACT)
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_DAYS):
        new_entities.append(
            GenvexConnectSensorFilterdays(
                genvexNabto, GenvexNabtoSetpointKey.FILTER_DAYS, "d"
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_MONTHS):
        new_entities.append(
            GenvexConnectSensorFilterdays(
                genvexNabto, GenvexNabtoSetpointKey.FILTER_MONTHS, "m"
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.FILTER_DAYS_LEFT):
        new_entities.append(
            GenvexConnectSensorFilterdays(
                genvexNabto, GenvexNabtoDatapointKey.FILTER_DAYS_LEFT, "d"
            )
        )

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DEFORST_TIMESINCELAST):
        new_entities.append(
            GenvexConnectSensorFilterdays(
                genvexNabto, GenvexNabtoDatapointKey.DEFORST_TIMESINCELAST, ""
            )
        )

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CO2_LEVEL):
        new_entities.append(
            GenvexConnectSensorCO2(genvexNabto, GenvexNabtoDatapointKey.CO2_LEVEL)
        )

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CONTROLSTATE_602):
        new_entities.append(
            GenvexConnectSensorControlState602(
                genvexNabto, GenvexNabtoDatapointKey.CONTROLSTATE_602
            )
        )
    async_add_entities(new_entities)


class GenvexConnectSensorTemperature(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvexNabto.getValue(self._valueKey)


class GenvexConnectSensorHumidity(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = "%"
        self._attr_device_class = SensorDeviceClass.HUMIDITY
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvexNabto.getValue(self._valueKey)


class GenvexConnectSensorCO2(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SensorDeviceClass.CO2
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvexNabto.getValue(self._valueKey)


class GenvexConnectSensorDutycycle(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"


class GenvexConnectSensorRPM(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = "rpm"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 0

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"


class GenvexConnectSensorFilterdays(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey, unit):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_native_unit_of_measurement = unit
        self._attr_state_class = SensorStateClass.MEASUREMENT

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:air-filter"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"


class GenvexConnectSensorControlState602(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [
            "state_0",
            "state_1",
            "state_2",
            "state_3",
            "state_4",
            "state_5",
            "state_6",
            "state_7",
            "state_8",
            "state_9",
            "state_10",
            "state_11",
            "state_12",
            "state_13",
            "state_14",
            "state_15",
            "state_16",
            "state_17",
        ]
        self._attr_native_value = "state_0"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{self.genvexNabto.getValue(self._valueKey)}"
