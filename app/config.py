from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Application settings and configuration management.

    This class defines the global configuration for the FastAPI application.
    It leverages Pydantic Settings to automatically load values from environment
    variables or a local `.env` file.

    :ivar graveuse_ip: The network IP address of the Gravotech machine (e.g., from GRAVEUSE_IP).
    :vartype graveuse_ip: str
    :ivar graveuse_port: The TCP port used for machine communication (e.g., from GRAVEUSE_PORT).
    :vartype graveuse_port: int
    :ivar environment: The current execution environment (e.g., 'dev', 'prod').
    :vartype environment: str
    """

    graveuse_ip: str
    graveuse_port: int
    environment: str

    # Configuration for the Pydantic Settings model.
    #
    # - env_file: Specifies the path to the environment file.
    # - env_file_encoding: Ensures UTF-8 decoding for environment variables.
    # - extra: Set to 'ignore' to prevent errors if extra variables are present in the .env.
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


# Singleton instance of the application settings to be used throughout the project.
settings = Settings()
