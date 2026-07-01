from pydantic import BaseModel, computed_field
from datetime import datetime
from app.modelos.clientes import Cliente
from app.modelos.transacciones import Transacciones
from sqlmodel import SQLModel, Field, Relationship

class FacturaBase(SQLModel):
    # atributos
    fecha: str = Field(default=datetime.now ())
    #cliente: Cliente
    #transacciones: list[Transacciones] = []
    
    @computed_field
    @property
    def valor_total(self) -> float:
        #factura_id_actual = getattr(self, "id", None)
        #if factura_id_actual is None or not self.transacciones:
            #return 0.0
        #return sum(
            #t.cantidad * t.vr_unitario
            #for t in self.transacciones
            #if t.factura_id == factura_id_actual
        #)
        return 0.0
        
class FacturaCrear(FacturaBase):
    
    pass

class FacturaEditar(BaseModel):
    
    pass


class Factura(FacturaBase, table=True):
    id: int | None = Field(default=None, primary_key=True )
    cliente_id: int= Field(default=None, foreign_key="cliente.id")
   