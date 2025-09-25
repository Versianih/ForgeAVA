from os import path, getenv
from dotenv import load_dotenv, set_key
from paths import Paths

class EnvManager:
    default_env = {
        'API_KEY': '',
        'MODEL': '',
        'LOGIN': '',
        'PASSWORD': '',
        'LANGUAGE': 'Python',
        'OUTPUT_PATH': f'{Paths.output.absolute()}',
        'USE_PROMPT': 'Sim',
        'DEBUG': 'False'
    }

    @staticmethod
    def get_env(key: str, default: str | None = None) -> str | None:
        load_dotenv(Paths.env, override=True)
        return getenv(key, default)

    @staticmethod
    def update_env(dict_values:dict) -> None:
        for key, value in dict_values.items():
            set_key(Paths.env, key, str(value))
        load_dotenv(Paths.env, override=True)

    @staticmethod
    def create_env_or_pass() -> None:
        if not path.isfile(Paths.env):
            for key, value in EnvManager.default_env.items():
                set_key(Paths.env, key, str(value))
            return

        missing_keys = []
        for key in EnvManager.default_env:
            if getenv(key, None) is None:
                missing_keys.append(key)

        if missing_keys:
            for key, value in EnvManager.default_env.items():
                current_value = getenv(key, None)
                if current_value is None:
                    set_key(Paths.env, key, str(value))
        
        load_dotenv(Paths.env, override=True)