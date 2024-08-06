"""Platform for sensor integration."""

from homeassistant.helpers.entity import Entity
from homeassistant.components.select import SelectEntity
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_SPEED):
        new_entities.append(GenvexConnectSelectFanLevel(genvexNabto, GenvexNabtoSetpointKey.FAN_SPEED))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY):
        new_entities.append(GenvexConnectSelectAntilegionellaDay(genvexNabto, GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_PRIORITY):
        new_entities.append(GenvexConnectSelectCoolingPriority(genvexNabto, GenvexNabtoSetpointKey.COOLING_PRIORITY))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_OFFSET):
        new_entities.append(GenvexConnectSelectCoolingOffset(genvexNabto, GenvexNabtoSetpointKey.COOLING_OFFSET))

    async_add_entities(new_entities)


class GenvexConnectSelectFanLevel(GenvexConnectEntityBase, SelectEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, f"{valueKey}_select", valueKey)
        self._valueKey = valueKey
        self._attr_options = ["Level 0", "Level 1", "Level 2", "Level 3", "Level 4"]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:fan"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentFanvalue = int(self.genvexNabto.getValue(self._valueKey))
        if currentFanvalue < 0 or currentFanvalue > 4:
            return "Level 0"
        return self._attr_options[currentFanvalue]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        fanLevel = 0
        if option in self._attr_options:
            fanLevel = self._attr_options.index(option)
        self.genvexNabto.setSetpoint(self._valueKey, fanLevel)


class GenvexConnectSelectAntilegionellaDay(GenvexConnectEntityBase, SelectEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_options = [
            "Off",
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday",
        ]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:bacteria"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentValue = int(self.genvexNabto.getValue(self._valueKey))
        if currentValue < 0 or currentValue > 7:
            return "Off"
        return self._attr_options[currentValue]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        day = 0
        if option in self._attr_options:
            day = self._attr_options.index(option)
        self.genvexNabto.setSetpoint(self._valueKey, day)


class GenvexConnectSelectCoolingPriority(GenvexConnectEntityBase, SelectEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_options = ["Hot water", "Supply air"]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:priority-high"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentValue = int(self.genvexNabto.getValue(self._valueKey))
        if currentValue < 0 or currentValue > 1:
            return "Hot water"
        return self._attr_options[currentValue]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        value = 0
        if option in self._attr_options:
            value = self._attr_options.index(option)
        self.genvexNabto.setSetpoint(self._valueKey, value)


class GenvexConnectSelectCoolingOffset(GenvexConnectEntityBase, SelectEntity):
    def __init__(self, genvexNabto, valueKey):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_options = ["Cooling deactivated", "+0", "+1", "+2", "+3", "+4", "+5", "+7", "+10"]

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return "mdi:priority-high"

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentValue = int(self.genvexNabto.getValue(self._valueKey))
        if currentValue < 0 or currentValue > 8:
            return "Cooling deactivated"
        return self._attr_options[currentValue]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        value = 0
        if option in self._attr_options:
            value = self._attr_options.index(option)
        self.genvexNabto.setSetpoint(self._valueKey, value)
