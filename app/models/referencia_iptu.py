from app.models.cidade import Cidade
from app.models.tipo_imovel import Tipo_Imovel


class Referencia_Iptu:
    """Model de referência de IPTU: encapsulamento com @property e validação das regras."""

    def __init__(self, id, cidade: Cidade, tipo_imovel: Tipo_Imovel, aliquota):
        """Cria a referência de IPTU; os setters validam cada campo."""
        self._id = id
        self.cidade = cidade
        self.tipo_imovel = tipo_imovel
        self.aliquota = aliquota

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
    def _validar_aliquota(aliquota):
        """Regra de negócio: valida a alíquota (fração)."""
        if aliquota is None or aliquota < 0:
            raise ValueError("referencia_iptu.erro_aliquota_negativa")

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
    def aliquota(self):
        """Encapsulamento: devolve a alíquota (fração)."""
        return self._aliquota

    @aliquota.setter
    def aliquota(self, nova_aliquota):
        """Encapsulamento: valida e altera a alíquota (fração)."""
        self._validar_aliquota(nova_aliquota)
        self._aliquota = nova_aliquota

    def atualizar_dados(self, nova_cidade, novo_tipo_imovel, nova_aliquota):
        """Valida todos os campos antes e só depois altera a referência de IPTU."""
        self._validar_cidade(nova_cidade)
        self._validar_tipo_imovel(novo_tipo_imovel)
        self._validar_aliquota(nova_aliquota)
        self.cidade = nova_cidade
        self.tipo_imovel = novo_tipo_imovel
        self.aliquota = nova_aliquota
