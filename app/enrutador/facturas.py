from fastapi import APIRouter, HTTPException
from datetime import datetime

from ..modelos.facturas import Factura, FacturaCrear, FacturaEditar, FacturaLeer
from ..listas import lista_facturas, lista_clientes
from..conexion_bd import Sesion_dependencia
from sqlmodel import select
from ..modelos.clientes import Cliente

rutas_facturas = APIRouter()


#CRUD FACTURAS

#LISTAR FACTURAS
@rutas_facturas.get("/facturas", response_model=list[FacturaLeer])
async def listar_facturas(sesion: Sesion_dependencia):
    #select * from factura
    consulta = select(Factura)
    lista_facturas = sesion.exec(consulta).all()
    return lista_facturas

#CREAR CLIENTES
@rutas_facturas.post("/facturas/{cliente_id}", response_model=Factura, status_code=201)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear, sesion: Sesion_dependencia):
    
    print("LISTA CLIENTES FACTURAS:", lista_clientes)
    
    cliente_encontrado = sesion.get(Cliente,cliente_id)
    
        
    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )
        
    factura_dict = datos_factura.model_dump()
    factura_dict["cliente_id"] = cliente_id
    factura_val = Factura.model_validate(factura_dict)
    
    sesion.add(factura_val)
    sesion.commit()
    sesion.refresh(factura_val)
    return factura_val

#EDITAR FACTURA
@rutas_facturas.put("/facturas/{id}", response_model=Factura)
async def editar_factura(id: int, datos_factura: FacturaEditar, sesion: Sesion_dependencia):

    factura_encontrada = sesion.get(Factura, id)


    if not factura_encontrada:
        raise HTTPException(
            status_code=404,
            detail=f"Factura con id {id} no encontrada"
        )

    cliente_encontrado = sesion.get(Cliente, datos_factura.cliente_id)



    if not cliente_encontrado:
        raise HTTPException(
            status_code=404,
            detail=f"Cliente con id {datos_factura.cliente_id} no encontrado"
        )

    datos_actualizados = datos_factura.model_dump()
    factura_encontrada.sqlmodel_update(datos_actualizados)

    sesion.add(factura_encontrada)
    sesion.commit()
    sesion.refresh(factura_encontrada)

    return factura_encontrada

#ELIMINAR FACTURA
@rutas_facturas.delete("/facturas/{id}")
async def eliminar_factura(id: int, sesion: Sesion_dependencia):

    factura_encontrada = sesion.get(Factura, id)

    if not factura_encontrada:
        raise HTTPException(
            status_code=404,
            detail=f"Factura con id {id} no encontrada"
        )

    
    sesion.delete(factura_encontrada)
    sesion.commit()

    return {"mensaje": "Factura eliminada correctamente"}