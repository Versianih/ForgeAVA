from PySide6.QtWidgets import (
    QVBoxLayout, QLabel
)
from PySide6.QtCore import (
    QThread, Signal
)

from modules.file_manager import FileManager
from modules.ava_manager import AvaManager
from modules.prompt_manager import PromptManager

from api.call_api import CallLLM

from modules.debug import Debug
debug = Debug()


class Utils:
    @staticmethod
    def add_label(layout: QVBoxLayout, name: str, *args):
        if name:
            layout.addWidget(QLabel(name))
        for arg in args:
            layout.addWidget(arg)

class ProcessingThread(QThread):
    progress_update = Signal(str)
    finished_success = Signal(str)
    finished_error = Signal(str)
    
    def __init__(self, data: dict, gen_type: str):
        super().__init__()
        self.data = data
        self.gen_type = gen_type
    
    def run(self):
        try:
            match self.gen_type:
                case 'AVA':
                    self._process_ava_activity()
                case 'PROMPT':
                    self._process_response()

        except Exception as e:
            debug.log(f"Erro ao processar atividade: {e}")
            self.finished_error.emit(str(e))
    
    def _process_ava_activity(self):
        self.progress_update.emit("🔧 Inicializando componentes...")
        ava_manager = AvaManager()
        llm = CallLLM()
        prompt_manager = PromptManager()

        valor = self.data['url_or_id']
        if not valor.isdigit():
            self.progress_update.emit("🔗 Extraindo ID da URL...")
            valor = ava_manager.extract_id_from_url(valor)

        self.progress_update.emit("🌐 Conectando ao AVA e obtendo atividade(Esta ação pode demorar um pouco)...")
        activity = ava_manager.get_activity_text(
            login=self.data['login'],
            password=self.data['password'],
            activity_id=valor
        )

        self.progress_update.emit("📝 Preparando prompt para IA...")
        prompt = prompt_manager.get_activity_prompt(activity_content=activity)
        
        self.progress_update.emit("🤖 Processando com IA (isso pode demorar)...")
        response = llm.call(prompt=prompt)
        
        self.progress_update.emit("💾 Salvando arquivo...")
        FileManager.save_response(
            content=response,
            filename=self.data['filename']
        )

        if self.data['action'] == 'Sim, quero enviar.':
            self.progress_update.emit("📤 Enviando resposta para o AVA...")
            ava_manager.submit_file(
                login=self.data['login'],
                password=self.data['password'],
                activity_id=valor,
                file_path=self.data['output_path'],
                filename=self.data['filename']
            )

        debug.log(f"Processamento concluído.")
        self.progress_update.emit("✅ Processamento concluído!")
        self.finished_success.emit(f"Arquivo '{self.data['filename']}' salvo com sucesso!")

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