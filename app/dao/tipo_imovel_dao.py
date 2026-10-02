from app.dao.dao import DAO
from app.models.tipo_imovel import Tipo_Imovel


class Tipo_Imovel_DAO(DAO):
    """DAO de tipo de imóvel: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database):
        """Recebe o Database (herança do DAO genérico)."""
        super().__init__(database)

    def save(self, tipo_imovel):
        """Grava o tipo de imóvel (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = "INSERT INTO tipo_imovel (NOME) VALUES (%s)"
            cursor.execute(sql, (tipo_imovel.nome,))
            conexao.commit()
            tipo_imovel.id = cursor.lastrowid
            return tipo_imovel
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os tipos de imóvel (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = "SELECT ID, NOME FROM tipo_imovel ORDER BY NOME"
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [Tipo_Imovel(r[0], r[1]) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o tipo de imóvel pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = "SELECT ID, NOME FROM tipo_imovel WHERE ID = %s"
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return Tipo_Imovel(registro[0], registro[1])
        finally:
            self.desconectar(cursor, conexao)

    def update(self, tipo_imovel):
        """Altera o tipo de imóvel no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "UPDATE tipo_imovel SET NOME = %s WHERE ID = %s"
            cursor.execute(sql, (tipo_imovel.nome, tipo_imovel.id))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o tipo de imóvel pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM tipo_imovel WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
