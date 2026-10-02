from app.models.movimentacao import Movimentacao
from app.core.idioma import Idioma


class Movimentacao_Controller:
    """Controller de movimentação: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.imovel_atual = None
        self.movimentacao_selecionada = None

    def carregar_imovel(self, imovel):
        """Guarda o imóvel do popup e lista os lançamentos dele (1:N)."""
        self.imovel_atual = imovel
        self.get_all()

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.movimentacao_selecionada = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            if self.imovel_atual is None:
                self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
                return
            tipo, valor, data_movimentacao, observacao = self.view.ler_dados_movimentacao()
            movimentacao = Movimentacao(
                None, self.imovel_atual, tipo, valor, data_movimentacao, observacao
            )
            self.dao.save(movimentacao)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("movimentacao.salvo_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca as movimentações no DAO e manda a view exibir."""
        if self.imovel_atual is None:
            self.view.exibir_movimentacoes([])
            return
        self.view.exibir_movimentacoes(self.dao.get_by_imovel(self.imovel_atual))

    def selecionar_movimentacao(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_movimentacao = self.view.get_id_selecionado()
            self.movimentacao_selecionada = self.dao.get_by_id(id_movimentacao)
            self.view.preencher_campos(self.movimentacao_selecionada)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza a movimentação selecionada e grava."""
        try:
            if self.movimentacao_selecionada is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            tipo, valor, data_movimentacao, observacao = self.view.ler_dados_movimentacao()
            self.movimentacao_selecionada.atualizar_dados(tipo, valor, data_movimentacao, observacao)
            self.dao.update(self.movimentacao_selecionada)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("movimentacao.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui a movimentação selecionada."""
        if self.movimentacao_selecionada is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            if self.dao.delete(self.movimentacao_selecionada.id):
                self.movimentacao_selecionada = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("movimentacao.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
