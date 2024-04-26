from datetime import datetime
from typing import Annotated, Optional

import arrow
import httpx
from pydantic import (
    BaseModel,
    EmailStr,
    Field,
    computed_field,
    field_validator,
)
from pydantic.functional_serializers import PlainSerializer
from pydantic.networks import IPvAnyAddress

from .config import config
from .util import VERIFY_CONTENT, screenshot


class LittleSkinUser(BaseModel):
    uid: int
    nickname: str
    email: EmailStr
    locale: Optional[str] = None
    score: int
    avatar: int = 0
    ip: list[IPvAnyAddress]
    is_dark_mode: bool = False
    permission: int = 0
    last_sign_at: datetime
    register_at: datetime
    verified: bool
    verification_token: str = ""
    salt: str = ""

    @field_validator("ip", mode="before")
    def validate_ip(cls, v: str):
        return v.split(", ")

    @classmethod
    async def query(cls, query_string: str):
        async with httpx.AsyncClient(
            http2=True,
            headers={"Authorization": f"Bearer {config.ltsk_api_token}"},
        ) as client:
            api = await client.get(
                "https://littleskin.cn/api/admin/users",
                params={"q": query_string},
            )
            if data := api.json()["data"]:
                return cls(**data[0])
            return None

    @classmethod
    async def qmail_api(cls, qq: int):
        return await cls.query(f"email:'{qq}@qq.com'")

    @classmethod
    async def uid_info(cls, uid: int):
        return await cls.query(f"uid:{uid}")


HumanReadableTime = Annotated[
    datetime,
    PlainSerializer(lambda t: arrow.get(t).format("YYYY-MM-DD HH:mm:ss")),
    Field(default_factory=datetime.now),
]


class BingLingIPIP(BaseModel):
    country_name: Optional[str] = None
    region_name: Optional[str] = None
    city_name: Optional[str] = None
    owner_domain: Optional[str] = None
    isp_domain: Optional[str] = None
    latitude: Optional[str] = None
    longitude: Optional[str] = None
    china_region_code: Optional[str] = None
    china_district_code: Optional[str] = None
    country_code: Optional[str] = None
    continent_code: Optional[str] = None

    @classmethod
    async def get(cls, ip: str):
        """
        获取 IP 信息
        ```json
        {
            "country_name": "中国",
            "region_name": "湖北",
            "city_name": "武汉",
            "owner_domain": "",
            "isp_domain": "移动",
            "latitude": "30.572399",
            "longitude": "114.279121",
            "china_region_code": null,
            "china_district_code": null,
            "country_code": "CN",
            "continent_code": "AP"
        }
        ```
        """
        async with httpx.AsyncClient(
            verify=VERIFY_CONTENT,
            base_url=config.ltsk_ipip_api,
            http2=True,
        ) as client:
            resp = await client.get(f"/{ip}")
        return cls(**resp.json())


class RenderUserInfo(BaseModel):
    generated_at: HumanReadableTime
    uid: int
    permission: int
    score: int
    nickname: str
    network: str = ""

    qq: Optional[str] = None
    qq_nickname: str = ""

    register_at: HumanReadableTime
    last_sign_at: HumanReadableTime

    email: EmailStr
    verified: bool

    ip: list[Annotated[str, IPvAnyAddress]]

    @computed_field
    def email_help(self) -> str:
        v: list[str] = []
        v.append("已验证" if self.verified else "未验证")
        if self.email.lower() != self.email:
            v.append("⚠️ 含有大写字母 ⚠️ ")
        return " / ".join(v)

    async def get_image(self) -> bytes:
        # 获取 IP 属地信息
        ipip = await BingLingIPIP.get(self.ip[0])
        self.network = f"{ipip.country_name}{ipip.region_name}{ipip.city_name} {ipip.isp_domain}{ipip.owner_domain}"

        return await screenshot("user-info.html.jinja", self, height=600)
