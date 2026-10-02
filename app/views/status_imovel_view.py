from app.core.idioma import Idioma

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Status_Imovel_View:
    """View de status de imóvel: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("status_imovel.janela_titulo"))
        self.root.geometry("700x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("status_imovel.titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("comum.nome"))
        self.frm_dados.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.frm_dados.grid_columnconfigure(0, weight=0)
        self.frm_dados.grid_columnconfigure(1, weight=1)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(
            row=0, column=0, padx=5, pady=5, sticky="w"
        )
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.nome')}:").grid(
            row=1, column=0, padx=5, pady=5, sticky="w"
        )
        self.txt_nome = tk.Entry(self.frm_dados, width=30)
        self.txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        self.frm_botoes = tk.Frame(self.frm_dados, border=2, relief="groove")
        self.frm_botoes.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

        self.btn_novo = tk.Button(self.frm_botoes, text=Idioma.t("comum.novo"), width=11)
        self.btn_novo.grid(row=0, column=0, padx=5, pady=5)
        self.btn_salvar = tk.Button(self.frm_botoes, text=Idioma.t("comum.salvar"), width=11)
        self.btn_salvar.grid(row=0, column=1, padx=5, pady=5)
        self.btn_alterar = tk.Button(self.frm_botoes, text=Idioma.t("comum.alterar"), width=11)
        self.btn_alterar.grid(row=0, column=2, padx=5, pady=5)
        self.btn_excluir = tk.Button(self.frm_botoes, text=Idioma.t("comum.excluir"), width=11)
        self.btn_excluir.grid(row=0, column=3, padx=5, pady=5)
        self.btn_fechar = tk.Button(self.frm_botoes, text=Idioma.t("comum.fechar"), width=11)
        self.btn_fechar.grid(row=0, column=4, padx=5, pady=5)

        self.tbl_status = ttk.Treeview(self.root, height=12)
        self.tbl_status.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_status["columns"] = ("id", "nome")
        self.tbl_status.column("#0", width=0, stretch=False)
        self.tbl_status.column("id", width=10, anchor="center")
        self.tbl_status.column("nome", width=60)
        self.tbl_status.heading("id", text=Idioma.t("comum.id"))
        self.tbl_status.heading("nome", text=Idioma.t("comum.nome"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_status.bind("<<TreeviewSelect>>", self.controller.selecionar_status)

    def preencher_campos(self, status_imovel):
        """Preenche o formulário com o status de imóvel selecionado."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(status_imovel.id))
        self.txt_id.config(state="readonly")
        self.txt_nome.insert(0, status_imovel.nome)

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.txt_nome.delete(0, tk.END)
        self.txt_nome.focus()

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_status.get_children():
            self.tbl_status.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_status.selection()[0]
        return self.tbl_status.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(Idioma.t("comum.confirmacao"), Idioma.t("comum.confirmar_exclusao"), parent=self.root)

    def ler_dados_status_imovel(self):
        """Lê os campos do formulário e devolve ao controller."""
        return self.txt_nome.get()

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_status_imovel(self, status_lista):
        """Mostra status de imóvel na Treeview."""
        self.limpar_treeview()
        for status in status_lista:
            self.tbl_status.insert("", tk.END, values=(status.id, status.nome))

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()

    def iniciar(self):
        """Ao abrir a tela, pede ao controller os dados iniciais."""
        self.controller.new()
        self.controller.get_all()
