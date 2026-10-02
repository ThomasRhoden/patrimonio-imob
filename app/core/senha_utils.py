import hashlib
import secrets


class Senha_Utils:
    """Hash de senha com salt (a senha nunca é gravada em texto)."""

    @staticmethod
    def gerar_hash(senha_texto_plano):
        """Gera salt + SHA-256 no formato salt$hash."""
        salt = secrets.token_hex(16)
        hash_senha = hashlib.sha256(
            (salt + senha_texto_plano).encode("utf-8")
        ).hexdigest()
        return f"{salt}${hash_senha}"

    @staticmethod
    def verificar_senha(senha_texto_plano, senha_armazenada):
        """Recalcula o hash com o salt guardado e compara."""
        salt, hash_esperado = senha_armazenada.split("$")
        hash_calculado = hashlib.sha256(
            (salt + senha_texto_plano).encode("utf-8")
        ).hexdigest()
        return hash_calculado == hash_esperado
