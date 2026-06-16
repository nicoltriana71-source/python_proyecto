from datetime import datetime
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from .modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from .modelos.facturas import Factura, FacturaCrear, FacturaEditar
from .modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar
from .enrutador import clientes
from .enrutador import facturas



app = FastAPI()

lista_clientes:list [Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones] = []

#SE INCLUYE RUTA DE CLIENTES 
app.include_router(clientes.rutas_clientes, tags=["Clientes"])

#SE INCLUYE RUTA DE facturas 
app.include_router(facturas.rutas_facturas, tags=["Facturas"])



#CRUD TRANSACCIONES 

@app.get("/transacciones", response_model=list[Transacciones])
async def listar_transacciones():
    return lista_transacciones

@app.post("/transacciones/{factura_id}")
async def crear_transaccion(
    factura_id: int, datos_transaccion: TransaccionesCrear, cliente_id: int
):
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
        
        
#EXCEPCION
    if not cliente_encontrado:
        raise HTTPException(
            status_code=400,
            detail=f"Error 400: No existe un cliente con ese id: {cliente_id}, debes crear el cliente.",
        )
        
#CONSULTA A LA FACTURA

    factura_encontrada = None
    for f in lista_facturas:
        if f.id == factura_id:
            factura_encontrada = f
            break
        
    if factura_encontrada:
        if factura_encontrada.cliente.id == cliente_id:
            transaccion_val = Transacciones.model_validate(
                datos_transaccion.model_dump()
            )
            transaccion_val.id = len(lista_transacciones) + 1
            transaccion_val.factura_id = factura_id
            lista_transacciones.append(transaccion_val)

            factura_encontrada.transacciones.append(transaccion_val)
            mensaje = f"Transaccion agregada a factura {factura_encontrada.id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura": factura_final}
        else:
            mensaje = f"Se encontro la factura de id: {factura_id}, pero es de otro cliente id: {cliente_id}"
            factura_final = factura_encontrada
            return {"mensaje": mensaje, "factura encontrada": factura_final}
    else:
        transaccion_val = Transacciones.model_validate(datos_transaccion.model_dump())
        transaccion_val.id = len(lista_transacciones) + 1
        transaccion_val.factura_id = len(lista_facturas) + 1
        
        factura = FacturaCrear(
            cliente=cliente_encontrado,
            fecha=str(datetime.now()),
            transacciones=[transaccion_val],
        
        )
            
        factura_val = Factura.model_validate(factura.model_dump())
        factura_val.id = len(lista_facturas) + 1
        lista_facturas.append(factura_val)
        
        lista_transacciones.append(transaccion_val)

        return {
            "mensaje": f"Factura no existe con el id: {factura_id}, pero se creo la nueva factura",
            "facturas": transaccion_val,
        }
        
        
@app.put("/factura/{id}/transacciones/{transacciones_id}")
async def editar_transaccion(id: int,transacciones_id: int, datos_transaccion:TransaccionesEditar):
    factura = next((f for f in lista_facturas if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "Factura no encontrada"}
        )
        
    for t in factura.transacciones:
        if t.id == transacciones_id:
            t.cantidad = datos_transaccion.cantidad
            t.vr_unitario = datos_transaccion.vr_unitario
            t.descripcion = datos_transaccion.descripcion
            
            factura.total = factura.valor_total
            return {"mensaje": "Transaccion actualizada", "factura": factura}
        
    return {"mensaje": "transaccion no encontrada"}

@app.delete("/factura/{id}/transacciones/{transacciones_id}")
async def eliminar_transacciones(id: int, transacciones_id: int):
    factura = next((f for f in lista_facturas if f.id == id), None)
    
    if factura is None:
        return JSONResponse(
            status_code=404,
            content={"error": "factura no encontrada"}
        )
        
    for t in factura.transacciones:
        if t.id == transacciones_id:
            factura.transacciones.remove(t)
            factura.total = factura.valor_total
            return {"mensaje": "transaccuion eliminada", "factura": factura}
        
    return {"mensaje": "Transaccion no encontrada"}
    
    
        