from app.models.despesa import Despesa
from app.core.idioma import Idioma


class Despesa_Controller:
    """Controller de despesa: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.imovel_atual = None
        self.despesa_selecionada = None

    def carregar_imovel(self, imovel):
        """Guarda o imóvel do popup e lista os lançamentos dele (1:N)."""
        self.imovel_atual = imovel
        self.get_all()

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.despesa_selecionada = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            if self.imovel_atual is None:
                self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
                return
            descricao, valor, data_despesa = self.view.ler_dados_despesa()
            despesa = Despesa(None, self.imovel_atual, descricao, valor, data_despesa)
            self.dao.save(despesa)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("despesa.salvo_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca as despesas no DAO e manda a view exibir."""
        if self.imovel_atual is None:
            self.view.exibir_despesas([])
            return
        self.view.exibir_despesas(self.dao.get_by_imovel(self.imovel_atual))

    def selecionar_despesa(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_despesa = self.view.get_id_selecionado()
            self.despesa_selecionada = self.dao.get_by_id(id_despesa)
            self.view.preencher_campos(self.despesa_selecionada)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza a despesa selecionada e grava."""
        try:
            if self.despesa_selecionada is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            descricao, valor, data_despesa = self.view.ler_dados_despesa()
            self.despesa_selecionada.atualizar_dados(descricao, valor, data_despesa)
            self.dao.update(self.despesa_selecionada)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("despesa.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui a despesa selecionada."""
        if self.despesa_selecionada is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            if self.dao.delete(self.despesa_selecionada.id):
                self.despesa_selecionada = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("despesa.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
