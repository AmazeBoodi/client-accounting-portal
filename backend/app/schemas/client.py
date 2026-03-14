from pydantic import BaseModel

class ClientCreate(BaseModel):
    name: str

class ClientOut(BaseModel):
    id: int
    name: str
    is_active: bool

    class Config:
        from_attributes = True
