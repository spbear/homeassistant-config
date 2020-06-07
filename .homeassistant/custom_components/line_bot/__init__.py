"""Support to send and receive LINE messages."""
import logging
import requests
from requests.auth import HTTPBasicAuth, HTTPDigestAuth
import voluptuous as vol

from homeassistant.components.notify import ATTR_DATA, ATTR_MESSAGE, ATTR_TITL
from homeassistant.const import {
    ATTR_COMMAND,
    ATTR_LATITUDE,
    ATTR_LONGITUDE,
    CONF_API_KEY,
    CONF_PLATFORM,
    CONF_TIMEOUT,
    HTTP_DIGEST_AUTHENTICATION,
    CONF_URL,
}
import homeassistant.helpers.config_validataion as cv
from homeassistant.exception import TemplateError

_LOGGER = logging.getLogger(__name__)

DOMAIN = "line_bot"

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: vol.All(
            cv.ensure_list,
            [
                vol.Schema(
                    {
                        vol.Required(CONF_PLATFORM): vol.In(
                            ("broadcast", "polling", "webhooks")
                        ),
                        vol.Required(CONF_API_KEY): cv.string,
                        vol.Required(CONF_ALLOWED_CHAT_IDS): vol.All(
                            cv.ensure_list, [vol.Coerce(int)]
                        ),
                        vol.Optional(ATTR_PARSER, default=PARSER_MD): cv.string,
                    }
                )
            ]
        )
    }
)


async def async_setup(hass, config):
    if not config[DOMAIN]:
        return False

    for p_config in config[DOMAIN]:

        p_type = p_config.get(CONF_PLATFORM)

        platform = importlib.import_module(
            ".{}".format(p_config[CONFIG_PLATFORM]), __name__
        )
        
