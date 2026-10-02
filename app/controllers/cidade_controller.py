from app.models.cidade import Cidade
from app.core.idioma import Idioma


class Cidade_Controller:
    """Controller de cidade: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, estado_dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.estado_dao = estado_dao
        self.view = view
        self.cidade_selecionada = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.cidade_selecionada = None
        self.view.limpar_campos()

    def carregar_estados(self):
        """Carrega estados do DAO para a Combobox da view."""
        estados = self.estado_dao.get_all()
        self.view.carregar_estados(estados)

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            nome, estado = self.view.ler_dados_cidade()
            cidade = Cidade(None, nome, estado)
            self.dao.save(cidade)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("cidade.cadastrado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca as cidades no DAO e manda a view exibir."""
        cidades = self.dao.get_all()
        self.view.exibir_cidades(cidades)

    def selecionar_cidade(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_cidade = self.view.get_id_selecionado()
            self.cidade_selecionada = self.dao.get_by_id(id_cidade)
            self.view.preencher_campos(self.cidade_selecionada)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza a cidade selecionada e grava."""
        try:
            if self.cidade_selecionada is None:
                self.view.exibir_mensagem(Idioma.t("cidade.selecione_da_lista"), False)
                return
            nome, estado = self.view.ler_dados_cidade()
            self.cidade_selecionada.atualizar_dados(nome, estado)
            self.dao.update(self.cidade_selecionada)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("cidade.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui a cidade selecionada."""
        if self.cidade_selecionada is None:
            self.view.exibir_mensagem(Idioma.t("cidade.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.cidade_selecionada.id)
            if sucesso:
                self.cidade_selecionada = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("cidade.excluido_sucesso"))
            else:
                self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
