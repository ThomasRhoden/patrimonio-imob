from app.models.imovel import Imovel


class Movimentacao:
    """Model de movimentação: encapsulamento com @property e validação das regras."""

    TIPOS = ("entrada_aluguel", "saida_manutencao", "outro")

    def __init__(self, id, imovel: Imovel, tipo, valor, data_movimentacao, observacao=None):
        """Cria a movimentação; os setters validam cada campo."""
        self._id = id
        self._imovel = imovel
        self.tipo = tipo
        self._valor = valor
        self.data_movimentacao = data_movimentacao
        self._observacao = observacao

    @staticmethod
    def _validar_tipo(tipo):
        """Regra de negócio: valida o tipo."""
        if not tipo or not tipo.strip():
            raise ValueError("movimentacao.erro_tipo_obrigatorio")

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
    def tipo(self):
        """Encapsulamento: devolve o tipo."""
        return self._tipo

    @tipo.setter
    def tipo(self, novo_tipo):
        """Encapsulamento: valida e altera o tipo."""
        self._validar_tipo(novo_tipo)
        self._tipo = novo_tipo

    @property
    def valor(self):
        """Encapsulamento: devolve o valor."""
        return self._valor

    @valor.setter
    def valor(self, novo_valor):
        """Encapsulamento: altera o valor."""
        self._valor = novo_valor

    @property
    def data_movimentacao(self):
        """Encapsulamento: devolve a data da movimentação."""
        return self._data_movimentacao

    @data_movimentacao.setter
    def data_movimentacao(self, nova_data):
        """Encapsulamento: valida e altera a data da movimentação."""
        self._validar_data(nova_data)
        self._data_movimentacao = nova_data

    @property
    def observacao(self):
        """Encapsulamento: devolve a observação."""
        return self._observacao

    @observacao.setter
    def observacao(self, nova_observacao):
        """Encapsulamento: altera a observação."""
        self._observacao = nova_observacao

    def atualizar_dados(self, novo_tipo, novo_valor, nova_data_movimentacao, nova_observacao):
        """Valida todos os campos antes e só depois altera a movimentação."""
        self._validar_tipo(novo_tipo)
        self._validar_data(nova_data_movimentacao)
        self.tipo = novo_tipo
        self.valor = novo_valor
        self.data_movimentacao = nova_data_movimentacao
        self.observacao = nova_observacao
