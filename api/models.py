from modules.env_manager import EnvManager

class Models:
    models = {
        # Google models
        'gemini-2.5-pro': {
            'provider': 'google'
        },
        'gemini-2.5-flash': {
            'provider': 'google'
        },
        'gemini-2.5-flash-lite': {
            'provider': 'google'
        },
        'gemini-2.0-flash': {
            'provider': 'google'
        },
        'gemini-2.0-flash-lite': {
            'provider': 'google'
        },

        # Groq models
        'llama-3.1-8b-instant': {
            'provider': 'groq'
        },
        'llama-3.3-70b-versatile': {
            'provider': 'groq'
        },
        'openai/gpt-oss-120b': {
            'provider': 'groq'
        },
        'openai/gpt-oss-20b': {
            'provider': 'groq'
        },
        'whisper-large-v3': {
            'provider': 'groq'
        },
        'whisper-large-v3-turbo': {
            'provider': 'groq'
        },
    }

    @staticmethod
    def get_model() -> str | None:
        model = EnvManager.get_env('MODEL')
        return model if model in Models.models else None
    
    @staticmethod
    def get_provider() -> str | None:
        model_data:dict = Models.models.get(EnvManager.get_env('MODEL'), None)
        return model_data['provider'] if model_data else None
    
    @staticmethod
    def get_models_list() -> list:
        return [key for key in Models.models.keys()] if Models.models else []
    
    @staticmethod
    def get_models_list_with_provider() -> list:
        return [
            f"{data['provider'].upper()}: {key}"
            for key, data in Models.models.items()
        ] if Models.models else []