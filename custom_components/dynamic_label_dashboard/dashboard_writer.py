from __future__ import annotations

import json
from pathlib import Path

from homeassistant.core import HomeAssistant

DASHBOARD_PATH = Path('/config/.storage/lovelace.dynamic_label_dashboard')
DASHBOARD_URL_PATH = 'dynamic-label-dashboard'
DASHBOARD_TITLE = 'Dynamic Label Dashboard'


def build_dashboard_payload() -> dict:
    return {
        'api_version': 1,
        'data': {
            'config': {
                'title': DASHBOARD_TITLE,
                'views': [
                    {
                        'title': 'Overview',
                        'path': 'overview',
                        'type': 'panel',
                        'cards': [
                            {
                                'type': 'markdown',
                                'title': 'Dynamic Label Dashboard',
                                'content': (
                                    'Die Integration ist geladen.\\n\\n'
                                    'Nächster Schritt: echte Datenansicht ins Lovelace-Dashboard rendern.'
                                ),
                            }
                        ],
                    }
                ],
            },
            'mode': 'storage',
            'url_path': DASHBOARD_URL_PATH,
            'require_admin': False,
            'show_in_sidebar': True,
            'icon': 'mdi:view-dashboard-outline',
            'title': DASHBOARD_TITLE,
        },
        'key': 'lovelace.dynamic_label_dashboard',
        'version': 1,
    }


async def async_ensure_dashboard_file(hass: HomeAssistant) -> None:
    payload = build_dashboard_payload()
    DASHBOARD_PATH.write_text(json.dumps(payload, ensure_ascii=False), encoding='utf-8')
