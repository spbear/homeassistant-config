"""LINE for notify component."""
import logging

import voluptuous as vol
from line_notify import LineNotify

from homeassistant.const import ATTR_LOCATION

from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_TITLE,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)

_LOGGER = logging.getLogger(__name__)

DOMAIN = "line"
ATTR_KEYBOARD = "keyboard"
ATTR_INLINE_KEYBOARD = "inline_keyboard"
ATTR_PHOTO = "photo"
ATTR_VIDEO = "video"
ATTR_DOCUMENT = "document"

CONF_ACCESS_TOKEN = "access_token"

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({vol.Required(CONF_ACCESS_TOKEN): vol.Coerce(str)})

"""
https://notify-bot.line.me/my/
"""

def get_service(hass, config, discovery_info=None):
    """Get the LINE notification service."""
    access_token = config.get(CONF_ACCESS_TOKEN)
    return LineNotificationService(hass, access_token)


class LineNotificationService(BaseNotificationService):
    """Implement the notification service for LINE"""

    def __init__(self, hass, access_token):
        """Initialize the service."""
        self._access_token = access_token
        self.hass = hass
        self._notify = LineNotify(access_token)

    def send_message(self, message="", **kwargs):
        """Send a message to a user."""
        service_data = {ATTR_TARGET: kwargs.get(ATTR_TARGET, self._access_token)}
        if ATTR_TITLE in kwargs:
            service_data.update({ATTR_TITLE: kwargs.get(ATTR_TITLE)})
        if message:
            service_data.update({ATTR_MESSAGE: message})
        data = kwargs.get(ATTR_DATA)

        # Get keyboard info
        if data is not None and ATTR_KEYBOARD in data:
            keys = data.get(ATTR_KEYBOARD)
            keys = keys if isinstance(keys, list) else [keys]
            service_data.update(keyboard=keys)
        elif data is not None and ATTR_INLINE_KEYBOARD in data:
            keys = data.get(ATTR_INLINE_KEYBOARD)
            keys = keys if isinstance(keys, list) else [keys]
            service_data.update(inline_keyboard=keys)

        # Send a photo, video, document, or location
        if data is not None and ATTR_PHOTO in data:
            photos = data.get(ATTR_PHOTO, None)
            photos = photos if isinstance(photos, list) else [photos]
            for photo_data in photos:
                service_data.update(photo_data)
                self.hass.services.call(DOMAIN, "send_photo", service_data=service_data)
            return
        if data is not None and ATTR_VIDEO in data:
            videos = data.get(ATTR_VIDEO, None)
            videos = videos if isinstance(videos, list) else [videos]
            for video_data in videos:
                service_data.update(video_data)
                self.hass.services.call(DOMAIN, "send_video", service_data=service_data)
            return
        if data is not None and ATTR_LOCATION in data:
            service_data.update(data.get(ATTR_LOCATION))
            return self.hass.services.call(
                DOMAIN, "send_location", service_data=service_data
            )
        if data is not None and ATTR_DOCUMENT in data:
            service_data.update(data.get(ATTR_DOCUMENT))
            return self.hass.services.call(
                DOMAIN, "send_document", service_data=service_data
            )

        # Send message
        _LOGGER.debug(
            "LINE NOTIFIER calling %s.send_message with %s", DOMAIN, service_data
        )

        self._notify.send(message)

        #return self.hass.services.call(
        #    DOMAIN, "send_message", service_data=service_data
        #)
