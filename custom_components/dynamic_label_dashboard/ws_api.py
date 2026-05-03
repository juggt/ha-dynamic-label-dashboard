from __future__ import annotations

from typing import Any, Mapping

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .const import DOMAIN
from .resolver import collect_dashboard_snapshot


@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "dynamic_label_dashboard/dashboard_snapshot"})
async def websocket_dashboard_snapshot(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: Mapping[str, Any],
) -> None:
    entry_data = next(iter(hass.data.get(DOMAIN, {}).values()), {}) if hass.data.get(DOMAIN) else {}
    config = dict(entry_data.get("options") or {})
    connection.send_result(msg["id"], collect_dashboard_snapshot(hass, config))


def async_register(hass: HomeAssistant) -> None:
    websocket_api.async_register_command(hass, websocket_dashboard_snapshot)
