from app.models.cidade import Cidade


class Proprietario:
    """Model de proprietário: encapsulamento com @property e validação das regras."""

    def __init__(self, id, nome, cpf, email, telefone, cidade: Cidade = None):
        """Cria o proprietário; os setters validam cada campo."""
        self._id = id
        self.nome = nome
        self._cpf = cpf
        self._email = email
        self._telefone = telefone
        self._cidade = cidade

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

    @property
    def cpf(self):
        """Encapsulamento: devolve o CPF."""
        return self._cpf

    @cpf.setter
    def cpf(self, novo_cpf):
        """Encapsulamento: altera o CPF."""
        self._cpf = novo_cpf

    @property
    def email(self):
        """Encapsulamento: devolve o e-mail."""
        return self._email

    @email.setter
    def email(self, novo_email):
        """Encapsulamento: altera o e-mail."""
        self._email = novo_email

    @property
    def telefone(self):
        """Encapsulamento: devolve o telefone."""
        return self._telefone

    @telefone.setter
    def telefone(self, novo_telefone):
        """Encapsulamento: altera o telefone."""
        self._telefone = novo_telefone

    @property
    def cidade(self):
        """Encapsulamento: devolve a cidade."""
        return self._cidade

    @cidade.setter
    def cidade(self, nova_cidade):
        """Encapsulamento: altera a cidade."""
        self._cidade = nova_cidade

    def atualizar_dados(self, novo_nome, novo_cpf, novo_email, novo_telefone, nova_cidade):
        """Valida todos os campos antes e só depois altera o proprietário."""
        self.nome = novo_nome
        self._cpf = novo_cpf
        self._email = novo_email
        self._telefone = novo_telefone
        self._cidade = nova_cidade
