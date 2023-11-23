from pydantic import AnyUrl, RedisDsn
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    edgedb_dsn: AnyUrl | None = None
    redis_dsn: RedisDsn = "redis://localhost"
    s3_host: str = "localhost:443"
    s3_access_key: str = "edCFhCQApXZm0bvRgeQX"
    s3_secret_key: str = "gqVyjEdL4wss7LBYxS3Qpzrd4mSVagZz5reCqtUw"
    s3_bucket: str = "bucket"
    s3_public_host: str = "https://minio.sosus.org"


SETTINGS = Settings()
