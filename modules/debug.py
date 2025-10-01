from time import time
from modules.env_manager import EnvManager

class Debug:
    def __init__(self):
        self.start_time = time()
        self.debug = self.in_debug()

    def log(self, message):
        if self.debug:
            elapsed_time = time() - self.start_time
            print(f"\033[1;93m[{elapsed_time:.2f}s]\033[0m {message}")

    @staticmethod
    def in_debug() -> bool:
        return EnvManager.get_env('DEBUG') == 'True'