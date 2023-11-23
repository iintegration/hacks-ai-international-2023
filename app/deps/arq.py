import arq
from arq.connections import ArqRedis, RedisSettings

from app.settings import SETTINGS

client: ArqRedis | None = None


async def init_client() -> None:
    global client

    client = await arq.create_pool(RedisSettings.from_dsn(SETTINGS.redis_dsn.unicode_string()))
