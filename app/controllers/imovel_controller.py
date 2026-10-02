from app.models.imovel import Imovel
from app.core.idioma import Idioma


class Imovel_Controller:
    """Controller de imóvel: coordena a view e o DAO (MVC)."""

    def __init__(
        self,
        dao,
        cidade_dao,
        estado_dao,
        tipo_imovel_dao,
        status_imovel_dao,
        proprietario_dao,
        participacao_proprietario_dao,
        avaliacao_dao,
        despesa_dao,
        movimentacao_dao,
        view
    ):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.cidade_dao = cidade_dao
        self.estado_dao = estado_dao
        self.tipo_imovel_dao = tipo_imovel_dao
        self.status_imovel_dao = status_imovel_dao
        self.proprietario_dao = proprietario_dao
        self.participacao_proprietario_dao = participacao_proprietario_dao
        self.avaliacao_dao = avaliacao_dao
        self.despesa_dao = despesa_dao
        self.movimentacao_dao = movimentacao_dao
        self.view = view
        self.imovel_selecionado = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.imovel_selecionado = None
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

    def carregar_tipos_imovel(self):
        """Carrega tipos de imóvel do DAO para a Combobox da view."""
        tipos = self.tipo_imovel_dao.get_all()
        self.view.carregar_tipos_imovel(tipos)

    def carregar_status_imovel(self):
        """Carrega status de imóvel do DAO para a Combobox da view."""
        status = self.status_imovel_dao.get_all()
        self.view.carregar_status_imovel(status)

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            (
                cidade, tipo_imovel, status, area_total, area_privativa,
                valor_compra, data_compra, comodos, banheiros, vagas_garagem,
                observacoes
            ) = self.view.ler_dados_imovel()

            imovel = Imovel(
                None, cidade, tipo_imovel, status, area_total, area_privativa,
                valor_compra, data_compra, comodos, banheiros, vagas_garagem,
                observacoes
            )
            self.dao.save(imovel)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("imovel.cadastrado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca os imóveis no DAO e manda a view exibir."""
        imoveis = self.dao.get_all()
        self.view.exibir_imoveis(imoveis)

    def selecionar_imovel(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_imovel = self.view.get_id_selecionado()
            self.imovel_selecionado = self.dao.get_by_id(id_imovel)
            cidades = self.cidade_dao.get_by_estado(
                self.imovel_selecionado.cidade.estado.id
            )
            self.view.preencher_campos(self.imovel_selecionado, cidades)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza o imóvel selecionado e grava."""
        try:
            if self.imovel_selecionado is None:
                self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
                return
            (
                cidade, tipo_imovel, status, area_total, area_privativa,
                valor_compra, data_compra, comodos, banheiros, vagas_garagem,
                observacoes
            ) = self.view.ler_dados_imovel()

            self.imovel_selecionado.atualizar_dados(
                cidade, tipo_imovel, status, area_total, area_privativa,
                valor_compra, data_compra, comodos, banheiros, vagas_garagem,
                observacoes
            )
            self.dao.update(self.imovel_selecionado)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("imovel.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui o imóvel selecionado."""
        if self.imovel_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.imovel_selecionado.id)
            if sucesso:
                self.imovel_selecionado = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("imovel.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)

    # ===========================
    # Popup N:N — Proprietários
    # ===========================

    def abrir_proprietarios(self):
        """Abre o popup (Toplevel) de donos do imóvel selecionado."""
        if self.imovel_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
            return

        proprietarios_disponiveis = self.proprietario_dao.get_all()
        if not proprietarios_disponiveis:
            self.view.exibir_mensagem(Idioma.t("proprietario.selecione_da_lista"), False)
            return

        self.imovel_selecionado.proprietarios = (
            self.participacao_proprietario_dao.get_participacoes_por_imovel(
                self.imovel_selecionado
            )
        )

        self.view.abrir_proprietarios(
            self.imovel_selecionado,
            proprietarios_disponiveis
        )

    def salvar_proprietarios(self, view_proprietarios, imovel, participacoes):
        """O model valida a soma (RN09) e o DAO grava os donos."""
        try:
            # o setter do model valida a RN09 (soma dos percentuais <= 100%)
            imovel.proprietarios = participacoes

            self.participacao_proprietario_dao.substituir_proprietarios_do_imovel(
                imovel,
                imovel.proprietarios
            )
            imovel.proprietarios = (
                self.participacao_proprietario_dao.get_participacoes_por_imovel(imovel)
            )
            view_proprietarios.exibir_mensagem(
                Idioma.t("imovel_proprietario.atualizado_sucesso")
            )
            view_proprietarios.fechar()
        except ValueError as e:
            view_proprietarios.exibir_mensagem(
                f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False
            )

    # ===========================
    # Popups no contexto do imóvel selecionado
    # ===========================

    def abrir_avaliacoes(self):
        """Abre o popup de avaliações do imóvel selecionado."""
        if self.imovel_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
            return
        from app.controllers.avaliacao_controller import Avaliacao_Controller
        controller = Avaliacao_Controller(self.avaliacao_dao, view=None)
        self.view.abrir_avaliacoes(controller, self.imovel_selecionado)

    def abrir_despesas(self):
        """Abre o popup de despesas do imóvel selecionado."""
        if self.imovel_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
            return
        from app.controllers.despesa_controller import Despesa_Controller
        controller = Despesa_Controller(self.despesa_dao, view=None)
        self.view.abrir_despesas(controller, self.imovel_selecionado)

    def abrir_movimentacoes(self):
        """Abre o popup de movimentações do imóvel selecionado."""
        if self.imovel_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("imovel.selecione_da_lista"), False)
            return
        from app.controllers.movimentacao_controller import Movimentacao_Controller
        controller = Movimentacao_Controller(self.movimentacao_dao, view=None)
        self.view.abrir_movimentacoes(controller, self.imovel_selecionado)
