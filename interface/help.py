from PySide6.QtWidgets import QWidget, QVBoxLayout, QTextEdit
from paths import Paths


class HelpInterface(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.texto = QTextEdit()
        self.texto.setReadOnly(True)
        layout.addWidget(self.texto)

        try:
            with open(Paths.help, "r", encoding="utf-8") as f:
                self.texto.setPlainText(f.read())
        except FileNotFoundError:
            self.texto.setPlainText("Arquivo help.txt não encontrado.")