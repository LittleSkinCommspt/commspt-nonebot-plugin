<!-- markdownlint-disable MD031 MD033 MD036 MD041 -->

<div align="center">

<a href="https://v2.nonebot.dev/store">
  <img src="https://raw.githubusercontent.com/A-kirami/nonebot-plugin-template/resources/nbp_logo.png" width="180" height="180" alt="NoneBotPluginLogo">
</a>

<p>
  <img src="https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/plugin.svg" alt="NoneBotPluginText">
</p>

# commspt-nonebot-plugin

_✨ 为 LittleSkin Commspt 量身定制的 Nonebot2 插件 ✨_

<img src="https://img.shields.io/badge/python-3.10+-blue.svg" alt="python">
<a href="https://pdm.fming.dev">
  <img src="https://img.shields.io/badge/pdm-managed-blueviolet" alt="pdm-managed">
</a>
<a href="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/95b7814f-eac0-48e1-b124-df3fb41c692d">
  <img src="https://wakatime.com/badge/user/de2f28c3-5c26-4f92-bfe0-7a392cbfed48/project/95b7814f-eac0-48e1-b124-df3fb41c692d.svg" alt="wakatime">
</a>

<br />

<!-- <a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v1.json" alt="Pydantic Version 1" >
</a> -->
<!-- <a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json" alt="Pydantic Version 2" >
</a> -->
<a href="https://pydantic.dev">
  <img src="https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/lgc-NB2Dev/readme/main/template/pyd-v2.json" alt="Pydantic Version 2" >
</a>
<!-- <a href="./LICENSE">
  <img src="https://img.shields.io/github/license/FalfaChino/commspt-nonebot-plugin.svg" alt="license">
</a>
<a href="https://pypi.python.org/pypi/commspt-nonebot-plugin">
  <img src="https://img.shields.io/pypi/v/commspt-nonebot-plugin.svg" alt="pypi">
</a>
<a href="https://pypi.python.org/pypi/commspt-nonebot-plugin">
  <img src="https://img.shields.io/pypi/dm/commspt-nonebot-plugin" alt="pypi download">
</a> -->

</div>

## 📖 介绍

这里是插件的详细介绍部分

## 💿 安装

<!-- 以下提到的方法 任选**其一** 即可

<details open>
<summary>[推荐] 使用 nb-cli 安装</summary>
在 nonebot2 项目的根目录下打开命令行, 输入以下指令即可安装

```bash
nb plugin install commspt-nonebot-plugin
```

</details>

<details>
<summary>使用包管理器安装</summary>
在 nonebot2 项目的插件目录下, 打开命令行, 根据你使用的包管理器, 输入相应的安装命令

<details>
<summary>pip</summary>

```bash
pip install commspt-nonebot-plugin
```

</details>
<details>
<summary>pdm</summary>

```bash
pdm add commspt-nonebot-plugin
```

</details>
<details>
<summary>poetry</summary>

```bash
poetry add commspt-nonebot-plugin
```

</details>
<details>
<summary>conda</summary>

```bash
conda install commspt-nonebot-plugin
```

</details>

打开 nonebot2 项目根目录下的 `pyproject.toml` 文件, 在 `[tool.nonebot]` 部分的 `plugins` 项里追加写入

```toml
[tool.nonebot]
plugins = [
    # ...
    "commspt_nonebot_plugin"
]
```

</details> -->

暂未发布，请手动 clone 以安装。

## ⚙️ 配置

在 nonebot2 项目的`.env`文件中添加下表中的必填配置

|         配置项          | 必填 | 默认值 |            示例             |            说明             |
| :---------------------: | :--: | :----: | :-------------------------: | :-------------------------: |
|    `LTSK_API_TOKEN`     |  是  |   无   | `xxxxxx-xxxxxxxxxxx-xxxxxx` |  Blessing SKinAdmin Token   |
| `LTSK_BROWSERLESS_API`  |  是  |   无   |   `http://10.0.0.5:19800`   | 远程 Browserless 服务端地址 |
|     `LTSK_IPIP_API`     |  是  |   无   |   `http://10.0.0.10:9999`   |    IPIP 数据库 API 地址     |
| `LTSK_SKINRENDERMC_API` |  是  |   无   | `http://10.0.10.100:10086`  |    SkinRenderMC API 地址    |

## 🎉 使用

### 指令表

|    指令    | 权限 | 需要@ | 范围 |                        说明                         |
| :--------: | :--: | :---: | :--: | :-------------------------------------------------: |
|   `ygg`    | 群员 |  否   | 通用 |            查询玩家的 Yggdrasil 档案信息            |
|   `uid`    | 群员 |  否   | 通用 |             查询 UID 对应的用户档案信息             |
| `view.ygg` | 群员 |  否   | 通用 | 查看指定玩家的 Yggdrasil 皮肤预览图 (等同于 `view`) |
| `view.pro` | 群员 |  否   | 通用 |           查看指定玩家的 正版 皮肤预览图            |

## 📝 更新日志

### 0.1.0

- 完成大部分指令适配迁移
- 新增配置项
  - `LTSK_API_TOKEN`
  - `LTSK_BROWSERLESS_API`
  - `LTSK_IPIP_API`
  - `LTSK_SKINRENDERMC_API`
