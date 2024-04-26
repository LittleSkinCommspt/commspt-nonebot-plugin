from nonebot import get_plugin_config
from pydantic import BaseModel


class ConfigModel(BaseModel):
    ltsk_api_token: str
    ltsk_browserless_api: str
    ltsk_ipip_api: str
    ltsk_skinrendermc_api: str


config: ConfigModel = get_plugin_config(ConfigModel)
