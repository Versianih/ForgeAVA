from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)

class AvaActivityInterface(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)

        self.identifier_type = QComboBox()
        self.identifier_type.addItems(["ID", "URL"])

        self.action = QComboBox()
        self.action.addItems(["Sim, quero enviar.", "Não, apenas salvar."])

        self.url_or_id = QLineEdit()

        self.filename = QLineEdit()

        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.setEnabled(False)

        layout.addWidget(QLabel("Identificador da atividade AVA:"))
        layout.addWidget(self.identifier_type)
        layout.addWidget(QLabel("Deseja enviar o código pro AVA automaticamente?"))
        layout.addWidget(self.action)
        layout.addWidget(QLabel("URL ou ID da atividade do AVA:"))
        layout.addWidget(self.url_or_id)
        layout.addWidget(QLabel("Nome do arquivo a ser gerado:"))
        layout.addWidget(self.filename)
        layout.addWidget(self.btn_enviar)

        self.url_or_id.textChanged.connect(self.validar_campos)
        self.filename.textChanged.connect(self.validar_campos)
        self.identifier_type.currentIndexChanged.connect(self.validar_campos)
        self.action.currentIndexChanged.connect(self.validar_campos)
        self.btn_enviar.clicked.connect(self.process_data)

        self.setLayout(layout)

    def validar_campos(self):
        if (self.url_or_id.text().strip() and 
            self.filename.text().strip() and 
            self.identifier_type.currentIndex() >= 0 and 
            self.action.currentIndex() >= 0):
            self.btn_enviar.setEnabled(True)
        else:
            self.btn_enviar.setEnabled(False)

    def get_data(self):
        return {
            "identifier_type": self.identifier_type.currentText(),
            "action": self.action.currentText(),
            "url_or_id": self.url_or_id.text(),
            "filename": self.filename.text()
        }

    def process_data(self):
        try:
            data = self.get_data()

            QMessageBox.information(self, "Sucesso", f"Dados processados com sucesso!\n{data}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox
)

class AvaActivityInterface(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)  # Define espaçamento fixo entre widgets

        self.identifier_type = QComboBox()
        self.identifier_type.addItems(["ID", "URL"])

        self.action = QComboBox()
        self.action.addItems(["Sim, quero enviar.", "Não, apenas salvar."])

        self.url_or_id = QLineEdit()

        self.filename = QLineEdit()

        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.setEnabled(False)

        layout.addWidget(QLabel("Identificador da atividade AVA:"))
        layout.addWidget(self.identifier_type)
        layout.addWidget(QLabel("Deseja enviar o código pro AVA automaticamente?"))
        layout.addWidget(self.action)
        layout.addWidget(QLabel("URL ou ID da atividade do AVA:"))
        layout.addWidget(self.url_or_id)
        layout.addWidget(QLabel("Nome do arquivo a ser gerado:"))
        layout.addWidget(self.filename)
        layout.addWidget(self.btn_enviar)
        
        # CORREÇÃO: Adiciona stretch para empurrar tudo para cima
        layout.addStretch()

        self.url_or_id.textChanged.connect(self.validar_campos)
        self.filename.textChanged.connect(self.validar_campos)
        self.identifier_type.currentIndexChanged.connect(self.validar_campos)
        self.action.currentIndexChanged.connect(self.validar_campos)
        self.btn_enviar.clicked.connect(self.process_data)

        self.setLayout(layout)

    def validar_campos(self):
        if (self.url_or_id.text().strip() and 
            self.filename.text().strip() and 
            self.identifier_type.currentIndex() >= 0 and 
            self.action.currentIndex() >= 0):
            self.btn_enviar.setEnabled(True)
        else:
            self.btn_enviar.setEnabled(False)

    def get_data(self):
        return {
            "identifier_type": self.identifier_type.currentText(),
            "action": self.action.currentText(),
            "url_or_id": self.url_or_id.text(),
            "filename": self.filename.text()
        }

    def process_data(self):
        try:
            data = self.get_data()

            QMessageBox.information(self, "Sucesso", f"Dados processados com sucesso!\n{data}")
        except Exception as e:
            QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {str(e)}")