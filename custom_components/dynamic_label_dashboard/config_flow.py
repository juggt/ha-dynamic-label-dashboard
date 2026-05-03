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

    # Options flow intentionally disabled for now.
    # Configuration will move into the dashboard UI itself once the first
    # usable panel is in place.
