from app.core.idioma import Idioma
from app.core.data_utils import Data_Utils

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Imovel_View:
    """View de imóvel: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self._estados = []
        self._cidades = []
        self._tipos_imovel = []
        self._status_imovel = []
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("imovel.janela_titulo"))
        self.root.geometry("950x700")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("imovel.titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=4, padx=5, pady=5)

        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("imovel.dados_frame"))
        self.frm_dados.grid(row=1, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        for col, peso in ((0, 0), (1, 1), (2, 0), (3, 1)):
            self.frm_dados.grid_columnconfigure(col, weight=peso)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(row=0, column=0, padx=5, pady=4, sticky="w")
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.estado')}:").grid(row=1, column=0, padx=5, pady=4, sticky="w")
        self.cmb_estados = ttk.Combobox(self.frm_dados, width=30, state="readonly")
        self.cmb_estados.grid(row=1, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.cidade')}:").grid(row=1, column=2, padx=5, pady=4, sticky="w")
        self.cmb_cidades = ttk.Combobox(self.frm_dados, width=30, state="readonly")
        self.cmb_cidades.grid(row=1, column=3, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.tipo')}:").grid(row=2, column=0, padx=5, pady=4, sticky="w")
        self.cmb_tipo = ttk.Combobox(self.frm_dados, width=30, state="readonly")
        self.cmb_tipo.grid(row=2, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.status')}:").grid(row=2, column=2, padx=5, pady=4, sticky="w")
        self.cmb_status = ttk.Combobox(self.frm_dados, width=30, state="readonly")
        self.cmb_status.grid(row=2, column=3, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.area_total')}:").grid(row=3, column=0, padx=5, pady=4, sticky="w")
        self.txt_area_total = tk.Entry(self.frm_dados, width=32)
        self.txt_area_total.grid(row=3, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.area_privativa')}:").grid(row=3, column=2, padx=5, pady=4, sticky="w")
        self.txt_area_privativa = tk.Entry(self.frm_dados, width=32)
        self.txt_area_privativa.grid(row=3, column=3, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.valor_compra')}:").grid(row=4, column=0, padx=5, pady=4, sticky="w")
        self.txt_valor_compra = tk.Entry(self.frm_dados, width=32)
        self.txt_valor_compra.grid(row=4, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.data_compra')} {Idioma.t('comum.formato_data')}:").grid(row=4, column=2, padx=5, pady=4, sticky="w")
        self.txt_data_compra = tk.Entry(self.frm_dados, width=32)
        self.txt_data_compra.grid(row=4, column=3, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.comodos')}:").grid(row=5, column=0, padx=5, pady=4, sticky="w")
        self.txt_comodos = tk.Entry(self.frm_dados, width=32)
        self.txt_comodos.grid(row=5, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.banheiros')}:").grid(row=5, column=2, padx=5, pady=4, sticky="w")
        self.txt_banheiros = tk.Entry(self.frm_dados, width=32)
        self.txt_banheiros.grid(row=5, column=3, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.vagas')}:").grid(row=6, column=0, padx=5, pady=4, sticky="w")
        self.txt_vagas = tk.Entry(self.frm_dados, width=32)
        self.txt_vagas.grid(row=6, column=1, padx=5, pady=4, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.observacoes')}:").grid(row=6, column=2, padx=5, pady=4, sticky="w")
        self.txt_observacoes = tk.Entry(self.frm_dados, width=32)
        self.txt_observacoes.grid(row=6, column=3, padx=5, pady=4, sticky="w")

        self.frm_botoes = tk.Frame(self.frm_dados, border=2, relief="groove")
        self.frm_botoes.grid(row=7, column=0, columnspan=4, padx=10, pady=6)

        self.btn_novo = tk.Button(self.frm_botoes, text=Idioma.t("comum.novo"), width=14)
        self.btn_novo.grid(row=0, column=0, padx=4, pady=5)
        self.btn_salvar = tk.Button(self.frm_botoes, text=Idioma.t("comum.salvar"), width=14)
        self.btn_salvar.grid(row=0, column=1, padx=4, pady=5)
        self.btn_alterar = tk.Button(self.frm_botoes, text=Idioma.t("comum.alterar"), width=14)
        self.btn_alterar.grid(row=0, column=2, padx=4, pady=5)
        self.btn_excluir = tk.Button(self.frm_botoes, text=Idioma.t("comum.excluir"), width=14)
        self.btn_excluir.grid(row=0, column=3, padx=4, pady=5)
        self.btn_proprietarios = tk.Button(self.frm_botoes, text=Idioma.t("imovel.proprietarios_botao"), width=14)
        self.btn_proprietarios.grid(row=0, column=4, padx=4, pady=5)
        self.btn_avaliacoes = tk.Button(self.frm_botoes, text=Idioma.t("imovel.avaliacoes_botao"), width=14)
        self.btn_avaliacoes.grid(row=1, column=0, padx=4, pady=5)
        self.btn_despesas = tk.Button(self.frm_botoes, text=Idioma.t("imovel.despesas_botao"), width=14)
        self.btn_despesas.grid(row=1, column=1, padx=4, pady=5)
        self.btn_movimentacoes = tk.Button(self.frm_botoes, text=Idioma.t("imovel.movimentacoes_botao"), width=14)
        self.btn_movimentacoes.grid(row=1, column=2, padx=4, pady=5)
        self.btn_fechar = tk.Button(self.frm_botoes, text=Idioma.t("comum.fechar"), width=14)
        self.btn_fechar.grid(row=1, column=3, padx=4, pady=5)

        self.tbl_imoveis = ttk.Treeview(self.root, height=12)
        self.tbl_imoveis.grid(row=2, column=0, columnspan=4, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_imoveis["columns"] = ("id", "cidade", "tipo", "status", "area_total", "valor_compra")
        self.tbl_imoveis.column("#0", width=0, stretch=False)
        self.tbl_imoveis.column("id", width=10, anchor="center")
        self.tbl_imoveis.column("cidade", width=40)
        self.tbl_imoveis.column("tipo", width=30)
        self.tbl_imoveis.column("status", width=25)
        self.tbl_imoveis.column("area_total", width=25, anchor="center")
        self.tbl_imoveis.column("valor_compra", width=30, anchor="e")
        self.tbl_imoveis.heading("id", text=Idioma.t("comum.id"))
        self.tbl_imoveis.heading("cidade", text=Idioma.t("imovel.cidade"))
        self.tbl_imoveis.heading("tipo", text=Idioma.t("imovel.tipo"))
        self.tbl_imoveis.heading("status", text=Idioma.t("imovel.status"))
        self.tbl_imoveis.heading("area_total", text=Idioma.t("imovel.area_total"))
        self.tbl_imoveis.heading("valor_compra", text=Idioma.t("imovel.valor_compra"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_proprietarios.config(command=self.controller.abrir_proprietarios)
        self.btn_avaliacoes.config(command=self.controller.abrir_avaliacoes)
        self.btn_despesas.config(command=self.controller.abrir_despesas)
        self.btn_movimentacoes.config(command=self.controller.abrir_movimentacoes)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_imoveis.bind("<<TreeviewSelect>>", self.controller.selecionar_imovel)
        self.cmb_estados.bind("<<ComboboxSelected>>", self.controller.carregar_cidades_do_estado_selecionado)
        # recarrega as listas do banco sempre que a combobox é aberta
        self.cmb_estados.config(postcommand=self.controller.carregar_estados)
        self.cmb_cidades.config(postcommand=lambda: self.controller.carregar_cidades_do_estado_selecionado(None))
        self.cmb_tipo.config(postcommand=self.controller.carregar_tipos_imovel)
        self.cmb_status.config(postcommand=self.controller.carregar_status_imovel)

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

    def carregar_tipos_imovel(self, tipos):
        """Preenche a Combobox com tipos de imóvel."""
        self._tipos_imovel = tipos
        valores = [f"{t.id} - {t.nome}" for t in tipos]
        selecionado = self.cmb_tipo.get()
        self.cmb_tipo["values"] = valores
        self.cmb_tipo.set(selecionado if selecionado in valores else "")

    def carregar_status_imovel(self, status_lista):
        """Preenche a Combobox com status de imóvel."""
        self._status_imovel = status_lista
        valores = [f"{s.id} - {s.nome}" for s in status_lista]
        selecionado = self.cmb_status.get()
        self.cmb_status["values"] = valores
        self.cmb_status.set(selecionado if selecionado in valores else "")

    def get_estado_selecionado_id(self):
        """Devolve o id do estado escolhido na Combobox."""
        indice = self.cmb_estados.current()
        if indice < 0:
            return None
        return self._estados[indice].id

    def preencher_campos(self, imovel, cidades):
        """Preenche o formulário com o imóvel selecionado."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(imovel.id))
        self.txt_id.config(state="readonly")

        for indice, estado in enumerate(self._estados):
            if estado.id == imovel.cidade.estado.id:
                self.cmb_estados.current(indice)
                break
        self.carregar_cidades(cidades)
        for indice, cidade in enumerate(self._cidades):
            if cidade.id == imovel.cidade.id:
                self.cmb_cidades.current(indice)
                break

        for indice, tipo in enumerate(self._tipos_imovel):
            if tipo.id == imovel.tipo_imovel.id:
                self.cmb_tipo.current(indice)
                break

        for indice, status in enumerate(self._status_imovel):
            if status.id == imovel.status.id:
                self.cmb_status.current(indice)
                break

        self.txt_area_total.insert(0, str(imovel.area_total))
        self.txt_area_privativa.insert(0, str(imovel.area_privativa))
        self.txt_valor_compra.insert(0, str(imovel.valor_compra))
        self.txt_data_compra.insert(0, Data_Utils.data_para_string(imovel.data_compra))
        self.txt_comodos.insert(0, str(imovel.comodos))
        self.txt_banheiros.insert(0, str(imovel.banheiros))
        self.txt_vagas.insert(0, str(imovel.vagas_garagem))
        self.txt_observacoes.insert(0, imovel.observacoes or "")

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        for campo in (
            self.txt_area_total, self.txt_area_privativa, self.txt_valor_compra,
            self.txt_data_compra, self.txt_comodos, self.txt_banheiros,
            self.txt_vagas, self.txt_observacoes
        ):
            campo.delete(0, tk.END)
        self.cmb_estados.set("")
        self.cmb_cidades.set("")
        self.cmb_cidades["values"] = []
        self._cidades = []
        self.cmb_tipo.set("")
        self.cmb_status.set("")

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_imoveis.get_children():
            self.tbl_imoveis.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_imoveis.selection()[0]
        return self.tbl_imoveis.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(
            Idioma.t("comum.confirmacao"), Idioma.t("imovel.confirmar_exclusao"), parent=self.root
        )

    def ler_dados_imovel(self):
        """Lê os campos do formulário e devolve ao controller."""
        indice_cidade = self.cmb_cidades.current()
        cidade = self._cidades[indice_cidade] if indice_cidade >= 0 else None

        indice_tipo = self.cmb_tipo.current()
        tipo_imovel = self._tipos_imovel[indice_tipo] if indice_tipo >= 0 else None

        indice_status = self.cmb_status.current()
        status = self._status_imovel[indice_status] if indice_status >= 0 else None

        area_total = Data_Utils.converter_numero(self.txt_area_total.get(), Idioma.t("imovel.area_total"))
        area_privativa = Data_Utils.converter_numero(self.txt_area_privativa.get(), Idioma.t("imovel.area_privativa"))
        valor_compra = Data_Utils.converter_numero(self.txt_valor_compra.get(), Idioma.t("imovel.valor_compra"))
        data_compra = Data_Utils.converter_data(self.txt_data_compra.get(), Idioma.t("imovel.data_compra"))
        comodos = Data_Utils.converter_inteiro(self.txt_comodos.get(), Idioma.t("imovel.comodos"))
        banheiros = Data_Utils.converter_inteiro(self.txt_banheiros.get(), Idioma.t("imovel.banheiros"))
        vagas_garagem = Data_Utils.converter_inteiro(self.txt_vagas.get(), Idioma.t("imovel.vagas"))
        observacoes = self.txt_observacoes.get() or None

        return (
            cidade, tipo_imovel, status, area_total, area_privativa,
            valor_compra, data_compra, comodos, banheiros, vagas_garagem,
            observacoes
        )

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_imoveis(self, imoveis):
        """Mostra imóveis na Treeview."""
        self.limpar_treeview()
        for imovel in imoveis:
            self.tbl_imoveis.insert(
                "", tk.END,
                values=(
                    imovel.id,
                    f"{imovel.cidade.nome}/{imovel.cidade.estado.sigla}",
                    imovel.tipo_imovel.nome,
                    imovel.status.nome,
                    Data_Utils.formatar_area(imovel.area_total),
                    Data_Utils.formatar_moeda(imovel.valor_compra)
                )
            )

    def abrir_proprietarios(self, imovel, proprietarios_disponiveis):
        """Abre o popup (Toplevel) de proprietários do imóvel."""
        from tkinter import Toplevel
        from app.views.participacao_proprietario_view import Participacao_Proprietario_View
        janela = Toplevel(self.root)
        Participacao_Proprietario_View(janela, self.controller, imovel, proprietarios_disponiveis)

    def abrir_avaliacoes(self, controller, imovel):
        """Abre o popup (Toplevel) de avaliações do imóvel."""
        from tkinter import Toplevel
        from app.views.avaliacao_view import Avaliacao_View
        janela = Toplevel(self.root)
        controller.view = Avaliacao_View(janela, controller, imovel)

    def abrir_despesas(self, controller, imovel):
        """Abre o popup (Toplevel) de despesas do imóvel."""
        from tkinter import Toplevel
        from app.views.despesa_view import Despesa_View
        janela = Toplevel(self.root)
        controller.view = Despesa_View(janela, controller, imovel)

    def abrir_movimentacoes(self, controller, imovel):
        """Abre o popup (Toplevel) de movimentações do imóvel."""
        from tkinter import Toplevel
        from app.views.movimentacao_view import Movimentacao_View
        janela = Toplevel(self.root)
        controller.view = Movimentacao_View(janela, controller, imovel)

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()

    def iniciar(self):
        """Ao abrir a tela, pede ao controller os dados iniciais."""
        self.controller.new()
        self.controller.carregar_estados()
        self.controller.carregar_tipos_imovel()
        self.controller.carregar_status_imovel()
        self.controller.get_all()
