from app.dao.dao import DAO
from app.models.imovel import Imovel


class Imovel_DAO(DAO):
    """DAO de imóvel: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, cidade_dao, tipo_imovel_dao, status_imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._cidade_dao = cidade_dao
        self._tipo_imovel_dao = tipo_imovel_dao
        self._status_imovel_dao = status_imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em Imovel, buscando cidade, tipo e status (1:N)."""
        cidade = self._cidade_dao.get_by_id(registro[1])
        tipo_imovel = self._tipo_imovel_dao.get_by_id(registro[2])
        status = self._status_imovel_dao.get_by_id(registro[3])
        return Imovel(
            registro[0],
            cidade,
            tipo_imovel,
            status,
            registro[4],
            registro[5],
            registro[6],
            registro[7],
            registro[8],
            registro[9],
            registro[10],
            registro[11]
        )

    def save(self, imovel):
        """Grava o imóvel (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO imovel
                    (
                        CIDADE_ID, TIPO_IMOVEL_ID, STATUS_ID,
                        AREA_TOTAL, AREA_PRIVATIVA, VALOR_COMPRA, DATA_COMPRA,
                        COMODOS, BANHEIROS, VAGAS_GARAGEM, OBSERVACOES
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  """
            cursor.execute(sql, (
                imovel.cidade.id,
                imovel.tipo_imovel.id,
                imovel.status.id,
                imovel.area_total,
                imovel.area_privativa,
                imovel.valor_compra,
                imovel.data_compra,
                imovel.comodos,
                imovel.banheiros,
                imovel.vagas_garagem,
                imovel.observacoes
            ))
            conexao.commit()
            imovel.id = cursor.lastrowid
            return imovel
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os imóveis (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        ID, CIDADE_ID, TIPO_IMOVEL_ID, STATUS_ID,
                        AREA_TOTAL, AREA_PRIVATIVA, VALOR_COMPRA, DATA_COMPRA,
                        COMODOS, BANHEIROS, VAGAS_GARAGEM, OBSERVACOES
                    FROM imovel
                    ORDER BY ID
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o imóvel pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        ID, CIDADE_ID, TIPO_IMOVEL_ID, STATUS_ID,
                        AREA_TOTAL, AREA_PRIVATIVA, VALOR_COMPRA, DATA_COMPRA,
                        COMODOS, BANHEIROS, VAGAS_GARAGEM, OBSERVACOES
                    FROM imovel
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def update(self, imovel):
        """Altera o imóvel no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE imovel
                    SET
                        CIDADE_ID = %s, TIPO_IMOVEL_ID = %s, STATUS_ID = %s,
                        AREA_TOTAL = %s, AREA_PRIVATIVA = %s, VALOR_COMPRA = %s, DATA_COMPRA = %s,
                        COMODOS = %s, BANHEIROS = %s, VAGAS_GARAGEM = %s, OBSERVACOES = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                imovel.cidade.id,
                imovel.tipo_imovel.id,
                imovel.status.id,
                imovel.area_total,
                imovel.area_privativa,
                imovel.valor_compra,
                imovel.data_compra,
                imovel.comodos,
                imovel.banheiros,
                imovel.vagas_garagem,
                imovel.observacoes,
                imovel.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_patrimonio_por_cidade(self):
        """Lê a view VW_PATRIMONIO_POR_CIDADE (aba Por cidade do dashboard)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        CIDADE, SIGLA, QUANTIDADE,
                        VALOR_COMPRA_TOTAL, VALOR_ESTIMADO_TOTAL, VALORIZACAO_TOTAL
                    FROM VW_PATRIMONIO_POR_CIDADE
                    ORDER BY CIDADE
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()

            resumo = {}
            for registro in registros:
                # nome em maiúsculas, igual ao que o model Cidade mostra
                chave = f"{registro[0].upper()}/{registro[1].upper()}"
                resumo[chave] = {
                    "quantidade": registro[2],
                    "valor_compra_total": registro[3],
                    "valor_estimado_total": registro[4],
                    "valorizacao_total": registro[5],
                }
            return resumo
        finally:
            self.desconectar(cursor, conexao)

    def get_resumo_por_proprietario(self):
        """Lê a view VW_RESUMO_POR_PROPRIETARIO (aba Por proprietário do dashboard)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT
                        PROPRIETARIO, QUANTIDADE, VALOR_COMPRA_PARTE,
                        VALOR_ESTIMADO_PARTE, VALORIZACAO_PARTE, IPTU_PARTE
                    FROM VW_RESUMO_POR_PROPRIETARIO
                    ORDER BY PROPRIETARIO
                  """
            cursor.execute(sql)
            resumo = []
            for registro in cursor.fetchall():
                resumo.append({
                    "proprietario": registro[0].upper(),
                    "quantidade": registro[1],
                    "valor_compra_parte": registro[2],
                    "valor_estimado_parte": registro[3],
                    "valorizacao_parte": registro[4],
                    "iptu_parte": registro[5],
                })
            return resumo
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o imóvel pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM imovel WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
