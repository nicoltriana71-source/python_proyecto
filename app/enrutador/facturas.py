from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar
from ..listas import lista_facturas, lista_clientes

rutas_facturas = APIRouter()


#CRUD FACTURAS

#LISTAR FACTURAS
@rutas_facturas.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas

#CREAR CLIENTES
@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura, status_code=201)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    
    print("LISTA CLIENTES FACTURAS:", lista_clientes)
    
    cliente_encontrado = None
    
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
        
    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )
        
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val

#EDITAR FACTURA
@rutas_facturas.put("/facturas/{id}", response_model=Factura)
async def editar_factura(id: int, datos_factura: FacturaEditar):

    factura_encontrada = None

    for factura in lista_facturas:
        if factura.id == id:
            factura_encontrada = factura
            break

    if not factura_encontrada:
        raise HTTPException(
            status_code=404,
            detail=f"Factura con id {id} no encontrada"
        )

    cliente_encontrado = None

    for cliente in lista_clientes:
        if cliente.id == datos_factura.cliente_id:
            cliente_encontrado = cliente
            break

    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con id {datos_factura.cliente_id} no encontrado"
        )

    factura_encontrada.cliente = cliente_encontrado

    return factura_encontrada

#ELIMINAR FACTURA
@rutas_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int):
    for i, obj_factura in enumerate(lista_facturas):
        if obj_factura.id == id:
            factura_eliminada = lista_facturas.pop(i)
            return{"mensaje": "Factura eliminada correctamente", "factura": factura_eliminada}
    raise HTTPException(status_code=404,detail=f"Factura con id {id} no encontrada")