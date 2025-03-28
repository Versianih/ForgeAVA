# Python libs
import os
import subprocess
import threading
import webbrowser
import re
import tkinter as tk
from tkinter import filedialog, messagebox

# Modules
from brain.generator import call_gemini, save_file, read_prompt
from brain.ava import get_ava_text, send_file_to_ava, get_id

# Libs
from dotenv import load_dotenv, set_key


class ForgeAVA:
    # Interface settings 
    def __init__(self, root):
        self.root = root
        self.root.title("ForgeAVA")
        self.root.geometry("1000x600")
        
        # VRSE icon
        vrse_path = os.path.join(".", "media", "VRSE.png")
        try:
            icon_image = tk.PhotoImage(file=vrse_path)
            self.root.iconphoto(True, icon_image)
        except Exception as e:
            print(f"Erro ao carregar ícone: {e}")


        # .env settings
        self.env_file = ".env"
        load_dotenv(self.env_file)

        if not os.path.exists(f"{os.getcwd()}/generatedCodes"):
            os.mkdir(f"{os.getcwd()}/generatedCodes")

        self.API_KEY = os.getenv("API_KEY", "")
        self.LOGIN = os.getenv("LOGIN", "")
        self.SENHA = os.getenv("SENHA", "")
        self.PASTA_SAIDA = os.getenv("PASTA_SAIDA", f"{os.getcwd()}/generatedCodes")
        self.GET_PROMPT = os.getenv("GET_PROMPT", "False") == "True"
        try:
            self.prompt = read_prompt("prompt.txt")
        except UnicodeDecodeError as e:
            print(f"Erro ao ler o prompt: {e}")
            return
        
        # Home screen
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(side="right", fill="both", expand=True)


        # Sidebar
        self.side_frame = tk.Frame(self.root, width=200, bg="lightgray")
        self.side_frame.pack(side="left", fill="y")


        # Sidebar buttons
        self.generate_code_button = tk.Button(self.side_frame, text="Gerar Código de Atividade AVA", command=self.show_generate_ava_code)
        self.generate_code_button.pack(fill="x")

        self.generate_code_button_with_text = tk.Button(self.side_frame, text="Gerar Código com Texto", command=self.show_generate_text_code)
        self.generate_code_button_with_text.pack(fill="x")

        self.files_button = tk.Button(self.side_frame, text="Arquivos Gerados", command=self.show_generated_files)
        self.files_button.pack(fill="x")

        self.settings_button = tk.Button(self.side_frame, text="Configurações", command=self.show_settings)
        self.settings_button.pack(fill="x")

        self.help_button = tk.Button(self.side_frame, text="Ajuda", command=self.show_help)
        self.help_button.pack(fill="x")

        self.exit_button = tk.Button(self.side_frame, text="Sair", bg="red3", command=self.root.quit)
        self.exit_button.pack(fill="x", side="bottom")

        self.forgeava = tk.Label(self.side_frame, text="ForgeAVA - VRSE", bg="lightgray").pack(fill="x", side="bottom")



    # Interface functions
    def clean_screen(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()


    def create_field(self, parent, text, entry_text="", password=False, entry_camp=False):
        frame = tk.Frame(parent, relief="solid", borderwidth=1, padx=5, pady=5)
        frame.pack(fill="x", pady=5)

        tk.Label(frame, text=text).pack(side="top", anchor="w", pady=2)

        var = tk.StringVar(value=entry_text)
        entry = tk.Entry(frame, textvariable=var, show="*" if password else "")
        entry.pack(fill="x", pady=2)

        if password or entry_camp:
            return entry
        else:
            return var



    # First button: Generete ava activity code
    def show_generate_ava_code(self):
        self.clean_screen()

        generate_code_frame = tk.LabelFrame(self.main_frame, text="Gerar Código de Atividade AVA", padx=10, pady=10)
        generate_code_frame.pack(fill="both", padx=20, pady=20)

        self.ava_option_selected = tk.StringVar()
        self.file_option_selected = tk.StringVar()

        ava_options_frame = tk.Frame(generate_code_frame, relief="solid", borderwidth=1, padx=5, pady=5)
        ava_options_frame.pack(fill="x", pady=5)

        tk.Label(ava_options_frame, text="Identificação da Atividade AVA:", fg="black").pack(pady=5, side="left")
        tk.Checkbutton(ava_options_frame, text="ID", variable=self.ava_option_selected, onvalue="id", offvalue="").pack(side="left", padx=5)
        tk.Checkbutton(ava_options_frame, text="URL", variable=self.ava_option_selected, onvalue="url", offvalue="").pack(side="left", padx=5)

        file_options_frame = tk.Frame(generate_code_frame, relief="solid", borderwidth=1, padx=5, pady=5)
        file_options_frame.pack(fill="x", pady=5)

        tk.Label(file_options_frame, text="Enviar arquivo para o AVA após gerar?", fg="black").pack(pady=5, side="left")
        tk.Checkbutton(file_options_frame, text="Sim, enviar o arquivo", variable=self.file_option_selected, onvalue="enviar", offvalue="").pack(side="left", padx=5)
        tk.Checkbutton(file_options_frame, text="Não, apenas salvar", variable=self.file_option_selected, onvalue="salvar", offvalue="").pack(side="left", padx=5)

        self.id_or_url_activity = self.create_field(generate_code_frame, "ID ou URL da Atividade AVA")
        self.file = self.create_field(generate_code_frame, "Nome do Arquivo a ser salvo")

        # Messages
        self.ava_success_message = tk.Label(generate_code_frame, text="", fg="green")
        self.ava_success_message.pack(pady=5, side="left")

        self.ava_error_message = tk.Label(generate_code_frame, text="", fg="red")
        self.ava_error_message.pack(pady=5, side="left")

        self.ava_loading_message = tk.Label(generate_code_frame, text="", fg="black")
        self.ava_loading_message.pack(pady=5, side="left")

        # Button "generate code"
        self.code_button = tk.Button(generate_code_frame, text="Gerar Código", command=self.button_ava_code, bg="grey", fg="black", state="disabled")
        self.code_button.pack(pady=10, side="right")

        if not self.API_KEY or not self.LOGIN or not self.SENHA or not os.path.isdir(self.PASTA_SAIDA):
            error_frame = tk.LabelFrame(self.main_frame, text="Erro", padx=10, pady=10)
            error_frame.pack(fill="both", padx=20, pady=20)
            error_msg = tk.Label(error_frame, text="Configurações não encontradas:", fg="red")
            error_msg.pack(padx=20, pady=5)
            if not self.API_KEY:
                error_msg = tk.Label(error_frame, text="Chave API Gemini.", fg="red")
                error_msg.pack(padx=20, pady=5)
            if not self.LOGIN:
                error_msg = tk.Label(error_frame, text="Login AVA.", fg="red")
                error_msg.pack(padx=20, pady=5)
            if not self.SENHA:
                error_msg = tk.Label(error_frame, text="Senha AVA.", fg="red")
                error_msg.pack(padx=20, pady=5)
            if not os.path.isdir(self.PASTA_SAIDA):
                error_msg = tk.Label(error_frame, text="Pasta de Saída.", fg="red")
                error_msg.pack(padx=20, pady=5)
            error_msg = tk.Label(error_frame, text="ATUALIZE AS CONFIGURAÇÕES", fg="red")
            error_msg.pack(padx=20, pady=5)
            return
        
        # Checking the completion of fields
        def check_fields():
            all_filled = (
                self.ava_option_selected.get() and
                self.file_option_selected.get() and
                self.id_or_url_activity.get().strip() and
                self.file.get().strip() and
                self.API_KEY and
                self.LOGIN and
                self.SENHA and
                os.path.isdir(self.PASTA_SAIDA)
            )
            self.code_button.config(
                state="normal" if all_filled else "disabled",
                bg="green" if all_filled else "grey",
                fg="white" if all_filled else "black"
            )

        # Traces to monitor changes
        self.ava_option_selected.trace("w", lambda *args: check_fields())
        self.file_option_selected.trace("w", lambda *args: check_fields())
        self.id_or_url_activity.trace_add("write", lambda *args: check_fields())
        self.file.trace_add("write", lambda *args: check_fields())


    def button_ava_code(self):
        self.ava_loading_message.config(text="Acessando Atividade...")
        threading.Thread(target=self.generate_ava_code).start()

    def generate_ava_code(self):
        if self.ava_option_selected.get() == "url":
            # Get the id attribute if it is a url
            self.id_url_activity = get_id(url=self.id_or_url_activity.get())
            if self.id_url_activity == "error":
                self.ava_loading_message.config(text="")
                print("ERRO ao obter o atributo 'ID' da URL")
                messagebox.showinfo("Gerador AVA", "ERRO ao obter atributo 'ID' da URL")
                self.root.after(3, self.show_generate_ava_code)

            self.activity_text = get_ava_text(login=self.LOGIN, password=self.SENHA, id=self.id_url_activity)
            if self.activity_text == "error":
                self.ava_loading_message.config(text="")
                print("ERRO ao acessar atividade AVA")
                messagebox.showinfo("Gerador AVA", "ERRO ao acessar atividade AVA")
                self.root.after(5, self.show_generate_ava_code)

        elif self.ava_option_selected.get() == "id":
            self.activity_text = get_ava_text(login=self.LOGIN, password=self.SENHA, id=self.id_or_url_activity.get())
            if self.activity_text == "error":
                self.ava_loading_message.config(text="")
                print("ERRO ao acessar atividade AVA")
                messagebox.showinfo("Gerador AVA", "ERRO ao acessar atividade AVA")
                self.root.after(2, self.show_generate_ava_code)

        # Try to get response from Gemini
        self.ava_loading_message.config(text="Gerando Código...")
        prompt = str(self.prompt if self.GET_PROMPT == True else "") + f'\n{self.activity_text}'
        try:
            response = call_gemini(prompt, self.API_KEY)
        except Exception as e :
            self.ava_loading_message.config(text="")
            print(f"ERRO ao obter resposta do Gemini: {e}")
            messagebox.showinfo("Gerador AVA", "ERRO ao obter a resposta do Gemini")
            self.root.after(2, self.show_generate_ava_code)

        self.ava_loading_message.config(text="Salvando Arquivo...")
        try:
            save_file(self.file.get(), response, self.PASTA_SAIDA)
            self.ava_loading_message.config(text="")
            messagebox.showinfo("Gerador AVA", f"Arquivo salvo com sucesso em: {self.PASTA_SAIDA}/{self.file.get()}")
        except Exception as e:
            self.ava_loading_message.config(text="")
            print(f"ERRO ao salvar o arquivo: {e}")
            messagebox.showinfo("Gerador AVA", "ERRO ao salvar arquivo")
            self.ava_error_message.config(text="")
            self.root.after(2, self.show_generate_ava_code)

        # Send file to AVA if requested
        if self.file_option_selected.get() == "enviar":
            self.ava_loading_message.config(text="Enviando Arquivo Para o AVA...")
            if send_file_to_ava(login=self.LOGIN, password=self.SENHA, id=self.id_url_activity if self.ava_option_selected.get() == 'url' else self.id_or_url_activity.get(), file_path=self.PASTA_SAIDA, file=self.file.get()) == "error":
                self.ava_loading_message.config(text="")
                print("ERRO ao enviar arquivo para o AVA")
                messagebox.showinfo("Gerador AVA", "ERRO ao enviar arquivo para o AVA")
                self.root.after(5, self.show_generate_ava_code)


            self.ava_loading_message.config(text="")
            self.ava_success_message.config(text="Código salvo e enviado pro AVA com sucesso!")

        self.root.after(1200, self.show_generate_ava_code)



    # Second Button: Generate code with text
    def show_generate_text_code(self):
        self.clean_screen()

        generate_text_code_frame = tk.LabelFrame(self.main_frame, text="Gerar Código com Texto", padx=10, pady=10)
        generate_text_code_frame.pack(fill="both", padx=20, pady=20)

        self.text = self.create_field(generate_text_code_frame, "Texto para geração de código")
        self.file = self.create_field(generate_text_code_frame, "Nome do Arquivo a ser salvo")

        # Mesages
        self.success_message_text = tk.Label(generate_text_code_frame, text="", fg="green")
        self.success_message_text.pack(pady=5, side="left")

        self.error_message_text = tk.Label(generate_text_code_frame, text="", fg="red")
        self.error_message_text.pack(pady=5, side="left")

        self.message_loading_text = tk.Label(generate_text_code_frame, text="", fg="black")
        self.message_loading_text.pack(pady=5, side="left")

        # Button "Generate code"
        self.code_button = tk.Button(generate_text_code_frame, text="Gerar Código", command=self.text_code_button, bg="grey", fg="black", state="disabled")
        self.code_button.pack(pady=10, side="right")

        if not self.API_KEY or not os.path.isdir(self.PASTA_SAIDA):
            error_frame = tk.LabelFrame(self.main_frame, text="Erro", padx=10, pady=10)
            error_frame.pack(fill="both", padx=20, pady=20)
            error_msg = tk.Label(error_frame, text="Configurações não encontradas:", fg="red")
            error_msg.pack(padx=20, pady=5)
            if not self.API_KEY:
                error_msg = tk.Label(error_frame, text="Chave API Gemini.", fg="red")
                error_msg.pack(padx=20, pady=5)
            if not os.path.isdir(self.PASTA_SAIDA):
                error_msg = tk.Label(error_frame, text="Pasta de Saída.", fg="red")
                error_msg.pack(padx=20, pady=5)
            error_msg = tk.Label(error_frame, text="ATUALIZE AS CONFIGURAÇÕES", fg="red")
            error_msg.pack(padx=20, pady=5)
            return

        # Checking the completion of fields
        def check_fields():
            all_filled = (
                self.text.get().strip() and
                self.file.get().strip() and
                self.API_KEY and
                self.PASTA_SAIDA
            )
            self.code_button.config(
                state="normal" if all_filled else "disabled",
                bg="green" if all_filled else "grey",
                fg="white" if all_filled else "black"
            )

        # Traces to monitor changes
        self.text.trace_add("write", lambda *args: check_fields())
        self.file.trace_add("write", lambda *args: check_fields())

    def text_code_button(self):
        self.message_loading_text.config(text="Gerando Código...")
        threading.Thread(target=self.generate_text_code).start()

    def generate_text_code(self):
        prompt = str(self.prompt if self.GET_PROMPT == True else "") + f'\n{self.text.get()}'
        # Try to get the answer from Gemini
        try:
            resposta = call_gemini(prompt=prompt, api_key=self.API_KEY)
            self.message_loading_text.config(text="Salvando Arquivo...")
        except Exception as e:
            self.message_loading_text.config(text="")
            print(f"ERRO ao obter resposta do Gemini: {e}")
            messagebox.showinfo("Gerador AVA", "ERRO ao obter resposta do Gemini")
            self.root.after(2, self.show_generate_text_code)
        
        # Try saving the file 
        try:
            save_file(self.file.get(), resposta, self.PASTA_SAIDA)
            self.message_loading_text.config(text="")
            messagebox.showinfo("Gerador AVA", f"Código salvo com sucesso em: {self.PASTA_SAIDA}/{self.file.get()}")
            self.root.after(2, self.show_generate_text_code)
        except Exception as e:
            self.message_loading_text.config(text="")
            print(f"ERRO ao salvar arquivo: {e}")
            messagebox.showinfo("Gerador AVA", "ERRO ao salvar arquivo")
            self.root.after(2, self.show_generate_text_code)



    # Third Button: Generated files
    def show_generated_files(self):
        self.clean_screen()
        if not os.path.isdir(self.PASTA_SAIDA):
            error_frame = tk.LabelFrame(self.main_frame, text="Erro", padx=10, pady=10)
            error_frame.pack(fill="both", padx=20, pady=20)
            error_msg = tk.Label(error_frame, text="Não foi possível encontrar a pasta de saída.", fg="red")
            error_msg.pack(padx=20, pady=20)
            return

        files_frame = tk.LabelFrame(self.main_frame, text="Arquivos Gerados", padx=10, pady=10)
        files_frame.pack(fill="both", padx=20, pady=20)

        files = [f for f in os.listdir(self.PASTA_SAIDA) if os.path.isfile(os.path.join(self.PASTA_SAIDA, f))]
        
        if not files:
            msg = tk.Label(files_frame, text="Nenhum arquivo encontrado na pasta de saída.", fg="red")
            msg.pack(padx=20, pady=10)
            return

        self.list_files = tk.Listbox(files_frame, selectmode="single", height=10, width=60)
        for file in files:
            self.list_files.insert(tk.END, file)
        self.list_files.pack(padx=20, pady=10)

        tk.Button(files_frame, text="Selecionar Arquivo", command=self.open_file).pack(pady=10)

    def open_file(self):
        self.selected_file = self.list_files.get(tk.ACTIVE)
        if not self.selected_file:
            return
        
        file_path = os.path.join(self.PASTA_SAIDA, self.selected_file)
        self.clean_screen()

        try:
            with open(file_path, "r", encoding="utf-8") as file:
                content = file.read()
            
            editing_frame = tk.LabelFrame(self.main_frame, text=f"Edição do Arquivo: {self.selected_file}", padx=10, pady=10)
            editing_frame.pack(fill="both", padx=20, pady=20)

            self.editing_area = tk.Text(editing_frame, wrap="word", height=20, bg="white", fg="black")
            self.editing_area.pack(fill="both", expand=True, padx=10, pady=10)

            if self.selected_file.endswith(".py"):
                run_code_button = tk.Button(editing_frame, text="Rodar Código Python", command=lambda: self.run_code(file_path))
                run_code_button.place(relx=1.0, rely=0.0, anchor="ne", x=-10, y=10)
            
            content = content.replace("\t", "    ")
            self.editing_area.insert(tk.END, content)

            self.editing_area.bind('<Tab>', self.insert_spaces)

            buttons_frame = tk.Frame(editing_frame)
            buttons_frame.pack(fill="x", pady=10, padx=10, anchor="e")
            
            save_button = tk.Button(buttons_frame, text="Salvar Alterações", command=lambda: self.save_editions(self.selected_file), fg="white", bg="green")
            save_button.pack(side="right", padx=5)
            select_button = tk.Button(buttons_frame, text="Voltar", command=self.show_generated_files)
            select_button.pack(side="right", padx=5)

        except Exception as e:
            print(f"Erro ao tentar abrir o arquivo '{file_path}': {e}")
            messagebox.showerror("Erro", f"Erro ao tentar abrir o arquivo: {file_path}, arquivo não suportado.")
            self.show_generated_files()

    def insert_spaces(self, event):
        pos_cursor = self.editing_area.index(tk.INSERT)
        self.editing_area.insert(pos_cursor, '    ')
        return 'break'

    def save_editions(self, file_name):
        edit_content = self.editing_area.get("1.0", tk.END)
        file_path = os.path.join(self.PASTA_SAIDA, file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(edit_content)

        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")

    def run_code(self, file_path):
        def terminal():
            try:
                if os.name == 'nt':  # Windows
                    command = f'start cmd /K "cd {self.PASTA_SAIDA} && python {self.selected_file} && pause && exit"'
                else: # Linux and MacOS
                    command = f'gnome-terminal -- bash -c "python3 \"{file_path}\"; exec bash"'

                    if subprocess.call(["which", "gnome-terminal"], stdout=subprocess.PIPE, stderr=subprocess.PIPE) != 0:
                        command = f'xterm -hold -e "python3 {file_path}"'

                subprocess.Popen(command, shell=True)
            except Exception as e:
                messagebox.showerror("Erro", f"Erro ao executar o código: {str(e)}")

        threading.Thread(target=terminal).start()



    # Fourth Button: Settings
    def show_settings(self):
        self.clean_screen()

        settings_frame = tk.LabelFrame(self.main_frame, text="Configurações", padx=10, pady=10)
        settings_frame.pack(fill="both", padx=20, pady=20)

        self.api_key_entry = self.create_field(settings_frame, "Chave API Gemini", self.API_KEY)
        self.login_ava_entry = self.create_field(settings_frame, "Login AVA", self.LOGIN)

        password_ava_frame = tk.Frame(settings_frame, relief="solid", borderwidth=1, padx=5, pady=5)
        password_ava_frame.pack(fill="x", pady=5)
        tk.Label(password_ava_frame, text="Senha AVA").pack(side="top", anchor="w", pady=2)
        str_var_password = tk.StringVar(value=str(self.SENHA))
        self.ava_password_entry = tk.Entry(password_ava_frame, textvariable=str_var_password, show="*")
        self.ava_password_entry.pack(fill="x", pady=2)

        self.view_password_button = tk.Button(password_ava_frame, text="Visualizar Senha", command=self.toggle_senha)
        self.view_password_button.pack(pady=5, side="right")

        folder_frame = tk.Frame(settings_frame, relief="solid", borderwidth=1, padx=5, pady=5)
        folder_frame.pack(fill="x", pady=5)
        tk.Label(folder_frame, text="Pasta de Saída:").pack(side="left")
        self.output_folder_label = tk.Label(folder_frame, text=self.PASTA_SAIDA if self.PASTA_SAIDA else "Nenhuma pasta selecionada", fg="green" if self.PASTA_SAIDA else "red")
        self.output_folder_label.pack(side="left")

        tk.Button(folder_frame, text="Selecionar Outra Pasta" if self.PASTA_SAIDA else "Selecionar Pasta", command=self.select_folder).pack(pady=10, side="right")

        self.prompt_option = tk.StringVar(value=str(self.GET_PROMPT))

        frame_check_prompt = tk.Frame(settings_frame, relief="solid", borderwidth=1, padx=5, pady=5)
        frame_check_prompt.pack(fill="x", pady=5)

        tk.Label(frame_check_prompt, text="Usar Prompt:", fg="black").pack(pady=5, side="left")
        tk.Checkbutton(frame_check_prompt, text="", variable=self.prompt_option, onvalue="True", offvalue="False").pack(side="left", padx=5)
        tk.Button(frame_check_prompt, text="Editar Prompt", command=self.open_prompt).pack(pady=10, side="left")

        tk.Button(settings_frame, text="Salvar Configurações", command=self.salvar_configuracoes, bg="green", fg="white").pack(pady=10, side="right")

    def salvar_configuracoes(self):
        # Update values ​​in .env file
        set_key(self.env_file, "API_KEY", self.api_key_entry.get())
        set_key(self.env_file, "LOGIN", self.login_ava_entry.get())
        set_key(self.env_file, "SENHA", self.ava_password_entry.get())
        set_key(self.env_file, "PASTA_SAIDA", self.PASTA_SAIDA)
        set_key(self.env_file, "GET_PROMPT", "True" if self.prompt_option.get() == "True" else "False")

        # Update the values ​​stored in variables
        self.API_KEY = self.api_key_entry.get()
        self.LOGIN = self.login_ava_entry.get()
        self.SENHA = self.ava_password_entry.get()
        self.GET_PROMPT = self.prompt_option.get()

        messagebox.showinfo("Configurações", "As configurações foram salvas com sucesso!")
        self.show_settings()

    def toggle_senha(self):
        # Toggles password display
        if self.ava_password_entry.cget('show') == "*":
            self.ava_password_entry.config(show="")
            self.view_password_button.config(text="Esconder Senha")
        else:
            self.ava_password_entry.config(show="*")
            self.view_password_button.config(text="Visualizar Senha")

    def select_folder(self):
        # Open the folder selector and update the path
        new_folder = filedialog.askdirectory()
        if new_folder:
            self.PASTA_SAIDA = new_folder
            self.output_folder_label.config(text=self.PASTA_SAIDA)

    def open_prompt(self):
        self.prompt_path = os.path.join('brain', 'files', 'prompt.txt')

        self.clean_screen()

        edit_frame = tk.LabelFrame(self.main_frame, text="Edição de prompt.txt", padx=10, pady=10)
        edit_frame.pack(fill="both", padx=20, pady=20)

        self.editing_area = tk.Text(edit_frame, wrap="word", height=20, bg="white", fg="black")
        self.editing_area.pack(fill="both", expand=True, padx=10, pady=10)

        with open(self.prompt_path, "r", encoding="utf-8") as file:
            content = file.read()

        content = content.replace("\t", "    ")
        self.editing_area.insert(tk.END, content)

        self.editing_area.bind('<Tab>', self.insert_prompt_space)

        button_frame = tk.Frame(edit_frame)
        button_frame.pack(fill="x", pady=10, padx=10, anchor="e")
        
        save_button = tk.Button(button_frame, text="Salvar Alterações", command=lambda: self.save_prompt_edition(file_name='prompt.txt'), fg="white", bg="green")
        save_button.pack(side="right", padx=5)
        select_button = tk.Button(button_frame, text="Voltar", command=self.show_settings)
        select_button.pack(side="right", padx=5)

    def insert_prompt_space(self, event):
        pos_cursor = self.editing_area.index(tk.INSERT)
        self.editing_area.insert(pos_cursor, '    ')
        return 'break'

    def save_prompt_edition(self, file_name='prompt.txt'):
        edit_content = self.editing_area.get("1.0", tk.END)
        file_path = os.path.join('brain', 'files', file_name)
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(edit_content)

        messagebox.showinfo("Sucesso", "Alterações salvas com sucesso!")



    # Fifth Button: Help
    def show_help(self):
        self.clean_screen()

        help_frame = tk.LabelFrame(self.main_frame, text="Ajuda", padx=10, pady=10)
        help_frame.pack(fill="both", padx=20, pady=20)

        try:
            help_path = os.path.join("brain", "files", "ajuda.txt")
            with open(help_path, "r", encoding="utf-8") as arquivo_ajuda:
                help_content = arquivo_ajuda.read()
        except FileNotFoundError:
            help_content = "Arquivo de ajuda não encontrado. Certifique-se de que 'ajuda.txt' está no diretório correto."
        except Exception as e:
            help_content = f"Erro ao carregar a ajuda: {e}"

        # Displaying help content in a Text widget
        help_text = tk.Text(help_frame, wrap="word", bg="white", fg="black", height=20)
        help_text.insert("1.0", help_content)
        help_text.configure(state="normal")
        help_text.pack(fill="both", expand=True, padx=10, pady=10)

        # Detect and mark links in text
        def bookmark_links():
            standard_url = r"https?://[^\s]+"
            for match in re.finditer(standard_url, help_content):
                start_idx = f"1.0+{match.start()}c"
                end_idx = f"1.0+{match.end()}c"
                help_text.tag_add("link", start_idx, end_idx)
                help_text.tag_config("link", foreground="blue", underline=True)

                # Event to open the link in the browser
                help_text.tag_bind("link", "<Button-1>", lambda e, url=match.group(): webbrowser.open(url))
                help_text.tag_bind("link", "<Enter>", lambda e: help_text.config(cursor="hand2"))
                help_text.tag_bind("link", "<Leave>", lambda e: help_text.config(cursor=""))

        bookmark_links()
        help_text.configure(state="disabled")


def interface():
    root = tk.Tk()
    app = ForgeAVA(root)
    root.mainloop()

if __name__ == '__main__':
    interface()