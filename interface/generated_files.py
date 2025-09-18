from os import listdir, path
from pathlib import Path
from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QTextEdit, QPushButton
from modules.env_manager import EnvManager


class GeneratedFilesInterface(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.lista = QListWidget()
        self.editor = QTextEdit()
        self.btn_salvar = QPushButton("Salvar Arquivo")

        layout.addWidget(self.lista)
        layout.addWidget(self.editor)
        layout.addWidget(self.btn_salvar)

        self.pasta = Path(EnvManager.get_env('OUTPUT_PATH'))
        self.carregar_arquivos()

        self.lista.itemClicked.connect(self.abrir_arquivo)
        self.btn_salvar.clicked.connect(self.salvar_arquivo)

        self.arquivo_atual = None

    def carregar_arquivos(self):
        self.lista.clear()
        for f in listdir(self.pasta):
            if path.isfile(path.join(self.pasta, f)):
                self.lista.addItem(f)

    def abrir_arquivo(self, item):
        file_path = path.join(self.pasta, item.text())
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            self.editor.setPlainText(f.read())
        self.arquivo_atual = file_path

    def salvar_arquivo(self):
        if self.arquivo_atual:
            with open(self.arquivo_atual, "w", encoding="utf-8") as f:
                f.write(self.editor.toPlainText())