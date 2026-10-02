from app.core.idioma import Idioma
from app.core.data_utils import Data_Utils

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Avaliacao_View:
    """View de avaliação: só monta a tela e repassa os cliques ao controller."""

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
        self.root.title(f"{Idioma.t('avaliacao.janela_titulo')} {self.imovel.id}")
        self.root.geometry("700x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("avaliacao.dados_frame"))
        self.frm_dados.grid(row=0, column=0, columnspan=2, padx=10, pady=10, sticky="ew")
        self.frm_dados.grid_columnconfigure(1, weight=1)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('avaliacao.data')} {Idioma.t('comum.formato_data')}:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.txt_data = tk.Entry(self.frm_dados, width=30)
        self.txt_data.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('avaliacao.valor_estimado')}:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.txt_valor = tk.Entry(self.frm_dados, width=30)
        self.txt_valor.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.observacoes')}:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.txt_observacao = tk.Entry(self.frm_dados, width=30)
        self.txt_observacao.grid(row=3, column=1, padx=5, pady=5, sticky="w")

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

        self.tbl_avaliacoes = ttk.Treeview(self.root, height=10)
        self.tbl_avaliacoes.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_avaliacoes["columns"] = ("id", "data", "valor_estimado", "valorizacao")
        self.tbl_avaliacoes.column("#0", width=0, stretch=False)
        self.tbl_avaliacoes.column("id", width=10, anchor="center")
        self.tbl_avaliacoes.column("data", width=30)
        self.tbl_avaliacoes.column("valor_estimado", width=35, anchor="e")
        self.tbl_avaliacoes.column("valorizacao", width=35, anchor="e")
        self.tbl_avaliacoes.heading("id", text=Idioma.t("comum.id"))
        self.tbl_avaliacoes.heading("data", text=Idioma.t("comum.data"))
        self.tbl_avaliacoes.heading("valor_estimado", text=Idioma.t("avaliacao.valor_estimado"))
        self.tbl_avaliacoes.heading("valorizacao", text=Idioma.t("avaliacao.valorizacao"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_avaliacoes.bind("<<TreeviewSelect>>", self.controller.selecionar_avaliacao)

    def preencher_campos(self, avaliacao):
        """Preenche o formulário com a avaliação selecionada."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(avaliacao.id))
        self.txt_id.config(state="readonly")
        self.txt_data.insert(0, Data_Utils.data_para_string(avaliacao.data_avaliacao))
        self.txt_valor.insert(0, str(avaliacao.valor_estimado))
        self.txt_observacao.insert(0, avaliacao.observacao or "")

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.txt_data.delete(0, tk.END)
        self.txt_valor.delete(0, tk.END)
        self.txt_observacao.delete(0, tk.END)

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_avaliacoes.get_children():
            self.tbl_avaliacoes.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_avaliacoes.selection()[0]
        return self.tbl_avaliacoes.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(Idioma.t("comum.confirmacao"), Idioma.t("comum.confirmar_exclusao"), parent=self.root)

    def ler_dados_avaliacao(self):
        """Lê os campos do formulário e devolve ao controller."""
        data_avaliacao = Data_Utils.converter_data(self.txt_data.get(), Idioma.t("avaliacao.data"))
        valor_estimado = Data_Utils.converter_numero(self.txt_valor.get(), Idioma.t("avaliacao.valor_estimado"))
        observacao = self.txt_observacao.get() or None
        return data_avaliacao, valor_estimado, observacao

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_avaliacoes(self, avaliacoes):
        """Mostra avaliações na Treeview."""
        self.limpar_treeview()
        for avaliacao in avaliacoes:
            self.tbl_avaliacoes.insert(
                "", tk.END,
                values=(
                    avaliacao.id,
                    Data_Utils.data_para_string(avaliacao.data_avaliacao),
                    Data_Utils.formatar_moeda(avaliacao.valor_estimado),
                    Data_Utils.formatar_moeda(avaliacao.valorizacao)
                )
            )

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()
