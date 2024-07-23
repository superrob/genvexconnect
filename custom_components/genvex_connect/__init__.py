"""The Genvex Connect integration."""

from __future__ import annotations
import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.core import HomeAssistant, Config
from homeassistant.exceptions import ConfigEntryNotReady, ConfigEntryAuthFailed

from genvexnabto import GenvexNabto, GenvexNabtoConnectionErrorType
from .const import DOMAIN, CONF_DEVICE_ID, CONF_AUTHENTICATED_EMAIL

_LOGGER = logging.getLogger(__name__)
PLATFORMS: list[Platform] = [
    Platform.SENSOR,
    Platform.BINARY_SENSOR,
    Platform.CLIMATE,
    Platform.SWITCH,
    Platform.NUMBER,
    Platform.BUTTON,
    Platform.SELECT,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Genvex Connect from a config entry."""
    if hass.data.get(DOMAIN) is None:
        hass.data.setdefault(DOMAIN, {})

    deviceID = entry.data.get(CONF_DEVICE_ID)
    authenticatedEmail = entry.data.get(CONF_AUTHENTICATED_EMAIL)

    genvexNabto = GenvexNabto(authenticatedEmail, deviceID)
    discoveryResult = await genvexNabto.waitForDiscovery()
    if discoveryResult is False:  # Waits for GenvexNabto to discover the current device IP
        raise ConfigEntryNotReady(f"Timed out while trying to discover {deviceID}")
    genvexNabto.connectToDevice()
    await genvexNabto.waitForConnection()
    _LOGGER.info(f"Controller model: {genvexNabto._device_model}")
    if genvexNabto._connection_error is not False:
        if genvexNabto._connection_error is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
            raise ConfigEntryAuthFailed(f"Credentials expired for {deviceID}")
        if genvexNabto._connection_error is GenvexNabtoConnectionErrorType.TIMEOUT:
            raise ConfigEntryNotReady(f"Timed out while trying to connect to {deviceID}")
        if genvexNabto._connection_error is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
            raise ConfigEntryNotReady(
                f"Timed out while trying to get data from {deviceID} did not correctly load a model for Model no: {genvexNabto._device_model}, device number: {genvexNabto._device_number} and slavedevice number: {genvexNabto._slavedevice_number}"
            )

    dataResult = await genvexNabto.waitForData()
    if dataResult is False:  # Waits for GenvexNabto to get fresh data
        if genvexNabto._model_adapter is None:
            raise ConfigEntryNotReady(
                f"Timed out while trying to get data from {deviceID} did not correctly load a model for Model no: {genvexNabto._device_model}, device number: {genvexNabto._device_number} and slavedevice number: {genvexNabto._slavedevice_number}"
            )
        _LOGGER.error(f"Could not get data from {deviceID} has loaded model for {genvexNabto._model_adapter.getModelName()}")
        _LOGGER.error(f"Current data available: {genvexNabto._model_adapter._values}")
        raise ConfigEntryNotReady(
            f"Timed out while trying to get data from {deviceID} has loaded model for {genvexNabto._model_adapter.getModelName()} with received data: {genvexNabto._model_adapter._values}"
        )

    hass.data[DOMAIN][entry.entry_id] = genvexNabto

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    genvexNabto.notifyAllUpdateHandlers()
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    genvexNabto = hass.data[DOMAIN][entry.entry_id]
    genvexNabto.stopListening()
    hass.data[DOMAIN].pop(entry.entry_id)
    return True


async def async_reload_entry(hass: HomeAssistant, entry: ConfigEntry):
    """Reload config entry."""
    await async_unload_entry(hass, entry)
    await async_setup_entry(hass, entry)
