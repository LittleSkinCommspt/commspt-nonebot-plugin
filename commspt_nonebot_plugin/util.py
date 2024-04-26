import json
import ssl
from io import BytesIO
from pathlib import Path
from typing import Optional

import httpx
import jinja2
from PIL import Image, ImageDraw, ImageFont
from pydantic import BaseModel

from .config import config

VERIFY_CONTENT = httpx.create_ssl_context(
    verify=ssl.create_default_context(),
    http2=True,
)
TEMPLATE_PATH = Path(__file__).parent / "templates"
MOJANGLES_FONT_PATH = Path(__file__).parent / "fonts" / "mojangles.ttf"


async def screenshot(
    template_name: str,
    params,
    width: int = 530,
    height: int = 800,  # origin: 800
    is_mobile: bool = True,
    device_scale_factor: float = 2.5,
) -> bytes:
    # Jinja2 render
    template_file = TEMPLATE_PATH / template_name
    template = jinja2.Template(
        template_file.read_text(encoding="u8"),
        enable_async=True,
    )
    if isinstance(params, BaseModel):
        html = await template.render_async(params.model_dump())
    else:
        html = await template.render_async(params)

    # send request to /screenshot
    async with httpx.AsyncClient(
        base_url=config.ltsk_browserless_api,
        verify=VERIFY_CONTENT,
        http2=True,
    ) as client:
        resp = await client.post(
            "/screenshot",
            params={
                "launch": json.dumps(
                    {
                        "ignoreHTTPSErrors": True,
                        "headless": True,
                    },
                ),
            },
            json={
                "html": html,
                "options": {"type": "png"},
                "viewport": {
                    "width": width,
                    "height": height,
                    "isMobile": is_mobile,
                    "deviceScaleFactor": device_scale_factor,
                },
                "setExtraHTTPHeaders": {"Accept-Language": "zh-CN,en;q=0.9"},
                "gotoOptions": {"waitUntil": ["networkidle0"]},
            },
        )

        # raise exception if status is bad
        resp.raise_for_status()

        # return image from response
        return resp.content


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
