# Architecture Draft

## Product summary

`ha-dynamic-label-dashboard` is a Home Assistant custom component that generates a dynamic room-based dashboard from:
- floors
- areas
- devices
- entities
- labels

The dashboard is intentionally minimal and only shows items selected through label-based configuration.

## Key decisions

- Existing Home Assistant labels are reused, no forced extra label taxonomy
- Entity label match has priority over device label match
- Device and entity matches must not create duplicates
- Rooms are grouped by area
- Floors determine room ordering
- Only rooms with matching content are shown
- Items without room assignment go to `Ohne Raum`
- Mobile uses collapsible room sections
- Desktop uses a right-side drawer detail view
- Summary and detail labels are configured separately
- Group order is configurable
- Global configuration acts as default, rooms can override

## Registry model assumptions

Home Assistant provides registries/helpers for:
- `area_registry`
- `floor_registry`
- `device_registry`
- `entity_registry`
- `label_registry`

Relevant fields confirmed during initial research:
- areas have `floor_id` and `labels`
- devices have `area_id` and `labels`
- entities have `area_id`, `device_id`, and `labels`
- labels have `name`, `icon`, `color`, `description`

## Proposed backend modules

- `__init__.py` integration bootstrap
- `manifest.json`
- `const.py` constants/domain keys
- `config_flow.py` config/options flow
- `storage.py` persisted configuration
- `models.py` internal typed data structures
- `resolver.py` registry/state resolution logic
- `dashboard_builder.py` room/dashboard view model builder
- `coordinator.py` refresh orchestration
- `ws_api.py` websocket endpoints for frontend

## Proposed frontend responsibilities

- render room overview
- render mobile collapsible sections
- render desktop drawer
- render summary mini controls
- render detail groups by configured label order

## Resolution rules

For each candidate item:
1. Check entity label matches
2. If no entity match, check device label matches
3. Resolve area using entity area first, then device area
4. Resolve floor via area
5. Put item into the first matching configured label group
6. Prevent duplicate rendering

## Update model

Two update channels are expected:
- registry updates: labels, areas, floors, devices, entities
- state updates: open/closed, on/off, temperature, presence, etc.

The integration should rebuild affected room models automatically.
