from app.models.usuario import Usuario
from app.core.senha_utils import Senha_Utils
from app.core.idioma import Idioma


class Usuario_Controller:
    """Controller de usuário: coordena a view e o DAO (MVC)."""

    def __init__(self, dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.dao = dao
        self.view = view
        self.usuario_selecionado = None
        self.usuario_logado = None

    def new(self):
        """Botão Novo: limpa a seleção e o formulário."""
        self.usuario_selecionado = None
        self.view.limpar_campos()

    def save(self):
        """Botão Salvar: o model valida, o DAO grava e a view mostra a mensagem."""
        try:
            login, nome, senha = self.view.ler_dados_usuario()
            Usuario.validar_senha(senha)
            usuario = Usuario(None, nome, login, Senha_Utils.gerar_hash(senha))
            self.dao.save(usuario)
            self.new()
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("usuario.salvo_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def get_all(self):
        """Busca os usuários no DAO e manda a view exibir."""
        usuarios = self.dao.get_all()
        self.view.exibir_usuarios(usuarios)

    def selecionar_usuario(self, event):
        """Clique na Treeview: carrega o registro e preenche o formulário."""
        try:
            id_usuario = self.view.get_id_selecionado()
            self.usuario_selecionado = self.dao.get_by_id(id_usuario)
            self.view.preencher_campos(self.usuario_selecionado)
        except IndexError:
            pass

    def update(self):
        """Botão Alterar: atualiza o usuário selecionado e grava."""
        try:
            if self.usuario_selecionado is None:
                self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
                return
            login, nome, nova_senha = self.view.ler_dados_usuario()
            self.usuario_selecionado.atualizar_dados(nome, login)
            self.dao.update(self.usuario_selecionado)
            if nova_senha:
                novo_hash = Senha_Utils.gerar_hash(nova_senha)
                self.dao.atualizar_senha(self.usuario_selecionado, novo_hash)
            self.get_all()
            self.view.exibir_mensagem(Idioma.t("usuario.atualizado_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)

    def delete(self):
        """Botão Excluir: confirma e exclui o usuário selecionado."""
        if self.usuario_selecionado is None:
            self.view.exibir_mensagem(Idioma.t("comum.selecione_da_lista"), False)
            return
        # não deixa excluir a própria conta (assim sempre sobra um acesso)
        if self.usuario_logado is not None and self.usuario_selecionado.id == self.usuario_logado.id:
            self.view.exibir_mensagem(Idioma.t("usuario.erro_excluir_logado"), False)
            return
        if not self.view.confirmar_exclusao():
            return
        try:
            sucesso = self.dao.delete(self.usuario_selecionado.id)
            if sucesso:
                self.usuario_selecionado = None
                self.view.limpar_campos()
                self.get_all()
                self.view.exibir_mensagem(Idioma.t("usuario.excluido_sucesso"))
        except ValueError as e:
            self.view.exibir_mensagem(f"{Idioma.t('comum.erro_prefixo')}{Idioma.t(str(e))}", False)
        except Exception:
            self.view.exibir_mensagem(Idioma.t("comum.erro_inesperado"), False)
