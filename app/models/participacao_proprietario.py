from app.models.proprietario import Proprietario


class Participacao_Proprietario:
    """
    Representa uma linha da tabela N:N imovel_proprietario:
    um proprietário associado a um imóvel, com seu percentual
    de participação. Usada dentro de Imovel.proprietarios.
    """

    def __init__(self, proprietario: Proprietario, percentual_participacao):
        """Cria a participação de proprietário; os setters validam cada campo."""
        self._proprietario = proprietario
        self.percentual_participacao = percentual_participacao

    @property
    def proprietario(self):
        """Encapsulamento: devolve o proprietário."""
        return self._proprietario

    @proprietario.setter
    def proprietario(self, novo_proprietario):
        """Encapsulamento: altera o proprietário."""
        self._proprietario = novo_proprietario

    @property
    def percentual_participacao(self):
        """Encapsulamento: devolve o percentual de participação."""
        return self._percentual_participacao

    @percentual_participacao.setter
    def percentual_participacao(self, novo_percentual):
        """Encapsulamento: altera o percentual de participação."""
        if novo_percentual < 0 or novo_percentual > 100:
            raise ValueError("imovel_proprietario.erro_percentual_invalido")
        self._percentual_participacao = novo_percentual
