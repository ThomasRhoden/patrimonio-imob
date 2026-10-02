from app.core.idioma import Idioma

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Cidade_View:
    """View de cidade: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self._estados = []
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("cidade.janela_titulo"))
        self.root.geometry("700x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("cidade.titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("cidade.dados_frame"))
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
        self.txt_nome = tk.Entry(self.frm_dados, width=40)
        self.txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('cidade.estado')}:").grid(
            row=2, column=0, padx=5, pady=5, sticky="w"
        )
        self.cmb_estados = ttk.Combobox(self.frm_dados, width=37, state="readonly")
        self.cmb_estados.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        self.frm_botoes = tk.Frame(self.frm_dados, border=2, relief="groove")
        self.frm_botoes.grid(row=3, column=0, columnspan=2, padx=10, pady=5)

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

        self.tbl_cidades = ttk.Treeview(self.root, height=12)
        self.tbl_cidades.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_cidades["columns"] = ("id", "nome", "estado")
        self.tbl_cidades.column("#0", width=0, stretch=False)
        self.tbl_cidades.column("id", width=10, anchor="center")
        self.tbl_cidades.column("nome", width=60)
        self.tbl_cidades.column("estado", width=40)
        self.tbl_cidades.heading("id", text=Idioma.t("comum.id"))
        self.tbl_cidades.heading("nome", text=Idioma.t("comum.nome"))
        self.tbl_cidades.heading("estado", text=Idioma.t("cidade.estado"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_cidades.bind("<<TreeviewSelect>>", self.controller.selecionar_cidade)
        # recarrega a lista de estados sempre que a combobox é aberta
        self.cmb_estados.config(postcommand=self.controller.carregar_estados)

    def carregar_estados(self, estados):
        """Preenche a Combobox com estados."""
        self._estados = estados
        valores = [f"{estado.id} - {estado.sigla} - {estado.nome}" for estado in estados]
        selecionado = self.cmb_estados.get()
        self.cmb_estados["values"] = valores
        self.cmb_estados.set(selecionado if selecionado in valores else "")

    def preencher_campos(self, cidade):
        """Preenche o formulário com a cidade selecionada."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(cidade.id))
        self.txt_id.config(state="readonly")
        self.txt_nome.insert(0, cidade.nome)
        for indice, estado in enumerate(self._estados):
            if estado.id == cidade.estado.id:
                self.cmb_estados.current(indice)
                break

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.txt_nome.delete(0, tk.END)
        self.cmb_estados.set("")
        self.txt_nome.focus()

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_cidades.get_children():
            self.tbl_cidades.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_cidades.selection()[0]
        return self.tbl_cidades.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(
            Idioma.t("comum.confirmacao"), Idioma.t("cidade.confirmar_exclusao"), parent=self.root
        )

    def ler_dados_cidade(self):
        """Lê os campos do formulário e devolve ao controller."""
        nome = self.txt_nome.get()
        indice = self.cmb_estados.current()
        estado = self._estados[indice] if indice >= 0 else None
        return nome, estado

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_cidades(self, cidades):
        """Mostra cidades na Treeview."""
        self.limpar_treeview()
        for cidade in cidades:
            self.tbl_cidades.insert(
                "", tk.END,
                values=(cidade.id, cidade.nome, f"{cidade.estado.sigla} - {cidade.estado.nome}")
            )

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()

    def iniciar(self):
        """Ao abrir a tela, pede ao controller os dados iniciais."""
        self.controller.new()
        self.controller.carregar_estados()
        self.controller.get_all()
