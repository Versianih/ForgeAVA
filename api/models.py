from modules.env_manager import EnvManager

class Models:
    models = {
        # Google models
        # https://ai.google.dev/gemini-api/docs/models?hl=pt-br
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
        # https://console.groq.com/docs/models
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

        # OpenAI models
        # https://platform.openai.com/api-keys
        'gpt-5-2025-08-07': {
            'name': 'GPT-5',
            'provider': 'openai'
        },
        'gpt-5-mini-2025-08-07': {
            'name': 'GPT-5 Mini',
            'provider': 'openai'
        },
        'gpt-5-nano-2025-08-07': {
            'name': 'GPT-5 Nano',
            'provider': 'openai'
        },
        'gpt-4.1-2025-04-14': {
            'name': 'GPT-4.1',
            'provider': 'openai'
        },

        # Anthropic models
        # https://docs.claude.com/pt/docs/about-claude/models/overview
        'claude-opus-4-1-20250805': {
            'name': 'Claude 4.1 Opus',
            'provider': 'anthropic',
        },
        'claude-opus-4-20250514': {
            'name': 'Claude 4 Opus',
            'provider': 'anthropic'
        },
        'claude-sonnet-4-20250514': {
            'name': 'Claude 4 Sonnet',
            'provider': 'anthropic'
        },
        'claude-3-7-sonnet-latest': {
            'name': 'Claude 3.7 Sonnet',
            'provider': 'anthropic'
        },
        'claude-3-5-haiku-latest': {
            'name': 'Claude 3.5 Haiku',
            'provider': 'anthropic'
        },
        'claude-3-haiku-20240307': {
            'name': 'Claude 3 Haiku',
            'provider': 'anthropic'
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
            f"{data['provider'].upper()}: {data.get('name', key)}"
            for key, data in Models.models.items()
        ] if Models.models else []