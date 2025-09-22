from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QPushButton, QMessageBox, QProgressBar
)
from PySide6.QtCore import QThread, Signal
from modules.prompt_manager import PromptManager
from modules.file_manager import FileManager
from api.call_api import CallLLM

from modules.debug import Debug
debug = Debug()


class ProcessingThread(QThread):
    progress_update = Signal(str)
    finished_success = Signal(str)
    finished_error = Signal(str)
    
    def __init__(self, data):
        super().__init__()
        self.data = data
    
    def run(self):
        try:
            self._process_response()
        except Exception as e:
            debug.log(f"Erro ao processar resposta: {e}")
            self.finished_error.emit(str(e))
    
    def _process_response(self):
        self.progress_update.emit("🔧 Inicializando componentes...")
        llm = CallLLM()
        prompt_manager = PromptManager()
        prompt_text = self.data['prompt_text']
        
        self.progress_update.emit("📝 Preparando prompt para IA...")
        prompt = prompt_manager.get_activity_prompt(activity_content=prompt_text)
        
        self.progress_update.emit("🤖 Processando com IA (isso pode demorar)...")
        response = llm.call(prompt=prompt)
        
        self.progress_update.emit("💾 Salvando arquivo...")
        FileManager.save_response(
            content=response,
            filename=self.data['filename']
        )
        
        self.progress_update.emit("✅ Processamento concluído!")
        self.finished_success.emit(f"Arquivo '{self.data['filename']}' salvo com sucesso!")


class PromptGeneratorInterface(QWidget):
    def __init__(self):
        super().__init__()
        self.processing_thread = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.prompt_text = QLineEdit()
        self.filename = QLineEdit()

        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.setEnabled(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        
        self.status_label = QLabel("")
        self.status_label.setVisible(False)
        self.status_label.setStyleSheet("color: #666; font-style: italic;")

        layout.addWidget(QLabel("Prompt para geração de código:"))
        layout.addWidget(self.prompt_text)
        layout.addWidget(QLabel("Nome do arquivo a ser gerado:"))
        layout.addWidget(self.filename)
        layout.addWidget(self.btn_enviar)
        
        layout.addWidget(self.progress_bar)
        layout.addWidget(self.status_label)
        
        layout.addStretch()
        self.setLayout(layout)

    def _connect_signals(self):
        self.prompt_text.textChanged.connect(self.validar_campos)
        self.filename.textChanged.connect(self.validar_campos)
        self.btn_enviar.clicked.connect(self.process_data)

    def validar_campos(self) -> None:
        campos_validos = (
            bool(self.prompt_text.text().strip()) and 
            bool(self.filename.text().strip())
        )
        self.btn_enviar.setEnabled(campos_validos)

    def get_data(self) -> dict:
        return {
            "prompt_text": self.prompt_text.text().strip(),
            "filename": self.filename.text().strip()
        }

    def _show_processing_ui(self) -> None:
        self.btn_enviar.setEnabled(False)
        self.btn_enviar.setText("Processando...")
        self.progress_bar.setVisible(True)
        self.status_label.setVisible(True)

    def _hide_processing_ui(self) -> None:
        self.btn_enviar.setEnabled(True)
        self.btn_enviar.setText("Enviar")
        self.progress_bar.setVisible(False)
        self.status_label.setVisible(False)
        self.validar_campos()

    def _update_progress(self, message: str) -> None:
        self.status_label.setText(message)

    def _on_processing_success(self, message: str) -> None:
        self._hide_processing_ui()
        QMessageBox.information(self, "Sucesso", message)
        self.prompt_text.clear()
        self.filename.clear()
        self._reload_generated_files()

    def _reload_generated_files(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, "stack"):
                widget = parent.stack.widget(2)
                if hasattr(widget, "carregar_arquivos"):
                    widget.carregar_arquivos()
                break
            parent = parent.parent()

    def _on_processing_error(self, error_message: str) -> None:
        self._hide_processing_ui()
        QMessageBox.critical(self, "Erro", f"Ocorreu um erro: {error_message}")

    def process_data(self) -> None:
        try:
            data = self.get_data()
            if not data or not all(data.values()):
                QMessageBox.warning(self, "Aviso", "Por favor, preencha todos os campos.")
                return
            
            self._show_processing_ui()

            self.processing_thread = ProcessingThread(data)
            self.processing_thread.progress_update.connect(self._update_progress)
            self.processing_thread.finished_success.connect(self._on_processing_success)
            self.processing_thread.finished_error.connect(self._on_processing_error)
            self.processing_thread.start()
            
        except Exception as e:
            self._hide_processing_ui()
            debug.log(f"Erro inesperado ao iniciar o processamento: {e}")
            QMessageBox.critical(self, "Erro", f"Erro inesperado: {str(e)}")

    def closeEvent(self, event):
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
        event.accept()