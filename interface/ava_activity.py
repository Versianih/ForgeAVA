from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QMessageBox, QProgressBar
)
from interface.utils import Utils, ProcessingThread
from modules.env_manager import EnvManager

from modules.debug import Debug
debug = Debug()


class AvaActivityInterface(QWidget, Utils):
    def __init__(self):
        super().__init__()
        self.processing_thread = None
        self._setup_ui()
        self._connect_signals()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(10)

        self.action = QComboBox()
        self.action.addItems(["Sim, quero enviar.", "Não, apenas salvar."])

        self.url_or_id = QLineEdit()
        self.filename = QLineEdit()

        self.btn_enviar = QPushButton("Enviar")
        self.btn_enviar.setEnabled(False)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.progress_bar.setRange(0, 0)
        
        self.status_label = QLabel("")
        self.status_label.setVisible(False)
        self.status_label.setStyleSheet("color: #666; font-style: italic;")

        self.add_label(layout, 'Deseja enviar o código pro AVA automaticamente?', self.action)
        self.add_label(layout, 'URL ou ID da atividade do AVA:', self.url_or_id)
        self.add_label(layout, 'Nome do arquivo a ser gerado:', self.filename)
        
        self.add_label(
            layout,
            None,
            self.btn_enviar,
            self.progress_bar,
            self.status_label
        )
        
        layout.addStretch()
        self.setLayout(layout)

    def _connect_signals(self):
        self.url_or_id.textChanged.connect(self.validar_campos)
        self.filename.textChanged.connect(self.validar_campos)
        self.action.currentIndexChanged.connect(self.validar_campos)
        self.btn_enviar.clicked.connect(self.process_data)

    def validar_campos(self) -> None:
        campos_validos = (
            bool(self.url_or_id.text().strip()) and 
            bool(self.filename.text().strip()) and 
            self.action.currentIndex() >= 0
        )
        self.btn_enviar.setEnabled(campos_validos)

    def get_data(self) -> dict:
        return {
            'action': self.action.currentText(),
            'url_or_id': self.url_or_id.text().strip(),
            'filename': self.filename.text().strip(),
            'login': EnvManager.get_env('LOGIN'),
            'password': EnvManager.get_env('PASSWORD'),
            'output_path': EnvManager.get_env('OUTPUT_PATH')
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
        self.url_or_id.clear()
        self.filename.clear()
        self._reload_generated_files()

    def _reload_generated_files(self):
        parent = self.parent()
        while parent:
            if hasattr(parent, "stack"):
                widget = parent.stack.widget(2)
                if hasattr(widget, "load_files"):
                    widget.load_files()
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

            self.processing_thread = ProcessingThread(data, 'AVA')
            self.processing_thread.progress_update.connect(self._update_progress)
            self.processing_thread.finished_success.connect(self._on_processing_success)
            self.processing_thread.finished_error.connect(self._on_processing_error)
            self.processing_thread.start()
            
        except Exception as e:
            self._hide_processing_ui()
            debug.log(f"Erro inesperado ao iniciar o processamento: {e}")
            QMessageBox.critical(self, "Erro", f"Erro inesperado.")

    def closeEvent(self, event):
        if self.processing_thread and self.processing_thread.isRunning():
            self.processing_thread.terminate()
            self.processing_thread.wait()
        event.accept()