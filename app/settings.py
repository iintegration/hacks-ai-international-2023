from pydantic import AnyUrl, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    edgedb_dsn: AnyUrl | None = None
    redis_dsn: RedisDsn
    s3_host: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str
    s3_public_host: str


SETTINGS = Settings()
