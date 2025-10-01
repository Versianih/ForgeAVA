# Ajuda! Como eu uso esse sistema?
## Obtenção das chaves de API
1. **Gemini** (Paga c/ limite gratuito): https://aistudio.google.com/api-keys

2. **Groq** (Paga c/ limite gratuito): https://console.groq.com/keys

3. **OpenAI** (Paga): https://platform.openai.com/api-keys

4. **Anthropic** (Paga): ...

## Prompt
> O prompt é inserido junto com o conteúdo da atividade/prompt, como forma de moldar a resposta da IA, fornecendo instruções detalhadas de como a IA deve se comportar. 
### TAGS no Prompt
- No prompt, existem TAGS que podem ser inseridas para passar informações diretamente a IA através do prompt, essas TAGS são:
```bash
{language}           # Linguagem de programação escolhida nas configurações
{date_now}           # Data atual no formato dd/mm/aaaa
{activity_content}   # Conteúdo da atividade/prompt
```
## Utilizando o sistema
### Gerando código por uma atividade do AVA
- Basta copiar a URL da atividade, ou o número após o parâmetro `?id=` e colar no campo especificado, no outro campo deve ser inserido o nome no qual o arquivo gerado deverá ser salvo, inclua a extensão do arquivo, Ex: `xxxxx.py`

### Gerando código por um prompt próprio
- Essa funcionalidade funciona como qualquer outro chat LLM, onde você especifica o código no prompt e o sistema já chama a IA e salva seu arquivo automaticamente.

## Debug
Caso você esteja testando funções e modificando o código, o sistema conta com um sistema de debug, que é ativado substituindo a váriavel debug no .env por:
```python
DEBUG='True'
```