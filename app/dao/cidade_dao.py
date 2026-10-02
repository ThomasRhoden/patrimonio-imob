from app.dao.dao import DAO
from app.models.cidade import Cidade


class Cidade_DAO(DAO):
    """DAO de cidade: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, estado_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._estado_dao = estado_dao

    def save(self, cidade):
        """Grava a cidade (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO cidade
                    (NOME, ESTADO_ID)
                    VALUES (%s, %s)
                  """
            cursor.execute(sql, (cidade.nome, cidade.estado.id))
            conexao.commit()
            cidade.id = cursor.lastrowid
            return cidade
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista as cidades (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, ESTADO_ID
                    FROM cidade
                    ORDER BY NOME
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            cidades = []
            for r in registros:
                estado = self._estado_dao.get_by_id(r[2])
                cidades.append(Cidade(r[0], r[1], estado))
            return cidades
        finally:
            self.desconectar(cursor, conexao)

    def get_by_estado(self, id_estado):
        """Lista só as cidades de um estado (cascata estado → cidade)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, ESTADO_ID
                    FROM cidade
                    WHERE ESTADO_ID = %s
                    ORDER BY NOME
                  """
            cursor.execute(sql, (id_estado,))
            registros = cursor.fetchall()
            cidades = []
            for r in registros:
                estado = self._estado_dao.get_by_id(r[2])
                cidades.append(Cidade(r[0], r[1], estado))
            return cidades
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a cidade pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, ESTADO_ID
                    FROM cidade
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            estado = self._estado_dao.get_by_id(registro[2])
            return Cidade(registro[0], registro[1], estado)
        finally:
            self.desconectar(cursor, conexao)

    def update(self, cidade):
        """Altera a cidade no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE cidade
                    SET NOME = %s, ESTADO_ID = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (cidade.nome, cidade.estado.id, cidade.id))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui a cidade pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM cidade WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
