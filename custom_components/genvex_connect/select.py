"""Platform for sensor integration."""

from homeassistant.helpers.entity import Entity
from homeassistant.components.select import SelectEntity
from homeassistant.const import EntityCategory
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase
from typing import List, Dict

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_SPEED):
        new_entities.append(GenvexConnectSelectGeneric(genvexNabto, GenvexNabtoSetpointKey.FAN_SPEED, ["0", "1", "2", "3", "4"], "mdi:fan"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto,
                GenvexNabtoSetpointKey.ANTILEGIONELLA_DAY,
                [
                    "off",
                    "monday",
                    "tuesday",
                    "wednesday",
                    "thursday",
                    "friday",
                    "saturday",
                    "sunday",
                ],
                "mdi:bacteria",
                category=EntityCategory.CONFIG,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_PRIORITY):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto,
                GenvexNabtoSetpointKey.COOLING_PRIORITY,
                ["hot_water", "supply_air"],
                "mdi:priority-high",
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_OFFSET):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto,
                GenvexNabtoSetpointKey.COOLING_OFFSET,
                ["Cooling deactivated", "+0", "+1", "+2", "+3", "+4", "+5", "+7", "+10"],
                "mdi:priority-high",
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CENTRALHEAT_PUMP_MODE):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto, GenvexNabtoSetpointKey.CENTRALHEAT_PUMP_MODE, ["only_when_active", "continuous"], "mdi:pump"
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CENTRALHEAT_TYPE):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto, GenvexNabtoSetpointKey.CENTRALHEAT_TYPE, ["off", "electric", "heatpump", "both_heatpump_priority"], "mdi:heat"
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CENTRALHEAT_SELECT):
        new_entities.append(
            GenvexConnectSelectGeneric(
                genvexNabto, GenvexNabtoSetpointKey.CENTRALHEAT_SELECT, ["only_pump", "always_heating", "heating_when_low"], "mdi:heat"
            )
        )

    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CTS400_HUMIDITY_LOW_STEP):
        new_entities.append(
            GenvexConnectSelectDefinedValues(
                genvexNabto,
                GenvexNabtoSetpointKey.CTS400_HUMIDITY_LOW_STEP,
                {0: "0", 1: "1", 2: "2", 3: "3"},
                "mdi:fan",
                category=EntityCategory.CONFIG,
            )
        )
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.CTS400_HUMIDITY_HIGH_STEP):
        new_entities.append(
            GenvexConnectSelectDefinedValues(
                genvexNabto,
                GenvexNabtoSetpointKey.CTS400_HUMIDITY_HIGH_STEP,
                {2: "2", 3: "3", 4: "4"},
                "mdi:fan",
                category=EntityCategory.CONFIG,
            )
        )

    async_add_entities(new_entities)


class GenvexConnectSelectGeneric(GenvexConnectEntityBase, SelectEntity):
    def __init__(
        self,
        genvexNabto,
        valueKey,
        options: List[str],
        icon: str,
        category: EntityCategory | None = None,
        optionValues: List[int] | bool = False,
    ):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_options = options
        self._icon = icon
        self._attr_entity_category = category
        self._optionValues = optionValues

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentValue = int(self.genvexNabto.getValue(self._valueKey))
        if currentValue < 0 or currentValue > len(self._attr_options) - 1:
            return self._attr_options[0]
        return self._attr_options[currentValue]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        chosenValue = 0
        if option in self._attr_options:
            chosenValue = self._attr_options.index(option)
        self.genvexNabto.setSetpoint(self._valueKey, chosenValue)


class GenvexConnectSelectDefinedValues(GenvexConnectEntityBase, SelectEntity):
    def __init__(self, genvexNabto, valueKey, options: Dict[int, str], icon: str, category: EntityCategory | None = None):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._options_keyed = options
        self._attr_options = list(options.values())
        self._icon = icon
        self._attr_entity_category = category

    @property
    def icon(self):
        """Return the icon of the sensor."""
        return self._icon

    @property
    def current_option(self) -> str | None:
        """Return the selected entity option to represent the entity state."""
        currentValue = int(self.genvexNabto.getValue(self._valueKey))
        if currentValue not in self._options_keyed:
            return self._attr_options[0]
        return self._attr_options[list(self._options_keyed.keys()).index(currentValue)]

    async def async_select_option(self, option: str) -> None:
        """Change the selected option."""
        chosenValue = 0
        if option in self._attr_options:
            chosenIndex = self._attr_options.index(option)
            chosenValue = list(self._options_keyed.keys())[chosenIndex]
        self.genvexNabto.setSetpoint(self._valueKey, chosenValue)
