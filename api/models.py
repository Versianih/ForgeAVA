from modules.env_manager import EnvManager

class Models:
    models = {
        'gemini-1.5-pro': {
            'model': 'gemini-1.5-pro',
            'provider': 'google'
        },
        'llama-3.1-8b-instant': {
            'model': 'llama-3.1-8b-instant',
            'provider': 'groq'
        },
        'llama-3.3-70b-versatile': {
            'model': 'llama-3.3-70b-versatile',
            'provider': 'groq'
        },
        'openai/gpt-oss-120b': {
            'model': 'openai/gpt-oss-120b',
            'provider': 'groq'
        },
        'openai/gpt-oss-20b': {
            'model': 'openai/gpt-oss-20b',
            'provider': 'groq'
        },
        'whisper-large-v3': {
            'model': 'whisper-large-v3',
            'provider': 'groq'
        },
        'whisper-large-v3-turbo': {
            'model': 'whisper-large-v3-turbo',
            'provider': 'groq'
        },
    }

    @staticmethod
    def get_model() -> str | None:
        model_data = Models.models.get(EnvManager.get_env('MODEL'), None)
        return model_data['model']
    
    @staticmethod
    def get_provider() -> str | None:
        model_data = Models.models.get(EnvManager.get_env('MODEL'), None)
        return model_data['provider']
    
    @staticmethod
    def get_models_list() -> list:
        return [key for key in Models.models.keys()]