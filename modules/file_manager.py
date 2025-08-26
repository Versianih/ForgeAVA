from os import makedirs
from pathlib import Path
from paths import Paths

class FileManager:
    @staticmethod
    def create_output_or_pass() -> None:
        makedirs(Paths.output, exist_ok=True)

    @staticmethod
    def save_file(content: str, file_path: Path) -> None:
        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(content)
        except PermissionError:
            raise RuntimeError(f"Sem permissão para salvar o arquivo: {file_path}")
        except OSError as e:
            raise RuntimeError(f"Erro de sistema ao salvar o arquivo {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido ao salvar o arquivo: {e}")
    
    @staticmethod
    def read_file(file_path: Path) -> str | None:
        try: 
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
            return content
        except PermissionError:
            raise RuntimeError(f"Sem permissão para ler o arquivo: {file_path}")
        except OSError as e:
            raise RuntimeError(f"Erro de sistema ao ler o arquivo {file_path}: {e}")
        except Exception as e:
            raise RuntimeError(f"Erro desconhecido ao ler o arquivo: {e}")