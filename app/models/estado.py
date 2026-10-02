class Estado:
    """Model de estado: encapsulamento com @property e validação das regras."""

    def __init__(self, id, nome, sigla):
        """Cria o estado; os setters validam cada campo."""
        self._id = id
        self.nome = nome
        self.sigla = sigla

    @staticmethod
    def _validar_nome(nome):
        """Regra de negócio: valida o nome."""
        if not nome or not nome.strip():
            raise ValueError("comum.erro_nome_obrigatorio")

    @staticmethod
    def _validar_sigla(sigla):
        """Regra de negócio: valida a sigla."""
        if not sigla or len(sigla.strip()) != 2:
            raise ValueError("estado.erro_sigla_tamanho")

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
        return self._nome.upper()

    @nome.setter
    def nome(self, novo_nome):
        """Encapsulamento: valida e altera o nome."""
        self._validar_nome(novo_nome)
        self._nome = novo_nome.strip()

    @property
    def sigla(self):
        """Encapsulamento: devolve a sigla."""
        return self._sigla.upper()

    @sigla.setter
    def sigla(self, nova_sigla):
        """Encapsulamento: valida e altera a sigla."""
        self._validar_sigla(nova_sigla)
        self._sigla = nova_sigla.strip().upper()

    def atualizar_dados(self, novo_nome, nova_sigla):
        """Valida todos os campos antes e só depois altera o estado."""
        self._validar_nome(novo_nome)
        self._validar_sigla(nova_sigla)
        self.nome = novo_nome
        self.sigla = nova_sigla
