"""Platform for sensor integration."""

from typing import Callable
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
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_SUPPLY,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_SUPPLY_AFTER_HEATER):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_SUPPLY_AFTER_HEATER,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
                defaultEnabled=False
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_EXTRACT,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_OUTSIDE):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_OUTSIDE,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_HEATER):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_HEATER,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
                defaultEnabled=False,
            )
        )

    if (
        genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_SUPPLY)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        and genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_OUTSIDE)
    ):
        new_entities.append(GenvexConnectSensorEfficiency(genvexNabto))

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EXHAUST):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_EXHAUST,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_ROOM):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_ROOM,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_CONDENSER):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_CONDENSER,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_EVAPORATOR):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_EVAPORATOR,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HOTWATER_TOP):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HOTWATER_TOP,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HOTWATER_BOTTOM):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HOTWATER_BOTTOM,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HUMIDITY):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto, GenvexNabtoDatapointKey.HUMIDITY, unitOfMeasurement="%", deviceClass=SensorDeviceClass.HUMIDITY
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_SUPPLY, unitOfMeasurement="%"))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.DUTYCYCLE_EXTRACT, unitOfMeasurement="%"))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.PREHEAT_PWM):
        new_entities.append(
            GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.PREHEAT_PWM, unitOfMeasurement="%", defaultEnabled=False)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.REHEAT_PWM):
        new_entities.append(
            GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.REHEAT_PWM, unitOfMeasurement="%", defaultEnabled=False)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.RPM_SUPPLY):
        new_entities.append(
            GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.RPM_SUPPLY, unitOfMeasurement="rpm", displayPrecision=0)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.RPM_EXTRACT):
        new_entities.append(
            GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.RPM_EXTRACT, unitOfMeasurement="rpm", displayPrecision=0)
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ROTOR_SPEED):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto, GenvexNabtoDatapointKey.ROTOR_SPEED, unitOfMeasurement="rpm", displayPrecision=0, defaultEnabled=False
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.FAN_LEVEL_SUPPLY))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.FAN_LEVEL_EXTRACT))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_DAYS):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoSetpointKey.FILTER_DAYS, unitOfMeasurement="d"))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.FILTER_DAYS_LEFT):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.FILTER_DAYS_LEFT, unitOfMeasurement="d"))

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.DEFORST_TIMESINCELAST):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.DEFORST_TIMESINCELAST))

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CO2_LEVEL):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.CO2_LEVEL,
                unitOfMeasurement="ppm",
                deviceClass=SensorDeviceClass.CO2,
                defaultEnabled=False,
            )
        )

    # Device specific sensors
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CONTROLSTATE_602):
        new_entities.append(GenvexConnectSensorControlState602(genvexNabto, GenvexNabtoDatapointKey.CONTROLSTATE_602))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_OPTIMA270):
        new_entities.append(GenvexConnectSensorAlarmOptima270(genvexNabto, GenvexNabtoDatapointKey.ALARM_OPTIMA270))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_CTS400CRITICAL):
        alarmHandler = GenvexConnectCTS400AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorCTS400AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorCTS400AlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
    # CTS 602 Heatpump
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_TEMP_AFTER_CONDENSER):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HPS_TEMP_AFTER_CONDENSER,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_TEMP_BEFORE_CONDENSER):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HPS_TEMP_BEFORE_CONDENSER,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_TEMP_BUFFERTANK):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HPS_TEMP_BUFFERTANK,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_TEMP_HEATPUMP_OUTDOOR):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HPS_TEMP_HEATPUMP_OUTDOOR,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_TEMP_PRESSURE_PIPE):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.HPS_TEMP_PRESSURE_PIPE,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_CAPACITY_ACTUAL):
        new_entities.append(GenvexConnectSensorGeneric(genvexNabto, GenvexNabtoDatapointKey.HPS_CAPACITY_ACTUAL, unitOfMeasurement="%"))
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.HPS_OPERATION_STATE):
        new_entities.append(GenvexConnectSensorCTS602Heatpump(genvexNabto, GenvexNabtoDatapointKey.HPS_OPERATION_STATE))

    async_add_entities(new_entities)


class GenvexConnectSensorGeneric(GenvexConnectEntityBase, SensorEntity):
    def __init__(
        self,
        genvexNabto,
        valueKey,
        deviceClass=None,
        stateClass=SensorStateClass.MEASUREMENT,
        unitOfMeasurement=None,
        displayPrecision=None,
        defaultEnabled=True,
    ):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_state_class = stateClass
        self._attr_device_class = deviceClass
        if unitOfMeasurement:
            self._attr_native_unit_of_measurement = unitOfMeasurement
        if displayPrecision:
            self._attr_suggested_display_precision = displayPrecision
        self._attr_entity_registry_enabled_default = defaultEnabled

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvexNabto.getValue(self._valueKey)


