# Development Workflow

## Goal

Keep the iteration loop fast so Home Assistant changes become visible quickly.

## Recommended local workflow

### Option 1: real Home Assistant config directory

Develop this repo normally, then symlink or copy:

- `custom_components/dynamic_label_dashboard/`

into:

- `<HA_CONFIG>/custom_components/dynamic_label_dashboard/`

Benefits:
- close to real usage
- easy to test install/update behavior

### Change loop

#### Backend changes (Python)
Usually require:
- Home Assistant reload where possible
- otherwise Home Assistant restart

#### Frontend changes (JS/TS/CSS)
Usually require:
- rebuild frontend assets if used
- browser refresh
- cache busting if necessary

## Future improvement

A dedicated devcontainer/docker-compose based Home Assistant test environment would speed this up further:
- mount custom component directly
- restart only HA service
- inspect logs quickly

## Open question

Need to decide the fastest practical test setup available on k0nsti's machine:
- existing Home Assistant instance config path
- local HA container
- dedicated disposable dev instance
