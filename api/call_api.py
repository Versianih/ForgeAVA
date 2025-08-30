from api.models import Models
from api.process_response import ProcessResponse
from modules.env_manager import EnvManager

class CallLLM(Models):
    def __init__(self):
        self.model = self.get_model()
        self.provider = self.get_provider()
        self.api_key = EnvManager.get_env('API_KEY')

        if not self.api_key:
            raise ValueError("API_KEY não encontrada no .env")

        self._validate_provider()

    def _validate_provider(self):
        if self.provider not in ('google', 'groq'):
            raise ValueError(f"Provedor não suportado: {self.provider}")

    def _get_api_method(self):
        if self.provider == 'google':
            return self._call_gemini
        if self.provider == 'groq':
            return self._call_groq
        return

    def call(self, prompt: str) -> str:
        method = self._get_api_method()

        try:
            raw_response = method(prompt)
            response = ProcessResponse.clean_response(raw_response)
            return response
        except Exception as e:
            raise RuntimeError(f"Erro ao chamar o modelo {self.model} via {self.provider}: {str(e)}") from e

    def _call_gemini(self, prompt: str) -> str:
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model)
        response = model.generate_content(prompt)
        return response.text

    def _call_groq(self, prompt: str) -> str:
        from groq import Groq
        client = Groq(api_key=self.api_key)
        response = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model,
        )
        return response.choices[0].message.content