基于 Universal Radio Hacker 2.10.0 的简体中文版本。

- 默认使用简体中文，覆盖信号解析、协议分析、信号生成、协议仿真、设备设置、解码和常用提示。
- 在“编辑 → 选项 → 视图”中选择界面语言，重启生效。
- 保留原有协议格式、解码标识与工程数据兼容性。
- GitHub Actions 编译原生扩展，执行翻译校验、中文界面自检和回归测试，并检查打包后的程序能启动。

下载文件说明：

- `windows-x64-setup.exe`：Windows 64 位安装包。
- `windows-x64-portable.zip`：Windows 便携版，解压后运行 `urh/urh.exe`。
- `linux-x64.tar.gz`：Linux x64 便携版，在 Ubuntu 22.04 上构建；解压后运行 `urh/urh`。
- `macos-arm64.dmg`：Apple Silicon Mac 版本，将应用拖到 Applications。
- `.whl`：Python 3.12 对应平台的安装包，用 `python -m pip install 文件名.whl` 安装。
- `source.tar.gz`：源码。
- `SHA256SUMS.txt`：全部文件的 SHA-256 校验值。

Windows 包含上游 SDR 驱动库。Linux/macOS 的设备权限及部分 SDR 驱动仍需按上游文档配置。安装包未做代码签名。

源码与问题反馈：https://github.com/78-HAM/urh-zh_cn
上游项目：https://github.com/jopohl/urh
