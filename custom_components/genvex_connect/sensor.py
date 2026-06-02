"""Platform for sensor integration."""

from typing import Callable
from homeassistant.helpers.entity import Entity
from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorStateClass,
)
from homeassistant.const import UnitOfTemperature, EntityCategory
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
                defaultEnabled=False,
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

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.TEMP_FROSTPROTECTION):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.TEMP_FROSTPROTECTION,
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
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_OPTIMA314_1):
        alarmHandler = GenvexConnectOptima314AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorOptima314AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorAlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_OPTIMA270_1):
        alarmHandler = GenvexConnectOptima270AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorOptima270AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorAlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_OPTIMA25X):
        alarmHandler = GenvexConnectOptima25XAlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorOptima25XAlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorAlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_CTS400CRITICAL):
        alarmHandler = GenvexConnectCTS400AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorCTS400AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorAlarmCount(genvexNabto, alarmHandler))
        # Trigger the alarm handler to react on the starting state
        alarmHandler._on_change(0, 0)
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.ALARM_CTS602NO1):
        alarmHandler = GenvexConnectCTS602AlarmHandler(genvexNabto)
        new_entities.append(GenvexConnectSensorCTS602AlarmList(genvexNabto, alarmHandler))
        new_entities.append(GenvexConnectSensorAlarmCount(genvexNabto, alarmHandler))
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
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.SACRIFICIAL_ANODE):
        new_entities.append(GenvexConnectSensorSacrificialAnode(genvexNabto, GenvexNabtoDatapointKey.SACRIFICIAL_ANODE))

    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CENTRALHEAT_TEMP_SUPPLY):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.CENTRALHEAT_TEMP_SUPPLY,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoDatapointKey.CENTRALHEAT_TEMP_RETURN):
        new_entities.append(
            GenvexConnectSensorGeneric(
                genvexNabto,
                GenvexNabtoDatapointKey.CENTRALHEAT_TEMP_RETURN,
                unitOfMeasurement=UnitOfTemperature.CELSIUS,
                deviceClass=SensorDeviceClass.TEMPERATURE,
            )
        )

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET):
        new_entities.append(GenvexConnectSensorOptimaBypassOffset(genvexNabto))
        if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_FORCE_TEMP):
            new_entities.append(GenvexConnectSensorOptimaBypassForceTemp(genvexNabto))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_TURNOFF):
        new_entities.append(GenvexConnectSensorOptimaBypassTurnoff(genvexNabto))

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


class GenvexConnectSensorSacrificialAnode(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SensorDeviceClass.ENUM
        self._attr_options = ["off", "on", "service", "error"]
        self._attr_native_value = "off"

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:water-opacity"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self._attr_options[int(self.genvexNabto.getValue(self._valueKey))]


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

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:heat-pump-outline"

    def update(self) -> None:
        """Fetch new state data for the sensor."""

        # Removed redundant code and made it more concise
        self._attr_native_value = f"state_{self.genvexNabto.getValue(self._valueKey)}"


class GenvexConnectOptima25XAlarmHandler:
    def __init__(self, genvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_OPTIMA25X, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        alarmBits = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_OPTIMA25X))

        self.activeAlarms = []
        for i in range(0, 16):
            if i & alarmBits:
                self.activeAlarms.append(pow(2, i))
            alarmBits >>= 1

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


class GenvexConnectSensorOptima25XAlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectOptima25XAlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmlist", "cts400_alarmlist", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
        self._alarmTextValues = {
            1: "External stop",
            2: "Change Filter",
            4: "High pressure",
            8: "Frost failure",
            16: "CommError Panel -> Controller",
            32: "External filter",
            64: "Fan speed",
            128: "Sensor error",
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
            self._attr_native_value = "No Alarms"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.getActiveAlarms()))


class GenvexConnectOptima314AlarmHandler:
    def __init__(self, genvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_OPTIMA314_1, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_OPTIMA314_2, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        lowerBits = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_OPTIMA314_1))
        higherBits = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_OPTIMA314_2))

        self.activeAlarms = []
        for i in range(0, 16):
            if i & higherBits:
                self.activeAlarms.append(pow(2, i + 16))
            higherBits >>= 1
        for i in range(0, 16):
            if i & lowerBits:
                self.activeAlarms.append(pow(2, i))
            lowerBits >>= 1

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


class GenvexConnectSensorOptima314AlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectOptima314AlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmlist", "cts400_alarmlist", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
        self._alarmTextValues = {
            2: "Change Filter",
            4: "External stop",
            8: "T1 Sensor error",
            16: "T2 Sensor error",
            32: "T3 Sensor error",
            64: "T4 Sensor error",
            128: "T5 Sensor error",
            256: "T6 Sensor error",
            512: "T7 Sensor error",
            1024: "T8 Sensor error",
            2048: "T9 Sensor error",
            4096: "Humidity sensor",
            8192: "Fire error / test",
            16384: "Supply Fan RPM ERR",
            32768: "Extract Fan RPM ERR",
            131072: "Fire error damper 1",
            262144: "Fire error damper 2",
            524288: "Fire error damper 3",
            1048576: "Fire error damper 4",
            2097152: "Fire Box 1 failure",
            4194304: "Fire Box 2 failure",
            16777216: "Internal Modbus error",
            33554432: "High pressure error",
            67108864: "Low pressure error",
            134217728: "Flow temperature error",
            268435456: "Return temperature error",
            536870912: "T10 Sensor error",
            1073741824: "T11 Sensor error",
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
            self._attr_native_value = "No Alarms"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.getActiveAlarms()))


