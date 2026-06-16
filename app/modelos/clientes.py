from pydantic import BaseModel
from sqlmodel import  SQLModel, Field, Relationship

class ClienteBase(SQLModel):
    nombre: str
    edad: int
    descripcion: str | None
    
class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class ClienteEliminar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    