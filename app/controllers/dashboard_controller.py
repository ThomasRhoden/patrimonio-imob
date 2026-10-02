from app.core.relatorio import Relatorio


class Dashboard_Controller:
    """Controller de dashboard: coordena a view e o DAO (MVC)."""

    def __init__(self, imovel_dao, avaliacao_dao, referencia_m2_dao, referencia_iptu_dao, view):
        """Guarda os DAOs e a view que este controller coordena."""
        self.imovel_dao = imovel_dao
        self.avaliacao_dao = avaliacao_dao
        self.referencia_m2_dao = referencia_m2_dao
        self.referencia_iptu_dao = referencia_iptu_dao
        self.view = view

    def _calcular_valores_estimados(self, imoveis):
        """Valor estimado: última avaliação; senão área × m²; senão compra."""
        valores_estimados = {}

        for imovel in imoveis:
            avaliacao = self.avaliacao_dao.get_ultima_por_imovel(imovel)

            if avaliacao is not None:
                valores_estimados[imovel.id] = avaliacao.valor_estimado
                continue

            referencia = self.referencia_m2_dao.get_by_cidade_e_tipo(
                imovel.cidade.id,
                imovel.tipo_imovel.id
            )
            valor_m2 = referencia.valor_m2 if referencia else None

            valores_estimados[imovel.id] = Relatorio.calcular_valor_estimado(
                imovel.valor_compra,
                imovel.area_privativa,
                valor_m2
            )

        return valores_estimados

    def _calcular_iptus_estimados(self, imoveis, valores_estimados):
        """IPTU estimado = valor estimado × alíquota da cidade + tipo."""
        iptus_estimados = {}

        for imovel in imoveis:
            referencia = self.referencia_iptu_dao.get_by_cidade_e_tipo(
                imovel.cidade.id,
                imovel.tipo_imovel.id
            )
            aliquota = referencia.aliquota if referencia else None

            iptus_estimados[imovel.id] = Relatorio.calcular_iptu_estimado(
                valores_estimados[imovel.id],
                aliquota
            )

        return iptus_estimados

    def atualizar(self):
        """Recalcula os totais e resumos e manda a view exibir."""
        imoveis = self.imovel_dao.get_all()
        valores_estimados = self._calcular_valores_estimados(imoveis)
        iptus_estimados = self._calcular_iptus_estimados(imoveis, valores_estimados)

        resumo_geral = Relatorio.resumo_geral(imoveis, valores_estimados, iptus_estimados)

        # o resumo por cidade vem pronto da view VW_PATRIMONIO_POR_CIDADE
        resumo_por_cidade = self.imovel_dao.get_patrimonio_por_cidade()

        resumo_por_estado = Relatorio.resumo_por_agrupamento(
            imoveis,
            valores_estimados,
            lambda imovel: imovel.cidade.estado.nome
        )

        detalhes_por_imovel = Relatorio.detalhe_por_imovel(
            imoveis,
            valores_estimados,
            iptus_estimados
        )

        # parte de cada dono (N:N): vem pronta da view VW_RESUMO_POR_PROPRIETARIO
        resumo_por_proprietario = self.imovel_dao.get_resumo_por_proprietario()

        self.view.exibir_resumo(
            resumo_geral,
            resumo_por_cidade,
            resumo_por_estado,
            detalhes_por_imovel,
            resumo_por_proprietario
        )
