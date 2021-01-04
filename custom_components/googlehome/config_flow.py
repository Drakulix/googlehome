from homeassistant import config_entries
from homeassistant.core import callback
from collections import OrderedDict
from .auth import get_master_token, get_access_token
from .const import (
    DOMAIN,
    CONF_USERNAME,
    CONF_PASSWORD,
    CONF_MASTER_TOKEN,
    CONF_DEVICE_TYPES,
    CONF_RSSI_THRESHOLD,
    CONF_TRACK_ALARMS,
    CONF_TRACK_DEVICES,
    CONF_TRACK_NEW_DEVICES,
    CONF_CONSIDER_HOME,
    DEFAULT_DEVICE_TYPES,
    DEFAULT_RSSI_THRESHOLD,
)
from homeassistant.components.device_tracker.const import DEFAULT_CONSIDER_HOME, DEFAULT_TRACK_NEW
import homeassistant.helpers.config_validation as cv
import voluptuous as vol


class GoogleHomeConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    async def async_step_user(self, user_input=None):
        errors = {}
        if user_input is not None:
            if CONF_MASTER_TOKEN in user_input:
                at = await self.hass.async_add_executor_job(
                    get_access_token, user_input[CONF_USERNAME], user_input[CONF_MASTER_TOKEN]
                )
                if at is not None:
                    return self.async_create_entry(
                        title=user_input[CONF_USERNAME],
                        data={
                            CONF_USERNAME: user_input[CONF_USERNAME],
                            CONF_MASTER_TOKEN: user_input[CONF_MASTER_TOKEN],
                        },
                    )
                else:
                    errors["base"] = "master_token_incorrect"
            else:
                mt = await self.hass.async_add_executor_job(
                    get_master_token, user_input[CONF_USERNAME], user_input[CONF_PASSWORD]
                )
                if mt is not None:
                    return self.async_create_entry(
                        title=user_input[CONF_USERNAME],
                        data={
                            CONF_USERNAME: user_input[CONF_USERNAME],
                            CONF_MASTER_TOKEN: mt,
                        },
                    )
                else:
                    errors["base"] = "auth_error"

        data_schema = OrderedDict()
        data_schema[vol.Required(CONF_USERNAME)] = str
        data_schema[vol.Required(CONF_PASSWORD)] = str
        data_schema[vol.Optional(CONF_MASTER_TOKEN)] = str

        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(data_schema), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return GoogleHomeOptionsFlow(config_entry)


class GoogleHomeOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry
    
    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title=self.config_entry.data[CONF_USERNAME], data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_TRACK_ALARMS, default=self.config_entry.options.get(CONF_TRACK_ALARMS, False)): bool,
                    vol.Required(CONF_TRACK_DEVICES, default=self.config_entry.options.get(CONF_TRACK_DEVICES, True)): bool,
                    #vol.Required(CONF_TRACK_NEW_DEVICES, default=self.config_entry.options.get(CONF_TRACK_NEW_DEVICES, DEFAULT_TRACK_NEW)): bool,
                    vol.Required(CONF_CONSIDER_HOME, default=self.config_entry.options.get(CONF_CONSIDER_HOME, DEFAULT_CONSIDER_HOME.total_seconds())): int,
                    vol.Required(
                        CONF_RSSI_THRESHOLD,
                        default=self.config_entry.options.get(CONF_RSSI_THRESHOLD, DEFAULT_RSSI_THRESHOLD),
                    ): int,
                    #vol.Required(
                    #    CONF_DEVICE_TYPES,
                    #    default=self.config_entry.data.get(CONF_DEVICE_TYPES, DEFAULT_DEVICE_TYPES),
                    #): [vol.In(DEFAULT_DEVICE_TYPES)],
                }
            ),
        )
