# ForgeAVA

> Solução que utiliza LLMs para geração de código referentes a atividades de programação do Ambiente Virtual de Aprendizagem (AVA), integrando-se diretamente à plataforma.

---

## Índice

- [Pré-requisitos](#pré-requisitos)
- [Instalação Manual](#instalação-manual)
- [Instalação via Makefile](#instalação-via-makefile)
- [Executando o ForgeAVA](#executando-o-forgeava)
- [Funcionamento do Sistema](#funcionamento-do-sistema)
- [Atalhos e Dicas de Uso](#atalhos-e-dicas-de-uso)
- [Configuração e .env](#configuração-e-env)
- [Modelos Suportados](#modelos-suportados)
- [Licença](#licença)
- [Contribua](#contribua)
- [Dúvidas](#dúvidas)

---

## Pré-requisitos

### Windows
- [Python](https://www.python.org/downloads/) (recomendado Python 3.10+)

### Linux
- Python 3.10+
  ```shell
  sudo apt-get install python3 python3-venv python3-pip  # Ubuntu/Debian
  sudo dnf install python3 python3-venv python3-pip     # Fedora
  sudo pacman -S python python-virtualenv python-pip     # Arch Linux
  ```

---

## Instalação Manual

### 1. Clone o repositório
```sh
git clone https://github.com/versianih/forgeava
cd forgeava
```

### 2. Crie e ative o ambiente virtual

#### Linux/macOS
```sh
python3 -m venv .venv
source .venv/bin/activate
```

#### Windows
```sh
python -m venv .venv
.venv\Scripts\activate
```

### 3. Instale as dependências
```sh
pip install --upgrade pip
pip install uv
uv pip install -r requirements.txt
```

---

## Instalação via Makefile

O projeto inclui um Makefile para facilitar a instalação e execução.

Para instalar o Make, siga as instruções abaixo:
- **Linux:** Geralmente já vem instalado. Caso contrário, use o gerenciador de pacotes da sua distribuição.
- **Windows:** Instale o [Git Bash](https://git-scm.com/downloads) ou [WSL](https://learn.microsoft.com/en-us/windows/wsl/install) para obter suporte ao Make.
- **MacOS:** Instale o [Homebrew](https://brew.sh/) e depois execute `brew install make`.

Com o Make instalado, use o comando abaixo para instalar e preparar o ambiente automaticamente:

```shell
make setup
```

Após isso, o sistema estará pronto para uso.

### Comandos disponíveis no Makefile:
```shell
make venv        # Cria o ambiente virtual
make install     # Instala as dependências
make setup       # Instala as dependências e configura o ambiente
make run         # Executa o ForgeAVA
make clean       # Remove o ambiente virtual
```

---

## Executando o ForgeAVA

Com o ambiente virtual ativo, execute:
```shell
python main.py
```
Ou, se estiver usando o Makefile:
```shell
make run
```

---

## Funcionamento do Sistema

- **Interface Gráfica:** Utiliza PySide6 (Qt) para uma experiência moderna e responsiva.
- **Geração de Código:** Integra com APIs de LLMs (Gemini, Groq, OpenAI, Anthropic) para gerar códigos a partir de atividades do AVA.
- **Automação AVA:** Usa Selenium para acessar e extrair atividades do AVA automaticamente.
- **Gestão de Arquivos:** Os códigos gerados são salvos na pasta de output configurada.
- **Configurações:** Todas as configurações (login, senha, modelo, pasta de saída, etc.) são salvas no arquivo `.env` e podem ser alteradas na interface.

---

## Configuração e .env

O arquivo `.env` armazena todas as configurações do sistema.  
Exemplo de variáveis:
```
[EXEMPLO de .env]
API_KEY=suachave
MODEL=gpt-4o
LOGIN=seulogin
PASSWORD=suasenha
LANGUAGE=Python
OUTPUT_PATH=/caminho/para/output
USE_PROMPT=Sim
DEBUG=False
```
Você pode editar essas configurações pela interface ou manualmente.

---

## Modelos Suportados

- **Gemini**
- **Groq**
- **OpenAI**
- **Anthropic**

<small><small>Consulte a documentação de cada provedor para detalhes sobre chaves de API e limites de uso.</small></small>
---

## Licença

Esse código está sob a **GNU Affero General Public License v3.0 (AGPL-3.0)**, Veja mais em [LICENSE](LICENSE).

---

## Contribua

Bifurque o repositório, faça suas alterações e crie uma [pull request](https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/creating-a-pull-request).

---

## Dúvidas

Dúvidas e sugestões: versiani.ifes@gmail.com

---

## Observações

Este projeto faz parte do meu portfólio pessoal e é desenvolvido unicamente para fins de estudos e aprendizado.

---