from app.models.imovel import Imovel


class Despesa:
    """Model de despesa: encapsulamento com @property e validação das regras."""

    def __init__(self, id, imovel: Imovel, descricao, valor, data_despesa):
        """Cria a despesa; os setters validam cada campo."""
        self._id = id
        self._imovel = imovel
        self.descricao = descricao
        self.valor = valor
        self.data_despesa = data_despesa

    @staticmethod
    def _validar_descricao(descricao):
        """Regra de negócio: valida a descrição."""
        if not descricao or not descricao.strip():
            raise ValueError("despesa.erro_descricao_obrigatoria")

    @staticmethod
    def _validar_valor(valor):
        """Regra de negócio: valida o valor."""
        if valor is None or valor < 0:
            raise ValueError("despesa.erro_valor_negativo")

    @staticmethod
    def _validar_data(data):
        """Regra de negócio: valida data."""
        if data is None:
            raise ValueError("comum.erro_data_obrigatoria")

    @property
    def id(self):
        """Encapsulamento: devolve o ID."""
        return self._id

    @id.setter
    def id(self, novo_id):
        """Encapsulamento: altera o ID."""
        self._id = novo_id

    @property
    def imovel(self):
        """Encapsulamento: devolve o imóvel."""
        return self._imovel

    @imovel.setter
    def imovel(self, novo_imovel):
        """Encapsulamento: altera o imóvel."""
        self._imovel = novo_imovel

    @property
    def descricao(self):
        """Encapsulamento: devolve a descrição."""
        return self._descricao

    @descricao.setter
    def descricao(self, nova_descricao):
        """Encapsulamento: valida e altera a descrição."""
        self._validar_descricao(nova_descricao)
        self._descricao = nova_descricao.strip()

    @property
    def valor(self):
        """Encapsulamento: devolve o valor."""
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        """Encapsulamento: valida e altera o valor."""
        self._validar_valor(novo_valor)
        self._valor = novo_valor

    @property
    def data_despesa(self):
        """Encapsulamento: devolve a data da despesa."""
        return self._data_despesa

    @data_despesa.setter
    def data_despesa(self, nova_data):
        """Encapsulamento: valida e altera a data da despesa."""
        self._validar_data(nova_data)
        self._data_despesa = nova_data

    def atualizar_dados(self, nova_descricao, novo_valor, nova_data_despesa):
        """Valida todos os campos antes e só depois altera a despesa."""
        self._validar_descricao(nova_descricao)
        self._validar_valor(novo_valor)
        self._validar_data(nova_data_despesa)
        self.descricao = nova_descricao
        self.valor = novo_valor
        self.data_despesa = nova_data_despesa