class GenvexConnectSensorEfficiency(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto):
        super().__init__(genvexNabto, "efficiency", "efficiency", False)
        self._attr_native_unit_of_measurement = "%"
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_suggested_display_precision = 1

    @property
    def should_poll(self) -> bool:
        """HA should poll this entity"""
        return True

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:variable"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        supply = self.genvexNabto.getValue(GenvexNabtoDatapointKey.TEMP_SUPPLY)
        outside = self.genvexNabto.getValue(GenvexNabtoDatapointKey.TEMP_OUTSIDE)
        extract = self.genvexNabto.getValue(GenvexNabtoDatapointKey.TEMP_EXTRACT)
        if extract - outside == 0:
            return

        self._attr_native_value = ((supply - outside) / (extract - outside)) * 100


class GenvexConnectSensorCTS602Heatpump(GenvexConnectEntityBase, SensorEntity):
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
            "state_11" "state_12",
            "state_13",
            "state_14",
            "state_15",
            "state_16",
            "state_17",
            "state_18",
            "state_19",
            "state_20",
            "state_21",
            "state_22",
            "state_23",
            "state_24",
            "state_25",
            "state_26",
            "state_27",
            "state_28",
            "state_29",
        ]
        self._attr_native_value = "state_0"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:heat-pump-outline"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{int(self.genvexNabto.getValue(self._valueKey))}"


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
        self._attr_native_value = f"state_{int(self.genvexNabto.getValue(self._valueKey))}"


class GenvexConnectSensorAlarmOptima270(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = [
            "state_0",
            "state_1",
            "state_2",
            "state_4",
            "state_8",
            "state_16",
            "state_32",
            "state_64",
            "state_128",
            "state_256",
            "state_512",
            "state_1024",
            "state_2048",
            "state_4096",
            "state_8192",
            "state_16384",
            "state_32768",
            "state_65536",
            "state_131072",
            "state_262144",
            "state_524288",
            "state_1048576",
            "state_2097152",
            "state_4194304",
            "state_8388608",
        ]
        self._attr_native_value = "state_0"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-bell"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = f"state_{int(self.genvexNabto.getValue(self._valueKey))}"


class GenvexConnectCTS400AlarmHandler:
    def __init__(self, genvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS400CRITICAL, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS400WARNING, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS400INFO, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        criticalErrors = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS400CRITICAL))
        warningErrors = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS400WARNING))
        infoErrors = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS400INFO))

        self.activeAlarms = []
        for i in range(0, 16):
            if i & criticalErrors:
                self.activeAlarms.append(i + 48)
            criticalErrors >>= 1
        for i in range(0, 16):
            if i & warningErrors:
                self.activeAlarms.append(i + 16)
            warningErrors >>= 1
        for i in range(0, 16):
            if i & infoErrors:
                self.activeAlarms.append(i)
            infoErrors >>= 1

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmlist", "cts400_alarmlist", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
        self._alarmTextValues = {
            1: "Filterchange",
            15: "De-icing (timeout)",
            16: "T1 disconnected",
            17: "T1 short-circuited",
            18: "T2 disconnected",
            19: "T2 short-circuited",
            20: "T3 disconnected",
            21: "T3 short-circuited",
            22: "T4 disconnected",
            23: "T4 short-circuited",
            24: "T7 disconnected",
            25: "T7 short-circuited",
            26: "Failure humidity sensor",
            27: "Failure CO2 sensor",
            28: "Failure thermostat afterheating",
            29: "Frost risk afterheating",
            48: "Firedamper",
            49: "Fire",
            50: "Frost afterheating",
            51: "Low room temperature",
            52: "Emergency stop",
        }

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-light"

    def translateKey(self, key) -> str:
        if key in self._alarmTextValues:
            return self._alarmTextValues[key]
        return "Unknown alarm"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        if self._alarmHandler.getActiveAlarmCount() == 0:
            self._attr_native_value = "No Alarm"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.getActiveAlarms()))


# This sensor is more complex than the others, due to using the values of 3 datapoints.
class GenvexConnectSensorCTS400AlarmCount(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectCTS400AlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmcount", "cts400_alarmcount", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:alarm-light"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._alarmHandler.getActiveAlarmCount()
