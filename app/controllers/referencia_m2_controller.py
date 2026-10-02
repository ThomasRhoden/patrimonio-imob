from app.models.referencia_m2 import Referencia_M2
from app.core.idioma import Idioma


class Referencia_M2_Controller:
    """Controller de referência de m²: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, cidade_dao, tipo_imovel_dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.cidade_dao = cidade_dao
        self.tipo_imovel_dao = tipo_imovel_dao
        self.view = view
        self.referencia_selecionada = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.referencia_selecionada = None
        self.view.limpar_campos()

    def carregar_cidades(self):
        """Carrega cidades do DAO para a Combobox da view."""
        self.view.carregar_cidades(self.cidade_dao.get_all())

    def carregar_tipos_imovel(self):
        """Carrega tipos de imóvel do DAO para a Combobox da view."""
        self.view.carregar_tipos_imovel(self.tipo_imovel_dao.get_all())

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            cidade, tipo_imovel, valor_m2 = self.view.ler_dados_referencia()
            referencia = Referencia_M2(None, cidade, tipo_imovel, valor_m2)
            self.dao.save(referencia)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("referencia_m2.salvo_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca as referências de m² no DAO e manda a view exibir."""
        self.view.exibir_referencias(self.dao.get_all())

    def selecionar_referencia(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_referencia = self.view.get_id_selecionado()
            self.referencia_selecionada = self.dao.get_by_id(id_referencia)
            self.view.preencher_campos(self.referencia_selecionada)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza a referência de m² selecionada e grava."""
        try:
            if self.referencia_selecionada is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            cidade, tipo_imovel, valor_m2 = self.view.ler_dados_referencia()
            self.referencia_selecionada.atualizar_dados(cidade, tipo_imovel, valor_m2)
            self.dao.update(self.referencia_selecionada)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("referencia_m2.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui a referência de m² selecionada."""
        if self.referencia_selecionada is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            if self.dao.delete(self.referencia_selecionada.id):
                self.referencia_selecionada = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("referencia_m2.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
