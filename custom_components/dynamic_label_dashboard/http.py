from __future__ import annotations

from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.core import HomeAssistant


async def async_register_static(hass: HomeAssistant) -> None:
    static_dir = Path(__file__).parent / "www"
    await hass.http.async_register_static_paths(
        [StaticPathConfig("/dynamic_label_dashboard-static", str(static_dir), cache_headers=False)]
    )
