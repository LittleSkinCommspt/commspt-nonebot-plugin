from arclet.alconna import Alconna, Args, Arparma, CommandMeta
from arclet.alconna.exceptions import SpecialOptionTriggered
from httpx import HTTPStatusError
from nonebot_plugin_alconna import AlconnaMatcher, CommandResult, on_alconna
from nonebot_plugin_alconna.uniseg import Image
from yggdrasil_mc.exceptions import PlayerNotFoundError

from .util import (
    get_player_profile_by_name,
    get_texture_image,
    get_authlib_injector_latest,
    get_csl_latest,
    get_liberica_java_latest,
)


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

csl_latest_cmd = on_alconna(
    Alconna(
        "csl.latest",
        meta=CommandMeta(
            description="获取 CustomSkinLoader 最新版本信息",
            usage="csl.latest",
            example="csl.latest",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)

ygg_latest = on_alconna(
    Alconna(
        "ygg.latest",
        meta=CommandMeta(
            description="获取 Yggdrasil 最新版本信息",
            usage="ygg.latest",
            example="ygg.latest",
        ),
    ),
    use_cmd_start=True,
    skip_for_unmatch=False,
)

java_latest = on_alconna(
    Alconna(
        "java.latest",
        Args["version", int, 17]["type", str, "jre"]["os", str, "windows"],
        meta=CommandMeta(
            description="获取 Java 最新版本信息",
            usage="java.latest [version] [type] [os]",
            example="java.latest 17 jdk windows",
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
    except HTTPStatusError as e:
        await matcher.finish(
            f"请求 Yggdrasil API 时发生错误: {e.response.status_code} | {e.response.text}",
        )
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


# region csl.latest cmd
@csl_latest_cmd.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `csl.latest -h` 查看帮助")


@csl_latest_cmd.handle()
async def _(matcher: AlconnaMatcher):
    csl_latest = await get_csl_latest()
    await matcher.finish(
        f"「CustomSkinLoader」\n当前最新版本 > {csl_latest.version}\n\n{csl_latest.downloads.generate_download_text}",
    )


# endregion


# region ygg.latest cmd
@ygg_latest.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `ygg.latest -h` 查看帮助")


@ygg_latest.handle()
async def _(matcher: AlconnaMatcher):
    ygg_latest = await get_authlib_injector_latest()
    await matcher.finish(
        f"「Authlib Injector」\n当前最新版本 > {ygg_latest.version}\n下载地址 > {ygg_latest.download_url}",
    )


# endregion


# region java.latest cmd
@java_latest.handle()
async def _(matcher: AlconnaMatcher, res: CommandResult):
    if not res.result.error_info:
        return
    if isinstance(res.result.error_info, SpecialOptionTriggered):
        await matcher.finish(res.output)
    await matcher.finish(f"{res.result.error_info}\n使用指令 `java.latest -h` 查看帮助")


@java_latest.handle()
async def _(matcher: AlconnaMatcher, parma: Arparma):
    version: int = parma["version"]
    type: str = parma["type"]
    os: str = parma["os"]
    java_latest = await get_liberica_java_latest(
        version_feature=version,
        bundle_type=f"{type}-full",
        os=os,
    )
    await matcher.finish(
        f"「Liberica Java {java_latest[0].feature_version} ({java_latest[0].bundle_type})」\n下载地址 > {java_latest[0].download_url_mirror}",
    )


# endregion


# endregion
