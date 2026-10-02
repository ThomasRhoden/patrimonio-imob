from app.models.cidade import Cidade
from app.models.tipo_imovel import Tipo_Imovel
from app.models.status_imovel import Status_Imovel


class Imovel:
    """Model de imóvel: @property + regras de área/valor; FKs 1:N e donos N:N."""

    def __init__(
        self,
        id,
        cidade: Cidade,
        tipo_imovel: Tipo_Imovel,
        status: Status_Imovel,
        area_total,
        area_privativa,
        valor_compra,
        data_compra,
        comodos,
        banheiros,
        vagas_garagem,
        observacoes=None,
        proprietarios=None
    ):
        """Cria o imóvel; os setters validam cada campo."""
        self._validar_dados(
            cidade, tipo_imovel, status, area_total, area_privativa,
            valor_compra, data_compra, comodos, banheiros, vagas_garagem
        )

        self._id = id
        self._cidade = cidade
        self._tipo_imovel = tipo_imovel
        self._status = status
        self._area_total = area_total
        self._area_privativa = area_privativa
        self._valor_compra = valor_compra
        self._data_compra = data_compra
        self._comodos = comodos
        self._banheiros = banheiros
        self._vagas_garagem = vagas_garagem
        self._observacoes = observacoes
        self.proprietarios = proprietarios if proprietarios is not None else []

    @staticmethod
    def _validar_dados(
        cidade, tipo_imovel, status, area_total, area_privativa,
        valor_compra, data_compra, comodos, banheiros, vagas_garagem
    ):
        """Regra de negócio: valida dados."""
        if cidade is None:
            raise ValueError("imovel.erro_cidade_obrigatoria")
        if tipo_imovel is None:
            raise ValueError("imovel.erro_tipo_obrigatorio")
        if status is None:
            raise ValueError("imovel.erro_status_obrigatorio")
        Imovel._validar_areas(area_total, area_privativa)
        Imovel._validar_valor_compra(valor_compra)
        if data_compra is None:
            raise ValueError("comum.erro_data_obrigatoria")
        Imovel._validar_quantidade(comodos)
        Imovel._validar_quantidade(banheiros)
        Imovel._validar_quantidade(vagas_garagem)

    @staticmethod
    def _validar_areas(area_total, area_privativa):
        """Regra de negócio: valida areas."""
        if area_total <= 0:
            raise ValueError("imovel.erro_area_total")
        if area_privativa < 0:
            raise ValueError("imovel.erro_area_privativa_negativa")
        if area_privativa > area_total:
            raise ValueError("imovel.erro_area_privativa")

    @staticmethod
    def _validar_valor_compra(valor_compra):
        """Regra de negócio: valida o valor de compra."""
        if valor_compra < 0:
            raise ValueError("imovel.erro_valor_negativo")

    @staticmethod
    def _validar_quantidade(quantidade):
        """Regra de negócio: valida quantidade."""
        if quantidade < 0:
            raise ValueError("imovel.erro_quantidade_negativa")

    @staticmethod
    def validar_percentuais(proprietarios):
        """RN09: a soma dos percentuais dos donos não pode passar de 100%."""
        soma = sum(p.percentual_participacao for p in proprietarios)
        if soma > 100:
            raise ValueError("imovel_proprietario.erro_soma_percentual")

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
        """Encapsulamento: altera a cidade."""
        self._cidade = nova_cidade

    @property
    def tipo_imovel(self):
        """Encapsulamento: devolve o tipo de imóvel."""
        return self._tipo_imovel

    @tipo_imovel.setter
    def tipo_imovel(self, novo_tipo):
        """Encapsulamento: altera o tipo de imóvel."""
        self._tipo_imovel = novo_tipo

    @property
    def status(self):
        """Encapsulamento: devolve o status."""
        return self._status

    @status.setter
    def status(self, novo_status):
        """Encapsulamento: altera o status."""
        self._status = novo_status

    @property
    def area_total(self):
        """Encapsulamento: devolve a área total."""
        return self._area_total

    @area_total.setter
    def area_total(self, nova_area_total):
        """Encapsulamento: valida e altera a área total."""
        self._validar_areas(nova_area_total, self._area_privativa)
        self._area_total = nova_area_total

    @property
    def area_privativa(self):
        """Encapsulamento: devolve a área privativa."""
        return self._area_privativa

    @area_privativa.setter
    def area_privativa(self, nova_area_privativa):
        """Encapsulamento: valida e altera a área privativa."""
        self._validar_areas(self._area_total, nova_area_privativa)
        self._area_privativa = nova_area_privativa

    @property
    def valor_compra(self):
        """Encapsulamento: devolve o valor de compra."""
        return self._valor_compra

    @valor_compra.setter
    def valor_compra(self, novo_valor):
        """Encapsulamento: valida e altera o valor de compra."""
        self._validar_valor_compra(novo_valor)
        self._valor_compra = novo_valor

    @property
    def data_compra(self):
        """Encapsulamento: devolve a data de compra."""
        return self._data_compra

    @data_compra.setter
    def data_compra(self, nova_data):
        """Encapsulamento: altera a data de compra."""
        self._data_compra = nova_data

    @property
    def comodos(self):
        """Encapsulamento: devolve os cômodos."""
        return self._comodos

    @comodos.setter
    def comodos(self, novo_valor):
        """Encapsulamento: valida e altera os cômodos."""
        self._validar_quantidade(novo_valor)
        self._comodos = novo_valor

    @property
    def banheiros(self):
        """Encapsulamento: devolve os banheiros."""
        return self._banheiros

    @banheiros.setter
    def banheiros(self, novo_valor):
        """Encapsulamento: valida e altera os banheiros."""
        self._validar_quantidade(novo_valor)
        self._banheiros = novo_valor

    @property
    def vagas_garagem(self):
        """Encapsulamento: devolve as vagas de garagem."""
        return self._vagas_garagem

    @vagas_garagem.setter
    def vagas_garagem(self, novo_valor):
        """Encapsulamento: valida e altera as vagas de garagem."""
        self._validar_quantidade(novo_valor)
        self._vagas_garagem = novo_valor

    @property
    def observacoes(self):
        """Encapsulamento: devolve as observações."""
        return self._observacoes

    @observacoes.setter
    def observacoes(self, novas_observacoes):
        """Encapsulamento: altera as observações."""
        self._observacoes = novas_observacoes

    @property
    def proprietarios(self):
        """Encapsulamento: devolve a lista de proprietários (N:N)."""
        return self._proprietarios

    @proprietarios.setter
    def proprietarios(self, novos_proprietarios):
        """Encapsulamento: valida e altera a lista de proprietários (N:N)."""
        self.validar_percentuais(novos_proprietarios)
        self._proprietarios = novos_proprietarios

    def atualizar_dados(
        self,
        nova_cidade,
        novo_tipo_imovel,
        novo_status,
        nova_area_total,
        nova_area_privativa,
        novo_valor_compra,
        nova_data_compra,
        novos_comodos,
        novos_banheiros,
        novas_vagas_garagem,
        novas_observacoes
    ):
        """Valida todos os campos antes e só depois altera o imóvel."""
        self._validar_dados(
            nova_cidade, novo_tipo_imovel, novo_status, nova_area_total, nova_area_privativa,
            novo_valor_compra, nova_data_compra, novos_comodos, novos_banheiros, novas_vagas_garagem
        )

        self._cidade = nova_cidade
        self._tipo_imovel = novo_tipo_imovel
        self._status = novo_status
        self._area_total = nova_area_total
        self._area_privativa = nova_area_privativa
        self._valor_compra = novo_valor_compra
        self._data_compra = nova_data_compra
        self._comodos = novos_comodos
        self._banheiros = novos_banheiros
        self._vagas_garagem = novas_vagas_garagem
        self._observacoes = novas_observacoes
