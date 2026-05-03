from __future__ import annotations

from collections import defaultdict

from homeassistant.core import HomeAssistant
from homeassistant.helpers import area_registry as ar
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers import entity_registry as er
from homeassistant.helpers import floor_registry as fr
from homeassistant.helpers import label_registry as lr


def _sorted_labels(label_reg: lr.LabelRegistry) -> list[dict]:
    return [
        {
            "id": entry.label_id,
            "name": entry.name,
            "color": entry.color,
            "icon": entry.icon,
            "description": entry.description,
        }
        for entry in sorted(label_reg.labels.values(), key=lambda x: x.name.lower())
    ]


def _resolve_area_id(entity_entry, device_entry) -> str | None:
    if entity_entry is not None and entity_entry.area_id:
        return entity_entry.area_id
    if device_entry is not None and device_entry.area_id:
        return device_entry.area_id
    return None


def _has_any_selected_label(labels: set[str], selected: set[str]) -> bool:
    return bool(labels & selected)


def collect_dashboard_snapshot(hass: HomeAssistant, config: dict | None = None) -> dict:
    config = config or {}
    selected_summary = set(config.get("summary_labels") or [])
    selected_detail = set(config.get("detail_labels") or [])
    selected_labels = selected_summary | selected_detail

    area_reg = ar.async_get(hass)
    device_reg = dr.async_get(hass)
    entity_reg = er.async_get(hass)
    floor_reg = fr.async_get(hass)
    label_reg = lr.async_get(hass)

    floors_by_id = {
        entry.floor_id: {
            "id": entry.floor_id,
            "name": entry.name,
            "level": entry.level,
        }
        for entry in floor_reg.floors.values()
    }
    areas_by_id = {
        entry.id: {
            "id": entry.id,
            "name": entry.name,
            "floor_id": entry.floor_id,
            "labels": sorted(entry.labels),
        }
        for entry in area_reg.areas.values()
    }

    matched_items_by_area: dict[str | None, list[dict]] = defaultdict(list)

    for entity_entry in entity_reg.entities.values():
        device_entry = device_reg.async_get(entity_entry.device_id) if entity_entry.device_id else None
        entity_labels = set(entity_entry.labels)
        device_labels = set(device_entry.labels) if device_entry else set()
        matched_by_entity = _has_any_selected_label(entity_labels, selected_labels)
        matched_by_device = (not matched_by_entity) and _has_any_selected_label(device_labels, selected_labels)
        if not matched_by_entity and not matched_by_device:
            continue

        area_id = _resolve_area_id(entity_entry, device_entry)
        state = hass.states.get(entity_entry.entity_id)
        matched_items_by_area[area_id].append(
            {
                "id": entity_entry.entity_id,
                "name": entity_entry.name or entity_entry.original_name or entity_entry.entity_id,
                "state": state.state if state else None,
                "match_source": "entity" if matched_by_entity else "device",
                "entity_labels": sorted(entity_labels),
                "device_labels": sorted(device_labels),
                "summary_match": sorted(entity_labels & selected_summary if matched_by_entity else device_labels & selected_summary),
                "detail_match": sorted(entity_labels & selected_detail if matched_by_entity else device_labels & selected_detail),
            }
        )

    rooms = []
    no_room_items = matched_items_by_area.get(None, [])

    for area_id, area in areas_by_id.items():
        items = sorted(matched_items_by_area.get(area_id, []), key=lambda x: x["name"].lower())
        if not items:
            continue
        floor = floors_by_id.get(area["floor_id"])
        rooms.append(
            {
                "id": area_id,
                "name": area["name"],
                "floor_id": area["floor_id"],
                "floor_name": floor["name"] if floor else None,
                "floor_level": floor["level"] if floor else None,
                "items": items,
            }
        )

    rooms.sort(
        key=lambda room: (
            room["floor_level"] is None,
            room["floor_level"] if room["floor_level"] is not None else 999999,
            room["name"].lower(),
        )
    )

    labels = _sorted_labels(label_reg)
    selectable_labels = [
        {
            **label,
            "selected_summary": label["id"] in selected_summary,
            "selected_detail": label["id"] in selected_detail,
        }
        for label in labels
    ]

    return {
        "version": "0.2-snapshot",
        "counts": {
            "labels": len(labels),
            "floors": len(floors_by_id),
            "areas": len(areas_by_id),
            "rooms_with_matches": len(rooms),
            "items_without_room": len(no_room_items),
        },
        "config": {
            "summary_labels": sorted(selected_summary),
            "detail_labels": sorted(selected_detail),
        },
        "labels": selectable_labels,
        "rooms": rooms,
        "no_room": sorted(no_room_items, key=lambda x: x["name"].lower()),
    }
