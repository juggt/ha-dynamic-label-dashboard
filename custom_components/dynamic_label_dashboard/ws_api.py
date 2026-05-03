from __future__ import annotations

from typing import Any, Mapping

import voluptuous as vol
from homeassistant.components import websocket_api
from homeassistant.core import HomeAssistant

from .resolver import collect_debug_snapshot


@websocket_api.async_response
@websocket_api.websocket_command({vol.Required("type"): "dynamic_label_dashboard/debug_snapshot"})
async def websocket_debug_snapshot(
    hass: HomeAssistant,
    connection: websocket_api.ActiveConnection,
    msg: Mapping[str, Any],
) -> None:
    connection.send_result(msg["id"], collect_debug_snapshot(hass))


def async_register(hass: HomeAssistant) -> None:
    websocket_api.async_register_command(hass, websocket_debug_snapshot)
