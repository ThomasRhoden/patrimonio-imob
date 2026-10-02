from app.dao.dao import DAO
from app.models.participacao_proprietario import Participacao_Proprietario


class Participacao_Proprietario_DAO:
    """DAO da N:N imovel_proprietario (classe associativa); só SQL, sem CRUD genérico."""

    def __init__(self, database, proprietario_dao):
        """Recebe o Database e o DAO de proprietários (para montar os objetos)."""
        self._database = database
        self._proprietario_dao = proprietario_dao

    def get_participacoes_por_imovel(self, imovel):
        """Lista os donos de um imóvel com o percentual de cada um."""
        conexao = self._database.conectar()
        cursor = conexao.cursor()

        try:
            sql = """
                    SELECT
                        PROPRIETARIO_ID,
                        PERCENTUAL_PARTICIPACAO
                    FROM
                        imovel_proprietario
                    WHERE
                        IMOVEL_ID = %s
                  """
            cursor.execute(sql, (imovel.id,))
            registros = cursor.fetchall()

            participacoes = []
            for registro in registros:
                proprietario = self._proprietario_dao.get_by_id(registro[0])
                participacoes.append(
                    Participacao_Proprietario(proprietario, float(registro[1]))
                )

            return participacoes

        finally:
            self._database.desconectar(cursor, conexao)

    def substituir_proprietarios_do_imovel(self, imovel, participacoes):
        """Apaga os vínculos e grava cada dono com CALL SP_ADICIONAR_PROPRIETARIO."""
        conexao = self._database.conectar()
        cursor = conexao.cursor()

        try:
            cursor.execute(
                "DELETE FROM imovel_proprietario WHERE IMOVEL_ID = %s",
                (imovel.id,)
            )

            # cada vínculo passa pela procedure, que confere no banco
            # se a soma dos percentuais não passa de 100%
            for participacao in participacoes:
                cursor.execute(
                    "CALL SP_ADICIONAR_PROPRIETARIO(%s, %s, %s)",
                    (
                        imovel.id,
                        participacao.proprietario.id,
                        participacao.percentual_participacao
                    )
                )

            conexao.commit()

        except Exception as erro:
            conexao.rollback()
            raise DAO.traduzir_erro(erro)

        finally:
            self._database.desconectar(cursor, conexao)
