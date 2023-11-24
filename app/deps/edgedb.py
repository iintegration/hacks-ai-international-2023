import edgedb

from app.settings import SETTINGS

if SETTINGS.edgedb_dsn:
    dsn = SETTINGS.edgedb_dsn.unicode_string()
else:
    dsn = None

client = edgedb.create_async_client(dsn=dsn)
