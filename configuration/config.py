from pydantic_settings import BaseSettings
from pydantic import Field
from typing import Literal
from functools import lru_cache

class Settings(BaseSettings):
    # Redis Settings
    redis_host: str = Field(..., env='REDIS_HOST')
    redis_port: int = Field(default=6379, env='REDIS_PORT')
    redis_password: str = Field(..., env='REDIS_PASSWORD')
    redis_channel: str = Field(default='solar_control', env='REDIS_CHANNEL')

    # Modbus Settings
    modbus_host: str = Field(..., env='MODBUS_HOST')
    modbus_port: int = Field(default=502, env='MODBUS_PORT')
    modbus_unit_id: int = Field(default=1, env='MODBUS_UNIT_ID')

    # Solar Panel Settings
    panel_count: int = Field(default=4, env='PANEL_COUNT')
    panel_max_power: int = Field(default=100, env='PANEL_MAX_POWER')
    panel_control_mode: Literal['binary', 'variable'] = Field(
        default='binary',
        env='PANEL_CONTROL_MODE'
    )

    # Logging Settings
    log_level: str = Field(default='INFO', env='LOG_LEVEL')

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()