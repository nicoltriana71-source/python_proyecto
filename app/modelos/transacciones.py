from pydantic import BaseModel
from sqlmodel import SQLModel, Field, Relationship


class TransaccionesBase(SQLModel):
    # atributos
    cantidad: int = Field(default=0)
    vr_unitario: float = Field(default=0.0)
    


class TransaccionesCrear(TransaccionesBase):
    pass


class TransaccionesEditar(TransaccionesBase):
    pass


class Transacciones(TransaccionesBase, Table=True):
    id: int | None = Field(default=None, primary_key=True)
    factura_id: int | None = Field(default=None, foreign_key="factura.id")