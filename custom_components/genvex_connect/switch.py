"""Platform for switch integration."""

from homeassistant.components.switch import SwitchDeviceClass, SwitchEntity
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.REHEATING):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.REHEATING, "mdi:heating-coil"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.PREHEATING):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.PREHEATING, "mdi:heating-coil"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.COOLING_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.COOLING_ENABLE, "mdi:coolant-temperature"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.HUMIDITY_CONTROL):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.HUMIDITY_CONTROL, "mdi:water-circle"))
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.BOOST_ENABLE):
        new_entities.append(GenvexConnectSwitch(genvexNabto, GenvexNabtoSetpointKey.BOOST_ENABLE, "mdi:fan-chevron-up"))

    async_add_entities(new_entities)


class GenvexConnectSwitch(GenvexConnectEntityBase, SwitchEntity):
    def __init__(self, genvexNabto, valueKey, icon):
        super().__init__(genvexNabto, valueKey, valueKey)
        self._valueKey = valueKey
        self._attr_device_class = SwitchDeviceClass.SWITCH
        self._icon = icon

    @property
    def icon(self):
        """Return the icon of the switch."""
        return self._icon

    async def async_turn_on(self, **kwargs) -> None:
        """Turn the entity on."""
        self.genvexNabto.setSetpoint(self._valueKey, 1)

    async def async_turn_off(self, **kwargs) -> None:
        """Turn the entity on."""
        self.genvexNabto.setSetpoint(self._valueKey, 0)

    @property
    def is_on(self) -> None:
        """Fetch new state data for the switch."""
        return int(self.genvexNabto.getValue(self._valueKey)) == 1
