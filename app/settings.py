from pydantic import AnyUrl, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    edgedb_dsn: AnyUrl | None = None
    redis_dsn: RedisDsn = "redis://localhost"
    s3_host: str = "192.168.31.97:9000"
    s3_access_key: str = "I5bCf1TtFbHmwd9XEdRt"
    s3_secret_key: str = "u92qVxBYjbea26SX8OQJ7dJdSrbaVN3zzHZPDuE5"
    s3_bucket: str = "bucket"


SETTINGS = Settings()
