# Fast Home Assistant Testing

## Recommended quick setup

Use the real Home Assistant VM config directory and sync this component into:

`/config/custom_components/dynamic_label_dashboard/`

Current target:
- host: `k0nsti@192.168.178.173`
- path: `/config/custom_components/dynamic_label_dashboard`

## Practical loop

### Deploy
Use:

```bash
./scripts/deploy-to-ha.sh
```

### Python/backend changes
- deploy
- restart Home Assistant, or reload the integration if possible

### Frontend changes
- deploy
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
