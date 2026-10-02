from app.models.estado import Estado


class Cidade:
    """Model de cidade: encapsulamento com @property; pertence a um estado (1:N)."""

    def __init__(self, id, nome, estado: Estado):
        """Cria a cidade; os setters validam cada campo."""
        self._id = id
        self.nome = nome
        self.estado = estado

    @staticmethod
    def _validar_nome(nome):
        """Regra de negócio: valida o nome."""
        if not nome or not nome.strip():
            raise ValueError("comum.erro_nome_obrigatorio")

    @staticmethod
    def _validar_estado(estado):
        """Regra de negócio: valida o estado."""
        if estado is None:
            raise ValueError("cidade.erro_estado_obrigatorio")

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
    def estado(self):
        """Encapsulamento: devolve o estado."""
        return self._estado

    @estado.setter
    def estado(self, novo_estado):
        """Encapsulamento: valida e altera o estado."""
        self._validar_estado(novo_estado)
        self._estado = novo_estado

    def atualizar_dados(self, novo_nome, novo_estado):
        """Valida todos os campos antes e só depois altera a cidade."""
        self._validar_nome(novo_nome)
        self._validar_estado(novo_estado)
        self.nome = novo_nome
        self.estado = novo_estado
