from app.dao.dao import DAO
from app.models.estado import Estado


class Estado_DAO(DAO):
    """DAO de estado: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database):
        """Recebe o Database (herança do DAO genérico)."""
        super().__init__(database)

    def save(self, estado):
        """Grava o estado (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO estado
                    (NOME, SIGLA)
                    VALUES (%s, %s)
                  """
            cursor.execute(sql, (estado.nome, estado.sigla))
            conexao.commit()
            estado.id = cursor.lastrowid
            return estado
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os estados (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, SIGLA
                    FROM estado
                    ORDER BY NOME
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [Estado(r[0], r[1], r[2]) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o estado pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, SIGLA
                    FROM estado
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return Estado(registro[0], registro[1], registro[2])
        finally:
            self.desconectar(cursor, conexao)

    def update(self, estado):
        """Altera o estado no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE estado
                    SET NOME = %s, SIGLA = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (estado.nome, estado.sigla, estado.id))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o estado pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM estado WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
