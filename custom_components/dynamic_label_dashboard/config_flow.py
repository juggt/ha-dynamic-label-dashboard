from __future__ import annotations

import logging
from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_TITLE, DOMAIN

_LOGGER = logging.getLogger(__name__)


class DynamicLabelDashboardConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        if user_input is not None:
            await self.async_set_unique_id(DOMAIN)
            self._abort_if_unique_id_configured()
            return self.async_create_entry(title=user_input["title"], data={"title": user_input["title"]})

        schema = vol.Schema({vol.Required("title", default=DEFAULT_TITLE): str})
        return self.async_show_form(step_id="user", data_schema=schema)

    @staticmethod
    def async_get_options_flow(config_entry: config_entries.ConfigEntry) -> config_entries.OptionsFlow:
        return DynamicLabelDashboardOptionsFlow(config_entry)


class DynamicLabelDashboardOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> FlowResult:
        _LOGGER.warning("dynamic_label_dashboard: options flow opened")

        if user_input is not None:
            _LOGGER.warning("dynamic_label_dashboard: options flow submitted")
            return self.async_create_entry(title="", data={})

        try:
            schema = vol.Schema({})
            return self.async_show_form(step_id="init", data_schema=schema)
        except Exception:
            _LOGGER.exception("dynamic_label_dashboard: options flow crashed")
            raise
