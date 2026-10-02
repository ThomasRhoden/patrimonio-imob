from app.dao.dao import DAO
from app.models.referencia_m2 import Referencia_M2


class Referencia_M2_DAO(DAO):
    """DAO de referência de m²: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, cidade_dao, tipo_imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._cidade_dao = cidade_dao
        self._tipo_imovel_dao = tipo_imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em Referencia_M2 (cidade + tipo)."""
        cidade = self._cidade_dao.get_by_id(registro[1])
        tipo_imovel = self._tipo_imovel_dao.get_by_id(registro[2])
        return Referencia_M2(registro[0], cidade, tipo_imovel, registro[3])

    def save(self, referencia):
        """Grava a referência de m² (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO referencia_m2
                    (CIDADE_ID, TIPO_IMOVEL_ID, VALOR_M2)
                    VALUES (%s, %s, %s)
                  """
            cursor.execute(sql, (
                referencia.cidade.id,
                referencia.tipo_imovel.id,
                referencia.valor_m2
            ))
            conexao.commit()
            referencia.id = cursor.lastrowid
            return referencia
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def get_all(self):
        """Lista as referências de m² (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, VALOR_M2
                    FROM referencia_m2
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a referência de m² pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, VALOR_M2
                    FROM referencia_m2
                    WHERE ID = %s
                  """
            cursor.execute(sql, (id,))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def get_by_cidade_e_tipo(self, id_cidade, id_tipo_imovel):
        """Busca o valor do m² da cidade + tipo; None se não houver."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, VALOR_M2
                    FROM referencia_m2
                    WHERE CIDADE_ID = %s AND TIPO_IMOVEL_ID = %s
                  """
            cursor.execute(sql, (id_cidade, id_tipo_imovel))
            registro = cursor.fetchone()
            if registro is None:
                return None
            return self._montar(registro)
        finally:
            self.desconectar(cursor, conexao)

    def update(self, referencia):
        """Altera a referência de m² no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE referencia_m2
                    SET CIDADE_ID = %s, TIPO_IMOVEL_ID = %s, VALOR_M2 = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                referencia.cidade.id,
                referencia.tipo_imovel.id,
                referencia.valor_m2,
                referencia.id
            ))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)

    def delete(self, id):
        """Exclui a referência de m² pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM referencia_m2 WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
