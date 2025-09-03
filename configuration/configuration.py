import os
from functools import lru_cache

from pydantic_settings import SettingsConfigDict
from pydantic_settings_yaml import YamlBaseSettings

from configuration.models import IntegrationSettings
from src.constants import APP_ENV

config = dict(local="local.yml", development="development.yml")

dir_name = os.path.abspath(os.path.dirname(__file__))


class Settings(YamlBaseSettings):
    integration: IntegrationSettings

    model_config = SettingsConfigDict(
        yaml_file=str(os.path.join(dir_name, "environments", config[APP_ENV]))
    )


@lru_cache
def get_settings():
    return Settings()
