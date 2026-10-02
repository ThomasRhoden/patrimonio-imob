import mysql.connector
import os
from dotenv import load_dotenv

class Database:
    """Conexão com o MySQL/MariaDB usando os dados do .env."""

    load_dotenv()

    def conectar(self):
        """Abre uma conexão nova com o banco."""
        return mysql.connector.connect(
            host =      os.getenv("DB_HOST"),
            port =      os.getenv("DB_PORT"),
            database =  os.getenv("DB_NAME"),
            user =      os.getenv("DB_USER"),
            password =  os.getenv("DB_PASSWORD")
        )
    def desconectar(self, cursor=None, conexao=None):
        """Fecha o cursor e a conexão, se estiverem abertos."""
        if cursor:
            cursor.close()
        if conexao and conexao.is_connected():
            conexao.close()