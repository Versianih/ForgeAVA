from modules.env_manager import EnvManager

class Models:
    models = {
        'gemini-1.5-pro': {
            'model': 'gemini-1.5-pro',
            'provider': 'google'
        },
        'llama3-70b-8192': {
            'model': 'llama3-70b-8192',
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