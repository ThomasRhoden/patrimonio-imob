from app.models.imovel import Imovel


class Avaliacao:
    """Model de avaliação: encapsulamento com @property e validação das regras."""

    def __init__(self, id, imovel: Imovel, data_avaliacao, valor_estimado, observacao=None):
        """Cria a avaliação; os setters validam cada campo."""
        self._id = id
        self._imovel = imovel
        self.data_avaliacao = data_avaliacao
        self.valor_estimado = valor_estimado
        self._observacao = observacao

    @staticmethod
    def _validar_data(data):
        """Regra de negócio: valida data."""
        if data is None:
            raise ValueError("comum.erro_data_obrigatoria")

    @staticmethod
    def _validar_valor(valor):
        """Regra de negócio: valida o valor."""
        if valor is None or valor < 0:
            raise ValueError("avaliacao.erro_valor_negativo")

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
    def data_avaliacao(self):
        """Encapsulamento: devolve a data da avaliação."""
        return self._data_avaliacao

    @data_avaliacao.setter
    def data_avaliacao(self, nova_data):
        """Encapsulamento: valida e altera a data da avaliação."""
        self._validar_data(nova_data)
        self._data_avaliacao = nova_data

    @property
    def valor_estimado(self):
        """Encapsulamento: devolve o valor estimado."""
        return self._valor_estimado

    @valor_estimado.setter
    def valor_estimado(self, novo_valor):
        """Encapsulamento: valida e altera o valor estimado."""
        self._validar_valor(novo_valor)
        self._valor_estimado = novo_valor

    @property
    def observacao(self):
        """Encapsulamento: devolve a observação."""
        return self._observacao

    @observacao.setter
    def observacao(self, nova_observacao):
        """Encapsulamento: altera a observação."""
        self._observacao = nova_observacao

    @property
    def valorizacao(self):
        """Encapsulamento: devolve valorizacao."""
        return self._valor_estimado - self._imovel.valor_compra

    def atualizar_dados(self, nova_data_avaliacao, novo_valor_estimado, nova_observacao):
        """Valida todos os campos antes e só depois altera a avaliação."""
        self._validar_data(nova_data_avaliacao)
        self._validar_valor(novo_valor_estimado)
        self.data_avaliacao = nova_data_avaliacao
        self.valor_estimado = novo_valor_estimado
        self.observacao = nova_observacao
