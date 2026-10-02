from app.core.idioma import Idioma
from app.core.senha_utils import Senha_Utils


class Login_Controller:
    """Controller de login: coordena a view e o DAO (MVC)."""

    def __init__(self, usuario_dao, view, ao_autenticar):
        """Guarda os DAOs e a view que este controller coordena."""
        self.usuario_dao = usuario_dao
        self.view = view
        self.ao_autenticar = ao_autenticar

    def autenticar(self):
        """Confere login e senha (hash); se der certo, chama o callback do main."""
        login, senha = self.view.ler_dados_login()

        if not login or not senha:
            self.view.exibir_mensagem(Idioma.t("login.erro_campos_vazios"), False)
            return

        usuario = self.usuario_dao.get_by_login(login.strip())

        if usuario is None or not Senha_Utils.verificar_senha(senha, usuario.senha_hash):
            self.view.exibir_mensagem(Idioma.t("login.erro_credenciais"), False)
            return

        self.ao_autenticar(usuario)
