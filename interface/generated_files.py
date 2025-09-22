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
        self.pasta = Path(EnvManager.get_env('OUTPUT_PATH'))
        self.arquivo_atual = None
        self.arquivo_original = None

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(20, 20, 20, 20)

        self.label_caminho = QLabel(str(self.pasta))
        self.label_caminho.setAlignment(Qt.AlignCenter)

        self.lista = QListWidget()
        self.editor = CustomTextEdit()
        self.editor.hide()

        self.btn_salvar = QPushButton("Salvar Alterações")
        self.btn_salvar.setEnabled(False)
        self.btn_salvar.hide()

        self.btn_voltar = QPushButton("← Voltar")
        self.btn_voltar.setFixedWidth(80)
        self.btn_voltar.hide()

        self.top_bar = QHBoxLayout()
        self.top_bar.addWidget(self.btn_voltar)
        self.top_bar.addStretch()
        self.top_bar.addWidget(self.label_caminho)
        self.top_bar.addStretch()

        # Adiciona a barra superior (com caminho da pasta) antes da lista
        self.layout.addLayout(self.top_bar)
        self.layout.addWidget(self.lista)
        self.layout.addWidget(self.editor)
        self.layout.addWidget(self.btn_salvar)

        self.carregar_arquivos()

        self.lista.itemClicked.connect(self.abrir_arquivo)
        self.btn_salvar.clicked.connect(self.salvar_arquivo)
        self.btn_voltar.clicked.connect(self.voltar_lista)
        self.editor.textChanged.connect(self.verificar_alteracoes)

    def carregar_arquivos(self):
        self.label_caminho.setText(str(self.pasta))
        self.lista.clear()
        if self.pasta.exists():
            for f in listdir(self.pasta):
                if path.isfile(path.join(self.pasta, f)):
                    self.lista.addItem(f)

    def abrir_arquivo(self, item):
        file_path = str(path.join(self.pasta, item.text()))
        conteudo = FileManager.read_file(file_path)
        self.editor.setPlainText(conteudo)
        self.arquivo_original = conteudo
        self.arquivo_atual = file_path
        self.lista.hide()
        self.editor.show()
        self.btn_salvar.hide()
        self.btn_voltar.show()
        self.label_caminho.setText(file_path)
        self.verificar_alteracoes()

    def verificar_alteracoes(self):
        if self.arquivo_atual is not None:
            conteudo_atual = self.editor.toPlainText()
            if conteudo_atual != self.arquivo_original:
                self.btn_salvar.show()
                self.btn_salvar.setEnabled(True)
            else:
                self.btn_salvar.hide()
                self.btn_salvar.setEnabled(False)

    def salvar_arquivo(self):
        if self.arquivo_atual:
            FileManager.save_file(self.editor.toPlainText(), self.arquivo_atual)
            self.arquivo_original = self.editor.toPlainText()
            self.btn_salvar.hide()
            self.btn_salvar.setEnabled(False)
            debug.log(f"Arquivo salvo: {self.arquivo_atual}")
            QMessageBox.information(self, "Sucesso", "Alterações salvas com sucesso!")

    def voltar_lista(self):
        self.editor.hide()
        self.btn_salvar.hide()
        self.btn_voltar.hide()
        self.lista.show()
        self.label_caminho.setText(str(self.pasta))
        self.carregar_arquivos()
        self.arquivo_atual = None
        self.arquivo_original = None