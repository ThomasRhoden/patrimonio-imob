from app.models.cidade import Cidade
from app.models.tipo_imovel import Tipo_Imovel


class Referencia_M2:
    """Model de referência de m²: encapsulamento com @property e validação das regras."""

    def __init__(self, id, cidade: Cidade, tipo_imovel: Tipo_Imovel, valor_m2):
        """Cria a referência de m²; os setters validam cada campo."""
        self._id = id
        self.cidade = cidade
        self.tipo_imovel = tipo_imovel
        self.valor_m2 = valor_m2

    @staticmethod
    def _validar_cidade(cidade):
        """Regra de negócio: valida a cidade."""
        if cidade is None:
            raise ValueError("imovel.erro_cidade_obrigatoria")

    @staticmethod
    def _validar_tipo_imovel(tipo_imovel):
        """Regra de negócio: valida o tipo de imóvel."""
        if tipo_imovel is None:
            raise ValueError("imovel.erro_tipo_obrigatorio")

    @staticmethod
    def _validar_valor_m2(valor_m2):
        """Regra de negócio: valida o valor do m²."""
        if valor_m2 is None or valor_m2 < 0:
            raise ValueError("referencia_m2.erro_valor_negativo")

    @property
    def id(self):
        """Encapsulamento: devolve o ID."""
        return self._id

    @id.setter
    def id(self, novo_id):
        """Encapsulamento: altera o ID."""
        self._id = novo_id

    @property
    def cidade(self):
        """Encapsulamento: devolve a cidade."""
        return self._cidade

    @cidade.setter
    def cidade(self, nova_cidade):
        """Encapsulamento: valida e altera a cidade."""
        self._validar_cidade(nova_cidade)
        self._cidade = nova_cidade

    @property
    def tipo_imovel(self):
        """Encapsulamento: devolve o tipo de imóvel."""
        return self._tipo_imovel

    @tipo_imovel.setter
    def tipo_imovel(self, novo_tipo):
        """Encapsulamento: valida e altera o tipo de imóvel."""
        self._validar_tipo_imovel(novo_tipo)
        self._tipo_imovel = novo_tipo

    @property
    def valor_m2(self):
        """Encapsulamento: devolve o valor do m²."""
        return self._valor_m2

    @valor_m2.setter
    def valor_m2(self, novo_valor):
        """Encapsulamento: valida e altera o valor do m²."""
        self._validar_valor_m2(novo_valor)
        self._valor_m2 = novo_valor

    def atualizar_dados(self, nova_cidade, novo_tipo_imovel, novo_valor_m2):
        """Valida todos os campos antes e só depois altera a referência de m²."""
        self._validar_cidade(nova_cidade)
        self._validar_tipo_imovel(novo_tipo_imovel)
        self._validar_valor_m2(novo_valor_m2)
        self.cidade = nova_cidade
        self.tipo_imovel = novo_tipo_imovel
        self.valor_m2 = novo_valor_m2
