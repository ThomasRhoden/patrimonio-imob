from app.core.idioma import Idioma

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Proprietario_View:
    """View de proprietário: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self._estados = []
        self._cidades = []
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("proprietario.janela_titulo"))
        self.root.geometry("800x600")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("proprietario.titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("proprietario.dados_frame"))
        self.frm_dados.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        for col, peso in ((0, 0), (1, 1), (2, 0), (3, 1)):
            self.frm_dados.grid_columnconfigure(col, weight=peso)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.nome')}:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.txt_nome = tk.Entry(self.frm_dados, width=35)
        self.txt_nome.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('proprietario.cpf')}:").grid(row=1, column=2, padx=5, pady=5, sticky="w")
        self.txt_cpf = tk.Entry(self.frm_dados, width=20)
        self.txt_cpf.grid(row=1, column=3, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.email')}:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.txt_email = tk.Entry(self.frm_dados, width=35)
        self.txt_email.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('proprietario.telefone')}:").grid(row=2, column=2, padx=5, pady=5, sticky="w")
        self.txt_telefone = tk.Entry(self.frm_dados, width=20)
        self.txt_telefone.grid(row=2, column=3, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('cidade.estado')}:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.cmb_estados = ttk.Combobox(self.frm_dados, width=32, state="readonly")
        self.cmb_estados.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.cidade')}:").grid(row=3, column=2, padx=5, pady=5, sticky="w")
        self.cmb_cidades = ttk.Combobox(self.frm_dados, width=32, state="readonly")
        self.cmb_cidades.grid(row=3, column=3, padx=5, pady=5, sticky="w")

        self.frm_botoes = tk.Frame(self.frm_dados, border=2, relief="groove")
        self.frm_botoes.grid(row=4, column=0, columnspan=4, padx=10, pady=5)

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

        self.tbl_proprietarios = ttk.Treeview(self.root, height=12)
        self.tbl_proprietarios.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_proprietarios["columns"] = ("id", "nome", "cpf", "cidade")
        self.tbl_proprietarios.column("#0", width=0, stretch=False)
        self.tbl_proprietarios.column("id", width=10, anchor="center")
        self.tbl_proprietarios.column("nome", width=50)
        self.tbl_proprietarios.column("cpf", width=30)
        self.tbl_proprietarios.column("cidade", width=40)
        self.tbl_proprietarios.heading("id", text=Idioma.t("comum.id"))
        self.tbl_proprietarios.heading("nome", text=Idioma.t("comum.nome"))
        self.tbl_proprietarios.heading("cpf", text=Idioma.t("proprietario.cpf"))
        self.tbl_proprietarios.heading("cidade", text=Idioma.t("imovel.cidade"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_proprietarios.bind("<<TreeviewSelect>>", self.controller.selecionar_proprietario)
        self.cmb_estados.bind("<<ComboboxSelected>>", self.controller.carregar_cidades_do_estado_selecionado)
        # recarrega as listas do banco sempre que a combobox é aberta
        self.cmb_estados.config(postcommand=self.controller.carregar_estados)
        self.cmb_cidades.config(postcommand=lambda: self.controller.carregar_cidades_do_estado_selecionado(None))

    def carregar_estados(self, estados):
        """Preenche a Combobox com estados."""
        self._estados = estados
        valores = [f"{e.id} - {e.sigla} - {e.nome}" for e in estados]
        selecionado = self.cmb_estados.get()
        self.cmb_estados["values"] = valores
        self.cmb_estados.set(selecionado if selecionado in valores else "")

    def carregar_cidades(self, cidades):
        """Preenche a Combobox com cidades."""
        self._cidades = cidades
        valores = [f"{c.id} - {c.nome}" for c in cidades]
        selecionado = self.cmb_cidades.get()
        self.cmb_cidades["values"] = valores
        self.cmb_cidades.set(selecionado if selecionado in valores else "")

    def get_estado_selecionado_id(self):
        """Devolve o id do estado escolhido na Combobox."""
        indice = self.cmb_estados.current()
        if indice < 0:
            return None
        return self._estados[indice].id

    def preencher_campos(self, proprietario, cidades):
        """Preenche o formulário com o proprietário selecionado."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(proprietario.id))
        self.txt_id.config(state="readonly")
        self.txt_nome.insert(0, proprietario.nome)
        self.txt_cpf.insert(0, proprietario.cpf or "")
        self.txt_email.insert(0, proprietario.email or "")
        self.txt_telefone.insert(0, proprietario.telefone or "")

        if proprietario.cidade is not None:
            for indice, estado in enumerate(self._estados):
                if estado.id == proprietario.cidade.estado.id:
                    self.cmb_estados.current(indice)
                    break
            self.carregar_cidades(cidades)
            for indice, cidade in enumerate(self._cidades):
                if cidade.id == proprietario.cidade.id:
                    self.cmb_cidades.current(indice)
                    break

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.txt_nome.delete(0, tk.END)
        self.txt_cpf.delete(0, tk.END)
        self.txt_email.delete(0, tk.END)
        self.txt_telefone.delete(0, tk.END)
        self.cmb_estados.set("")
        self.cmb_cidades.set("")
        self.cmb_cidades["values"] = []
        self._cidades = []
        self.txt_nome.focus()

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_proprietarios.get_children():
            self.tbl_proprietarios.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_proprietarios.selection()[0]
        return self.tbl_proprietarios.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(
            Idioma.t("comum.confirmacao"), Idioma.t("proprietario.confirmar_exclusao"), parent=self.root
        )

    def ler_dados_proprietario(self):
        """Lê os campos do formulário e devolve ao controller."""
        nome = self.txt_nome.get()
        cpf = self.txt_cpf.get() or None
        email = self.txt_email.get() or None
        telefone = self.txt_telefone.get() or None
        indice = self.cmb_cidades.current()
        cidade = self._cidades[indice] if indice >= 0 else None
        return nome, cpf, email, telefone, cidade

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_proprietarios(self, proprietarios):
        """Mostra proprietários na Treeview."""
        self.limpar_treeview()
        for proprietario in proprietarios:
            cidade_texto = ""
            if proprietario.cidade is not None:
                cidade_texto = f"{proprietario.cidade.nome}/{proprietario.cidade.estado.sigla}"
            self.tbl_proprietarios.insert(
                "", tk.END,
                values=(proprietario.id, proprietario.nome, proprietario.cpf or "", cidade_texto)
            )

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()

    def iniciar(self):
        """Ao abrir a tela, pede ao controller os dados iniciais."""
        self.controller.new()
        self.controller.carregar_estados()
        self.controller.get_all()
