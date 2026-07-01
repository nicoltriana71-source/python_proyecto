from fastapi import APIRouter, HTTPException
from fastapi.responses import JSONResponse
from datetime import datetime
from ..modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from ..modelos.facturas import Factura, FacturaCrear
from .clientes import lista_clientes
from .facturas import lista_facturas
from ..listas import lista_clientes, lista_facturas, lista_transacciones
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select


rutas_transacciones = APIRouter()


#CRUD TRANSACCIONES 

#LISTAR ODAS LAS TRANSACCIONES
@rutas_transacciones.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones(sesion: Sesion_dependencia):
    #consulta = select(Transacciones)
    #lista_transacciones = sesion.exec(consulta).all()
    return sesion.exec(select(Transacciones)).all()


#LISTAR TRANSACCION POR ID
@rutas_transacciones.get("/transacciones/{id_transaccion}", response_model=Transacciones)
async def listar_transaccion(id_transaccion: int):
    pass


#CREAR TRANSACCION
@rutas_transacciones.post("/transacciones/{factura_id}")
async def crear_transaccion(factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int, sesion: Sesion_dependencia):

    factura_encontrada = sesion.get(Factura, factura_id)
        
#EXCEPCION
    if not factura_encontrada:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )
        
#CONSULTA A LA FACTURA
    transaccion_dict = datos_transaccion.model_dump()
    transaccion_dict["factura_id"] = factura_id
    transaccion_val =   Transacciones.model_validate(transaccion_dict)
    sesion.add(transaccion_val)
    sesion.commit()
    sesion.refresh(transaccion_val)
    return transaccion_val 

        
#EDITAR TRANSACCION  
@rutas_transacciones.put("/factura/{id}/transacciones/{transacciones_id}", response_model=Transacciones)
async def editar_transaccion(id: int,transacciones_id: int, datos_transaccion:TransaccionesEditar, sesion: Sesion_dependencia):
    

    factura = sesion.get(Factura, id)

    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )
        
    transaccion = sesion.get(Transacciones, transacciones_id)

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )
    
    if transaccion.factura_id != factura.id:
        raise HTTPException(
            status_code=400,
            detail="La transacción no pertenece a esa factura"
        )
    
    datos = datos_transaccion.model_dump()

    sesion.add(transaccion)
    sesion.commit()
    sesion.refresh(transaccion)
        
    return transaccion


#ELIMINAR TRANSACCION
@rutas_transacciones.delete("/factura/{id}/transacciones/{transacciones_id}")
async def eliminar_transacciones(id: int, transacciones_id: int, sesion: Sesion_dependencia):

    factura = sesion.get(Factura, id)
    
    if not factura:
        raise HTTPException(
            status_code=404,
            detail="Factura no encontrada"
        )
    
    transaccion = sesion.get(Transacciones, transacciones_id)

    if not transaccion:
        raise HTTPException(
            status_code=404,
            detail="Transacción no encontrada"
        )
    
    if transaccion.factura_id != factura.id:
        raise HTTPException(
            status_code=400,
            detail="La transacción no pertenece a esa factura"
        )
    
    sesion.delete(transaccion)
    sesion.commit()

    return {"mensaje": "Transacción eliminada correctamente"}