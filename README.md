# ha-dynamic-label-dashboard

A Home Assistant custom component for a dynamic, area-based dashboard powered by labels, areas, floors, devices, and entities.

## Goal

Build a clean, automatic dashboard inspired by Dwains Dashboard, but much more minimal and configurable.

Core ideas:
- group by areas/rooms
- sort by floors
- use existing Home Assistant labels as the source of truth for what should be shown
- configurable summary and detail sections
- mobile-friendly collapsed room sections
- desktop drawer detail view

## MVP direction

- Custom component
- Uses Home Assistant registries for areas, floors, devices, entities, labels
- Global label configuration for summary/detail
- Per-room overrides
- Dynamic rendering, automatic updates

## Planned structure

- `docs/` architecture and product docs
- `custom_components/dynamic_label_dashboard/` integration code

## Development notes

Fastest local Home Assistant development loop will likely be:
- develop the custom component in this repo
- link or copy `custom_components/dynamic_label_dashboard` into a Home Assistant config dir
- refresh browser for frontend changes
- reload or restart Home Assistant for backend changes

More detailed dev workflow will be documented in `docs/development.md`.
