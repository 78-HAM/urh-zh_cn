"""Validate the catalog and exercise the Chinese GUI without radio hardware."""

import json
import os
import re
import string
import sys
from collections import Counter
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from PyQt6.QtCore import Qt, QSettings
from PyQt6.QtWidgets import QApplication

from urh import settings
from urh.i18n import ChineseTranslator, install_translators, tr


def fields(text):
    return Counter(
        (field, spec, conversion)
        for _, field, spec, conversion in string.Formatter().parse(text)
        if field is not None
    )


def main():
    # Do not touch the user's preferences during a smoke test.
    import tempfile

    test_dir = tempfile.TemporaryDirectory()
    QSettings.setPath(
        QSettings.Format.IniFormat, QSettings.Scope.UserScope, test_dir.name
    )
    app = QApplication([])
    translator = ChineseTranslator()
    for source, target in translator.messages.items():
        assert target.strip(), source
        assert fields(source) == fields(target), (source, target)
        assert Counter(re.findall(r"href=[\'\"]([^\'\"]+)", source)) == Counter(
            re.findall(r"href=[\'\"]([^\'\"]+)", target)
        ), source
        assert Counter(re.findall(r"%[psvmdn]|%s", source)) == Counter(
            re.findall(r"%[psvmdn]|%s", target)
        ), source

    install_translators(app, "zh_CN")
    assert tr("Search") == "搜索"
    assert (
        tr("A missing translation must stay visible")
        == "A missing translation must stay visible"
    )
    assert app.translate("QPlatformTheme", "Cancel") == "取消"

    settings.write("not_show_close_dialog", True)
    settings.write("not_show_save_dialog", True)
    from urh.controller.MainController import MainController
    from urh.controller.dialogs.OptionsDialog import OptionsDialog
    from urh.controller.widgets.ChecksumWidget import ChecksumWidget
    from urh.signalprocessing.ChecksumLabel import ChecksumLabel
    from urh.signalprocessing.FieldType import FieldType
    from urh.signalprocessing.Modulator import Modulator
    from urh.signalprocessing.Message import Message
    from urh.signalprocessing.MessageType import MessageType
    from urh.controller.dialogs.ModulatorDialog import ModulatorDialog

    window = MainController()
    assert [window.ui.tabWidget.tabText(i) for i in range(4)] == [
        "信号解析",
        "协议分析",
        "信号生成",
        "协议仿真",
    ]
    options = OptionsDialog(window.plugin_manager.installed_plugins, parent=window)
    assert options.windowTitle() == "选项"
    options.language_combo.setCurrentIndex(1)
    assert settings.read("language") == "en"
    options.language_combo.setCurrentIndex(0)
    assert settings.read("language") == "zh_CN"
    assert (
        options.device_options_model.headerData(0, Qt.Orientation.Horizontal)
        == "软件定义无线电"
    )
    options.close()

    label = ChecksumLabel(
        "CRC", 8, 16, 0, FieldType("Checksum", FieldType.Function.CHECKSUM)
    )
    checksum = ChecksumWidget(label, Message([0] * 32, 0, MessageType("test")), 0)
    checksum.ui.comboBoxCategory.setCurrentIndex(1)
    assert label.category == ChecksumLabel.Category.wsp
    checksum.ui.comboBoxCategory.setCurrentIndex(0)
    assert label.category == ChecksumLabel.Category.generic
    checksum.close()

    modulation = ModulatorDialog([Modulator("test")])
    for i in range(modulation.ui.comboBoxModulationType.count()):
        modulation.ui.comboBoxModulationType.setCurrentIndex(i)
        assert (
            modulation.current_modulator.modulation_type in Modulator.MODULATION_TYPES
        )
    modulation.close()

    sample = Path(__file__).resolve().parents[1] / "tests/data/ask.complex"
    window.add_signalfile(str(sample))
    frame = window.signal_tab_controller.signal_frames[0]
    frame.ui.cbSignalView.setCurrentIndex(2)
    assert frame.ui.stackedWidget.currentWidget() == frame.ui.pageSpectrogram
    frame.ui.cbSignalView.setCurrentIndex(0)
    window.close_all_files()
    window.close()
    install_translators(app, "en")
    assert tr("Search") == "Search"
    print(
        f"Validated {len(translator.messages)} catalog entries and Chinese GUI smoke checks."
    )
    app.quit()


if __name__ == "__main__":
    main()
