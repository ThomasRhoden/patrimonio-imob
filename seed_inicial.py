from getpass import getpass

from app.core.database import Database
from app.core.senha_utils import Senha_Utils
from app.dao.usuario_dao import Usuario_DAO
from app.models.usuario import Usuario


LOGIN_SUGERIDO = "admin"
NOME_INICIAL = "Usuário inicial"


def ler_login():
    """Pede o login (Enter = admin); sem espaços e até 50 caracteres."""
    while True:
        login = input(f"Login do primeiro acesso [{LOGIN_SUGERIDO}]: ").strip() or LOGIN_SUGERIDO
        if " " in login or len(login) > 50:
            print("O login não pode ter espaços nem passar de 50 caracteres.")
            continue
        return login


def ler_senha():
    """Pede a senha duas vezes (getpass) até as duas conferirem."""
    while True:
        senha = getpass("Digite a senha: ")
        if not senha:
            print("A senha não pode ficar em branco.")
            continue
        confirmacao = getpass("Confirme a senha: ")
        if senha != confirmacao:
            print("As senhas não conferem. Tente novamente.")
            continue
        return senha


def criar_primeiro_acesso():
    """Cria o primeiro usuário com a senha em hash, se o login ainda não existir."""
    database = Database()
    dao = Usuario_DAO(database)

    login = ler_login()
    if dao.get_by_login(login) is not None:
        print(f"O login {login} já existe. Nada a fazer.")
        return

    senha = ler_senha()

    usuario = Usuario(None, NOME_INICIAL, login, Senha_Utils.gerar_hash(senha))
    dao.save(usuario)
    print("Acesso criado com sucesso!")
    print(f"  Login: {login}")
    print("  Senha: a que você acabou de digitar")


if __name__ == "__main__":
    criar_primeiro_acesso()
