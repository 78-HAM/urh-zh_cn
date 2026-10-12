"""Build a standalone Chinese URH GUI and command-line launcher."""

import os
import subprocess
import sys
from pathlib import Path

from PyInstaller.utils.hooks import collect_submodules

root = Path(__file__).resolve().parents[1]
qt_dir = Path(__import__("PyQt6").__file__).parent / "Qt6"
args = [
    sys.executable,
    "-m",
    "PyInstaller",
    "--noconfirm",
    "--clean",
    "--paths",
    str(root / "src"),
    "--distpath",
    str(root / "pyinstaller"),
    "--workpath",
    str(root / "build/pyinstaller"),
    "--add-data",
    f"{root / 'src/urh/i18n/zh_CN.json'}{os.pathsep}urh/i18n",
    "--add-data",
    f"{root / 'src/urh/plugins'}{os.pathsep}urh/plugins",
    "--add-data",
    f"{qt_dir / 'translations/qtbase_zh_CN.qm'}{os.pathsep}PyQt6/Qt6/translations",
    "--exclude-module",
    "matplotlib",
]
for module in collect_submodules("urh.plugins") + collect_submodules(
    "urh.dev.native.lib"
):
    args.extend(["--hidden-import", module])
drivers = root / "src/urh/dev/native/lib/shared"
if drivers.exists():
    for dll in drivers.glob("*.dll"):
        args.extend(["--add-binary", f"{dll}{os.pathsep}."])
    for license_file in drivers.glob("*.txt"):
        args.extend(["--add-data", f"{license_file}{os.pathsep}."])
icon = root / (
    "data/icons/appicon.icns" if sys.platform == "darwin" else "data/icons/appicon.ico"
)
gui = args + ["--name", "urh", "--icon", str(icon)]
if sys.platform == "darwin":
    gui += ["--windowed", "--osx-bundle-identifier", "icu.bi4loj.urh-zh-cn"]
subprocess.run(gui + [str(root / "src/urh/main.py")], cwd=root, check=True)
subprocess.run(
    args + ["--name", "urh_cli", str(root / "src/urh/cli/urh_cli.py")],
    cwd=root,
    check=True,
)
if sys.platform == "win32":
    subprocess.run(
        args
        + [
            "--name",
            "urh_gui",
            "--windowed",
            "--icon",
            str(icon),
            str(root / "src/urh/main.py"),
        ],
        cwd=root,
        check=True,
    )
    import shutil

    shutil.copy2(
        root / "pyinstaller/urh/urh.exe", root / "pyinstaller/urh/urh_debug.exe"
    )
    shutil.copy2(
        root / "pyinstaller/urh_gui/urh_gui.exe", root / "pyinstaller/urh/urh.exe"
    )
    shutil.copy2(
        root / "pyinstaller/urh_cli/urh_cli.exe", root / "pyinstaller/urh/urh_cli.exe"
    )
    shutil.copytree(
        root / "pyinstaller/urh_cli/_internal",
        root / "pyinstaller/urh/_internal",
        dirs_exist_ok=True,
    )
    for document in ("LICENSE", "README.md"):
        shutil.copy2(root / document, root / "pyinstaller/urh" / document)
elif sys.platform == "darwin":
    import plistlib

    plist_file = root / "pyinstaller/urh.app/Contents/Info.plist"
    with plist_file.open("rb") as handle:
        plist = plistlib.load(handle)
    plist["CFBundleDisplayName"] = "URH 简体中文版"
    plist["NSMicrophoneUsageDescription"] = "URH 需要访问麦克风，通过声卡采集信号。"
    with plist_file.open("wb") as handle:
        plistlib.dump(plist, handle)
print("Standalone builds completed.")
