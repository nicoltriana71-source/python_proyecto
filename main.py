from datetime import datetime

from fastapi import FastAPI, HTTPException
from modelos.clientes import Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from modelos.facturas import Factura, FacturaCrear, FacturaEditar
from modelos.transacciones import Transacciones, TransaccionesCrear


app = FastAPI()

#LISTA DE CLIENTES 
lista_clientes:list [Cliente] = []
lista_facturas: list[Factura] = []
lista_transacciones: list[Transacciones]

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

@app.get("/facturas", response_model=list[Factura])
async def listar_facturas():
    return lista_facturas

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
        
    factura_encontrada.total = datos_factura.total
    factura_encontrada.descripcion = datos_factura.descripcion

    return factura_encontrada

@app.delete("/facturas/{id}")
async def eliminar_factura(id: int):
    for i, obj_factura in enumerate(lista_facturas):
        if obj_factura.id == id:
            factura_eliminada = lista_facturas.pop(i)
            return{"mensaje": "Factura eliminada correctamente", "factura": factura_eliminada}
    raise HTTPException(status_code=404,detail=f"Factura con id {id} no encontrada")
    