"""Data coordinator for YI Camera Connect camera inventory."""

from __future__ import annotations

import time
from datetime import timedelta
from typing import Any

from homeassistant.core import HomeAssistant
from homeassistant.helpers import device_registry as dr
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import YiHomeApi, YiHomeApiError
from .const import DOMAIN

INVENTORY_REFRESH_SECONDS = 300.0


class YiHomeCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Refresh secret-safe camera state from the YI RTSP App."""

    def __init__(
        self,
        hass: HomeAssistant,
        api: YiHomeApi,
        config_entry_id: str,
    ) -> None:
        self.api = api
        self._config_entry_id = config_entry_id
        self._next_inventory_refresh_at = 0.0
        super().__init__(
            hass,
            logger=__import__("logging").getLogger(__name__),
            name="YI Camera Connect cameras",
            update_interval=timedelta(seconds=30),
        )

    async def _async_update_data(self) -> dict[str, Any]:
        now = time.monotonic()
        if now >= self._next_inventory_refresh_at:
            self._next_inventory_refresh_at = now + INVENTORY_REFRESH_SECONDS
            try:
                await self.api.discover()
            except YiHomeApiError:
                pass

        try:
            payload = await self.api.cameras()
        except YiHomeApiError as exc:
            raise UpdateFailed("Unable to refresh YI camera state") from exc
        if payload.get("secrets_exposed") is not False:
            raise UpdateFailed("YI RTSP App returned an unsafe camera payload")
        cameras = payload.get("cameras")
        if not isinstance(cameras, list):
            raise UpdateFailed("YI RTSP App returned an invalid camera inventory")
        self._sync_device_names(cameras)
        return payload

    def _sync_device_names(self, cameras: list[Any]) -> None:
        """Reconcile YI display-name changes without changing HA entity identity."""
        registry = dr.async_get(self.hass)
        for camera in cameras:
            if not isinstance(camera, dict):
                continue
            stable_id = camera.get("stable_id")
            name = camera.get("name")
            if not isinstance(stable_id, str) or not stable_id:
                continue
            if not isinstance(name, str) or not name.strip():
                continue
            device = registry.async_get_device_by_identifier(
                (DOMAIN, stable_id), self._config_entry_id
            )
            if device is None or device.name == name:
                continue
            registry.async_update_device(device.id, name=name)

    def camera_ids(self) -> set[str]:
        """Return stable camera identities from the latest inventory."""
        if not self.data:
            return set()
        result: set[str] = set()
        for camera in self.data.get("cameras", []):
            if isinstance(camera, dict) and isinstance(camera.get("stable_id"), str):
                result.add(str(camera["stable_id"]))
        return result

    def camera(self, stable_id: str) -> dict[str, Any] | None:
        """Return one camera from the latest secret-safe snapshot."""
        if not self.data:
            return None
        for camera in self.data.get("cameras", []):
            if isinstance(camera, dict) and camera.get("stable_id") == stable_id:
                return camera
        return None
