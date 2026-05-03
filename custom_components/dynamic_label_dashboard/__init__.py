from __future__ import annotations

import logging

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .http import async_register_static
from .panel import async_register_panel
from .ws_api import async_register as async_register_ws

_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    hass.data.setdefault(DOMAIN, {})
    _LOGGER.warning("dynamic_label_dashboard: async_setup called")
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.setdefault(DOMAIN, {})
    options = dict(entry.options)
    if "summary_labels" not in options:
        options["summary_labels"] = []
    if "detail_labels" not in options:
        options["detail_labels"] = []
    hass.data[DOMAIN][entry.entry_id] = {
        "config": dict(entry.data),
        "options": options,
    }
    await async_register_static(hass)
    async_register_panel(hass)
    async_register_ws(hass)
    _LOGGER.warning("dynamic_label_dashboard: setup_entry %s, panel/websocket/static registered", entry.entry_id)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    hass.data.get(DOMAIN, {}).pop(entry.entry_id, None)
    return True
