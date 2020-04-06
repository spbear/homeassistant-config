"""New HA Connector"""
import logging

from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.const import (
    EVENT_STATE_CHANGED,
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "new_ha_connector"

SERVICE_NEW_HA_CONNECTOR = "new_ha_connector"

def setup(hass, config):
    _LOGGER.info("Setup New HA Connector")

    async def new_ha_connector_discovered(service, discovery_info):
        """Perform action when device(s) has been found """

    discovery.listen(hass, SERVICE_NEW_HA_CONNECTOR, new_ha_connector_discovered)

    for component in ["sensor", "binary_sensor", "switch"]:
        discovery.load_platform(hass, component, DOMAIN, config, config)

    def event_listener(event):
        #_LOGGER.debug("%s", event.data['new_state'])
        return

    hass.bus.listen(EVENT_STATE_CHANGED, event_listener)

    return True

class NewSTDevice(Entity):
    """Representation a base NewSTDevice."""

    def __init__(self, device, device_type, st_hub):
        """Initialize the NewSTDevice."""
        self._state = None
        self._is_available = True
        self._sid = device["sid"]
        self._name = f"{device_type}_{self._sid}"
        self._type = device_type
        self._device_state_attributes = {}
        self._unique_id = self._name

    @property
    def name(self):
        """Return the name of the device."""
        return self._name

    @property
    def unique_id(self) -> str:
        """Return a unique ID."""
        return self._unique_id

    @property
    def available(self):
        """Return True if entity is available."""
        return self._is_available

    @property
    def should_poll(self) -> bool:
        """Return the polling state. No polling needed."""
        return False

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._device_state_attributes

    @callback
    def _async_set_unavailable(self, now):
        """Set state to UNAVAILABLE."""
        self._is_available = False

    @callback
    def _async_track_unavailable(self):
        """Track Unavailable."""
        return False

    @callback
    def push_data(self, data, raw_data):
        """Push from Hub."""
        _LOGGER.debug("PUSH >> %s: %s", self, data)
