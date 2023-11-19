from pydantic import BaseModel, SecretStr


class TokenResponse(BaseModel):
    token: SecretStr
