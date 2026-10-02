from app.models.avaliacao import Avaliacao
from app.core.idioma import Idioma


class Avaliacao_Controller:
    """Controller de avaliação: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.imovel_atual = None
        self.avaliacao_selecionada = None

    def carregar_imovel(self, imovel):
        """Guarda o imóvel do popup e lista os lançamentos dele (1:N)."""
        self.imovel_atual = imovel
        self.get_all()

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.avaliacao_selecionada = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            if self.imovel_atual is None:
                self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
                return
            data_avaliacao, valor_estimado, observacao = self.view.ler_dados_avaliacao()
            avaliacao = Avaliacao(None, self.imovel_atual, data_avaliacao, valor_estimado, observacao)
            self.dao.save(avaliacao)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("avaliacao.salvo_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca as avaliações no DAO e manda a view exibir."""
        if self.imovel_atual is None:
            self.view.exibir_avaliacoes([])
            return
        self.view.exibir_avaliacoes(self.dao.get_by_imovel(self.imovel_atual))

    def selecionar_avaliacao(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_avaliacao = self.view.get_id_selecionado()
            self.avaliacao_selecionada = self.dao.get_by_id(id_avaliacao)
            self.view.preencher_campos(self.avaliacao_selecionada)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza a avaliação selecionada e grava."""
        try:
            if self.avaliacao_selecionada is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            data_avaliacao, valor_estimado, observacao = self.view.ler_dados_avaliacao()
            self.avaliacao_selecionada.atualizar_dados(data_avaliacao, valor_estimado, observacao)
            self.dao.update(self.avaliacao_selecionada)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("avaliacao.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui a avaliação selecionada."""
        if self.avaliacao_selecionada is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            if self.dao.delete(self.avaliacao_selecionada.id):
                self.avaliacao_selecionada = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("avaliacao.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
