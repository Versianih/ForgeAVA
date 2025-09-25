from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton,
    QFileDialog, QPlainTextEdit, QLabel, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt

from modules.debug import Debug
debug = Debug()


class Utils:
    @staticmethod
    def add_label(layout: QVBoxLayout, name: str, *args):
        if name:
            layout.addWidget(QLabel(name))
        for arg in args:
            layout.addWidget(arg)