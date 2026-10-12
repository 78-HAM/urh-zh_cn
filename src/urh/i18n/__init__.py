"""Qt translations; protocol identifiers and saved data remain language independent."""

import json
import os
from pathlib import Path

from PyQt6.QtCore import QCoreApplication, QLibraryInfo, QTranslator

SUPPORTED_LANGUAGES = ("zh_CN", "en")


class ChineseTranslator(QTranslator):
    def __init__(self, parent=None):
        super().__init__(parent)
        with Path(__file__).with_name("zh_CN.json").open(encoding="utf-8") as catalog:
            self.messages = json.load(catalog)

    def isEmpty(self):
        return not self.messages

    def translate(self, context, sourceText, disambiguation=None, n=-1):
        return self.messages.get(sourceText)


def tr(text):
    return QCoreApplication.translate("urh", text)


def install_translators(app, language=None):
    """Install before creating widgets and keep translators alive on the app.

    This fork defaults to Chinese. URH_LANGUAGE overrides the saved preference
    for a single launch, including English regression tests and troubleshooting.
    """
    from urh import settings

    if language is None:
        language = os.environ.get("URH_LANGUAGE") or settings.read("language", "zh_CN")
    if language not in SUPPORTED_LANGUAGES:
        language = "zh_CN"
    for translator in getattr(app, "_urh_translators", []):
        app.removeTranslator(translator)
    app._urh_translators = []
    if language == "zh_CN":
        qt_translator = QTranslator(app)
        translations_dir = QLibraryInfo.path(QLibraryInfo.LibraryPath.TranslationsPath)
        if qt_translator.load("qtbase_zh_CN", translations_dir):
            app.installTranslator(qt_translator)
            app._urh_translators.append(qt_translator)
        translator = ChineseTranslator(app)
        if not app.installTranslator(translator):
            raise RuntimeError("Could not install the Chinese translation catalog")
        app._urh_translators.append(translator)
    return language
