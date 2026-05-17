from datetime import datetime, timezone

import dlipower

from config import DeviceConfig
from log import get_logger


logger = get_logger()


class SwitchDevice:
    """Low-level driver for the Digital Loggers EPC7 (HTTP)."""

    def __init__(self, device_config: DeviceConfig):
        self._config = device_config

        # Connection state
        self._device: dlipower.PowerSwitch | None = None
        self._connected = False
        self._connecting = False

        self._names: list[str] = []

    #######################################
    # ASCOM Methods Common To All Devices #
    #######################################
    def connect(self):
        """Establish connection to the DLI ePDU."""
        if self._connecting or self._connected:
            return

        self._connecting = True
        try:
            self._device = dlipower.PowerSwitch(
                hostname=self._config.dl_host,
                userid=self._config.dl_username,
                password=self._config.dl_password,
                timeout=self._config.timeout,
            )
            # Verify the connection actually works — dlipower does not
            # raise on construction, it just stores credentials.
            status = self._device.statuslist()
            if status is None:
                raise RuntimeError(
                    f"Cannot reach ePDU at {self._config.dl_host}"
                )
            self._names = [outlet[1] for outlet in status]
            self._connected = True
            logger.info(f"Connected to switch: {self._config.entity}")
        except Exception as e:
            logger.error(f"Connect error: {e}")
            self._connected = False
            raise
        finally:
            self._connecting = False

    @property
    def connected(self) -> bool:
        return self._connected

    @connected.setter
    def connected(self, value: bool):
        if value and not self._connected:
            self.connect()
        elif not value and self._connected:
            self.disconnect()

    @property
    def connecting(self) -> bool:
        return self._connecting

    def disconnect(self):
        """Close connection to the DLI ePDU."""
        self._device = None
        self._names = []
        self._connected = False
        logger.info(f"Disconnected from switch: {self._config.entity}")

    @property
    def entity(self) -> str:
        return self._config.entity

    ########################
    # ISwitchV3 properties #
    ########################
    @property
    def max_switch(self) -> int:
        return len(self._names)

    @property
    def timestamp(self) -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    #####################
    # ISwitchV3 methods #
    #####################
    def can_async(self, switch_id: int) -> bool:
        return False

    def cancel_async(self, switch_id: int):
        pass

    def can_write(self, switch_id: int) -> bool:
        return True

    def get_switch(self, switch_id: int) -> bool:
        state = self._device[switch_id].state
        return state == "ON"

    def get_switch_name(self, switch_id: int) -> str:
        return self._names[switch_id]

    def get_switch_value(self, switch_id: int) -> float:
        return 1.0 if self.get_switch(switch_id) else 0.0

    def max_switch_value(self, switch_id: int) -> float:
        return 1.0

    def min_switch_value(self, switch_id: int) -> float:
        return 0.0

    def set_switch(self, switch_id: int, state: bool):
        if state:
            self._device[switch_id].on()
        else:
            self._device[switch_id].off()
        logger.info(f"Switch {switch_id} set to {'ON' if state else 'OFF'}")

    def switch_step(self, switch_id: int) -> float:
        return 1.0