class GenvexConnectOptima270AlarmHandler:
    def __init__(self, genvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_OPTIMA270_1, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_OPTIMA270_2, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        lowerBits = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_OPTIMA270_1))
        higherBits = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_OPTIMA270_2))

        self.activeAlarms = []
        for i in range(0, 16):
            if i & higherBits:
                self.activeAlarms.append(pow(2, i + 16))
            higherBits >>= 1
        for i in range(0, 16):
            if i & lowerBits:
                self.activeAlarms.append(pow(2, i))
            lowerBits >>= 1

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


class GenvexConnectSensorOptima270AlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectOptima270AlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmlist", "cts400_alarmlist", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
        self._alarmTextValues = {
            2: "Change Filter",
            4: "External stop",
            8: "T1 Sensor error",
            16: "T2 Sensor error",
            32: "T3 Sensor error",
            64: "T4 Sensor error",
            128: "T5 Sensor error",
            256: "T6 Sensor error",
            512: "T7 Sensor error",
            1024: "T8 Sensor error",
            2048: "T9 Sensor error",
            4096: "Humidity sensor",
            8192: "Fire error / test",
            16384: "Supply Fan RPM ERR",
            32768: "Extract Fan RPM ERR",
            65536: "Frost failure",
            131072: "Fire error damper 1",
            262144: "Fire error damper 2",
            524288: "Fire error damper 3",
            1048576: "Fire error damper 4",
            2097152: "Fire Box 1 failure",
            4194304: "Fire Box 2 failure",
            8388608: "Rotor alarm",
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
            self._attr_native_value = "No Alarms"
            return
        # Join the string representation of the active alarms
        self._attr_native_value = ", ".join(map(lambda x: self.translateKey(x), self._alarmHandler.getActiveAlarms()))


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


class GenvexConnectCTS602AlarmHandler:
    def __init__(self, genvexNabto) -> None:
        self.genvexNabto = genvexNabto
        self.activeAlarms = []
        self.updateHandlers = []
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS602NO1, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS602NO2, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoDatapointKey.ALARM_CTS602NO3, self._on_change)

    def _on_change(self, _old_value, _new_value):
        # Recalculate the active alarms
        alarm1 = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS602NO1))
        alarm2 = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS602NO2))
        alarm3 = int(self.genvexNabto.getValue(GenvexNabtoDatapointKey.ALARM_CTS602NO3))

        self.activeAlarms = []
        if alarm1 != 0:
            self.activeAlarms.append(alarm1)
        if alarm2 != 0:
            self.activeAlarms.append(alarm2)
        if alarm3 != 0:
            self.activeAlarms.append(alarm3)

        # Trigger an update of any sensors listening on this handler.
        for updateMethod in self.updateHandlers:
            updateMethod(0, 0)

    def getActiveAlarmCount(self):
        return len(self.activeAlarms)

    def getActiveAlarms(self):
        return self.activeAlarms

    def addUpdateHandler(self, updateMethod: Callable[[int, int], None]):
        self.updateHandlers.append(updateMethod)


