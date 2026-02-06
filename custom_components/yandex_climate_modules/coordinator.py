from __future__ import annotations

import asyncio
import logging
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import YandexIoTClient
from .const import DEFAULT_UPDATE_INTERVAL

_LOGGER = logging.getLogger(__name__)


class YandexClimateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch multiple module devices and keep their latest payloads."""

    def __init__(
        self,
        hass: HomeAssistant,
        client: YandexIoTClient,
        device_ids: list[str],
        interval_s: int,
        room_map: dict[str, str] | None = None,
    ) -> None:
        super().__init__(
            hass,
            _LOGGER,
            name="Yandex Climate Modules",
            update_interval=timedelta(seconds=interval_s or DEFAULT_UPDATE_INTERVAL),
        )
        self._client = client
        self.device_ids = device_ids
        self._room_map = room_map or {}

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            tasks = [self._client.get_device(did) for did in self.device_ids]
            devices = await asyncio.gather(*tasks)
            out: dict[str, Any] = {}
            for dev in devices:
                out[dev.id] = {
                    "name": dev.name,
                    "room": dev.room,
                    "room_name": self._room_map.get(dev.room),
                    "properties": dev.properties,
                }
            return out
        except Exception as e:  # noqa: BLE001
            raise UpdateFailed(str(e)) from e
