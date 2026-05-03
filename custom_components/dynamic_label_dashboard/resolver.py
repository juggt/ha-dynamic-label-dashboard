from __future__ import annotations

from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import floor_registry as fr
from homeassistant.helpers import label_registry as lr


def collect_debug_snapshot(hass: HomeAssistant) -> dict:
    area_reg = ar.async_get(hass)
    device_reg = dr.async_get(hass)
    entity_reg = er.async_get(hass)
    floor_reg = fr.async_get(hass)
    label_reg = lr.async_get(hass)

    labels = [
        {
            "id": entry.label_id,
            "name": entry.name,
            "color": entry.color,
            "icon": entry.icon,
            "description": entry.description,
        }
        for entry in sorted(label_reg.labels.values(), key=lambda x: x.name.lower())
    ]

    floors = [
        {
            "id": entry.floor_id,
            "name": entry.name,
            "level": getattr(entry, "level", None),
        }
        for entry in floor_reg.floors.values()
    ]

    areas = [
        {
            "id": entry.id,
            "name": entry.name,
            "floor_id": entry.floor_id,
            "labels": sorted(entry.labels),
        }
        for entry in area_reg.areas.values()
    ]

    devices = [
        {
            "id": entry.id,
            "name": entry.name_by_user or entry.name or entry.id,
            "area_id": entry.area_id,
            "labels": sorted(entry.labels),
        }
        for entry in device_reg.devices.values()
    ]

    entities = []
    for entry in entity_reg.entities.values():
        state = hass.states.get(entry.entity_id)
        entities.append({
            "id": entry.entity_id,
            "name": entry.name or entry.original_name or entry.entity_id,
            "area_id": entry.area_id,
            "device_id": entry.device_id,
            "labels": sorted(entry.labels),
            "state": state.state if state else None,
        })

    return {
        "counts": {
            "labels": len(labels),
            "floors": len(floors),
            "areas": len(areas),
            "devices": len(devices),
            "entities": len(entities),
        },
        "labels": labels,
        "floors": sorted(floors, key=lambda x: (999999 if x["level"] is None else x["level"], x["name"].lower())),
        "areas": sorted(areas, key=lambda x: x["name"].lower()),
        "devices": sorted(devices, key=lambda x: x["name"].lower())[:200],
        "entities": sorted(entities, key=lambda x: x["id"].lower())[:300],
    }
