from app.dao.dao import DAO
from app.models.usuario import Usuario


class Usuario_DAO(DAO):
    """DAO de usuário: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database):
        """Recebe o Database (herança do DAO genérico)."""
        super().__init__(database)

    def save(self, usuario):
        """Grava o usuário (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO usuario
                    (NOME, LOGIN, SENHA_HASH)
                    VALUES (%s, %s, %s)
                  """
            cursor.execute(sql, (
                usuario.nome,
                usuario.login,
                usuario.senha_hash
            ))
            conexao.commit()
            usuario.id = cursor.lastrowid
            return usuario
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista os usuários (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, LOGIN, SENHA_HASH
                    FROM usuario
                    ORDER BY NOME
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [Usuario(r[0], r[1], r[2], r[3]) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca o usuário pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, LOGIN, SENHA_HASH
                    FROM usuario
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return Usuario(registro[0], registro[1], registro[2], registro[3])
        finally:
            self.desconectar(cursor, conexao)

    def get_by_login(self, login):
        """Busca o usuário pelo login (usado no login e no seed)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, NOME, LOGIN, SENHA_HASH
                    FROM usuario
                    WHERE LOGIN = %s
                  """
            cursor.execute(sql, (login,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return Usuario(registro[0], registro[1], registro[2], registro[3])
        finally:
            self.desconectar(cursor, conexao)

    def update(self, usuario):
        """Altera o usuário no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE usuario
                    SET NOME = %s, LOGIN = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                usuario.nome,
                usuario.login,
                usuario.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def atualizar_senha(self, usuario, novo_senha_hash):
        """Grava só o novo hash da senha (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "UPDATE usuario SET SENHA_HASH = %s WHERE ID = %s"
            cursor.execute(sql, (novo_senha_hash, usuario.id))
            conexao.commit()
            usuario.senha_hash = novo_senha_hash
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui o usuário pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM usuario WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
