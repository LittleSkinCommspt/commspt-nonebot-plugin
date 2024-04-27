from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    ltsk_skinrendermc_api: str


config: ConfigModel = get_plugin_config(ConfigModel)
