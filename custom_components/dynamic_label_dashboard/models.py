from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(slots=True)
class LabelInfo:
    id: str
    name: str
    color: str | None = None
    icon: str | None = None
    description: str | None = None


@dataclass(slots=True)
class AreaInfo:
    id: str
    name: str
    floor_id: str | None = None
    labels: list[str] = field(default_factory=list)


@dataclass(slots=True)
class FloorInfo:
    id: str
    name: str
    level: int | None = None


@dataclass(slots=True)
class DeviceInfo:
    id: str
    name: str
    area_id: str | None = None
    labels: list[str] = field(default_factory=list)


@dataclass(slots=True)
class EntityInfo:
    id: str
    name: str
    area_id: str | None = None
    device_id: str | None = None
    labels: list[str] = field(default_factory=list)
    state: str | None = None
