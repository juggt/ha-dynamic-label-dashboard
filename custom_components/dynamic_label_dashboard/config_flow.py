from __future__ import annotations

from typing import Any

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult

from .const import DEFAULT_TITLE, DOMAIN


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
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema({
            vol.Optional("summary_labels", default=", ".join(self.config_entry.options.get("summary_labels", []))): str,
            vol.Optional("detail_labels", default=", ".join(self.config_entry.options.get("detail_labels", []))): str,
        })
        return self.async_show_form(step_id="init", data_schema=schema)
