from app.models.proprietario import Proprietario
from app.core.idioma import Idioma


class Proprietario_Controller:
    """Controller de proprietário: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, cidade_dao, estado_dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.cidade_dao = cidade_dao
        self.estado_dao = estado_dao
        self.view = view
        self.proprietario_selecionado = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.proprietario_selecionado = None
        self.view.limpar_campos()

    def carregar_estados(self):
        """Carrega estados do DAO para a Combobox da view."""
        estados = self.estado_dao.get_all()
        self.view.carregar_estados(estados)

    def carregar_cidades_do_estado_selecionado(self, event):
        """Carrega as cidades do estado escolhido (cascata) do DAO para a Combobox da view."""
        id_estado = self.view.get_estado_selecionado_id()
        if id_estado is None:
            self.view.carregar_cidades([])
            return
        cidades = self.cidade_dao.get_by_estado(id_estado)
        self.view.carregar_cidades(cidades)

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            nome, cpf, email, telefone, cidade = self.view.ler_dados_proprietario()
            proprietario = Proprietario(None, nome, cpf, email, telefone, cidade)
            self.dao.save(proprietario)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("proprietario.cadastrado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca os proprietários no DAO e manda a view exibir."""
        proprietarios = self.dao.get_all()
        self.view.exibir_proprietarios(proprietarios)

    def selecionar_proprietario(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_proprietario = self.view.get_id_selecionado()
            self.proprietario_selecionado = self.dao.get_by_id(id_proprietario)
            cidades = []
            if self.proprietario_selecionado.cidade is not None:
                cidades = self.cidade_dao.get_by_estado(
                    self.proprietario_selecionado.cidade.estado.id
                )
            self.view.preencher_campos(self.proprietario_selecionado, cidades)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza o proprietário selecionado e grava."""
        try:
            if self.proprietario_selecionado is None:
                self.view.exibir_mensagem(Idioma.t("proprietario.selecione_da_lista"), False)
                return
            nome, cpf, email, telefone, cidade = self.view.ler_dados_proprietario()
            self.proprietario_selecionado.atualizar_dados(nome, cpf, email, telefone, cidade)
            self.dao.update(self.proprietario_selecionado)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("proprietario.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui o proprietário selecionado."""
        if self.proprietario_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("proprietario.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.proprietario_selecionado.id)
            if sucesso:
                self.proprietario_selecionado = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("proprietario.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
