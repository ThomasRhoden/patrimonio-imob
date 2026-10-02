from app.models.status_imovel import Status_Imovel
from app.core.idioma import Idioma


class Status_Imovel_Controller:
    """Controller de status de imóvel: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.status_selecionado = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.status_selecionado = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            nome = self.view.ler_dados_status_imovel()
            status_imovel = Status_Imovel(None, nome)
            self.dao.save(status_imovel)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("status_imovel.cadastrado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca os status de imóvel no DAO e manda a view exibir."""
        status = self.dao.get_all()
        self.view.exibir_status_imovel(status)

    def selecionar_status(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_status = self.view.get_id_selecionado()
            self.status_selecionado = self.dao.get_by_id(id_status)
            self.view.preencher_campos(self.status_selecionado)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza o status de imóvel selecionado e grava."""
        try:
            if self.status_selecionado is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            nome = self.view.ler_dados_status_imovel()
            self.status_selecionado.atualizar_dados(nome)
            self.dao.update(self.status_selecionado)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("status_imovel.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui o status de imóvel selecionado."""
        if self.status_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.status_selecionado.id)
            if sucesso:
                self.status_selecionado = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("status_imovel.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
