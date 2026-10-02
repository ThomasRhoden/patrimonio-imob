from app.dao.dao import DAO
from app.models.despesa import Despesa


class Despesa_DAO(DAO):
    """DAO de despesa: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._imovel_dao = imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em objeto Despesa (com o imóvel)."""
        imovel = self._imovel_dao.get_by_id(registro[1])
        return Despesa(registro[0], imovel, registro[2], registro[3], registro[4])

    def save(self, despesa):
        """Grava a despesa (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO despesa
                    (IMOVEL_ID, DESCRICAO, VALOR, DATA_DESPESA)
                    VALUES (%s, %s, %s, %s)
                  """
            cursor.execute(sql, (
                despesa.imovel.id,
                despesa.descricao,
                despesa.valor,
                despesa.data_despesa
            ))
            conexao.commit()
            despesa.id = cursor.lastrowid
            return despesa
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista as despesas (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DESCRICAO, VALOR, DATA_DESPESA
                    FROM despesa
                    ORDER BY DATA_DESPESA DESC
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a despesa pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DESCRICAO, VALOR, DATA_DESPESA
                    FROM despesa
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
        """Lista as despesas de um imóvel (1:N)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, IMOVEL_ID, DESCRICAO, VALOR, DATA_DESPESA
                    FROM despesa
                    WHERE IMOVEL_ID = %s
                    ORDER BY DATA_DESPESA DESC
                  """
            cursor.execute(sql, (imovel.id,))
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def update(self, despesa):
        """Altera a despesa no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE despesa
                    SET DESCRICAO = %s, VALOR = %s, DATA_DESPESA = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                despesa.descricao,
                despesa.valor,
                despesa.data_despesa,
                despesa.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui a despesa pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM despesa WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
