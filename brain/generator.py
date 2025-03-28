# Python libs
import os

# Libs
import google.generativeai as genai



def clean_call_gemini(response):
    lines = response.splitlines()
    if lines and lines[0] in ['```python', '```python 3.xxx', '```python3']:
        lines = lines[1:]    
    if lines and lines[-1] == '```':
        lines = lines[:-1]
    return "\n".join(lines)


def call_gemini(prompt, api_key):
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-pro')
    try:
        response = model.generate_content(prompt)
        clean_response = clean_call_gemini(response.text)
        return clean_response
    except Exception as e:
        return (f"Erro ao conectar à API Gemini: {e}")


def save_file(file_name, content, folder):
    file_path = os.path.join(folder, file_name)
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        print("Arquivo salvo com sucesso!")
    except Exception as e:
        print(f"Erro ao salvar o arquivo: {e}")


def read_prompt(file_name):
    current_dir = os.getcwd()
    file_path = os.path.join(current_dir, "brain", "files", file_name)

    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Arquivo '{file_name}' não encontrado na pasta 'files'.")

    common_encodings = ["utf-8", "latin-1", "cp1252"]
    for encoding in common_encodings:
        try:
            with open(file_path, "r", encoding=encoding) as file:
                return file.read()
        except UnicodeDecodeError:
            continue

    try:
        with open(file_path, "rb") as file:
            raw_data = file.read()

        for encoding in ["utf-16", "utf-32"]:
            try:
                return raw_data.decode(encoding)
            except UnicodeDecodeError:
                continue
    except Exception as e:
        raise Exception(f"Erro ao processar o arquivo '{file_name}': {e}")

    raise UnicodeDecodeError("Falha ao ler o arquivo do Prompt com as codificações testadas.")