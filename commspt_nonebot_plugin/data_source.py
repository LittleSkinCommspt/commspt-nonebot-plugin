from yggdrasil_mc.client import YggdrasilMC
from yggdrasil_mc.exceptions import PlayerNotFoundError

LSTK_YGG = YggdrasilMC(api_root="https://littleskin.cn/api/yggdrasil")


async def get_player_profile_by_name(player_name: str) -> str:
    try:
        player = await LSTK_YGG.by_name_async(player_name)
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
