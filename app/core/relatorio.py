class Relatorio:
    """Cálculos do dashboard: valor estimado, valorização, IPTU e resumos."""

    @staticmethod
    def calcular_valor_estimado(valor_compra, area_privativa, valor_m2_referencia):
        """Área privativa × m²; sem m² de referência, usa o valor de compra."""
        if not valor_m2_referencia:
            return valor_compra
        return valor_m2_referencia * area_privativa

    @staticmethod
    def calcular_valorizacao(valor_compra, valor_estimado):
        """Valorização = valor estimado − valor de compra."""
        return valor_estimado - valor_compra

    @staticmethod
    def calcular_iptu_estimado(valor_estimado, aliquota):
        """
        Estimativa do IPTU anual de um imóvel.

        Base de cálculo: o valor estimado de mercado que o dashboard já
        calculou (última avaliação; senão área privativa x valor do m²
        da referência; senão valor de compra).

        Alíquota: vem da Referência de IPTU da cidade + tipo do imóvel,
        guardada como FRAÇÃO (0.0055 = 0,55%).

        Fórmula: IPTU estimado = valor estimado x alíquota
        Ex.: R$ 535.000,00 x 0.0055 = R$ 2.942,50

        É só uma aproximação: o IPTU real usa o valor venal da Planta
        Genérica de Valores da prefeitura (normalmente menor que o valor
        de mercado), pode ter faixas progressivas, descontos e isenções.
        """
        # sem referência cadastrada para a cidade + tipo: não estima
        if not aliquota:
            return 0
        return valor_estimado * aliquota

    @staticmethod
    def resumo_geral(imoveis, valores_estimados, iptus_estimados=None):
        """
        imoveis: lista de objetos Imovel (precisam de .id e .valor_compra)
        valores_estimados: dict {imovel_id: valor_estimado}
        iptus_estimados: dict {imovel_id: iptu_estimado} (opcional)
        """
        if iptus_estimados is None:
            iptus_estimados = {}
        quantidade = len(imoveis)
        valor_compra_total = sum(imovel.valor_compra for imovel in imoveis)
        valor_estimado_total = sum(
            valores_estimados.get(imovel.id, imovel.valor_compra)
            for imovel in imoveis
        )
        return {
            "quantidade": quantidade,
            "valor_compra_total": valor_compra_total,
            "valor_estimado_total": valor_estimado_total,
            "valorizacao_total": valor_estimado_total - valor_compra_total,
            "iptu_estimado_total": sum(iptus_estimados.values()),
        }

    @staticmethod
    def resumo_por_agrupamento(imoveis, valores_estimados, chave_agrupamento):
        """
        chave_agrupamento: função que recebe um imóvel e devolve a chave
        do grupo (ex.: lambda imovel: imovel.cidade.nome).
        Usado no resumo por estado (o resumo por cidade vem da view
        VW_PATRIMONIO_POR_CIDADE, lida pelo Imovel_DAO).
        """
        resumo = {}

        for imovel in imoveis:
            chave = chave_agrupamento(imovel)
            valor_estimado = valores_estimados.get(imovel.id, imovel.valor_compra)

            if chave not in resumo:
                resumo[chave] = {
                    "quantidade": 0,
                    "valor_compra_total": 0,
                    "valor_estimado_total": 0,
                }

            resumo[chave]["quantidade"] += 1
            resumo[chave]["valor_compra_total"] += imovel.valor_compra
            resumo[chave]["valor_estimado_total"] += valor_estimado

        for dados in resumo.values():
            dados["valorizacao_total"] = (
                dados["valor_estimado_total"] - dados["valor_compra_total"]
            )

        return resumo

    @staticmethod
    def detalhe_por_imovel(imoveis, valores_estimados, iptus_estimados):
        """
        Monta uma linha por imóvel com valor de compra, valor estimado,
        valorização e IPTU estimado (usado na aba "Por imóvel" do dashboard).
        """
        detalhes = []
        for imovel in imoveis:
            valor_estimado = valores_estimados.get(imovel.id, imovel.valor_compra)
            detalhes.append({
                "imovel": imovel,
                "valor_compra": imovel.valor_compra,
                "valor_estimado": valor_estimado,
                "valorizacao": Relatorio.calcular_valorizacao(imovel.valor_compra, valor_estimado),
                "iptu_estimado": iptus_estimados.get(imovel.id, 0),
            })
        return detalhes
