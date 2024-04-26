from datetime import datetime
from typing import Optional

import pytz
from yggdrasil_mc.client import YggdrasilMC
from yggdrasil_mc.exceptions import PlayerNotFoundError

from .util import process_image, request_skinrendermc

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")
LTSK_YGG = "https://littleskin.cn/api/yggdrasil"


async def get_player_profile_by_name(
    yggdrasil_api: Optional[str], player_name: str
) -> str:
    ygg = YggdrasilMC(api_root=yggdrasil_api)
    try:
        player = await ygg.by_name_async(player_name)
    except ValueError as e:
        raise PlayerNotFoundError from e
    # success
    skin_model = (
        player.skin.metadata.model if player.skin and player.skin.metadata else None
    )

    return f"""「{player.name}」的资料 - 来自 Yggdrasil API

» Skin ({skin_model}): {player.skin.hash if player.skin and player.skin.hash else None}

» Cape: {player.cape.hash if player.cape and player.cape.hash else None}

» UUID: {player.id}"""


async def get_texture_image(yggdrasil_api: Optional[str], player_name: str) -> bytes:
    ygg = YggdrasilMC(api_root=yggdrasil_api)
    try:
        player = await ygg.by_name_async(player_name)
    except ValueError as e:
        raise PlayerNotFoundError from e
    # success

    skin_url = player.skin.url if player.skin else None
    cape_url = player.cape.url if player.cape else None
    name_tag = player.name

    image = await request_skinrendermc(
        skin_url=str(skin_url) if skin_url else None,
        cape_url=str(cape_url) if cape_url else None,
        name_tag=name_tag,
    )

    skin_hash = player.skin.hash[:8] if player.skin and player.skin.hash else None
    skin_model = (
        player.skin.metadata.model if player.skin and player.skin.metadata else None
    )
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None
    api_name = (
        "LittleSkin"
        if yggdrasil_api == LTSK_YGG
        else ("Pro" if yggdrasil_api is None else "Unknown")
    )

    return process_image(
        image_bytes=image,
        text=f"Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, {api_name}",
    )
