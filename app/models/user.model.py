from pydantic import BaseModel, EmailStr

class User(BaseModel):
    nome: str
    email: EmailStr
    senha: str