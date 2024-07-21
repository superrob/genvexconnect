"""Platform for sensor integration."""
from homeassistant.helpers.entity import Entity
from homeassistant.components.select import (
    SelectEntity
)
from genvexnabto import GenvexNabto, GenvexNabtoDatapointKey, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities= []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FAN_SPEED):
        new_entities.append(GenvexConnectSelectFanLevel(genvexNabto, GenvexNabtoSetpointKey.FAN_SPEED))
        
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
        if option == "Level 1":
            fanLevel = 1
        elif option == "Level 2":
            fanLevel = 2
        elif option == "Level 3":
            fanLevel = 3
        elif option == "Level 4":
            fanLevel = 4
        self.genvexNabto.setSetpoint(GenvexNabtoSetpointKey.self._valueKey, fanLevel)

    
