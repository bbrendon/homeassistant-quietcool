

r'''

set_current_speed can't be called without first calling turn_on.  This is a bug in the library?

'''

import voluptuous as vol

from homeassistant.components.fan import (
    FanEntity,
    FanEntityFeature,
    PLATFORM_SCHEMA
)
from homeassistant.const import CONF_HOST
import homeassistant.helpers.config_validation as cv
from homeassistant.util.percentage import (
    ordered_list_item_to_percentage,
    percentage_to_ordered_list_item
)

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Required(CONF_HOST): cv.string
})

import logging
_LOGGER = logging.getLogger(__name__)


# Since "Off" is not a speed, we only list "Low" and "High".
ORDERED_NAMED_FAN_SPEEDS = ["Low", "High"]
SPEED_MAPPING = {"1": "Low", "3": "High"}

async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the fan platform."""
    import quietcool
    host = config.get(CONF_HOST)
    hub = await quietcool.Hub.create(host)
    fans = await hub.get_fans()
    async_add_entities(QuietcoolFan(fan) for fan in fans)

class QuietcoolFan(FanEntity):
    def __init__(self, fan):
        self._fan = fan

    @property
    def name(self):
        """Return the name of the fan."""
        return self._fan.name

    @property
    def supported_features(self):
        """Flag supported features."""
        return FanEntityFeature.SET_SPEED

    @property
    def is_on(self):
        """Return true if the entity is on."""
        return self._fan.current_power

    # @property
    # def percentage(self):
    #     """Return the current speed as a percentage."""
    #     return ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, self._fan.current_speed)

    @property
    def percentage(self):
        """Return the current speed as a percentage."""
        speed = SPEED_MAPPING.get(str(self._fan.current_speed), "Low")  # Default to "Low" if the speed is not recognized
        return ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, speed)

    @property
    def speed_count(self):
        """Return the number of speeds the fan supports."""
        return len(ORDERED_NAMED_FAN_SPEEDS) #  + 1  # +1 for 'Off'

    async def async_set_percentage(self, percentage: int):
        """Set the speed of the fan as a percentage."""

        _LOGGER.info(f"async_set_percentage: {self.name}, self.percentage: {self.percentage}")

        if percentage == 0:
            _LOGGER.info(f"async_set_percentage-percentage: {self.name}, self.percentage: {self.percentage}")
            await self.async_turn_off()
        else:
            _LOGGER.info(f"async_set_percentage-else: {self.name}, self.percentage: {self.percentage}")
            speed = percentage_to_ordered_list_item(ORDERED_NAMED_FAN_SPEEDS, percentage)

            # Convert Low/High to 1/3
            if speed == "Low":
                speed = 1
            elif speed == "High":
                speed = 3

            _LOGGER.info(f"speed: {speed}")

            await self._fan.turn_on()
            await self._fan.set_current_speed(speed)


    async def async_turn_on(self, percentage: int = None, preset_mode: str = None, **kwargs):
        """Turn on the fan."""
        _LOGGER.info(f"async_turn_on: {self.name}, percentage: {percentage}")
        _LOGGER.info("async_turn_on: turn_on")
        
        await self._fan.turn_on()

        _LOGGER.info("async_turn_on: set_current_speed")
        await self._fan.set_current_speed(1) # 1 is low.

        # TODO : Clean this up. pass percentage??
        # if percentage is not None:
        #     await self.async_set_percentage(percentage)
        # else:
        #     # If no percentage was specified, turn on to the last known speed
        #     # or default to "Low" speed.
        #     await self.async_set_percentage(self.percentage or
        #         ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, "Low"))


    # async def async_turn_on(self, percentage: int = None, **kwargs):
    #     """Turn on the fan."""
    #     await self._fan.turn_on()
    #     if percentage is not None:
    #         await self.async_set_percentage(percentage)
    #     else:
    #         # If no percentage was specified, turn on to the last known speed
    #         # or default to "Low" speed.
    #         await self.async_set_percentage(self.percentage or
    #             ordered_list_item_to_percentage(ORDERED_NAMED_FAN_SPEEDS, "Low"))

    async def async_turn_off(self, **kwargs):
        """Turn off the fan."""
        await self._fan.turn_off()
