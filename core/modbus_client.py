from dataclasses import dataclass
from typing import Optional
import structlog
from pymodbus.client import ModbusTcpClient
from pymodbus.exceptions import ModbusException
from configuration import get_settings

logger = structlog.get_logger()

@dataclass
class ModbusConfig:
    host: str
    port: int = 502  # Default Modbus TCP port
    unit_id: int = 1  # Default unit ID

class SolarModbusClient:
    def __init__(self):
        settings = get_settings()
        """Initialize the Modbus client with configuration from settings."""
        self.config = ModbusConfig(
            host=settings.modbus_host,
            port=settings.modbus_port,
            unit_id=settings.modbus_unit_id
        )

        self.client = None

        self.logger = logger.bind(
            host=self.config.host,
            port=self.config.port,
            unit_id=self.config.unit_id
        )


    async def connect(self) -> bool:
        """Establish connection to the Modbus TCP server."""
        try:
            self.client = ModbusTcpClient(
                host=self.config.host,
                port=self.config.port
            )
            connected = await self.client.connect()
            if connected:
                self.logger.info("Successfully connected to Modbus TCP server")
                return True
            self.logger.error("Failed to connect to Modbus TCP server")
            return False
        except ModbusException as e:
            self.logger.error("Modbus connection error", error=str(e))
            return False

    async def disconnect(self):
        """Close the Modbus TCP connection."""
        if self.client:
            self.client.close()
            self.logger.info("Disconnected from Modbus TCP server")

    async def write_coil(self, address: int, value: bool) -> bool:
        """Write a single coil value to control solar panel state."""
        if not self.client:
            self.logger.error("Not connected to Modbus server")
            return False
        
        try:
            result = await self.client.write_coil(
                address,
                value,
                slave=self.config.unit_id
            )
            if result.isError():
                self.logger.error("Failed to write coil", address=address, value=value)
                return False
            self.logger.info("Successfully wrote coil", address=address, value=value)
            return True
        except ModbusException as e:
            self.logger.error("Modbus write error", error=str(e))
            return False