from datetime import datetime
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from app.modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from app.modelos.facturas import Factura, FacturaCrear, FacturaEditar
from app.modelos.transacciones import Transacciones, TransaccionesCrear, TransaccionesEditar


app = FastAPI()

#LISTA DE CLIENTES 
lista_clientes:list [Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones] = []

#LISTAR CLIENTES
@app.get("/clientes")
async def listar_cliente():
    #creacion de sms mas adecuado al usuario
    if len(lista_clientes) > 0:
       return{"Existen clientes": lista_clientes}
    else:
        return{"No existen clientes"}
    

@app.get("/clientes/{id}")
async def listar_cliente(id:int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    

#CREAR CLIENTES

@app.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente:ClienteCrear):
    Cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    Cliente_val.id = len (lista_clientes) +1  #incremento de id
    lista_clientes.append(Cliente_val)
#    return {"Clientes": Cliente_val}
    return Cliente_val


#EDITAR CLIENTES 
@app.put("/cliente/{id}")
async def editar_clientes(id:int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
             
    return {"mensaje": "Se acualizo correctamente el cliente", "Cliente": cliente_val}


#ELIMINAR CLIENTES 
@app.delete("/cliente/{id}")
async def eliminar_clientes(id:int, datos_cliente:ClienteEliminar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_eliminado = lista_clientes.pop(i)
    return {"Cliente": "Cliente elminado", "Cliente": cliente_eliminado}

#CRUD FACTURAS

#LISTAR FACTURAS
@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas

#CREAR CLIENTES
@app.post("/facturas/{cliente_id}", response_model=Factura, status_code=201)
async def crear_facturas(cliente_id: int, datos_factura: FacturaCrear):
    cliente_encontrado = None
    for c in lista_clientes:
        if c.id == cliente_id:
            cliente_encontrado = c
            break
        
    if not cliente_encontrado:
        raise HTTPException(
            status_code=201,
            detail=f"Cliente con id {cliente_id} no existe, debes crear.",
        )
        
    factura_val = Factura.model_validate(datos_factura.model_dump())
    factura_val.id = len(lista_facturas) + 1
    factura_val.fecha = datetime.now()
    factura_val.cliente = cliente_encontrado
    lista_facturas.append(factura_val)
    return factura_val

#EDITAR FACTURA
@app.put("/facturas/{id}", response_model=Factura)
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
@app.delete("/facturas/{id}")
async def eliminar_factura(id: int):
    for i, obj_factura in enumerate(lista_facturas):
        if obj_factura.id == id:
            factura_eliminada = lista_facturas.pop(i)
            return{"mensaje": "Factura eliminada correctamente", "factura": factura_eliminada}
    raise HTTPException(status_code=404,detail=f"Factura con id {id} no encontrada")

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
    
    
        