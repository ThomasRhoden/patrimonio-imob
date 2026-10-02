from app.models.tipo_imovel import Tipo_Imovel
from app.core.idioma import Idioma


class Tipo_Imovel_Controller:
    """Controller de tipo de imóvel: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.tipo_selecionado = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.tipo_selecionado = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            nome = self.view.ler_dados_tipo_imovel()
            tipo_imovel = Tipo_Imovel(None, nome)
            self.dao.save(tipo_imovel)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("tipo_imovel.cadastrado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca os tipos de imóvel no DAO e manda a view exibir."""
        tipos = self.dao.get_all()
        self.view.exibir_tipos_imovel(tipos)

    def selecionar_tipo(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_tipo = self.view.get_id_selecionado()
            self.tipo_selecionado = self.dao.get_by_id(id_tipo)
            self.view.preencher_campos(self.tipo_selecionado)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza o tipo de imóvel selecionado e grava."""
        try:
            if self.tipo_selecionado is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            nome = self.view.ler_dados_tipo_imovel()
            self.tipo_selecionado.atualizar_dados(nome)
            self.dao.update(self.tipo_selecionado)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("tipo_imovel.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui o tipo de imóvel selecionado."""
        if self.tipo_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.tipo_selecionado.id)
            if sucesso:
                self.tipo_selecionado = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("tipo_imovel.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
