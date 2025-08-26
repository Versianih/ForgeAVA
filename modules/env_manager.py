from os import getenv, path
from dotenv import load_dotenv, set_key
from paths import Paths

class EnvManager:
    default_env = {
        'API_KEY': '',
        'MODEL': '',
        'LOGIN': '',
        'PASSWORD': '',
        'OUTPUT_PATH': '',
        'USE_PROMPT': 'True'
    }

    @staticmethod
    def get_env(key: str) -> str | None:
        load_dotenv(Paths.env)
        return getenv(key)

    @staticmethod
    def update_env(key: str, value: str) -> None:
        set_key(Paths.env, key, str(value))

    @staticmethod
    def create_env_or_pass() -> None:
        if not path.isfile(Paths.env):
            for key, value in EnvManager.default_env.items():
                set_key(Paths.env, key, str(value))
            return

        load_dotenv(Paths.env)

        missing_keys = []
        for key in EnvManager.default_env:
            if getenv(key) is None:
                missing_keys.append(key)

        if missing_keys:
            for key, value in EnvManager.default_env.items():
                current_value = getenv(key)
                if current_value is None:
                    set_key(Paths.env, key, str(value))