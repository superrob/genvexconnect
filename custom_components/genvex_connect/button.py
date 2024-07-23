"""Platform for button integration."""

from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.entity import EntityCategory
from genvexnabto import GenvexNabto, GenvexNabto, GenvexNabtoSetpointKey
from .entity import GenvexConnectEntityBase

from .const import DOMAIN


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Add sensors for passed config_entry in HA."""
    genvexNabto: GenvexNabto = hass.data[DOMAIN][config_entry.entry_id]

    new_entities = []
    if genvexNabto.providesValue(GenvexNabtoSetpointKey.FILTER_RESET):
        new_entities.append(
            GenvexConnectButton(
                genvexNabto, GenvexNabtoSetpointKey.FILTER_RESET, "mdi:air-filter"
            )
        )

    async_add_entities(new_entities)


class GenvexConnectButton(GenvexConnectEntityBase, ButtonEntity):
    def __init__(self, genvexNabto, valueKey, icon):
        super().__init__(genvexNabto, valueKey, valueKey, False)
        self._valueKey = valueKey
        self._icon = icon
        self._attr_entity_category = EntityCategory.CONFIG

    @property
    def icon(self):
        """Return the icon of the button."""
        return self._icon

    async def async_press(self) -> None:
        self.genvexNabto.setSetpoint(self._valueKey, 1)
