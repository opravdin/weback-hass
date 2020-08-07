"""Support for Weback Weback Vaccums."""
import logging
import datetime

# from weback_unofficial.client import WebackApi
import weback_unofficial.vacuum as wb_vacuum

from homeassistant.components.vacuum import (
    SUPPORT_BATTERY,
    SUPPORT_CLEAN_SPOT,
    SUPPORT_FAN_SPEED,
    SUPPORT_RETURN_HOME,
    SUPPORT_SEND_COMMAND,
    SUPPORT_STATUS,
    SUPPORT_STOP,
    SUPPORT_TURN_OFF,
    SUPPORT_TURN_ON,
    VacuumEntity,
)
from homeassistant.helpers.icon import icon_for_battery_level
from homeassistant.const import CONF_SCAN_INTERVAL

from . import WEBACK_DEVICES, DOMAIN, SCAN_INTERVAL

_LOGGER = logging.getLogger(__name__)

SUPPORT_WEBACK = (
    SUPPORT_BATTERY
    | SUPPORT_RETURN_HOME
    | SUPPORT_CLEAN_SPOT
    | SUPPORT_STOP
    | SUPPORT_TURN_OFF
    | SUPPORT_TURN_ON
    | SUPPORT_STATUS
    | SUPPORT_SEND_COMMAND
    | SUPPORT_FAN_SPEED
)

ATTR_ERROR = "error"
ATTR_COMPONENT_PREFIX = "component_"


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Set up the Weback vacuums."""
    vacuums = []
    for device in hass.data[WEBACK_DEVICES]:
        vacuums.append(WebackVacuum(device, SCAN_INTERVAL))
    _LOGGER.debug("Adding Weback Vacuums to Home Assistant: %s", vacuums)
    add_entities(vacuums, True)


class WebackVacuum(VacuumEntity):
    """Weback Vacuums such as Neatsvor X500."""

    def __init__(self, device: wb_vacuum.CleanRobot, scan_interval: datetime.timedelta):
        """Initialize the Weback Vacuum."""
        self.device = device
        self.scan_interval: datetime.timedelta = scan_interval
        self.last_fetch = None
        _LOGGER.debug("Vacuum initialized: %s", self.name)

    def update(self):
        """Update device's state"""
        self.device.update()

    def on_error(self, error):
        """Handle an error event from the robot."""

        self.hass.bus.fire(
            "weback_error", {"entity_id": self.entity_id, "error": error}
        )
        self.schedule_update_ha_state()

    @property
    def should_poll(self) -> bool:
        """Return True if entity has to be polled for state."""
        if self.last_fetch is None:
            return True
        if (
            datetime.datetime.now() - self.last_fetch
        ).total_seconds() > self.scan_interval.total_seconds():
            return True
        return False

    @property
    def unique_id(self) -> str:
        """Return an unique ID."""
        return self.device.name

    @property
    def is_on(self):
        """Return true if vacuum is currently cleaning."""
        return self.device.is_cleaning

    @property
    def available(self):
        """Returns true if vacuum is online"""
        return self.device.is_available

    @property
    def is_charging(self):
        """Return true if vacuum is currently charging."""
        return self.device.current_mode in wb_vacuum.CHARGING_STATES

    @property
    def name(self):
        """Return the name of the device."""
        return self.device.nickname

    @property
    def supported_features(self):
        """Flag vacuum cleaner robot features that are supported."""
        return SUPPORT_WEBACK

    @property
    def status(self):
        """Return the status of the vacuum cleaner."""
        return self.device.state

    def return_to_base(self, **kwargs):
        """Set the vacuum cleaner to return to the dock."""
        self.device.return_home()

    @property
    def battery_icon(self):
        """Return the battery icon for the vacuum cleaner."""
        return icon_for_battery_level(
            battery_level=self.device.battery_level, charging=self.is_charging
        )

    @property
    def battery_charging(self):
        """Returns true when robot is charging"""
        return self.device.is_charging

    @property
    def battery_level(self):
        """Return the battery level of the vacuum cleaner."""
        return self.device.battery_level

    @property
    def fan_speed(self):
        """Return the fan speed of the vacuum cleaner."""
        return self.device.shadow.get("fan_status")

    @property
    def fan_speed_list(self):
        """Get the list of available fan speed steps of the vacuum cleaner."""

        return [wb_vacuum.FAN_SPEED_NORMAL, wb_vacuum.FAN_SPEED_HIGH]

    def turn_on(self, **kwargs):
        """Turn the vacuum on and start cleaning."""

        self.device.turn_on()

    def turn_off(self, **kwargs):
        """Turn the vacuum off stopping the cleaning and returning home."""
        self.return_to_base()

    def stop(self, **kwargs):
        """Stop the vacuum cleaner."""
        self.device.stop()

    def clean_spot(self, **kwargs):
        """Perform a spot clean-up."""
        self.device.publish_single("working_status", wb_vacuum.CLEAN_MODE_SPOT)

    def set_fan_speed(self, fan_speed, **kwargs):
        """Set fan speed."""
        if self.is_on:
            self.device.publish_single("fan_status", fan_speed)

    def send_command(self, command, params=None, **kwargs):
        """Send a command to a vacuum cleaner."""
        self.device.publish(params)

    @property
    def device_state_attributes(self):
        """Return the device-specific state attributes of this vacuum."""
        return {"raw_state": self.device.current_mode}
