from arclet.alconna import Alconna, Args, Arparma, CommandMeta
from arclet.alconna.exceptions import SpecialOptionTriggered
from nonebot_plugin_alconna import AlconnaMatcher, CommandResult, on_alconna

from .data_source import get_player_profile_by_name
from yggdrasil_mc.exceptions import PlayerNotFoundError

# region handler
ygg_cmd = on_alconna(
    Alconna(
        "ygg",
        Args["player_name", str],
        meta=CommandMeta(
            description="查询玩家的 Yggdrasil 档案信息",
            usage="ygg <player_name>",
            example="ygg SerinaNya",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)
# endregion


# region matcher
@ygg_cmd.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `ygg -h` 查看帮助")


@ygg_cmd.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    player_name = parma["player_name"]
    try:
        profile = await get_player_profile_by_name(player_name)
    except PlayerNotFoundError:
        await matcher.finish(f"「{player_name}」不存在")
    await matcher.finish(profile)


# endregion
