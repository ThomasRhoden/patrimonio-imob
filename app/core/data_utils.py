from datetime import datetime

from app.core.idioma import Idioma


class Data_Utils:
    """Utilitários de data, conversão e formatação usados pelas views."""

    # formato mostrado e digitado nas telas (dia/mês/ano); no banco a data fica como DATE
    FORMATO_DATA = "%d/%m/%Y"

    @staticmethod
    def string_para_data(data):
        """Converte texto DD/MM/AAAA em date."""
        return datetime.strptime(data, Data_Utils.FORMATO_DATA).date()

    @staticmethod
    def data_para_string(data):
        """Converte date em texto DD/MM/AAAA."""
        return data.strftime(Data_Utils.FORMATO_DATA)

    @staticmethod
    def validar_data(data):
        """Diz se o texto é uma data DD/MM/AAAA válida."""
        try:
            datetime.strptime(data, Data_Utils.FORMATO_DATA)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def converter_numero(texto, nome_campo):
        """Converte o texto do campo em número ou lança erro com o nome do campo."""
        try:
            return float(texto)
        except (TypeError, ValueError):
            raise ValueError(f"{nome_campo}: {Idioma.t('comum.erro_numero')}") from None

    @staticmethod
    def converter_inteiro(texto, nome_campo):
        """Converte o texto do campo em inteiro ou lança erro com o nome do campo."""
        try:
            return int(texto)
        except (TypeError, ValueError):
            raise ValueError(f"{nome_campo}: {Idioma.t('comum.erro_inteiro')}") from None

    @staticmethod
    def converter_data(texto, nome_campo):
        """Valida e converte a data do campo ou lança erro com o nome do campo."""
        if not Data_Utils.validar_data(texto):
            raise ValueError(f"{nome_campo}: {Idioma.t('comum.erro_data')}")
        return Data_Utils.string_para_data(texto)

    @staticmethod
    def formatar_moeda(valor):
        """Formata em reais: 1234.5 → R$ 1.234,50."""
        if valor is None:
            valor = 0
        texto = f"{valor:,.2f}"
        texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
        return f"R$ {texto}"

    @staticmethod
    def formatar_area(valor):
        """Formata a área: 70 → 70,00 m²."""
        if valor is None:
            valor = 0
        texto = f"{valor:,.2f}"
        texto = texto.replace(",", "_").replace(".", ",").replace("_", ".")
        return f"{texto} m\u00b2"

    @staticmethod
    def formatar_percentual(valor):
        """Formata o percentual: 0.55 → 0.55%."""
        if valor is None:
            valor = 0
        texto = f"{valor:.2f}".rstrip("0").rstrip(".")
        return f"{texto}%"
