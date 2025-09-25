from time import time
from modules.env_manager import EnvManager

class Debug:
    def __init__(self):
        self.start_time = time()
        self.in_debug = EnvManager.get_env('DEBUG') == 'True'

    def log(self, message):
        if self.in_debug:
            elapsed_time = time() - self.start_time
            print(f"\033[1;93m[{elapsed_time:.2f}s]\033[0m {message}")