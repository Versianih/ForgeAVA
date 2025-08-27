from paths import Paths
from modules.file_manager import FileManager

class PromptManager:
    def __init__(self):
        self.raw_prompt = self.read_prompt()

    def get_activity_prompt(self, activity_content: str) -> str:
        prompt = self.raw_prompt.format(activity_content=activity_content)
        return prompt
    
    def read_prompt(self) -> str | None:
        prompt = FileManager.read_file(Paths.prompt)
        return prompt
    
    def save_prompt(self, content:str) -> None:
        FileManager.save_file(content, Paths.prompt)