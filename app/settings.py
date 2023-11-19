from pydantic import AnyUrl
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    edgedb_dsn: AnyUrl | None
    s3_host: str
    s3_access_key: str
    s3_secret_key: str
    s3_bucket: str


SETTINGS = Settings()
