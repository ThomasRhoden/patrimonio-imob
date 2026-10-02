from app.core.data_utils import Data_Utils
from app.core.idioma import Idioma

import tkinter as tk
from tkinter import ttk


class Dashboard_View:
    """View de dashboard: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self.controller.view = self
        self.criar_componentes()
        self.controller.atualizar()

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("dashboard.titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.pack(pady=10)

        self.frm_indicadores = tk.Frame(self.root)
        self.frm_indicadores.pack(pady=5, fill="x", padx=15)

        self.lbl_quantidade = self._criar_indicador(self.frm_indicadores, Idioma.t("dashboard.imoveis"), 0)
        self.lbl_valor_compra = self._criar_indicador(self.frm_indicadores, Idioma.t("dashboard.valor_compra_total"), 1)
        self.lbl_valor_estimado = self._criar_indicador(self.frm_indicadores, Idioma.t("dashboard.valor_estimado_total"), 2)
        self.lbl_valorizacao = self._criar_indicador(self.frm_indicadores, Idioma.t("dashboard.valorizacao_total"), 3)
        self.lbl_iptu = self._criar_indicador(self.frm_indicadores, Idioma.t("dashboard.iptu_estimado_anual"), 4)

        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(padx=15, pady=15, fill="both", expand=True)

        self.tbl_por_cidade = self._criar_aba_resumo(Idioma.t("dashboard.aba_por_cidade"))
        self.tbl_por_estado = self._criar_aba_resumo(Idioma.t("dashboard.aba_por_estado"))
        self.tbl_por_imovel = self._criar_aba_por_imovel(Idioma.t("dashboard.aba_por_imovel"))
        self.tbl_por_proprietario = self._criar_aba_por_proprietario(Idioma.t("dashboard.aba_por_proprietario"))

        self.btn_atualizar = tk.Button(self.root, text=Idioma.t("dashboard.atualizar"), command=self.controller.atualizar)
        self.btn_atualizar.pack(pady=10)

    def _criar_indicador(self, container, titulo, coluna):
        """Cria um quadro de indicador e devolve o Label do valor."""
        frm = tk.LabelFrame(container, text=titulo)
        frm.grid(row=0, column=coluna, padx=5, sticky="nsew")
        container.grid_columnconfigure(coluna, weight=1)
        lbl_valor = tk.Label(frm, text="-", font=("Arial", 13, "bold"))
        lbl_valor.pack(pady=10, padx=5)
        return lbl_valor

    def _criar_aba_resumo(self, titulo):
        """Cria uma aba com Treeview de resumo (cidade ou estado)."""
        aba = tk.Frame(self.notebook)
        self.notebook.add(aba, text=titulo)
        tabela = ttk.Treeview(aba, columns=("chave", "qtd", "compra", "estimado", "valorizacao"), show="headings")
        tabela.heading("chave", text=Idioma.t("dashboard.local"))
        tabela.heading("qtd", text=Idioma.t("dashboard.quantidade"))
        tabela.heading("compra", text=Idioma.t("imovel.valor_compra"))
        tabela.heading("estimado", text=Idioma.t("dashboard.valor_estimado"))
        tabela.heading("valorizacao", text=Idioma.t("dashboard.valorizacao"))
        tabela.column("chave", width=150)
        tabela.column("qtd", width=50, anchor="center")
        tabela.column("compra", width=120, anchor="e")
        tabela.column("estimado", width=120, anchor="e")
        tabela.column("valorizacao", width=120, anchor="e")
        tabela.pack(fill="both", expand=True, padx=5, pady=5)
        return tabela

    def _criar_aba_por_imovel(self, titulo):
        """Cria a aba Por imóvel com a Treeview do IPTU."""
        aba = tk.Frame(self.notebook)
        self.notebook.add(aba, text=titulo)
        tabela = ttk.Treeview(
            aba, columns=("id", "local", "tipo", "compra", "estimado", "valorizacao", "iptu"), show="headings"
        )
        tabela.heading("id", text=Idioma.t("comum.id"))
        tabela.heading("local", text=Idioma.t("dashboard.cidade_uf"))
        tabela.heading("tipo", text=Idioma.t("comum.tipo"))
        tabela.heading("compra", text=Idioma.t("imovel.valor_compra"))
        tabela.heading("estimado", text=Idioma.t("dashboard.valor_estimado"))
        tabela.heading("valorizacao", text=Idioma.t("dashboard.valorizacao"))
        tabela.heading("iptu", text=Idioma.t("dashboard.iptu_estimado"))
        tabela.column("id", width=40, anchor="center")
        tabela.column("local", width=150)
        tabela.column("tipo", width=100)
        tabela.column("compra", width=110, anchor="e")
        tabela.column("estimado", width=110, anchor="e")
        tabela.column("valorizacao", width=110, anchor="e")
        tabela.column("iptu", width=100, anchor="e")
        tabela.pack(fill="both", expand=True, padx=5, pady=5)
        return tabela

    def _criar_aba_por_proprietario(self, titulo):
        """Cria a aba Por proprietário: a parte de cada dono (valor × percentual)."""
        aba = tk.Frame(self.notebook)
        self.notebook.add(aba, text=titulo)
        tabela = ttk.Treeview(
            aba, columns=("proprietario", "qtd", "compra", "estimado", "valorizacao", "iptu"), show="headings"
        )
        tabela.heading("proprietario", text=Idioma.t("dashboard.proprietario"))
        tabela.heading("qtd", text=Idioma.t("dashboard.quantidade"))
        tabela.heading("compra", text=Idioma.t("dashboard.compra_parte"))
        tabela.heading("estimado", text=Idioma.t("dashboard.estimado_parte"))
        tabela.heading("valorizacao", text=Idioma.t("dashboard.valorizacao_parte"))
        tabela.heading("iptu", text=Idioma.t("dashboard.iptu_parte"))
        tabela.column("proprietario", width=170)
        tabela.column("qtd", width=45, anchor="center")
        tabela.column("compra", width=115, anchor="e")
        tabela.column("estimado", width=115, anchor="e")
        tabela.column("valorizacao", width=115, anchor="e")
        tabela.column("iptu", width=100, anchor="e")
        tabela.pack(fill="both", expand=True, padx=5, pady=(5, 0))
        # imóvel com menos de 100% distribuído: a parte sem dono não entra
        tk.Label(aba, text=Idioma.t("dashboard.nota_por_proprietario"), fg="#555555", wraplength=900,
                 justify="left", anchor="w").pack(fill="x", padx=5, pady=(2, 5))
        return tabela

    def exibir_resumo(self, resumo_geral, resumo_por_cidade, resumo_por_estado, detalhes_por_imovel,
                      resumo_por_proprietario=None):
        """Mostra os indicadores e preenche as abas do dashboard."""
        self.lbl_quantidade.config(text=str(resumo_geral["quantidade"]))
        self.lbl_valor_compra.config(text=Data_Utils.formatar_moeda(resumo_geral["valor_compra_total"]))
        self.lbl_valor_estimado.config(text=Data_Utils.formatar_moeda(resumo_geral["valor_estimado_total"]))
        self.lbl_valorizacao.config(text=Data_Utils.formatar_moeda(resumo_geral["valorizacao_total"]))
        self.lbl_iptu.config(text=Data_Utils.formatar_moeda(resumo_geral["iptu_estimado_total"]))

        self._preencher_tabela_resumo(self.tbl_por_cidade, resumo_por_cidade)
        self._preencher_tabela_resumo(self.tbl_por_estado, resumo_por_estado)
        self._preencher_tabela_por_imovel(detalhes_por_imovel)
        self._preencher_tabela_por_proprietario(resumo_por_proprietario or [])

    def _preencher_tabela_resumo(self, tabela, resumo):
        """Preenche uma Treeview de resumo com valores formatados."""
        for item in tabela.get_children():
            tabela.delete(item)
        for chave, dados in resumo.items():
            tabela.insert(
                "", tk.END,
                values=(
                    chave,
                    dados["quantidade"],
                    Data_Utils.formatar_moeda(dados["valor_compra_total"]),
                    Data_Utils.formatar_moeda(dados["valor_estimado_total"]),
                    Data_Utils.formatar_moeda(dados["valorizacao_total"])
                )
            )

    def _preencher_tabela_por_imovel(self, detalhes):
        """Preenche a Treeview Por imóvel (compra, estimado, IPTU)."""
        for item in self.tbl_por_imovel.get_children():
            self.tbl_por_imovel.delete(item)
        for detalhe in detalhes:
            imovel = detalhe["imovel"]
            self.tbl_por_imovel.insert(
                "", tk.END,
                values=(
                    imovel.id,
                    f"{imovel.cidade.nome}/{imovel.cidade.estado.sigla}",
                    imovel.tipo_imovel.nome,
                    Data_Utils.formatar_moeda(detalhe["valor_compra"]),
                    Data_Utils.formatar_moeda(detalhe["valor_estimado"]),
                    Data_Utils.formatar_moeda(detalhe["valorizacao"]),
                    Data_Utils.formatar_moeda(detalhe["iptu_estimado"])
                )
            )

    def _preencher_tabela_por_proprietario(self, resumo):
        """Preenche a Treeview Por proprietário com as partes formatadas."""
        for item in self.tbl_por_proprietario.get_children():
            self.tbl_por_proprietario.delete(item)
        for dados in resumo:
            self.tbl_por_proprietario.insert(
                "", tk.END,
                values=(
                    dados["proprietario"],
                    dados["quantidade"],
                    Data_Utils.formatar_moeda(dados["valor_compra_parte"]),
                    Data_Utils.formatar_moeda(dados["valor_estimado_parte"]),
                    Data_Utils.formatar_moeda(dados["valorizacao_parte"]),
                    Data_Utils.formatar_moeda(dados["iptu_parte"])
                )
            )