class GenvexConnectSensorCTS602AlarmList(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto, alarmHandler: GenvexConnectCTS602AlarmHandler):
        super().__init__(genvexNabto, "cts400_alarmlist", "cts400_alarmlist", False)
        self._alarmHandler = alarmHandler
        self._alarmHandler.addUpdateHandler(self._on_change)
        self._alarmTextValues = {
            1: "01 - Hardware error",
            2: "02 - Timeout error",
            3: "03 - Firealarm activated",
            4: "04 - Pressure switch error",
            5: "05 - Open door",
            6: "06 - De-icing error",
            7: "07 - Frost in water heating element",
            8: "08 - Frost thermostat triggered",
            9: "09 - High temperature electric boiler",
            10: "10 - Overheating electric surface",
            11: "11 - Low airflow over electric surface",
            12: "12 - Thermal fuse tripped",
            13: "13 - High temperature el. supplement hot water",
            14: "14 - Main sensor defect",
            15: "15 - Low room temperature",
            16: "16 - Software error",
            17: "17 - Watchdog error",
            18: "18 - Database content changed",
            19: "19 - Change filter",
            20: "20 - Error in legionella treatment",
            21: "21 - Set date and time",
            22: "22 - Error supply air temperature",
            23: "23 - Error temperature hot water",
            24: "24 - Error temperature central heating",
            25: "Error25",
            26: "Error26",
            27: "27 - T1 short-circuited",
            28: "28 - T1 disconnected",
            29: "29 - T2 short-circuited",
            30: "30 - T2 disconnected",
            31: "31 - T3 short-circuited",
            32: "32 - T3 disconnected",
            33: "33 - T4 short-circuited",
            34: "34 - T4 disconnected",
            35: "35 - T5 short-circuited",
            36: "36 - T5 disconnected",
            37: "37 - T6 short-circuited",
            38: "38 - T6 disconnected",
            39: "39 - T7 short-circuited",
            40: "40 - T7 disconnected",
            41: "41 - T8 short-circuited",
            42: "42 - T8 disconnected",
            43: "43 - T9 short-circuited",
            44: "44 - T9 disconnected",
            45: "45 - T10 short-circuited",
            46: "46 - T10 disconnected",
            47: "47 - T11 short-circuited",
            48: "48 - T11 disconnected",
            49: "49 - T12 short-circuited",
            50: "50 - T12 disconnected",
            51: "51 - T13 short-circuited",
            52: "52 - T13 disconnected",
            53: "53 - T14 short-circuited",
            54: "54 - T14 disconnected",
            55: "55 - T15 short-circuited",
            56: "56 - T15 disconnected",
            57: "57 - T16 short-circuited",
            58: "58 - T16 disconnected",
            59: "59 - T17 short-circuited",
            60: "60 - T17 disconnected",
            61: "Error61",
            62: "Error62",
            63: "Error63",
            64: "Error64",
            65: "Error65",
            66: "Error66",
            67: "Error67",
            68: "Error68",
            69: "Error69",
            70: "70 - Anode error",
            71: "71 - Error de-icing heat exchanger",
            72: "72 - Low evaporator temperature",
            73: "73 - High pressure switch triggered",
            74: "74 - Low pressure switch triggered",
            75: "Error75",
            76: "Error76",
            77: "Error77",
            78: "Error78",
            79: "Error79",
            80: "Error80",
            81: "Error81",
            82: "Error82",
            83: "Error83",
            84: "Error84",
            85: "Error85",
            86: "Error86",
            87: "Error87",
            88: "Error88",
            89: "Error89",
            90: "Error90",
            91: "91 - Expansion PCB missing",
            92: "92 - Backup error",
            93: "Error93",
            94: "Error94",
            95: "95 - Software update error",
            96: "96 - Damper test error",
            97: "97 - FC error",
            98: "98 - T13 and T14 error",
            99: "99 - Thermal relay and FC error",
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
class GenvexConnectSensorAlarmCount(GenvexConnectEntityBase, SensorEntity):
    def __init__(
        self,
        genvexNabto,
        alarmHandler: (
            GenvexConnectCTS400AlarmHandler
            | GenvexConnectCTS602AlarmHandler
            | GenvexConnectOptima270AlarmHandler
            | GenvexConnectOptima25XAlarmHandler
            | GenvexConnectOptima314AlarmHandler
        ),
    ):
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


class GenvexConnectSensorOptimaBypassOffset(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto):
        super().__init__(genvexNabto, "diag_bypass_openoffset", "diag_bypass_openoffset", False)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.TEMP_SETPOINT, self._on_change)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:temperature"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = self.genvexNabto.getValue(GenvexNabtoSetpointKey.TEMP_SETPOINT) + self.genvexNabto.getValue(
            GenvexNabtoSetpointKey.BYPASS_OPENOFFSET
        )


class GenvexConnectSensorOptimaBypassTurnoff(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto):
        super().__init__(genvexNabto, "diag_bypass_turnoff", "diag_bypass_turnoff", False)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.BYPASS_TURNOFF, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.TEMP_SETPOINT, self._on_change)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:temperature"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        turnoff_value = self.genvexNabto.getValue(GenvexNabtoSetpointKey.BYPASS_TURNOFF)
        if turnoff_value == 0.0:
            self._attr_native_value = -60
        else:
            self._attr_native_value = self.genvexNabto.getValue(GenvexNabtoSetpointKey.TEMP_SETPOINT) - turnoff_value


class GenvexConnectSensorOptimaBypassForceTemp(GenvexConnectEntityBase, SensorEntity):
    def __init__(self, genvexNabto):
        super().__init__(genvexNabto, "diag_bypass_force_temp", "diag_bypass_force_temp", False)
        self._attr_state_class = SensorStateClass.MEASUREMENT
        self._attr_device_class = SensorDeviceClass.TEMPERATURE
        self._attr_native_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_entity_category = EntityCategory.DIAGNOSTIC
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.BYPASS_FORCE_TEMP, self._on_change)
        genvexNabto.registerUpdateHandler(GenvexNabtoSetpointKey.TEMP_SETPOINT, self._on_change)

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:temperature"

    def update(self) -> None:
        """Fetch new state data for the sensor."""
        self._attr_native_value = (
            self.genvexNabto.getValue(GenvexNabtoSetpointKey.TEMP_SETPOINT)
            + self.genvexNabto.getValue(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET)
            + self.genvexNabto.getValue(GenvexNabtoSetpointKey.BYPASS_FORCE_TEMP)
        )
