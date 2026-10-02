class Tipo_Imovel:
    """Model de tipo de imóvel: encapsulamento com @property e validação das regras."""

    def __init__(self, id, nome):
        """Cria o tipo de imóvel; os setters validam cada campo."""
        self._id = id
        self.nome = nome

    @staticmethod
    def _validar_nome(nome):
        """Regra de negócio: valida o nome."""
        if not nome or not nome.strip():
            raise ValueError("comum.erro_nome_obrigatorio")

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

    def atualizar_dados(self, novo_nome):
        """Valida todos os campos antes e só depois altera o tipo de imóvel."""
        self.nome = novo_nome
