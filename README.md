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

### Linux e macOS:
```
python3 -m venv venv
source venv/bin/activate # Criando e ativando uma virtualenv
pip install -r requirements.txt
```

### Windows:
```
python -m venv venv
venv/scripts/activate #Criando e ativando uma virtualenv
pip install -r requirements.txt
```

## Executando o ForgeAVA
Com a venv ainda ativa execute o comando:

```
python main.py
```

Se tudo ocorreu bem, uma nova janela abrirá e você poderá usar o ForgeAVA.

## Sobre o ForgeAVA
O projeto usa atualmente a API do Gemini para a geração de códigos, podendo ser expandido futuramente para outras LLMs com melhor performance. As atividades do AVA são acessadas automaticamente utilizando a biblioteca Selenium, e a interface gráfica é feita com a biblioteca nativa Tkinter. Não nos responsabilizamos por usos indevidos da ferramenta, use por sua conta e risco.

## Contribua com o ForgeAVA
#### Para contribuir com o projeto, bifurque o repositório, faça suas alterações e crie uma [solicitação de pull](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).
#### Você é livre para utilizar e modificar este código.

## Licença
Esse código está sob licença, saiba mais em [LICENÇA](LICENSE)

## Dúvidas
Dúvidas e sugestões para o projeto, entre em contato por e-mail com: mevrse@protonmail.com