import ssl
from io import BytesIO
from pathlib import Path
from typing import Optional
from nonebot.compat import type_validate_json

import httpx
from PIL import Image, ImageDraw, ImageFont

from .config import config
from .models import CustomSkinLoaderLatest, LibericaJavaLatest, AuthlibInjectorLatest
import pytz
from yggdrasil_mc.client import YggdrasilMC
from yggdrasil_mc.exceptions import PlayerNotFoundError
from datetime import datetime

VERIFY_CONTENT = httpx.create_ssl_context(
    verify=ssl.create_default_context(),
    http2=True,
)
TEMPLATE_PATH = Path(__file__).parent / "templates"
MOJANGLES_FONT_PATH = Path(__file__).parent / "fonts" / "mojangles.ttf"

TZ_SHANGHAI = pytz.timezone("Asia/Shanghai")
LTSK_YGG = "https://littleskin.cn/api/yggdrasil"


async def request_skinrendermc(
    skin_url: Optional[str],
    cape_url: Optional[str],
    name_tag: Optional[str],
):
    p = {
        "skinUrl": skin_url,
        "capeUrl": cape_url,
        "nameTag": name_tag,
    }

    # 删除值为 None 的键值对
    # （SkinRenderMC 只判断键值对是否存在）
    for x in [k for k in p if not p[k]]:
        p.pop(x)

    async with httpx.AsyncClient(
        http2=True,
        base_url=config.ltsk_skinrendermc_api,
        follow_redirects=True,
    ) as client:
        resp = await client.get(
            "/url/image/both",
            params=p,
            timeout=30,  # 通常只需要不到 15 秒
        )
        # if resp.status_code == 200:
        #     image = resp.read()
        #     return image
        # else:
        #     return
        resp.raise_for_status()
        return resp.content


def process_image(image_bytes: bytes, text: str) -> bytes:
    # Open the image from the byte representation
    image = Image.open(BytesIO(image_bytes)).convert("RGB")
    image = image.crop((0, 0, image.width, int(image.height * 0.87)))

    # Create a draw object to draw on the image
    draw = ImageDraw.Draw(image)

    # Define the font to be used for the watermark
    font = ImageFont.truetype(MOJANGLES_FONT_PATH.absolute(), size=12)

    # Set the margin around the watermark
    margin_x = 20
    margin_y = 10

    # Calculate the width and height of the watermark text
    text_width = font.getmask(text).getbbox()[2]
    text_height = font.getmask(text).getbbox()[3]

    # Calculate the coordinates to place the watermark text
    x = image.width - margin_x - text_width
    y = image.height - margin_y - text_height

    # Draw the watermark text on the image
    draw.text((x, y), text, font=font, fill=(0, 0, 0))

    # Save the modified image as byte representation
    output_bytes = BytesIO()
    image.save(output_bytes, format="PNG")

    # Return the byte representation of the modified image
    return output_bytes.getvalue()


async def get_player_profile_by_name(yggdrasil_api: Optional[str], player_name: str) -> str:
    ygg = YggdrasilMC(api_root=yggdrasil_api)
    try:
        player = await ygg.by_name_async(player_name)
    except ValueError as e:
        raise PlayerNotFoundError from e
    # success
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None

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
    skin_model = player.skin.metadata.model if player.skin and player.skin.metadata else None
    cape_hash = player.cape.hash[:8] if player.cape and player.cape.hash else None
    api_name = "LittleSkin" if yggdrasil_api == LTSK_YGG else ("Pro" if yggdrasil_api is None else "Unknown")

    return process_image(
        image_bytes=image,
        text=f"Skin {skin_hash} ({skin_model}), Cape {cape_hash} / {datetime.now(TZ_SHANGHAI).isoformat()}, via SkinRenderMC, {api_name}",
    )


async def get_csl_latest() -> CustomSkinLoaderLatest:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        return type_validate_json(
            CustomSkinLoaderLatest,
            (await client.get(url="https://csl-1258131272.cos.ap-shanghai.myqcloud.com/latest.json"))
            .raise_for_status()
            .text,
        )


async def get_authlib_injector_latest() -> AuthlibInjectorLatest:
    async with httpx.AsyncClient(follow_redirects=True) as client:
        return type_validate_json(
            AuthlibInjectorLatest,
            (await client.get(url="https://authlib-injector.yushi.moe/artifact/latest.json")).raise_for_status().text,
        )


async def get_liberica_java_latest(**kwargs) -> list[LibericaJavaLatest]:
    for key, _ in kwargs.items():
        kwargs[key.replace("_", "-")] = kwargs.pop(key)
    async with httpx.AsyncClient() as client:
        return type_validate_json(
            list[LibericaJavaLatest],
            (
                await client.get(
                    "https://api.bell-sw.com/v1/liberica/releases",
                    params=kwargs,
                )
            )
            .raise_for_status()
            .text,
        )
