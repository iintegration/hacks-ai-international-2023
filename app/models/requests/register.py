from pydantic import BaseModel, EmailStr, SecretStr


class RegisterRequest(BaseModel):
    email: EmailStr
    password: SecretStr
