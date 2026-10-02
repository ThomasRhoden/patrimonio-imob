from app.dao.dao import DAO
from app.models.movimentacao import Movimentacao


class Movimentacao_DAO(DAO):
    """DAO de movimentação: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._imovel_dao = imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em objeto Movimentacao (com o imóvel)."""
        imovel = self._imovel_dao.get_by_id(registro[1])
        return Movimentacao(registro[0], imovel, registro[2], registro[3], registro[4], registro[5])

    def save(self, movimentacao):
        """Grava a movimentação (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO movimentacao
                    (IMOVEL_ID, TIPO, VALOR, DATA_MOVIMENTACAO, OBSERVACAO)
                    VALUES (%s, %s, %s, %s, %s)
                  """
            cursor.execute(sql, (
                movimentacao.imovel.id,
                movimentacao.tipo,
                movimentacao.valor,
                movimentacao.data_movimentacao,
                movimentacao.observacao
            ))
            conexao.commit()
            movimentacao.id = cursor.lastrowid
            return movimentacao
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista as movimentações (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, TIPO, VALOR, DATA_MOVIMENTACAO, OBSERVACAO
                    FROM movimentacao
                    ORDER BY DATA_MOVIMENTACAO DESC
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a movimentação pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, TIPO, VALOR, DATA_MOVIMENTACAO, OBSERVACAO
                    FROM movimentacao
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
        """Lista as movimentações de um imóvel (1:N)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, TIPO, VALOR, DATA_MOVIMENTACAO, OBSERVACAO
                    FROM movimentacao
                    WHERE IMOVEL_ID = %s
                    ORDER BY DATA_MOVIMENTACAO DESC
                  """
            cursor.execute(sql, (imovel.id,))
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def update(self, movimentacao):
        """Altera a movimentação no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE movimentacao
                    SET TIPO = %s, VALOR = %s, DATA_MOVIMENTACAO = %s, OBSERVACAO = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                movimentacao.tipo,
                movimentacao.valor,
                movimentacao.data_movimentacao,
                movimentacao.observacao,
                movimentacao.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui a movimentação pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM movimentacao WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
