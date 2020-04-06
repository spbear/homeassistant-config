"""New HA Connector"""

import logging
import requests
import re
import json

from homeassistant.exceptions import PlatformNotReady
from homeassistant.const import (
    CONF_AUTHENTICATION, CONF_FORCE_UPDATE, CONF_HEADERS, CONF_NAME,
    CONF_METHOD, CONF_PASSWORD, CONF_PAYLOAD, CONF_RESOURCE,
    CONF_UNIT_OF_MEASUREMENT, CONF_USERNAME,
    CONF_VALUE_TEMPLATE, CONF_VERIFY_SSL,
    HTTP_BASIC_AUTHENTICATION, HTTP_DIGEST_AUTHENTICATION, STATE_UNKNOWN,
    DEVICE_CLASS_BATTERY, DEVICE_CLASS_HUMIDITY, DEVICE_CLASS_ILLUMINANCE,
    DEVICE_CLASS_TEMPERATURE, DEVICE_CLASS_POWER
)
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.template import Template


DEVICE_CLASSES = [
    "motion",
    "tamper"
]
DEVICE_CLASS_FALSE = [
    "inactive",
    "clear"
]
DEFAULT_METHOD = 'GET'
DEFAULT_NAME = 'ST Sensor'
DEFAULT_VERIFY_SSL = True
DEFAULT_FORCE_UPDATE = False

CONF_JSON_ATTRS = 'json_attributes'
METHODS = ['POST', 'GET']

_LOGGER = logging.getLogger(__name__)

DOMAIN = "new_ha_connector"

KNOWN_DEVICES_KEY = "new_ha_connector_sensor_known_devices"

CONF_APP_URL = "app_url"
CONF_APP_ID = "app_id"
CONF_ACCESS_TOKEN = "access_token"

REMOVE_SPECIAL_CHARS = '[-=\[\]\(\)\s.#/?:$}]'


def get_device_url(config):
    app_url = config[DOMAIN].get(CONF_APP_URL)
    app_id = config[DOMAIN].get(CONF_APP_ID)
    access_token = config[DOMAIN].get(CONF_ACCESS_TOKEN)

    return app_url + app_id + "/get?access_token=" + access_token

def get_st_device(config):
    app_url = config[DOMAIN].get(CONF_APP_URL)
    app_id = config[DOMAIN].get(CONF_APP_ID)
    access_token = config[DOMAIN].get(CONF_ACCESS_TOKEN)

    url = app_url + app_id + "/getSTDevices?access_token=" + access_token

    response = requests.get(url);
    devices = json.loads(response.text)

    return devices



def setup_platform(hass, config, add_entities, discovery_info = None):
    """Set up the RESTful sensor."""
    name = config.get(CONF_NAME)
    resource = config.get(CONF_RESOURCE)
    method = config.get(CONF_METHOD)
    payload = config.get(CONF_PAYLOAD)
    verify_ssl = config.get(CONF_VERIFY_SSL)
    username = config.get(CONF_USERNAME)
    password = config.get(CONF_PASSWORD)
    headers = config.get(CONF_HEADERS)
    unit = config.get(CONF_UNIT_OF_MEASUREMENT)
    value_template = config.get(CONF_VALUE_TEMPLATE)
    json_attrs = config.get(CONF_JSON_ATTRS)
    force_update = config.get(CONF_FORCE_UPDATE)

    devices = []
    known_devices = hass.data.get(KNOWN_DEVICES_KEY)
    if known_devices is None:
        known_devices = set()
        hass.data[KNOWN_DEVICES_KEY] = known_devices

    config = discovery_info
    st_device_list = get_st_device(config)

    url = get_device_url(config)
    for item in st_device_list:
        if item['type'] != 'sensor':
            continue

        name = "nst_" + re.sub(REMOVE_SPECIAL_CHARS, '_', (item['id'].lower() + "_" + item['dni'].lower()))
        resource = url + "&dni=" + item['dni']
        value_template = Template("{{ value_json.state }}", hass)
        json_attrs = item['attr']

        rest = STData(DEFAULT_METHOD, resource, None, None, None, None)
        rest.update()

        for attr in json_attrs:
            device = name + '_' + attr
            if attr in DEVICE_CLASSES:
                add_entities([STSensor(
                    hass, rest, device, attr, unit, None, attr, DEFAULT_FORCE_UPDATE
                )], True)
                known_devices.add(device)



class STSensor(Entity):
    """Implementation of a REST sensor."""

    def __init__(self, hass, rest, name, device_class, unit_of_measurement,
                 value_template, json_attrs, force_update):
        """Initialize the REST sensor."""
        self._hass = hass
        self._rest = rest
        self._name = name
        self._uuid = name
        self._state = STATE_UNKNOWN
        self._unit_of_measurement = unit_of_measurement
        self._value_template = value_template
        self._device_class = device_class
        self._json_attrs = json_attrs
        self._attributes = None
        self._force_update = force_update

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

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
    def unique_id(self):
        """Return the unique id of this entity."""
        return f"{self._uuid}"

    @property
    def force_update(self):
        """Force update."""
        return self._force_update

    def update(self):
        """Get the latest data from REST API and update the state."""
        self._rest.update()
        _LOGGER.error("DATA: %s", self._rest.data)

        if self._rest.data is None:
            value = STATE_UNKNOWN
        elif self._rest.data['attributes'] is None:
            value = STATE_UNKNOWN
        else:
            value = self._rest.data['attributes'][self._device_class]

        if value in DEVICE_CLASS_FALSE:
            value = "off"
        else:
            value = "on"

        self._state = value

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
            _LOGGER.info("data info: %s", self.data)
        except requests.exceptions.RequestException:
            _LOGGER.error("Error fetching data: %s", self._request)
            self.data = None
