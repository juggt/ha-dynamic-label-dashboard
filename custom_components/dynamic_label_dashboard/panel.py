from __future__ import annotations

from homeassistant.components import frontend, panel_custom
from homeassistant.core import HomeAssistant

from .const import DOMAIN

PANEL_NAME = "dynamic-label-dashboard"
PANEL_TITLE = "Dynamic Label Dashboard"
PANEL_ICON = "mdi:view-dashboard-outline"
MODULE_URL = f"/dynamic_label_dashboard-static/{PANEL_NAME}.js"


async def async_register_panel(hass: HomeAssistant) -> None:
    frontend.add_extra_js_url(hass, MODULE_URL)
    panel_custom.async_register_panel(
        hass,
        webcomponent_name="dynamic-label-dashboard-panel",
        frontend_url_path=PANEL_NAME,
        module_url=MODULE_URL,
        sidebar_title=PANEL_TITLE,
        sidebar_icon=PANEL_ICON,
        require_admin=False,
        config={"domain": DOMAIN},
    )
