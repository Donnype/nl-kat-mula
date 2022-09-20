import os
from pathlib import Path

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application settings
    debug: bool = Field(False, env="SCHEDULER_DEBUG")
    log_cfg: str = Field(
        os.path.join(Path(__file__).parent.parent.parent, "logging.json"),
        env="SCHEDULER_LOG_CFG",
    )

    # Server settings
    # api_host: str = Field("0.0.0.0", env="SCHEDULER_API_HOST")
    # api_port: int = Field(8000, env="SCHEDULER_API_PORT")

    # Application settings
    boefje_populate: bool = Field(True, env="SCHEDULER_BOEFJE_POPULATE")
    normalizer_populate: bool = Field(True, env="SCHEDULER_NORMALIZER_POPULATE")

    # Queue settings (0 is infinite)
    pq_maxsize: int = Field(1000, env="SCHEDULER_PQ_MAXSIZE")
    pq_populate_interval: int = Field(10, env="SCHEDULER_PQ_INTERVAL")
    pq_populate_grace_period: int = Field(86400, env="SCHEDULER_PQ_GRACE")

    # Dispatcher settings
    dsp_interval: int = Field(5, env="SCHEDULER_DSP_INTERVAL")

    # Database settings
    database_dsn: str = Field("sqlite:///", env="SCHEDULER_DB_DSN")
