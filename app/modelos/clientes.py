from pydantic import BaseModel
from sqlmodel import  SQLModel, Field, Relationship

class ClienteBase(SQLModel):
    nombre: str = Field(default=None)
    edad: int = Field(default=None)
    descripcion: str | None = Field(default=None)
    
class ClienteCrear(ClienteBase):
    pass

class ClienteEditar(ClienteBase):
    pass

class ClienteEliminar(ClienteBase):
    pass

class Cliente(ClienteBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    #relacion virtual con factura 
    factura : list["Factura"] = Relationship(back_populates="cliente")

#MODELO DE VISTA AL CLIENTE 
class ClienteLeer(ClienteBase):
    id: int
    cliente: Cliente 
    
