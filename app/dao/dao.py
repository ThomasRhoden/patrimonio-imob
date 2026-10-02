from abc import ABC, abstractmethod
class DAO(ABC):
    """DAO genérico (abstração com ABC): cada DAO filho implementa o CRUD (polimorfismo)."""

    def __init__(self, database):
        """Guarda o Database usado por todos os DAOs filhos (herança)."""
        self._database = database

    def conectar(self):
        """Abre a conexão e o cursor; reaproveitado por todos os DAOs."""
        conexao = self._database.conectar()
        cursor = conexao.cursor()
        return conexao, cursor
    
    def desconectar(self, cursor, conexao):
        """Fecha cursor e conexão (chamado no finally)."""
        self._database.desconectar(cursor, conexao)

    @staticmethod
    def traduzir_erro(erro):
        # Converte erros conhecidos do MySQL em ValueError com chave do Idioma,
        # para o controller mostrar uma mensagem amigável na tela.
        """Troca códigos de erro do MySQL por chaves de mensagem amigável."""
        codigo = getattr(erro, "errno", None)
        if codigo in (1451, 1217):
            return ValueError("comum.erro_registro_vinculado")
        if codigo == 1062:
            return ValueError("comum.erro_registro_duplicado")
        if codigo == 1406:
            return ValueError("comum.erro_texto_longo")
        if codigo == 1644:
            # SIGNAL SQLSTATE '45000' da SP_ADICIONAR_PROPRIETARIO
            # (views_procedures.sql): soma dos percentuais passou de 100%
            return ValueError("imovel_proprietario.erro_soma_percentual")
        return erro

    @abstractmethod
    def save(self, objeto):
        """Método abstrato: grava um novo registro (INSERT)."""
        pass

    @abstractmethod
    def get_all(self):
        """Método abstrato: lista todos os registros (SELECT)."""
        pass
    @abstractmethod
    def get_by_id(self, id):
        """Método abstrato: busca um registro pelo id."""
        pass

    @abstractmethod
    def update(self, objeto):
        """Método abstrato: altera um registro (UPDATE)."""
        pass

    @abstractmethod
    def delete(self, id):
        """Método abstrato: exclui um registro pelo id (DELETE)."""
        pass