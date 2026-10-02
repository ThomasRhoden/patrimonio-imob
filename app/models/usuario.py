class Usuario:
    """Model de usuário: encapsulamento com @property e validação das regras."""

    # conta de acesso ao sistema (login + senha); não há tipos de usuário

    def __init__(self, id, nome, login, senha_hash):
        """Cria o usuário; os setters validam cada campo."""
        self._id = id
        self.nome = nome
        self.login = login
        self.senha_hash = senha_hash

    @staticmethod
    def _validar_nome(nome):
        """Regra de negócio: valida o nome."""
        if not nome or not nome.strip():
            raise ValueError("comum.erro_nome_obrigatorio")

    @staticmethod
    def _validar_login(login):
        # obrigatório, sem espaços e com até 50 caracteres (ex.: admin, thomas)
        """Regra de negócio: valida o login."""
        if not login or not login.strip() or " " in login.strip() or len(login.strip()) > 50:
            raise ValueError("usuario.erro_login_invalido")

    @staticmethod
    def validar_senha(senha_texto_plano):
        """Regra: a senha em texto não pode ficar vazia."""
        if not senha_texto_plano:
            raise ValueError("usuario.erro_senha_obrigatoria")

    @property
    def id(self):
        """Encapsulamento: devolve o ID."""
        return self._id

    @id.setter
    def id(self, novo_id):
        """Encapsulamento: altera o ID."""
        self._id = novo_id

    @property
    def nome(self):
        """Encapsulamento: devolve o nome."""
        return self._nome

    @nome.setter
    def nome(self, novo_nome):
        """Encapsulamento: valida e altera o nome."""
        self._validar_nome(novo_nome)
        self._nome = novo_nome.strip()

    @property
    def login(self):
        """Encapsulamento: devolve o login."""
        return self._login

    @login.setter
    def login(self, novo_login):
        """Encapsulamento: valida e altera o login."""
        self._validar_login(novo_login)
        self._login = novo_login.strip()

    @property
    def senha_hash(self):
        """Encapsulamento: devolve o hash da senha."""
        return self._senha_hash

    @senha_hash.setter
    def senha_hash(self, novo_hash):
        """Encapsulamento: valida e altera o hash da senha."""
        self.validar_senha(novo_hash)
        self._senha_hash = novo_hash

    def atualizar_dados(self, novo_nome, novo_login):
        """Valida todos os campos antes e só depois altera o usuário."""
        self._validar_nome(novo_nome)
        self._validar_login(novo_login)
        self.nome = novo_nome
        self.login = novo_login
