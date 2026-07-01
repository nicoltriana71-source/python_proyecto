from datetime import datetime
from sqlmodel import SQLModel, Field, Relationship
from pydantic import BaseModel, computed_field
from ..modelos.clientes import Cliente
from ..modelos.transacciones import Transacciones


class FacturaBase(SQLModel):
    fecha: str = Field(default=datetime.now ())
    cliente: Cliente
    transacciones: list[Transacciones] = []
    
    @computed_field
    @property
    def vr_total(self) -> float:
        total_factura= 0.0
        if self.transaccion== None:
            return total_factura
        for transaccion in self.transacciones:
                total_factura += transaccion.vr_unitario * transaccion.cantidad 
        return total_factura

   
        
class FacturaCrear(FacturaBase):
    
    pass

class FacturaEditar(BaseModel):
    
    pass

class Factura(FacturaBase):
    id: int | None = None

class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True )
    cliente_id: int= Field(default=None, foreign_key="cliente.id")
    cliente : Cliente = Relationship(back_populates="factura")
    transacciones: list[Transacciones] = Relationship(back_populates="factura")

class FacturaLeer(FacturaBase): 
    id: int
    cliente: Cliente
    #transacciones: list[Transacciones]=[]

class FacturaLeerCompuesta(FacturaLeer):
    transacciones: list[Transacciones]=[]
