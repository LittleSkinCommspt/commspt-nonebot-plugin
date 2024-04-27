from arclet.alconna import Alconna, Args, Arparma, CommandMeta
from arclet.alconna.exceptions import SpecialOptionTriggered
from httpx import HTTPStatusError
from nonebot_plugin_alconna import AlconnaMatcher, CommandResult, on_alconna
from nonebot_plugin_alconna.uniseg import Image
from yggdrasil_mc.exceptions import PlayerNotFoundError

from .data_source import get_player_profile_by_name, get_texture_image

LTSK_YGG = "https://littleskin.cn/api/yggdrasil"

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

view_cmd = on_alconna(
    Alconna(
        "view",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看指定玩家的皮肤预览图",
            usage="view <player_name>",
            example="view SerinaNya",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)

view_ygg_cmd = on_alconna(
    Alconna(
        "view.ygg",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看指定玩家的 Yggdrasil 皮肤预览图",
            usage="view.ygg <player_name>",
            example="view.ygg SerinaNya",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)

view_pro_cmd = on_alconna(
    Alconna(
        "view.pro",
        Args["player_name", str],
        meta=CommandMeta(
            description="查看指定玩家的 正版 皮肤预览图",
            usage="view.pro <player_name>",
            example="view.pro SerinaNya",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)
# endregion


# region matcher
# region ygg cmd
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
        profile = await get_player_profile_by_name(
            yggdrasil_api=LTSK_YGG,
            player_name=player_name,
        )
    except PlayerNotFoundError:
        await matcher.finish(f"「{player_name}」不存在")
    await matcher.finish(profile)


# endregion


# region view & view.ygg cmd
@view_cmd.handle()
@view_ygg_cmd.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `view -h` 查看帮助")


@view_cmd.handle()
@view_ygg_cmd.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    player_name = parma["player_name"]
    try:
        image = await get_texture_image(yggdrasil_api=LTSK_YGG, player_name=player_name)
    except PlayerNotFoundError:
        await matcher.finish(f"「{player_name}」不存在")
    except HTTPStatusError as e:
        await matcher.finish(
            f"请求 SkinRenderMC 时发生错误: {e.response.status_code} | {e.response.text}",
        )
    await matcher.finish(Image(raw=image))


# endregion


# region view.pro cmd
@view_pro_cmd.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `view.pro -h` 查看帮助")


@view_pro_cmd.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    player_name = parma["player_name"]
    try:
        image = await get_texture_image(yggdrasil_api=None, player_name=player_name)
    except PlayerNotFoundError:
        await matcher.finish(f"「{player_name}」不存在")
    except HTTPStatusError as e:
        await matcher.finish(
            f"请求 SkinRenderMC 时发生错误: {e.response.status_code} | {e.response.text}",
        )
    await matcher.finish(Image(raw=image))


# endregion
