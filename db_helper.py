import core
import psycopg_pool

conn_string = f'host={core.POSTGRES_HOST} user={core.POSTGRES_USER} password={core.POSTGRES_PASSWORD} dbname={core.POSTGRES_DB} port={core.POSTGRES_PORT}'

class DBConnectionPool:
    def __init__(self):
        self.psyco_async_pool : psycopg_pool.AsyncConnectionPool = psycopg_pool.AsyncConnectionPool(
            conn_string,
            min_size = 2,
            max_size = 5
        )

    async def close(self):
        await self.psyco_async_pool.close()



