from app.dao.dao import DAO
from app.models.avaliacao import Avaliacao


class Avaliacao_DAO(DAO):
    """DAO de avaliação: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._imovel_dao = imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em objeto Avaliacao (com o imóvel)."""
        imovel = self._imovel_dao.get_by_id(registro[1])
        return Avaliacao(registro[0], imovel, registro[2], registro[3], registro[4])

    def save(self, avaliacao):
        """Grava a avaliação (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO avaliacao
                    (IMOVEL_ID, DATA_AVALIACAO, VALOR_ESTIMADO, OBSERVACAO)
                    VALUES (%s, %s, %s, %s)
                  """
            cursor.execute(sql, (
                avaliacao.imovel.id,
                avaliacao.data_avaliacao,
                avaliacao.valor_estimado,
                avaliacao.observacao
            ))
            conexao.commit()
            avaliacao.id = cursor.lastrowid
            return avaliacao
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista as avaliações (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DATA_AVALIACAO, VALOR_ESTIMADO, OBSERVACAO
                    FROM avaliacao
                    ORDER BY DATA_AVALIACAO DESC
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a avaliação pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DATA_AVALIACAO, VALOR_ESTIMADO, OBSERVACAO
                    FROM avaliacao
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def get_by_imovel(self, imovel):
        """Lista as avaliações de um imóvel (1:N)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DATA_AVALIACAO, VALOR_ESTIMADO, OBSERVACAO
                    FROM avaliacao
                    WHERE IMOVEL_ID = %s
                    ORDER BY DATA_AVALIACAO DESC
                  """
            cursor.execute(sql, (imovel.id,))
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_ultima_por_imovel(self, imovel):
        """Devolve a avaliação mais recente do imóvel (base do valor estimado)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DATA_AVALIACAO, VALOR_ESTIMADO, OBSERVACAO
                    FROM avaliacao
                    WHERE IMOVEL_ID = %s
                    ORDER BY DATA_AVALIACAO DESC, ID DESC
                    LIMIT 1
                  """
            cursor.execute(sql, (imovel.id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def update(self, avaliacao):
        """Altera a avaliação no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE avaliacao
                    SET DATA_AVALIACAO = %s, VALOR_ESTIMADO = %s, OBSERVACAO = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                avaliacao.data_avaliacao,
                avaliacao.valor_estimado,
                avaliacao.observacao,
                avaliacao.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui a avaliação pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM avaliacao WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
