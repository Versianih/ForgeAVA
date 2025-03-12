# ForgeAVA
> Solução que utiliza LLMs para geração de código referentes a atividades de programação do Ambiente Virtual de Aprendizagem (AVA), integrando-se diretamente à plataforma.
## Pré-requisitos
### Windows:
- Versão atualizada da linguagem [Python](https://www.python.org/downloads/).
### Linux:
- Versão atualizada da linguagem Python
- Pacotes de desenvolvimento do Tkinter:

```
sudo apt-get install python3-tk  # Ubuntu/Debian  
sudo dnf install python3-tkinter  # Fedora
sudo pacman -S tk  # Arch Linux
```

## Instalando dependências do ForgeAVA
Para instalar as dependências, na pasta do ForgeAVA, siga estas etapas:
Linux e macOS:

```
python3 -m venv venv
source venv/bin/activate #Criando e ativando uma virtualenv
pip install -r requirements.txt
```

Windows:

```
python -m venv venv
venv/scripts/activate #Criando e ativando uma virtualenv
pip install -r requirements.txt
```

## Executando o ForgeAVA
Com a venv ainda ativada execute o comando:

```
python main.py
```

Se tudo ocorreu bem, uma nova janela abrirá e você poderá usar o ForgeAVA.