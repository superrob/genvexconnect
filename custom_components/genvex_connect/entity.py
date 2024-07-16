"""GenvexConnect base entity class"""
import logging

from typing import Optional
from genvexnabto import GenvexNabto
from homeassistant.helpers.entity import Entity


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


class GenvexConnectEntityBase(Entity):
    """Base for all GenvexConnect entities"""
    _attr_has_entity_name = True
    def __init__(
        self,
        genvexNabto: GenvexNabto,
        name: str,
        valueKey,
        useDefaultUpdateHandler: bool = True
    ) -> None:
        self.genvexNabto = genvexNabto
        self._translationKey = name
        if useDefaultUpdateHandler:
            genvexNabto.registerUpdateHandler(valueKey, self._on_change)

    @property
    def translation_key(self):
        """Return the translation key to translate the entity's name and states."""
        return self._translationKey

    @property
    def unique_id(self) -> str:
        """Return a unique ID to use for this entity."""
        return f"{self.genvexNabto._device_id}_{self._translationKey}" 

    @property
    def should_poll(self) -> bool:
        """Return false, we push changes to HA"""
        return False
    
    def _on_change(self, _old_value, _new_value):
        """Notify HA of changes"""
        if self.hass is not None:
            self.schedule_update_ha_state(force_refresh=True)

    @property
    def device_info(self):
        info = {
            "identifiers": {(DOMAIN, self.genvexNabto._device_id)},
            "name": self.genvexNabto._device_id,
            "manufacturer": self.genvexNabto._model_adapter.getManufacturer(),
            "model": self.genvexNabto._model_adapter.getModelName()
        }
        return info