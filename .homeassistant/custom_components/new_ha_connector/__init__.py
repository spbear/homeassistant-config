"""New HA Connector"""
import logging
import requests
import json
import homeassistant.loader as loader

from homeassistant.helpers import discovery
from homeassistant.helpers.entity import Entity
from homeassistant.core import callback
from homeassistant.const import (
    EVENT_STATE_CHANGED,
    STATE_UNKNOWN
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "new_ha_connector"
APP_URL = "app_url"
APP_ID = "app_id"
ACCESS_TOKEN = "access_token"

SERVICE_NEW_HA_CONNECTOR = "new_ha_connector"

def getRegisteredHADeviceList(app_url, app_id, access_token):
    response = requests.get(app_url + app_id + "/getHADevices?access_token=" + access_token)
    return json.loads(response.text)['list']

def setup(hass, config):
    _LOGGER.info("Setup New HA Connector")
    hass.data[DOMAIN] = {}
    app_url = hass.data[DOMAIN][APP_URL] = config[DOMAIN].get(APP_URL)
    app_id = hass.data[DOMAIN][APP_ID] = config[DOMAIN].get(APP_ID)
    access_token = hass.data[DOMAIN][ACCESS_TOKEN] = config[DOMAIN].get(ACCESS_TOKEN)

    registerList = getRegisteredHADeviceList(app_url, app_id, access_token)

    for component in ["sensor", "binary_sensor", "switch"]:
        discovery.load_platform(hass, component, DOMAIN, {}, config)

    def event_listener(event):

        newState = event.data['new_state']
        if newState is None:
            return None

        id = newState.entity_id
        if newState.state in (STATE_UNKNOWN, '') or id not in registerList:
            return None
        '''
        lastUpdateTime = newState.last_changed.timestamp()
        if id in _memory:
            if _memory[id] == lastUpdateTime:
                return None

        _memory[id] = lastUpdateTime
        '''
        url = app_url + app_id + "/update?access_token=" + access_token + "&entity_id=" + newState.entity_id + "&value=" + newState.state;
        try:
            if newState.attributes.unit_of_measurement:
                url += "&unit=" + newState.attributes.unit_of_measurement
        except:
            url = url

        try:
            attr = json.dumps(newState.as_dict().get('attributes'))
            url += "&attr="+base64.b64encode(attr.encode()).decode()
        except:
            attr = ""

        response = requests.get(url)


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
