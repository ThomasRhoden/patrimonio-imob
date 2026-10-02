from app.core.idioma import Idioma

import tkinter as tk
from tkinter import messagebox


class Login_View:
    """View de login: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("login.titulo"))
        self.root.geometry("400x250")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("app.nome"), font=("Arial", 14, "bold")
        )
        self.lbl_titulo.pack(pady=20)

        self.frm_dados = tk.Frame(self.root)
        self.frm_dados.pack(pady=5)

        tk.Label(self.frm_dados, text=f"{Idioma.t('usuario.login')}:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.txt_login = tk.Entry(self.frm_dados, width=30)
        self.txt_login.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.frm_dados, text=f"{Idioma.t('login.senha')}:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.txt_senha = tk.Entry(self.frm_dados, width=30, show="*")
        self.txt_senha.grid(row=1, column=1, padx=5, pady=5)

        self.btn_entrar = tk.Button(self.root, text=Idioma.t("login.entrar"), width=15)
        self.btn_entrar.pack(pady=20)
        self.txt_login.focus()

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_entrar.config(command=self.controller.autenticar)
        self.txt_login.bind("<Return>", self.ao_pressionar_enter)
        self.txt_senha.bind("<Return>", self.ao_pressionar_enter)

    def ao_pressionar_enter(self, event):
        """Enter no formulário equivale a clicar em Entrar."""
        self.controller.autenticar()

    def ler_dados_login(self):
        """Lê os campos do formulário e devolve ao controller."""
        return self.txt_login.get(), self.txt_senha.get()

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)
