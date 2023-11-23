from typing import cast

import arq
from arq.connections import ArqRedis, RedisSettings

from app.settings import SETTINGS

# TODO: rewrite without globals
client = cast(ArqRedis, None)


async def init_client() -> None:
    # TODO: rewrite without globals
    global client

    client = await arq.create_pool(
        RedisSettings.from_dsn(SETTINGS.redis_dsn.unicode_string())
    )
