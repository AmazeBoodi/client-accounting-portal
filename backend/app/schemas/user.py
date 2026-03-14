from pydantic import BaseModel, EmailStr

class UserCreateClient(BaseModel):
    email: EmailStr
    name: str
    password: str
    client_id: int

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: str
    role: str
    client_id: int | None
    is_active: bool

    class Config:
        from_attributes = True
