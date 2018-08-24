"""
Support for Chuang Mi IR Remote Controller.

Thank rytilahti for his great work
"""
import logging
from datetime import timedelta
import asyncio
from random import randint
import voluptuous as vol
from socket import timeout

import homeassistant.loader as loader
from homeassistant.components.switch import (SwitchDevice, PLATFORM_SCHEMA)
from homeassistant.const import (CONF_SWITCHES,
                                 CONF_COMMAND_OFF, CONF_COMMAND_ON,
                                 CONF_TIMEOUT, CONF_HOST, CONF_TOKEN,
                                 CONF_TYPE, CONF_NAME, )
import homeassistant.helpers.config_validation as cv
from homeassistant.util.dt import utcnow
from homeassistant.exceptions import PlatformNotReady

REQUIREMENTS = ['python-miio>=0.3.6']

_LOGGER = logging.getLogger(__name__)

DEVICE_DEFAULT_NAME = 'chuang_mi_ir'
SWITCH_DEFAULT_NAME = 'chuang_mi_ir_switch'
DOMAIN = "switch"
DEFAULT_TIMEOUT = 10
DEFAULT_RETRY = 3
SERVICE_LEARN = "learn_command"
SERVICE_SEND = "send_command"
ATTR_COMMAND = 'command'
ATTR_MODEL = 'model'
CONF_RETRIES = 'retries'

SWITCH_SCHEMA = vol.Schema({
    vol.Optional(CONF_COMMAND_OFF, default=None):
        vol.All(cv.string, vol.Length(min=1)),
    vol.Optional(CONF_COMMAND_ON, default=None):
        vol.All(cv.string, vol.Length(min=1)),
    vol.Optional(CONF_NAME, default=SWITCH_DEFAULT_NAME): cv.string,
})

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_SWITCHES, default={}):
        vol.Schema({cv.slug: SWITCH_SCHEMA}),
    vol.Required(CONF_HOST): cv.string,
    vol.Required(CONF_TOKEN): vol.All(cv.string, vol.Length(min=32, max=32)),
    vol.Optional(CONF_NAME, default=DEVICE_DEFAULT_NAME): cv.string,
    vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): cv.positive_int,
    vol.Optional(CONF_RETRIES, default=DEFAULT_RETRY): cv.positive_int
})

CHUANGMIIR_SERVICE_SCHEMA = vol.Schema({
    vol.Required(ATTR_COMMAND): vol.All(cv.string, vol.Length(min=1)),
})


# pylint: disable=unused-argument
def setup_platform(hass, config, add_devices, discovery_info=None):
    """Set up the smart mi fan platform."""
    from miio import ChuangmiIr, DeviceException
    host = config.get(CONF_HOST)
    token = config.get(CONF_TOKEN)
    devices = config.get(CONF_SWITCHES, {})
    retries = config.get(CONF_RETRIES)
    persistent_notification = loader.get_component('persistent_notification')

    _LOGGER.info("Initializing with host %s (token %s...)", host, token[:5])

    try:
        # The Chuang Mi IR Remote Controller wants to be re-discovered every
        # 5 minutes. As long as polling is disabled the device should be
        # re-discovered (lazy_discover=False) in front of every command.
        ir_remote = ChuangmiIr(host, token, lazy_discover=False)
        device_info = ir_remote.info()
    except DeviceException:
        _LOGGER.info("Connection failed.")
        raise PlatformNotReady

    @asyncio.coroutine
    def _learn_command(call):

        key = randint(1, 1000000)
        ir_remote.learn(key)

        _LOGGER.info(
            "Press the key to capture of your remote control")
        start_time = utcnow()
        while (utcnow() - start_time) < timedelta(seconds=DEFAULT_TIMEOUT):
            res = ir_remote.read(key)
            if res["code"]:
                log_msg = 'Captured infrared command: %s' % res["code"]
                _LOGGER.info(log_msg)
                persistent_notification.async_create(
                    hass, log_msg, title='Chuang Mi IR Remote Controller')
                return
            yield from asyncio.sleep(1, loop=hass.loop)

        log_msg = 'Timeout. No infrared command captured.'
        _LOGGER.error(log_msg)
        persistent_notification.async_create(
            hass, log_msg, title='Chuang Mi IR Remote Controller')

    @asyncio.coroutine
    def _send_command(call):
        command = str(call.data.get(ATTR_COMMAND))
        if command:
            for retry in range(retries):
                try:
                    ir_remote.play_raw(command, 38400)
                    break
                except (timeout, ValueError):
                    _LOGGER.error("Transmit infrared command failed.")
        else:
            _LOGGER.debug("Empty infrared command skipped.")

    hass.services.register(
        DOMAIN, SERVICE_LEARN + '_' + host.replace('.', '_'), _learn_command)

    hass.services.register(
        DOMAIN, SERVICE_SEND + '_' + host.replace('.', '_'), _send_command)

    switches = []
    for object_id, device_config in devices.items():
        switches.append(
            ChuangMiInfraredSwitch(
                ir_remote,
                device_config.get(CONF_NAME, object_id),
                device_config.get(CONF_COMMAND_ON),
                device_config.get(CONF_COMMAND_OFF),
                device_info
            )
        )

    add_devices(switches)


class ChuangMiInfraredSwitch(SwitchDevice):
    """Representation of an Chuang Mi IR switch."""

    def __init__(self, device, name, command_on, command_off, device_info):
        """Initialize the switch."""
        self._name = name
        self._state = False
        self._command_on = command_on or None
        self._command_off = command_off or None
        self._device_info = device_info
        self._device = device
        self._state_attrs = {
            ATTR_MODEL: self._device_info.model,
        }

    @property
    def name(self):
        """Return the name of the switch."""
        return self._name

    @property
    def assumed_state(self):
        """Return false if unable to access real state of entity."""
        return False

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes of the device."""
        return self._state_attrs

    @property
    def is_on(self):
        """Return true if device is on."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        if self._send_command(self._command_on):
            self._state = True
            self.schedule_update_ha_state()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        if self._send_command(self._command_off):
            self._state = False
            self.schedule_update_ha_state()

    def _send_command(self, command):
        """Send infrared command to device."""

        command = str(command)
        if not command:
            _LOGGER.debug("Empty infrared command skipped.")
            return True
        try:
            self._device.play_raw(command, 38400)
        except (timeout, ValueError) as error:
            _LOGGER.error(error)
            return False
        return True
