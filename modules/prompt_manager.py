from paths import Paths
from modules.file_manager import FileManager
from modules.env_manager import EnvManager

class PromptManager:
    @staticmethod
    def get_activity_prompt(activity_content: str) -> str:
        raw_prompt = PromptManager.read_prompt()
        format_keys = {
            'activity_content': activity_content,
            'language': EnvManager.get_env('LANGUAGE')
        }
        prompt = raw_prompt.format(**format_keys)
        return prompt
    
    @staticmethod
    def read_prompt() -> str:
        prompt = FileManager.read_file(Paths.prompt)
        return prompt
    
    @staticmethod
    def save_prompt(content:str) -> None:
        FileManager.save_file(content, Paths.prompt)