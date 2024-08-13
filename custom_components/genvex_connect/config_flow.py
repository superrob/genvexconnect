"""Config flow for Genvex Connect integration."""

from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError
from genvexnabto import GenvexNabto, GenvexNabtoConnectionErrorType

from .const import DOMAIN, CONF_DEVICE_ID, CONF_AUTHENTICATED_EMAIL, CONF_DEVICE_IP, CONF_DEVICE_PORT

_LOGGER = logging.getLogger(__name__)


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Genvex Connect."""

    VERSION = 1

    def __init__(self) -> None:
        """Initialize."""
        _LOGGER.info("Starting config flow")
        self._genvexNabto = GenvexNabto()
        self._genvexNabto.openSocket()
        self._genvexNabto.startListening()
        self._deviceID = None
        self._deviceIP = None
        self._devicePort = 5570
        self._authenticatedEmail = None

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the initial step."""
        devices = await self._genvexNabto.discoverDevices(True)
        _LOGGER.info(devices)
        return self.async_show_select_form()

    def async_show_select_form(self):
        """Show the select device form."""
        _LOGGER.info("Found %s on the network", self._genvexNabto._discovered_devices)

        deviceList = list(self._genvexNabto._discovered_devices.keys())
        deviceList += ["Manual"]
        _LOGGER.info(deviceList)

        data_schema = {
            vol.Required(
                CONF_DEVICE_ID,
            ): vol.In(deviceList),
        }

        return self.async_show_form(step_id="pick", data_schema=vol.Schema(data_schema), errors={})

    async def async_step_pick(self, user_input=None) -> ConfigFlowResult:
        """After user has picked a device"""
        _LOGGER.info("Async step user has picked {%s}", user_input)

        selectedDeviceID = user_input[CONF_DEVICE_ID][0]
        if selectedDeviceID is "M":
            return self.async_show_manual_form()

        self._deviceID = selectedDeviceID
        _LOGGER.info(
            "Previously, the user selected device %s to configure, locate it in %s",
            self._deviceID,
            self._genvexNabto._discovered_devices,
        )
        selectedDevice = self._genvexNabto._discovered_devices[self._deviceID]
        self._deviceIP = selectedDevice[0]
        self._devicePort = selectedDevice[1]
        self._genvexNabto.setDevice(self._deviceID)
        _LOGGER.info(
            "Selected %s with IP: %s and port: %s",
            self._deviceID,
            self._deviceIP,
            self._devicePort,
        )

        return self.async_show_email_form()

    def async_show_email_form(self, invalidEmail=False, connectionTimeout=False):
        """Show the email form."""
        data_schema = {
            vol.Required(
                CONF_AUTHENTICATED_EMAIL,
            ): str,
        }

        errors = {}
        if invalidEmail:
            errors["base"] = "invalid_auth"
        if connectionTimeout:
            errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="email", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_email(self, user_input=None) -> ConfigFlowResult:
        """After user has provided their email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step user has picked {%s}", user_input)

        self._authenticatedEmail = user_input[CONF_AUTHENTICATED_EMAIL]
        _LOGGER.info("User provided email: %s", self._authenticatedEmail)
        self._genvexNabto._authorized_email = self._authenticatedEmail
        self._genvexNabto.connectToDevice()
        await self._genvexNabto.waitForConnection()
        if self._genvexNabto._connection_error is not False:
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authenticatedEmail.lower() == self._authenticatedEmail:
                    return self.async_show_email_form(invalidEmail=True)
                user_input[CONF_AUTHENTICATED_EMAIL] = self._authenticatedEmail.lower()
                return await self.async_step_email(user_input)
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.TIMEOUT:
                return self.async_show_email_form(connectionTimeout=True)
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warn(
                    f"Tried to connect to device with unsupported model. Model no: {self._genvexNabto._device_model}, device number: {self._genvexNabto._device_number}, slavedevice number: {self._genvexNabto._slavedevice_number}, and slavedevice model: {self._genvexNabto._slavedevice_model}"
                )
                return self.async_abort(reason="unsupported_model")
        _LOGGER.info("Is connected to Genvex device successfully.")
        config_data = {
            CONF_DEVICE_ID: self._deviceID,
            CONF_AUTHENTICATED_EMAIL: self._authenticatedEmail,
        }
        return self.async_create_entry(title=self._deviceID, data=config_data)

    def async_show_manual_form(self, invalidEmail=False, connectionTimeout=False):
        """Show the manual form."""
        data_schema = {
            vol.Required(CONF_DEVICE_IP, default=self._deviceIP): str,
            vol.Required(CONF_DEVICE_PORT, default=self._devicePort): int,
            vol.Required(CONF_AUTHENTICATED_EMAIL, default=self._authenticatedEmail): str,
        }

        errors = {}
        if invalidEmail:
            errors["base"] = "invalid_auth"
        if connectionTimeout:
            errors["base"] = "cannot_connect"

        return self.async_show_form(step_id="manual", data_schema=vol.Schema(data_schema), errors=errors)

    async def async_step_manual(self, user_input=None) -> ConfigFlowResult:
        """After user has provided their ip, port and email. Try to connect and see if email is correct."""
        _LOGGER.info("Async step user has picked {%s}", user_input)

        self._authenticatedEmail = user_input[CONF_AUTHENTICATED_EMAIL]
        self._deviceIP = user_input[CONF_DEVICE_IP]
        self._devicePort = user_input[CONF_DEVICE_PORT]

        _LOGGER.info("User provided email: %s, ip: %s, port: %s", self._authenticatedEmail, self._deviceIP, self._devicePort)

        self._genvexNabto._authorized_email = self._authenticatedEmail
        self._genvexNabto.setManualIP(self._deviceIP, self._devicePort)
        self._deviceID = self._genvexNabto._device_id
        self._genvexNabto.connectToDevice()
        await self._genvexNabto.waitForConnection()
        if self._genvexNabto._connection_error is not False:
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.AUTHENTICATION_ERROR:
                if self._authenticatedEmail.lower() == self._authenticatedEmail:
                    return self.async_show_manual_form(invalidEmail=True)
                user_input[CONF_AUTHENTICATED_EMAIL] = self._authenticatedEmail.lower()
                return await self.async_step_manual(user_input)
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.TIMEOUT:
                return self.async_show_manual_form(connectionTimeout=True)
            if self._genvexNabto._connection_error is GenvexNabtoConnectionErrorType.UNSUPPORTED_MODEL:
                _LOGGER.warn(
                    f"Tried to connect to device with unsupported model. Model no: {self._genvexNabto._device_model}, device number: {self._genvexNabto._device_number}, slavedevice number: {self._genvexNabto._slavedevice_number}, and slavedevice model: {self._genvexNabto._slavedevice_model}"
                )
                return self.async_abort(reason="unsupported_model")
        _LOGGER.info("Is connected to Genvex device successfully.")
        config_data = {
            CONF_DEVICE_IP: self._deviceIP,
            CONF_DEVICE_PORT: self._devicePort,
            CONF_AUTHENTICATED_EMAIL: self._authenticatedEmail,
        }
        return self.async_create_entry(title=self._deviceID, data=config_data)


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
