from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextBrowser
from paths import Paths


class HelpInterface(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.texto = QTextBrowser()
        self.texto.setOpenExternalLinks(True)
        layout.addWidget(self.texto)

        try:
            with open(Paths.help, "r", encoding="utf-8") as f:
                self.texto.setMarkdown(f.read())
        except FileNotFoundError:
            self.texto.setMarkdown("**Arquivo help.md não encontrado.**")