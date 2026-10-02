from app.core.idioma import Idioma
from app.core.data_utils import Data_Utils

import tkinter as tk
from tkinter import messagebox
from tkinter import ttk


class Referencia_M2_View:
    """View de referência de m²: só monta a tela e repassa os cliques ao controller."""

    def __init__(self, root, controller):
        """Guarda a janela e o controller e monta a tela."""
        self.root = root
        self.controller = controller
        self._cidades = []
        self._tipos_imovel = []
        self.configurar_janela()
        self.criar_componentes()
        self.configurar_treeview()
        self.configurar_eventos()

    def configurar_janela(self):
        """Define o título e o tamanho fixo da janela."""
        self.root.title(Idioma.t("referencia_m2.janela_titulo"))
        self.root.geometry("700x550")
        self.root.resizable(False, False)

    def criar_componentes(self):
        """Monta o formulário, os botões e a Treeview."""
        self.lbl_titulo = tk.Label(
            self.root, text=Idioma.t("referencia_m2.janela_titulo"), font=("Arial", 16, "bold")
        )
        self.lbl_titulo.grid(row=0, column=0, columnspan=2, padx=5, pady=5)

        self.frm_dados = tk.LabelFrame(self.root, text=Idioma.t("referencia.dados_frame"))
        self.frm_dados.grid(row=1, column=0, columnspan=2, padx=10, pady=5, sticky="ew")
        self.frm_dados.grid_columnconfigure(0, weight=0)
        self.frm_dados.grid_columnconfigure(1, weight=1)

        tk.Label(self.frm_dados, text=f"{Idioma.t('comum.id')}:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.txt_id = tk.Entry(self.frm_dados, width=10, state="readonly")
        self.txt_id.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.cidade')}:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.cmb_cidade = ttk.Combobox(self.frm_dados, width=37, state="readonly")
        self.cmb_cidade.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('imovel.tipo')}:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.cmb_tipo = ttk.Combobox(self.frm_dados, width=37, state="readonly")
        self.cmb_tipo.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(self.frm_dados, text=f"{Idioma.t('referencia_m2.valor_m2')}:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        self.txt_valor_m2 = tk.Entry(self.frm_dados, width=20)
        self.txt_valor_m2.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        self.frm_botoes = tk.Frame(self.frm_dados, border=2, relief="groove")
        self.frm_botoes.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

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

        self.tbl_referencias = ttk.Treeview(self.root, height=10)
        self.tbl_referencias.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="nsew")

    def configurar_treeview(self):
        """Define as colunas e larguras da Treeview."""
        self.tbl_referencias["columns"] = ("id", "cidade", "tipo", "valor_m2")
        self.tbl_referencias.column("#0", width=0, stretch=False)
        self.tbl_referencias.column("id", width=10, anchor="center")
        self.tbl_referencias.column("cidade", width=50)
        self.tbl_referencias.column("tipo", width=40)
        self.tbl_referencias.column("valor_m2", width=30, anchor="e")
        self.tbl_referencias.heading("id", text=Idioma.t("comum.id"))
        self.tbl_referencias.heading("cidade", text=Idioma.t("imovel.cidade"))
        self.tbl_referencias.heading("tipo", text=Idioma.t("imovel.tipo"))
        self.tbl_referencias.heading("valor_m2", text=Idioma.t("referencia_m2.valor_m2_coluna"))

    def configurar_eventos(self):
        """Liga os cliques e a seleção da Treeview ao controller."""
        self.btn_novo.config(command=self.controller.new)
        self.btn_salvar.config(command=self.controller.save)
        self.btn_alterar.config(command=self.controller.update)
        self.btn_excluir.config(command=self.controller.delete)
        self.btn_fechar.config(command=self.fechar)
        self.tbl_referencias.bind("<<TreeviewSelect>>", self.controller.selecionar_referencia)
        # recarrega as listas do banco sempre que a combobox é aberta
        self.cmb_cidade.config(postcommand=self.controller.carregar_cidades)
        self.cmb_tipo.config(postcommand=self.controller.carregar_tipos_imovel)

    def carregar_cidades(self, cidades):
        """Preenche a Combobox com cidades."""
        self._cidades = cidades
        valores = [f"{c.id} - {c.nome}/{c.estado.sigla}" for c in cidades]
        selecionado = self.cmb_cidade.get()
        self.cmb_cidade["values"] = valores
        self.cmb_cidade.set(selecionado if selecionado in valores else "")

    def carregar_tipos_imovel(self, tipos):
        """Preenche a Combobox com tipos de imóvel."""
        self._tipos_imovel = tipos
        valores = [f"{t.id} - {t.nome}" for t in tipos]
        selecionado = self.cmb_tipo.get()
        self.cmb_tipo["values"] = valores
        self.cmb_tipo.set(selecionado if selecionado in valores else "")

    def preencher_campos(self, referencia):
        """Preenche o formulário com a referência de m² selecionada."""
        self.limpar_campos()
        self.txt_id.config(state="normal")
        self.txt_id.insert(0, str(referencia.id))
        self.txt_id.config(state="readonly")
        for indice, cidade in enumerate(self._cidades):
            if cidade.id == referencia.cidade.id:
                self.cmb_cidade.current(indice)
                break
        for indice, tipo in enumerate(self._tipos_imovel):
            if tipo.id == referencia.tipo_imovel.id:
                self.cmb_tipo.current(indice)
                break
        self.txt_valor_m2.insert(0, str(referencia.valor_m2))

    def limpar_campos(self):
        """Limpa o formulário."""
        self.txt_id.config(state="normal")
        self.txt_id.delete(0, tk.END)
        self.txt_id.config(state="readonly")
        self.cmb_cidade.set("")
        self.cmb_tipo.set("")
        self.txt_valor_m2.delete(0, tk.END)

    def limpar_treeview(self):
        """Apaga todas as linhas da Treeview."""
        for item in self.tbl_referencias.get_children():
            self.tbl_referencias.delete(item)

    def get_id_selecionado(self):
        """Devolve o ID da linha selecionada na Treeview."""
        item = self.tbl_referencias.selection()[0]
        return self.tbl_referencias.item(item)["values"][0]

    def confirmar_exclusao(self):
        """Pergunta se pode excluir (askyesno)."""
        return messagebox.askyesno(Idioma.t("comum.confirmacao"), Idioma.t("comum.confirmar_exclusao"), parent=self.root)

    def ler_dados_referencia(self):
        """Lê os campos do formulário e devolve ao controller."""
        indice_cidade = self.cmb_cidade.current()
        cidade = self._cidades[indice_cidade] if indice_cidade >= 0 else None
        indice_tipo = self.cmb_tipo.current()
        tipo_imovel = self._tipos_imovel[indice_tipo] if indice_tipo >= 0 else None
        valor_m2 = Data_Utils.converter_numero(self.txt_valor_m2.get(), Idioma.t("referencia_m2.valor_m2"))
        return cidade, tipo_imovel, valor_m2

    def exibir_mensagem(self, mensagem, sucesso=True):
        """Mostra sucesso ou erro em messagebox."""
        if sucesso:
            messagebox.showinfo(Idioma.t("app.nome"), mensagem, parent=self.root)
        else:
            messagebox.showerror(Idioma.t("app.nome"), mensagem, parent=self.root)

    def exibir_referencias(self, referencias):
        """Mostra referências na Treeview."""
        self.limpar_treeview()
        for referencia in referencias:
            self.tbl_referencias.insert(
                "", tk.END,
                values=(
                    referencia.id,
                    f"{referencia.cidade.nome}/{referencia.cidade.estado.sigla}",
                    referencia.tipo_imovel.nome,
                    Data_Utils.formatar_moeda(referencia.valor_m2)
                )
            )

    def fechar(self):
        """Fecha a janela (Toplevel)."""
        self.root.destroy()

    def iniciar(self):
        """Ao abrir a tela, pede ao controller os dados iniciais."""
        self.controller.new()
        self.controller.carregar_cidades()
        self.controller.carregar_tipos_imovel()
        self.controller.get_all()
