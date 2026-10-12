# Universal Radio Hacker 简体中文版

![URH](https://raw.githubusercontent.com/jopohl/urh/master/data/icons/banner.png)

[![构建与发布](https://github.com/78-HAM/urh-zh_cn/actions/workflows/ci.yml/badge.svg)](https://github.com/78-HAM/urh-zh_cn/actions/workflows/ci.yml)
[下载简体中文版](https://github.com/78-HAM/urh-zh_cn/releases/latest) · [English / 上游说明](README.en.md) · [上游项目](https://github.com/jopohl/urh)

URH 是无线协议分析工具，支持多种软件定义无线电（SDR）。它可以录制、解调和分析信号，识别协议字段，配置解码流程，生成和发送信号，以及执行协议模糊测试和仿真。

本项目基于上游 **2.10.0**，默认显示简体中文。翻译资源覆盖主界面、右键菜单、选项、收发、解码、校验和、调制、模糊测试与协议仿真窗口。调制缩写、设备型号、协议数据和解码内部标识保留原值，兼容已有工程。

## 下载与安装

在 [Releases](https://github.com/78-HAM/urh-zh_cn/releases/latest) 下载对应系统的文件：

| 文件 | 用途 |
| --- | --- |
| `URH-zh_CN-2.10.0-windows-x64-setup.exe` | Windows 64 位安装包 |
| `URH-zh_CN-2.10.0-windows-x64-portable.zip` | Windows 便携版，解压后运行 `urh/urh.exe` |
| `URH-zh_CN-2.10.0-linux-x64.tar.gz` | Linux x64 便携版，解压后运行 `urh/urh` |
| `URH-zh_CN-2.10.0-macos-arm64.dmg` | Apple Silicon Mac 版，拖到 Applications 安装 |
| `*.whl` | Python 3.12 对应平台的安装包 |
| `*-source.tar.gz` | 源码包 |
| `SHA256SUMS.txt` | 文件 SHA-256 校验值 |

Windows 包含上游 SDR 驱动库。Linux 包在 Ubuntu 22.04 上构建，需要兼容的系统及图形库；macOS 包适用于 Apple Silicon。访问实际硬件时，可能还需安装 USB 驱动或配置 [udev 规则](https://github.com/jopohl/urh/wiki/SDR-udev-rules)。未对安装包进行代码签名。

Python wheel 安装示例：

```sh
python -m pip install ./urh-2.10.0-cp312-cp312-win_amd64.whl
urh
```

通过 PyPI 安装 `urh` 得到的是上游版本；本项目的中文包从本仓库 Release 下载。

## 切换语言

打开 **编辑 → 选项 → 视图 → 界面语言**，选择简体中文或 English，重启生效。

也可临时设置环境变量，不修改保存的偏好：

```powershell
$env:URH_LANGUAGE = 'en'
urh
```

```sh
URH_LANGUAGE=zh_CN urh
```

## 从源码运行

需要 Python 3.9 或更高版本及 C/C++ 编译器；发布构建固定使用 Python 3.12。Windows 使用 Visual Studio C++ Build Tools，Linux 使用 GCC，macOS 使用 Xcode Command Line Tools。

```sh
git clone https://github.com/78-HAM/urh-zh_cn.git
cd urh-zh_cn
python -m venv venv
# Windows：venv\Scripts\activate
# Linux/macOS：source venv/bin/activate
python -m pip install -r data/release-requirements.txt
python setup.py build_ext --inplace
python -m pip install --no-build-isolation .
urh
```

## 翻译维护与验证

翻译目录为 `src/urh/i18n/zh_CN.json`。Qt 在创建窗口之前加载翻译，未翻译的文字回退为英文；标准按钮使用 Qt 的中文资源。新增动态界面文案时用 `self.tr("原文")` 或 `urh.i18n.tr("原文")`，先翻译模板再填充变量。保持格式占位符、链接地址、文件扩展名和内部数据标识不变。

```sh
python data/check_translations.py
```

该命令校验翻译占位符和链接，并在离屏环境检查中文主窗口、语言设置、校验和切换、调制和时频图功能，不需要 SDR 硬件。

## Actions 构建与发布

[Build and Release 工作流](https://github.com/78-HAM/urh-zh_cn/actions/workflows/ci.yml) 在 master 推送、PR 或手动触发时，编译 Windows x64、Linux x64 和 macOS ARM64 的原生扩展及独立应用，执行中文界面检查与回归测试，上传构建产物。

推送格式为 `v*-zh.*` 的标签（例如 `v2.10.0-zh.1`）后，所有平台构建及检查通过才会自动发布 GitHub Release，并附带安装包、便携包、wheel、源码和 SHA-256 校验值。

```sh
git tag v2.10.0-zh.1
git push origin v2.10.0-zh.1
```

## 文档与许可

- [上游用户手册 PDF](https://github.com/jopohl/urh/releases/download/v2.0.0/userguide.pdf)
- [支持的设备](https://github.com/jopohl/urh/wiki/Supported-devices)
- [上游 Wiki](https://github.com/jopohl/urh/wiki)
- [中文版本问题反馈](https://github.com/78-HAM/urh-zh_cn/issues)

URH 由 Johannes Pohl 和 Andreas Noack 等上游贡献者开发；本仓库提供简体中文适配与构建发布。沿用 [GPL-3.0 许可](LICENSE)，引用信息见 [上游说明](README.en.md)。
