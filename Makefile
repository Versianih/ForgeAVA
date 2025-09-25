PYTHON := $(shell command -v python3 2>/dev/null || command -v python)

VENV_DIR := .venv

ifeq ($(OS),Windows_NT)
	VENV_PYTHON := $(VENV_DIR)/Scripts/python.exe
	VENV_PIP := $(VENV_DIR)/Scripts/pip.exe
	VENV_UV := $(VENV_DIR)/Scripts/uv.exe
	RM = rmdir /S /Q
else
	VENV_PYTHON := $(VENV_DIR)/bin/python3
	VENV_PIP := $(VENV_DIR)/bin/pip3
	VENV_UV := $(VENV_DIR)/bin/uv
	RM = rm -rf
endif

help:
	@echo "Comandos disponíveis:"
	@echo "  make venv     - Cria o ambiente virtual"
	@echo "  make install  - Instala as dependências"
	@echo "  make setup    - Instala e configura o projeto"
	@echo "  make run      - Executa o projeto"
	@echo "  make clean    - Remove o ambiente virtual"

venv:
	$(PYTHON) -m venv $(VENV_DIR)

install: venv
	$(VENV_PIP) install --upgrade pip
	$(VENV_PIP) install uv
	$(VENV_UV) pip install -r requirements.txt

setup: install
	$(VENV_PYTHON) main.py -s

run:
	$(VENV_PYTHON) main.py

clean:
	$(RM) $(VENV_DIR)