import random

from homeassistant.helpers.entity import Entity
from homeassistant.components.number import NumberDeviceClass, NumberEntity
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase
from homeassistant.const import EntityCategory, UnitOfTemperature
from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_OPENOFFSET):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BYPASS_OPENOFFSET, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_TURNOFF):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BYPASS_TURNOFF, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_FORCE_SPEED):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BYPASS_FORCE_SPEED, unitOfMessurement="%"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BYPASS_FORCE_TEMP):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BYPASS_FORCE_TEMP, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    # Air supply level sliders
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL1):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL1, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL2):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL2, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL3):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL3, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL4):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLY_AIR_LEVEL4, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL1):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL1, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL2):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL2, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL3):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL3, defaultEnabled=False))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL4):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.EXTRACT_AIR_LEVEL4, defaultEnabled=False))
    # Boost time
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BOOST_TIME):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.BOOST_TIME, deviceClass=NumberDeviceClass.DURATION, unitOfMessurement="min"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.HOTWATER_TEMP):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.HOTWATER_TEMP, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.HOTWATER_BOOSTTEMP):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.HOTWATER_BOOSTTEMP, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_DAYS_SETTING):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_DAYS_SETTING, deviceClass=NumberDeviceClass.DURATION, unitOfMessurement="d"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_MONTHS_SETTING):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.FILTER_MONTHS_SETTING))

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLYAIR_MIN_TEMP_SUMMER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLYAIR_MIN_TEMP_SUMMER, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.SUPPLYAIR_MAX_TEMP_SUMMER):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.SUPPLYAIR_MAX_TEMP_SUMMER, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_TEMPERATURE):
        new_entities.append(GenvexConnectNumberSetpointTemperature(genvexNabto, GenvexNabtoSetpointKey.COOLING_TEMPERATURE))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.TEMP_SETPOINT):
        new_entities.append(GenvexConnectNumberSetpointTemperature(genvexNabto, GenvexNabtoSetpointKey.TEMP_SETPOINT))

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CENTRALHEAT_SUPPLY_MIN):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.CENTRALHEAT_SUPPLY_MIN, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CENTRALHEAT_SUPPLY_MAX):
        new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.CENTRALHEAT_SUPPLY_MAX, deviceClass=NumberDeviceClass.TEMPERATURE, unitOfMessurement=UnitOfTemperature.CELSIUS))

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CTS400_HUMIDITY_LOW_LEVEL):
            new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.CTS400_HUMIDITY_LOW_LEVEL, deviceClass=NumberDeviceClass.HUMIDITY, unitOfMessurement="%"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CTS400_HUMIDITY_HIGH_MAX_TIME):
            new_entities.append(GenvexConnectNumber(genvexNabto, GenvexNabtoSetpointKey.CTS400_HUMIDITY_HIGH_MAX_TIME, deviceClass=NumberDeviceClass.DURATION, unitOfMessurement="min"))

    async_add_entities(new_entities)


class GenvexConnectNumber(GenvexConnectEntityBase, NumberEntity):
    def __init__(self, genvexNabto, valueKey, defaultEnabled=True, deviceClass:NumberDeviceClass|bool=False, unitOfMessurement:UnitOfTemperature|str|bool=False):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        if deviceClass:
            self._attr_device_class = deviceClass
        if unitOfMessurement is not False:
            self._attr_unit_of_measurement = unitOfMessurement
        self._attr_native_min_value = genvexNabto.getSetpointMinValue(valueKey)
        self._attr_native_max_value = genvexNabto.getSetpointMaxValue(valueKey)
        self._attr_native_step = genvexNabto.getSetpointStep(valueKey)
        self._attr_entity_category = EntityCategory.CONFIG
        self._attr_entity_registry_enabled_default = defaultEnabled

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
        self._attr_unit_of_measurement = UnitOfTemperature.CELSIUS
        self._attr_native_min_value = genvexNabto.getSetpointMinValue(valueKey)
        self._attr_native_max_value = genvexNabto.getSetpointMaxValue(valueKey)
        self._attr_native_step = genvexNabto.getSetpointStep(valueKey)

    async def async_set_native_value(self, value: float) -> None:
        """Update the current value."""
        self.genvexNabto.setSetpoint(self._valueKey, value)

    def update(self) -> None:
        """Fetch new state data for the number."""
        self._attr_native_value = f"{self.genvexNabto.getValue(self._valueKey)}"
