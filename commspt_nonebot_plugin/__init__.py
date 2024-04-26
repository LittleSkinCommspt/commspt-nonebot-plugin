from nonebot.plugin import PluginMetadata, inherit_supported_adapters, require

require("nonebot_plugin_alconna")

from . import __main__ as __main__  # noqa: E402
from .config import ConfigModel  # noqa: E402

__version__ = "0.1.0"
__plugin_meta__ = PluginMetadata(
    name="commspt-nonebot-plugin",
    description="For LittleSkin Commspt.",
    usage="",
    type="application",
    homepage="https://github.com/LittleSkinCommspt/commspt-nonebot-plugin",
    config=ConfigModel,
    supported_adapters=inherit_supported_adapters("nonebot_plugin_alconna"),
    extra={"License": "MIT", "Author": "LittleSkin Commspt Team"},
)
