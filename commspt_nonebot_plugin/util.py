import json
import ssl
from pathlib import Path

import httpx
import jinja2
from pydantic import BaseModel

from .config import config

VERIFY_CONTENT = httpx.create_ssl_context(
    verify=ssl.create_default_context(),
    http2=True,
)
TEMPLATE_PATH = Path(__file__).parent / "templates" / "user-info.html.jinja"


async def screenshot(
    template_name: str,
    params,
    width: int = 530,
    height: int = 800,
    is_mobile: bool = True,
    device_scale_factor: float = 2.5,
) -> bytes:
    # Jinja2 render
    template = jinja2.Template(
        TEMPLATE_PATH.read_text(encoding="u8"),
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
