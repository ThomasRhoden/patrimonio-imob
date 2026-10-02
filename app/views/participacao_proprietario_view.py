from app.core.idioma import Idioma
from app.core.data_utils import Data_Utils
from app.models.imovel import Imovel
from app.models.participacao_proprietario import Participacao_Proprietario

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Participacao_Proprietario_View:
    """View de participação de proprietário: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller, imovel, proprietarios_disponiveis):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self.imovel = imovel
        self._disponiveis = proprietarios_disponiveis
        self._selecionados = {}

        for participacao in imovel.proprietarios:
            self._selecionados[participacao.proprietario.id] = participacao

        self.configurar_janela()
        self.criar_componentes()
        self.configurar_eventos()
        self.atualizar_listas()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(f"{Idioma.t('imovel_proprietario.janela_titulo')} {self.imovel.id}")
        self.root.geometry("820x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_instrucao = tk.Label(
            self.root, text=Idioma.t("imovel_proprietario.instrucao"), font=("Arial", 11)
        )
        self.lbl_instrucao.grid(row=0, column=0, columnspan=3, padx=10, pady=8, sticky="w")

        tk.Label(self.root, text=Idioma.t("proprietario.titulo")).grid(row=1, column=0, padx=10, sticky="w")
        self.tbl_disponiveis = ttk.Treeview(self.root, columns=("id", "nome"), show="headings", height=12)
        self.tbl_disponiveis.column("id", width=35, anchor="center")
        self.tbl_disponiveis.column("nome", width=190)
        self.tbl_disponiveis.heading("id", text=Idioma.t("comum.id"))
        self.tbl_disponiveis.heading("nome", text=Idioma.t("comum.nome"))
        self.tbl_disponiveis.grid(row=2, column=0, padx=10, pady=5, sticky="ns")

        self.frm_meio = tk.Frame(self.root)
        self.frm_meio.grid(row=2, column=1, padx=5)

        tk.Label(self.frm_meio, text=f"{Idioma.t('imovel_proprietario.percentual')}:").pack(pady=(30, 2))
        self.txt_percentual = tk.Entry(self.frm_meio, width=8)
        self.txt_percentual.insert(0, "100")
        self.txt_percentual.pack(pady=2)

        self.btn_adicionar = tk.Button(self.frm_meio, text=Idioma.t("imovel_proprietario.adicionar"), width=14)
        self.btn_adicionar.pack(pady=8)
        self.btn_remover = tk.Button(self.frm_meio, text=Idioma.t("imovel_proprietario.remover"), width=14)
        self.btn_remover.pack(pady=8)

        tk.Label(self.root, text=Idioma.t("imovel.proprietarios_botao")).grid(row=1, column=2, padx=10, sticky="w")
        self.tbl_selecionados = ttk.Treeview(
            self.root, columns=("id", "nome", "percentual"), show="headings", height=12
        )
        self.tbl_selecionados.column("id", width=35, anchor="center")
        self.tbl_selecionados.column("nome", width=170)
        self.tbl_selecionados.column("percentual", width=125, anchor="center")
        self.tbl_selecionados.heading("id", text=Idioma.t("comum.id"))
        self.tbl_selecionados.heading("nome", text=Idioma.t("comum.nome"))
        self.tbl_selecionados.heading("percentual", text=Idioma.t("imovel_proprietario.percentual"))
        self.tbl_selecionados.grid(row=2, column=2, padx=10, pady=5, sticky="ns")

        self.frm_botoes = tk.Frame(self.root)
        self.frm_botoes.grid(row=3, column=0, columnspan=3, pady=15)
        self.btn_salvar = tk.Button(self.frm_botoes, text=Idioma.t("comum.salvar"), width=15)
        self.btn_salvar.grid(row=0, column=0, padx=5)
        self.btn_cancelar = tk.Button(self.frm_botoes, text=Idioma.t("comum.cancelar"), width=15)
        self.btn_cancelar.grid(row=0, column=1, padx=5)

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_adicionar.config(command=self.adicionar_selecionado)
        self.btn_remover.config(command=self.remover_selecionado)
        self.btn_salvar.config(command=self.salvar)
        self.btn_cancelar.config(command=self.fechar)

    def atualizar_listas(self):
        """Redesenha as Treeviews de disponíveis e de donos do imóvel."""
        for item in self.tbl_disponiveis.get_children():
            self.tbl_disponiveis.delete(item)
        for proprietario in self._disponiveis:
            self.tbl_disponiveis.insert("", tk.END, values=(proprietario.id, proprietario.nome))

        for item in self.tbl_selecionados.get_children():
            self.tbl_selecionados.delete(item)
        for participacao in self._selecionados.values():
            self.tbl_selecionados.insert(
                "", tk.END,
                values=(
                    participacao.proprietario.id,
                    participacao.proprietario.nome,
                    f"{participacao.percentual_participacao:.2f}%"
                )
            )

    def adicionar_selecionado(self):
        """Passa o proprietário escolhido para a lista de donos, com o percentual."""
        selecao = self.tbl_disponiveis.selection()
        if not selecao:
            self.exibir_mensagem(Idioma.t("proprietario.selecione_da_lista"), False)
            return

        id_proprietario = self.tbl_disponiveis.item(selecao[0])["values"][0]
        proprietario = next(p for p in self._disponiveis if p.id == id_proprietario)

        # as regras (0 a 100% e soma <= 100%) ficam nos models
        try:
            percentual = Data_Utils.converter_numero(
                self.txt_percentual.get(), Idioma.t("imovel_proprietario.percentual")
            )
            selecionados = dict(self._selecionados)
            selecionados[id_proprietario] = Participacao_Proprietario(proprietario, percentual)
            Imovel.validar_percentuais(list(selecionados.values()))
        except ValueError as e:
            self.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
            return

        self._selecionados = selecionados
        self.atualizar_listas()

    def remover_selecionado(self):
        """Tira o dono selecionado da lista."""
        selecao = self.tbl_selecionados.selection()
        if not selecao:
            return
        id_proprietario = self.tbl_selecionados.item(selecao[0])["values"][0]
        self._selecionados.pop(id_proprietario, None)
        self.atualizar_listas()

    def salvar(self):
        """Botão Salvar: manda a lista de donos ao controller."""
        self.controller.salvar_proprietarios(
            self, self.imovel, list(self._selecionados.values())
        )

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()
