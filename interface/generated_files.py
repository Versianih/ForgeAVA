from os import listdir, path
from pathlib import Path
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton, QHBoxLayout, QLabel, QMessageBox
)
from PySide6.QtCore import Qt
from modules.env_manager import EnvManager
from modules.file_manager import FileManager

from modules.debug import Debug
debug = Debug()


class CustomTextEdit(QTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Tab:
            cursor = self.textCursor()
            cursor.insertText(" " * 4)
        else:
            super().keyPressEvent(event)


class GeneratedFilesInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.folder = Path(EnvManager.get_env('OUTPUT_PATH'))
        self.current_file = None
        self.original_file = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label_path = QLabel(str(self.folder))
        self.label_path.setAlignment(Qt.AlignCenter)

        self.list = QListWidget()
        self.editor = CustomTextEdit()
        self.editor.hide()

        self.save_btn = QPushButton("Salvar Alterações")
        self.save_btn.setEnabled(False)
        self.save_btn.hide()

        self.back_btn = QPushButton("← Voltar")
        self.back_btn.setFixedWidth(80)
        self.back_btn.hide()

        self.top_bar = QHBoxLayout()
        self.top_bar.addWidget(self.back_btn)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.label_path)
        self.top_bar.addStretch()

        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.list)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.save_btn)

        self.load_files()

        self.list.itemClicked.connect(self.open_files)
        self.save_btn.clicked.connect(self.save_file)
        self.back_btn.clicked.connect(self.back_list)
        self.editor.textChanged.connect(self.check_changes)

    def load_files(self):
        self.update_folder()
        self.label_path.setText(str(self.folder))
        self.list.clear()
        if self.folder.exists():
            for f in listdir(self.folder):
                if path.isfile(path.join(self.folder, f)):
                    self.list.addItem(f)

    def open_files(self, item):
        file_path = str(path.join(self.folder, item.text()))
        conteudo = FileManager.read_file(file_path)
        self.editor.setPlainText(conteudo)
        self.original_file = conteudo
        self.current_file = file_path
        self.list.hide()
        self.editor.show()
        self.save_btn.hide()
        self.back_btn.show()
        self.label_path.setText(file_path)
        self.check_changes()

    def check_changes(self):
        if self.current_file is not None:
            conteudo_atual = self.editor.toPlainText()
            if conteudo_atual != self.original_file:
                self.save_btn.show()
                self.save_btn.setEnabled(True)
            else:
                self.save_btn.hide()
                self.save_btn.setEnabled(False)

    def save_file(self):
        if self.current_file:
            FileManager.save_file(self.editor.toPlainText(), self.current_file)
            self.original_file = self.editor.toPlainText()
            self.save_btn.hide()
            self.save_btn.setEnabled(False)
            debug.log(f"Arquivo salvo: {self.current_file}")
            QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")

    def back_list(self):
        self.editor.hide()
        self.save_btn.hide()
        self.back_btn.hide()
        self.list.show()
        self.label_path.setText(str(self.folder))
        self.load_files()
        self.current_file = None
        self.original_file = None

    def update_folder(self):
        self.folder = Path(EnvManager.get_env('OUTPUT_PATH'))