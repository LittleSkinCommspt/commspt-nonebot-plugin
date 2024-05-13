from pydantic import BaseModel
from pydantic.fields import Field
from pydantic.networks import AnyHttpUrl
from typing import Annotated
from datetime import datetime


class CustomSkinLoaderLatest(BaseModel):

    class Downloads(BaseModel):
        fabric: Annotated[AnyHttpUrl, str] = Field(alias="Fabric")
        forge: Annotated[AnyHttpUrl, str] = Field(alias="Forge")
        forgeactive: Annotated[AnyHttpUrl, str] = Field(alias="ForgeActive")

        @property
        def generate_download_text(self) -> str:
            return f"Fabric > {self.fabric}\nForge > {self.forge}\nForge Active > {self.forgeactive}"

    version: str
    downloads: Downloads


class AuthlibInjectorLatest(BaseModel):

    class CheckSums(BaseModel):
        sha256: str

    build_number: int
    version: str
    release_time: datetime
    download_url: Annotated[AnyHttpUrl, str]
    checksums: CheckSums


class LibericaJavaLatest(BaseModel):
    bitness: int
    latest_lts: bool = Field(alias="latestLTS")
    update_version: int = Field(alias="updateVersion")
    download_url: Annotated[AnyHttpUrl, str] = Field(alias="downloadUrl")
    latest_in_feature_version: bool = Field(alias="latestInFeatureVersion")
    lts: bool = Field(alias="LTS")
    bundle_type: str = Field(alias="bundleType")
    feature_version: int = Field(alias="featureVersion")
    package_type: str = Field(alias="packageType")
    fx: bool = Field(alias="FX")
    ga: bool = Field(alias="GA")
    architecture: str
    latest: bool
    extra_version: int = Field(alias="extraVersion")
    build_version: int = Field(alias="buildVersion")
    eol: bool = Field(alias="EOL")
    os: str
    interim_version: int = Field(alias="interimVersion")
    version: str
    sha1: str
    filename: str
    installation_type: str = Field(alias="installationType")
    size: int
    patch_version: int = Field(alias="patchVersion")
    tck: bool = Field(alias="TCK")
    update_type: str = Field(alias="updateType")

    @property
    def download_url_mirror(self):
        return f"https://download.bell-sw.com/java/{self.version}/{self.filename}"
