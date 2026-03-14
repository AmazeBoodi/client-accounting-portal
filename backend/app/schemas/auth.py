from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class MeResponse(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    client_id: int | None
