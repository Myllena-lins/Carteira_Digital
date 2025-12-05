from dotenv import load_dotenv
import os

load_dotenv()

class Settings:
    DB_HOST = os.getenv("DB_HOST")
    DB_PORT = os.getenv("DB_PORT")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    DB_NAME = os.getenv("DB_NAME")

    TAXA_SAQUE = float(os.getenv("TAXA_SAQUE_PERCENTUAL"))
    TAXA_CONVERSAO = float(os.getenv("TAXA_CONVERSAO_PERCENTUAL"))
    TAXA_TRANSFERENCIA = float(os.getenv("TAXA_TRANSFERENCIA_PERCENTUAL"))

    PRIVATE_KEY_SIZE = int(os.getenv("PRIVATE_KEY_SIZE"))
    PUBLIC_KEY_SIZE = int(os.getenv("PUBLIC_KEY_SIZE"))

settings = Settings()
