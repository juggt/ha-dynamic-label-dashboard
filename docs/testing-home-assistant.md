# Fast Home Assistant Testing

## Recommended quick setup

Use a real Home Assistant config directory and mount or symlink this component into:

`<HA_CONFIG>/custom_components/dynamic_label_dashboard/`

## Practical loop

### Python/backend changes
- restart Home Assistant, or reload the integration if possible

### Frontend changes
- rebuild frontend assets if applicable
- hard refresh browser

## Fastest likely developer workflow

If Home Assistant is running in Docker:
- mount the component folder directly into the HA config volume
- restart only the HA container after backend changes

Example target path:
- `/config/custom_components/dynamic_label_dashboard/`

## Next thing to decide

We need the actual Home Assistant setup details on this machine:
- HA config path
- Docker vs bare metal
- whether a dedicated dev instance exists
