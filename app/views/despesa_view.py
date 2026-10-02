from app.core.idioma import Idioma
from app.core.data_utils import Data_Utils

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Despesa_View:
    """View de despesa: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller, imovel):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self.controller.view = self
        self.imovel = imovel
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()
        self.controller.carregar_imovel(imovel)

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(f"{Idioma.t('despesa.janela_titulo')} {self.imovel.id}")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("despesa.dados_frame"))
        self.frm_dados.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frm_dados.grid_columnconfigure(1, weight=1)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('despesa.descricao')}:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.txt_descricao = tk.Entry(self.frm_dados, width=30)
        self.txt_descricao.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.valor')}:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.txt_valor = tk.Entry(self.frm_dados, width=30)
        self.txt_valor.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.data')} {Idioma.t('comum.formato_data')}:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.txt_data = tk.Entry(self.frm_dados, width=30)
        self.txt_data.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.frm_botoes = tk.Frame(self.root)
        self.frm_botoes.grid(row=1, column=0, columnspan=2, pady=5)

        self.btn_novo = tk.Button(self.frm_botoes, text=Idioma.t("comum.novo"), width=11)
        self.btn_novo.grid(row=0, column=0, padx=4)
        self.btn_salvar = tk.Button(self.frm_botoes, text=Idioma.t("comum.salvar"), width=11)
        self.btn_salvar.grid(row=0, column=1, padx=4)
        self.btn_alterar = tk.Button(self.frm_botoes, text=Idioma.t("comum.alterar"), width=11)
        self.btn_alterar.grid(row=0, column=2, padx=4)
        self.btn_excluir = tk.Button(self.frm_botoes, text=Idioma.t("comum.excluir"), width=11)
        self.btn_excluir.grid(row=0, column=3, padx=4)
        self.btn_fechar = tk.Button(self.frm_botoes, text=Idioma.t("comum.fechar"), width=11)
        self.btn_fechar.grid(row=0, column=4, padx=4)

        self.tbl_despesas = ttk.Treeview(self.root, height=10)
        self.tbl_despesas.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_despesas["columns"] = ("id", "descricao", "valor", "data")
        self.tbl_despesas.column("#0", width=0, stretch=False)
        self.tbl_despesas.column("id", width=10, anchor="center")
        self.tbl_despesas.column("descricao", width=60)
        self.tbl_despesas.column("valor", width=30, anchor="e")
        self.tbl_despesas.column("data", width=30)
        self.tbl_despesas.heading("id", text=Idioma.t("comum.id"))
        self.tbl_despesas.heading("descricao", text=Idioma.t("despesa.descricao"))
        self.tbl_despesas.heading("valor", text=Idioma.t("comum.valor"))
        self.tbl_despesas.heading("data", text=Idioma.t("comum.data"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_despesas.bind("<<TreeviewSelect>>", self.controller.selecionar_despesa)

    def preencher_campos(self, despesa):
        """Preenche o formulário com a despesa selecionada."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(despesa.id))
        self.txt_id.config(state="readonly")
        self.txt_descricao.insert(0, despesa.descricao)
        self.txt_valor.insert(0, str(despesa.valor))
        self.txt_data.insert(0, Data_Utils.data_para_string(despesa.data_despesa))

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.txt_descricao.delete(0, tk.END)
        self.txt_valor.delete(0, tk.END)
        self.txt_data.delete(0, tk.END)

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_despesas.get_children():
            self.tbl_despesas.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_despesas.selection()[0]
        return self.tbl_despesas.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(Idioma.t("comum.confirmacao"), Idioma.t("comum.confirmar_exclusao"), parent=self.root)

    def ler_dados_despesa(self):
        """Lê os campos do formulário e devolve ao controller."""
        descricao = self.txt_descricao.get()
        valor = Data_Utils.converter_numero(self.txt_valor.get(), Idioma.t("comum.valor"))
        data_despesa = Data_Utils.converter_data(self.txt_data.get(), Idioma.t("comum.data"))
        return descricao, valor, data_despesa

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_despesas(self, despesas):
        """Mostra despesas na Treeview."""
        self.limpar_treeview()
        for despesa in despesas:
            self.tbl_despesas.insert(
                "", tk.END,
                values=(
                    despesa.id,
                    despesa.descricao,
                    Data_Utils.formatar_moeda(despesa.valor),
                    Data_Utils.data_para_string(despesa.data_despesa)
                )
            )

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()
