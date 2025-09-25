from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLineEdit, QComboBox, QPushButton,
    QFileDialog, QPlainTextEdit, QLabel, QMessageBox, QScrollArea
)
from PySide6.QtCore import Qt
from interface.utils import Utils
from modules.env_manager import EnvManager
from modules.prompt_manager import PromptManager
from modules.language import Language
from api.models import Models

from modules.debug import Debug
debug = Debug()


class SettingsInterface(QWidget, Utils):
    def __init__(self):
        super().__init__()
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        
        content_widget = QWidget()
        layout = QVBoxLayout(content_widget)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.login = QLineEdit()
        self.login.setPlaceholderText("Login AVA")

        self.password = QLineEdit()
        self.password.setPlaceholderText("Senha AVA")
        self.password.setEchoMode(QLineEdit.Password)

        self.api_key = QLineEdit()
        self.api_key.setPlaceholderText("Chave API")

        self.model_dropdown = QComboBox()
        for label, value in zip(Models.get_models_list_with_provider(), Models.get_models_list()):
            self.model_dropdown.addItem(label, value)
        self.model_dropdown.setEditable(False)
        self.model_dropdown.setInsertPolicy(QComboBox.NoInsert)

        self.language_dropdown = QComboBox()
        self.language_dropdown.addItems(Language.languages)
        self.language_dropdown.setEditable(False)
        self.language_dropdown.setInsertPolicy(QComboBox.NoInsert)

        self.use_prompt = QComboBox()
        self.use_prompt.addItems(["Sim", "Não"])

        self.prompt_btn = QPushButton("Abrir Prompt")
        self.prompt_editor = QPlainTextEdit()
        self.prompt_editor.hide()
        self.prompt_editor.setMinimumHeight(200)

        self.prompt_save_btn = QPushButton("Salvar Prompt")
        self.prompt_save_btn.hide()

        self.output_path = QLabel("Nenhuma pasta selecionada")
        self.output_path.setStyleSheet("font-size: 12px; color: #aaa;")
        self.path_btn = QPushButton("Selecionar Pasta")

        self.save_btn = QPushButton("Salvar Configurações")

        self.add_label(layout, "Login AVA:", self.login)
        self.add_label(layout, "Senha AVA:", self.password)
        self.add_label(layout, "API-KEY:", self.api_key)
        self.add_label(
            layout, 
            "Usar Prompt?", 
            self.use_prompt, 
            self.prompt_btn, 
            self.prompt_editor, 
            self.prompt_save_btn
        )
        self.add_label(layout, "Modelo de IA:", self.model_dropdown)
        self.add_label(layout, "Linguagem Utilizada:", self.language_dropdown)
        self.add_label(
            layout, 
            "Pasta de output dos arquivos gerados:", 
            self.output_path, 
            self.path_btn
        )

        layout.addStretch()
        self.add_label(layout, None, self.save_btn)

        scroll_area.setWidget(content_widget)
        main_layout.addWidget(scroll_area)

        self.prompt_btn.clicked.connect(self.toggle_prompt)
        self.path_btn.clicked.connect(self.selecionar_pasta)
        self.save_btn.clicked.connect(self.save_settings)
        self.prompt_save_btn.clicked.connect(self.save_prompt)

        self.load_settings()

    def toggle_prompt(self):
        visible = not self.prompt_editor.isVisible()
        self.prompt_editor.setVisible(visible)
        self.prompt_save_btn.setVisible(visible)
        
        if visible: self.prompt_btn.setText("Fechar Prompt")
        else: self.prompt_btn.setText("Abrir Prompt")

    def selecionar_pasta(self):
        pasta = QFileDialog.getExistingDirectory(self, "Selecionar Pasta")
        if pasta:
            self.output_path.setText(pasta)

    def save_settings(self):
        try:
            data = self.get_settings()
            new_settings = {
                'LOGIN': data['login'],
                'PASSWORD': data['password'],
                'API_KEY': data['api_key'],
                'MODEL': data['model'],
                'LANGUAGE': data['language'],
                'OUTPUT_PATH': data['output'],
                'USE_PROMPT': data['use_prompt']
            }
            EnvManager.update_env(new_settings)

            debug.log("Configurações salvas com sucesso.")
            QMessageBox.information(self, "Sucesso", "Configurações salvas com sucesso!")

            parent = self.parent()
            while parent:
                if hasattr(parent, "stack"):
                    widget = parent.stack.widget(2)
                    if hasattr(widget, "load_files"):
                        widget.load_files()
                    break
                parent = parent.parent()

        except Exception as e:
            debug.log(f"Erro ao salvar configurações: {e}")
            QMessageBox.critical(self, "Erro", "Erro ao salvar configurações.")

    def save_prompt(self):
        try:
            prompt = self.get_prompt()
            prompt_manager = PromptManager()
            prompt_manager.save_prompt(prompt)

            debug.log("Prompt salvo com sucesso.")
            QMessageBox.information(self, "Sucesso", "Prompt salvo com sucesso!")
        except Exception as e:
            debug.log(f"Erro ao salvar o prompt: {e}")
            QMessageBox.critical(self, "Erro", "Erro ao salvar o prompt.")

    def load_settings(self):
        manager = EnvManager()
        prompt_manager = PromptManager()

        self.login.setText(manager.get_env("LOGIN"))
        self.password.setText(manager.get_env("PASSWORD"))
        self.api_key.setText(manager.get_env("API_KEY"))
        self.output_path.setText(manager.get_env("OUTPUT_PATH"))

        model_value = manager.get_env("MODEL")
        index = self.model_dropdown.findData(model_value)
        if index >= 0:
            self.model_dropdown.setCurrentIndex(index)

        prompt_value = manager.get_env("USE_PROMPT")
        index = self.use_prompt.findText(prompt_value)
        if index >= 0:
            self.use_prompt.setCurrentIndex(index)

        language_value = manager.get_env("LANGUAGE")
        index = self.language_dropdown.findText(language_value)
        if index >= 0:
            self.language_dropdown.setCurrentIndex(index)

        saved_prompt = prompt_manager.read_prompt()
        if saved_prompt:
            self.prompt_editor.setPlainText(saved_prompt)

    def get_settings(self):
        return {
            "login": self.login.text(),
            "password": self.password.text(),
            "api_key": self.api_key.text(),
            "model": self.model_dropdown.currentData(),
            "language": self.language_dropdown.currentText(),
            "use_prompt": self.use_prompt.currentText(),
            "output": self.output_path.text()
        }

    def get_prompt(self):
        return self.prompt_editor.toPlainText()