from app.dao.dao import DAO
from app.models.proprietario import Proprietario


class Proprietario_DAO(DAO):
    """DAO de proprietário: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, cidade_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._cidade_dao = cidade_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em objeto Proprietario (com a cidade)."""
        cidade = None
        if registro[5] is not None:
            cidade = self._cidade_dao.get_by_id(registro[5])
        return Proprietario(registro[0], registro[1], registro[2], registro[3], registro[4], cidade)

    def save(self, proprietario):
        """Grava o proprietário (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO proprietario
                    (NOME, CPF, EMAIL, TELEFONE, CIDADE_ID)
                    VALUES (%s, %s, %s, %s, %s)
                  """
            cidade_id = proprietario.cidade.id if proprietario.cidade else None
            cursor.execute(sql, (
                proprietario.nome,
                proprietario.cpf,
                proprietario.email,
                proprietario.telefone,
                cidade_id
            ))
            conexao.commit()
            proprietario.id = cursor.lastrowid
            return proprietario
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os proprietários (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, CPF, EMAIL, TELEFONE, CIDADE_ID
                    FROM proprietario
                    ORDER BY NOME
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o proprietário pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, CPF, EMAIL, TELEFONE, CIDADE_ID
                    FROM proprietario
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def update(self, proprietario):
        """Altera o proprietário no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE proprietario
                    SET NOME = %s, CPF = %s, EMAIL = %s, TELEFONE = %s, CIDADE_ID = %s
                    WHERE ID = %s
                  """
            cidade_id = proprietario.cidade.id if proprietario.cidade else None
            cursor.execute(sql, (
                proprietario.nome,
                proprietario.cpf,
                proprietario.email,
                proprietario.telefone,
                cidade_id,
                proprietario.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o proprietário pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM proprietario WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
