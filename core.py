from starlette.config import Config

config = Config(".env")

POSTGRES_HOST : str = config("POSTGRES_HOST")
POSTGRES_USER : str = config("POSTGRES_USER")
POSTGRES_PASSWORD : str = config("POSTGRES_PASSWORD")
POSTGRES_DB : str = config("POSTGRES_DB")
POSTGRES_PORT: str = config("POSTGRES_PORT", cast=int)

