from pydantic import BaseModel, computed_field

from app.modelos.clientes import Cliente
from app.modelos.transacciones import Transacciones

class FacturaBase(BaseModel):
    # atributos
    fecha: str
    cliente: Cliente
    transacciones: list[Transacciones] = []
    
    @computed_field
    @property
    def valor_total(self) -> float:
        factura_id_actual = getattr(self, "id", None)
        if factura_id_actual is None or not self.transacciones:
            return 0.0
        return sum(
            t.cantidad * t.vr_unitario
            for t in self.transacciones
            if t.factura_id == factura_id_actual
        )
        
class FacturaCrear(FacturaBase):
    cliente_id: int


class FacturaEditar(BaseModel):
    cliente_id: int


class Factura(FacturaBase):
    id: int | None = None
    cliente: Cliente | None = None
    total: float | None = None