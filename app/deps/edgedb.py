import edgedb

from app.settings import SETTINGS

client = edgedb.create_async_client(dsn=SETTINGS.edgedb_dsn)
