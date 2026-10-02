from app.dao.dao import DAO
from app.models.status_imovel import Status_Imovel


class Status_Imovel_DAO(DAO):
    """DAO de status de imóvel: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database):
        """Recebe o Database (herança do DAO genérico)."""
        super().__init__(database)

    def save(self, status_imovel):
        """Grava o status de imóvel (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = "INSERT INTO status_imovel (NOME) VALUES (%s)"
            cursor.execute(sql, (status_imovel.nome,))
            conexao.commit()
            status_imovel.id = cursor.lastrowid
            return status_imovel
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os status de imóvel (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = "SELECT ID, NOME FROM status_imovel ORDER BY NOME"
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [Status_Imovel(r[0], r[1]) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o status de imóvel pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = "SELECT ID, NOME FROM status_imovel WHERE ID = %s"
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return Status_Imovel(registro[0], registro[1])
        finally:
            self.desconectar(cursor, conexao)

    def update(self, status_imovel):
        """Altera o status de imóvel no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "UPDATE status_imovel SET NOME = %s WHERE ID = %s"
            cursor.execute(sql, (status_imovel.nome, status_imovel.id))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o status de imóvel pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM status_imovel WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
