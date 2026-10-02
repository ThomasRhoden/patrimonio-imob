from app.dao.dao import DAO
from app.models.referencia_iptu import Referencia_Iptu


class Referencia_Iptu_DAO(DAO):
    """DAO de referência de IPTU: herda do DAO genérico e só tem o SQL da tabela."""

    def __init__(self, database, cidade_dao, tipo_imovel_dao):
        """Recebe o Database e os DAOs das FKs (herança do DAO genérico)."""
        super().__init__(database)
        self._cidade_dao = cidade_dao
        self._tipo_imovel_dao = tipo_imovel_dao

    def _montar(self, registro):
        """Converte uma linha do SELECT em Referencia_Iptu (cidade + tipo)."""
        cidade = self._cidade_dao.get_by_id(registro[1])
        tipo_imovel = self._tipo_imovel_dao.get_by_id(registro[2])
        return Referencia_Iptu(registro[0], cidade, tipo_imovel, registro[3])

    def save(self, referencia):
        """Grava a referência de IPTU (INSERT) e preenche o id gerado."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    INSERT INTO referencia_iptu
                    (CIDADE_ID, TIPO_IMOVEL_ID, ALIQUOTA)
                    VALUES (%s, %s, %s)
                  """
            cursor.execute(sql, (
                referencia.cidade.id,
                referencia.tipo_imovel.id,
                referencia.aliquota
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
        """Lista as referências de IPTU (SELECT) como objetos."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, ALIQUOTA
                    FROM referencia_iptu
                  """
            cursor.execute(sql)
            registros = cursor.fetchall()
            return [self._montar(r) for r in registros]
        finally:
            self.desconectar(cursor, conexao)

    def get_by_id(self, id):
        """Busca a referência de IPTU pelo id (SELECT ... WHERE); None se não achar."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, ALIQUOTA
                    FROM referencia_iptu
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
        """Busca a alíquota da cidade + tipo; None se não houver."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    SELECT ID, CIDADE_ID, TIPO_IMOVEL_ID, ALIQUOTA
                    FROM referencia_iptu
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
        """Altera a referência de IPTU no banco (UPDATE)."""
        conexao, cursor = self.conectar()
        try:
            sql = """
                    UPDATE referencia_iptu
                    SET CIDADE_ID = %s, TIPO_IMOVEL_ID = %s, ALIQUOTA = %s
                    WHERE ID = %s
                  """
            cursor.execute(sql, (
                referencia.cidade.id,
                referencia.tipo_imovel.id,
                referencia.aliquota,
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
        """Exclui a referência de IPTU pelo id (DELETE)."""
        conexao, cursor = self.conectar()
        try:
            sql = "DELETE FROM referencia_iptu WHERE ID = %s"
            cursor.execute(sql, (id,))
            conexao.commit()
            return cursor.rowcount > 0
        except Exception as erro:
            conexao.rollback()
            raise self.traduzir_erro(erro)
        finally:
            self.desconectar(cursor, conexao)
