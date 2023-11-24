import edgedb

from app.settings import SETTINGS

dsn = SETTINGS.edgedb_dsn.unicode_string() if SETTINGS.edgedb_dsn else None

client = edgedb.create_async_client(dsn=dsn, timeout=60)
