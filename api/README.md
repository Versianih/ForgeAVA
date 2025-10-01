# API
## Esse módulo é responsável pela chamada da API de um modelo de linguagem externo, processar dados referentes aos modelos e resposta da API

O módulo conta com o arquivo central `call_api.py`, que contém toda a lógica de processamento da chamada da API externa utilizando de bibliotecas fornecidas pelos provedores das APIs

## Modelos implementados
### Google

| Modelo                | Nome | Provedor |
|-----------------------|------|----------|
| gemini-2.5-pro        |  -   | google   |
| gemini-2.5-flash      |  -   | google   |
| gemini-2.5-flash-lite |  -   | google   |
| gemini-2.0-flash      |  -   | google   |
| gemini-2.0-flash-lite |  -   | google   |

### Groq

| Modelo                  | Nome | Provedor |
|-------------------------|------|----------|
| llama-3.1-8b-instant    |  -   | groq     |
| llama-3.3-70b-versatile |  -   | groq     |
| openai/gpt-oss-120b     |  -   | groq     |
| openai/gpt-oss-20b      |  -   | groq     |
| whisper-large-v3        |  -   | groq     |
| whisper-large-v3-turbo  |  -   | groq     |

### OpenAI

| Modelo                | Nome        | Provedor |
|-----------------------|-------------|----------|
| gpt-5-2025-08-07      | GPT-5       | openai   |
| gpt-5-mini-2025-08-07 | GPT-5 Mini  | openai   |
| gpt-5-nano-2025-08-07 | GPT-5 Nano  | openai   |
| gpt-4.1-2025-04-14    | GPT-4.1     | openai   |

### Anthropic

| Modelo                | Nome        | Provedor |
|-----------------------|-------------|----------|
| claude-opus-4-1-20250805 | Claude 4.1 Opus | anthropic   |
| claude-opus-4-20250514 | Claude 4 Opus  | anthropic   |
| claude-sonnet-4-20250514 | Claude 4 Sonnet | anthropic   |
| claude-3-7-sonnet-latest | Claude 3.7 Sonnet | anthropic   |
| claude-3-5-haiku-latest | Claude 3.5 Haiku | anthropic   |
| claude-3-haiku-20240307 | Claude 3 Haiku | anthropic   |

## Estrutura de arquivos
```
api/
├── call_api.py          # Chamada da API e seleção de provedor
├── models.py            # Modelos de Linguagem
├── process_response.py  # Pós processamento da resposta da API
├── prompt.md            # Prompt enviado para a API junto ao prompt da atividade
└── README.md            # Este Arquivo
```