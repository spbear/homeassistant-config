"""New HA Connector"""

import logging
import requests
import re
import json

from homeassistant.exceptions import PlatformNotReady
from homeassistant.const import (
    CONF_AUTHENTICATION, CONF_FORCE_UPDATE, CONF_HEADERS, CONF_NAME,
    CONF_METHOD, CONF_PASSWORD, CONF_PAYLOAD, CONF_RESOURCE,
    TEMP_CELSIUS,
    CONF_UNIT_OF_MEASUREMENT, CONF_USERNAME,
    CONF_VALUE_TEMPLATE, CONF_VERIFY_SSL,
    HTTP_BASIC_AUTHENTICATION, HTTP_DIGEST_AUTHENTICATION, STATE_UNKNOWN,
    DEVICE_CLASS_BATTERY, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_POWER
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.template import Template


DEVICE_CLASSES = [
    DEVICE_CLASS_BATTERY,
    DEVICE_CLASS_HUMIDITY,
    DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_POWER
]

DEVICE_UNITS = {
    DEVICE_CLASS_BATTERY:'%',
    DEVICE_CLASS_HUMIDITY:'%',
    DEVICE_CLASS_ILLUMINANCE:'lux',
    DEVICE_CLASS_TEMPERATURE:TEMP_CELSIUS,
    DEVICE_CLASS_POWER:'W'
}

DEFAULT_METHOD = 'GET'
DEFAULT_NAME = 'ST Sensor'
DEFAULT_VERIFY_SSL = True
DEFAULT_FORCE_UPDATE = False

CONF_JSON_ATTRS = 'json_attributes'
METHODS = ['POST', 'GET']

_LOGGER = logging.getLogger(__name__)

DOMAIN = "new_ha_connector"
APP_URL = "app_url"
APP_ID = "app_id"
ACCESS_TOKEN = "access_token"

REMOVE_SPECIAL_CHARS = '[-=\[\]\(\)\s.#/?:$}]'


def get_device_url(hass):
    app_url = hass.data[DOMAIN].get(APP_URL)
    app_id = hass.data[DOMAIN].get(APP_ID)
    access_token = hass.data[DOMAIN].get(ACCESS_TOKEN)

    return app_url + app_id + "/get?access_token=" + access_token

def get_st_device(hass):
    app_url = hass.data[DOMAIN].get(APP_URL)
    app_id = hass.data[DOMAIN].get(APP_ID)
    access_token = hass.data[DOMAIN].get(ACCESS_TOKEN)

    url = app_url + app_id + "/getSTDevices?access_token=" + access_token

    response = requests.get(url);
    devices = json.loads(response.text)

    return devices

def setup_platform(hass, config, async_add_entities, discovery_info):
    st_device_list = get_st_device(hass)

    for item in st_device_list:
        if item['type'] != 'sensor':
            continue

        url = get_device_url(hass)
        name = "nst_" + re.sub(REMOVE_SPECIAL_CHARS, '_', (item['id'].lower() + "_" + item['dni'].lower()))
        resource_url = url + "&dni=" + item['dni']
        json_attrs = item['attr']

        for device_class in json_attrs:
            device_name = name + '_' + device_class

            if device_class in DEVICE_CLASSES:
                sensor = STSensor(device_name, device_class, resource_url, DEFAULT_FORCE_UPDATE)
                async_add_entities([sensor], True)


class STSensor(Entity):
    """Implementation of a REST sensor."""

    def __init__(self, name, device_class, resource_url, force_update):
        """Initialize the REST sensor."""
        self._name = name
        self._uuid = name
        self._state = STATE_UNKNOWN
        self._device_class = device_class
        self._unit_of_measurement = DEVICE_UNITS[device_class]
        self._attributes = None
        self._force_update = force_update
        self._rest = STData(DEFAULT_METHOD, resource_url, None, None, None, DEFAULT_VERIFY_SSL)
        self._rest.update()

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return the unique id of this entity."""
        return f"{self._uuid}"

    @property
    def unit_of_measurement(self):
        """Return the unit the value is expressed in."""
        return self._unit_of_measurement

    @property
    def available(self):
        """Return if the sensor data are available."""
        return self._rest.data is not None

    @property
    def device_class(self):
        """Return the device class."""
        return self._device_class

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def force_update(self):
        """Force update."""
        return self._force_update

    def update(self):
        """Get the latest data from REST API and update the state."""
        self._rest.update()

        if self._rest.data is None:
            value = STATE_UNKNOWN
        elif self._rest.data['attributes'] is None:
            value = STATE_UNKNOWN
        else:
            value = self._rest.data['attributes'][self._device_class]

        self._state = float(value)

    @property
    def device_state_attributes(self):
        """Return the state attributes."""
        return self._attributes


class STData(object):
    """Class for handling the data retrieval."""

    def __init__(self, method, resource, auth, headers, data, verify_ssl):
        """Initialize the data object."""
        self._request = requests.Request(
            method, resource, headers=headers, auth=auth, data=data).prepare()
        self._verify_ssl = verify_ssl
        self.data = None

    def update(self):
        """Get the latest data from REST service with provided method."""
        try:
            with requests.Session() as sess:
                response = sess.send(
                    self._request, timeout=10, verify=self._verify_ssl)

            self.data = json.loads(response.text)
        except requests.exceptions.RequestException:
            _LOGGER.error("Error fetching data: %s", self._request)
            self.data = None
