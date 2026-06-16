from fastapi import APIRouter

from ..modelos.clientes import  Cliente, ClienteCrear, ClienteEditar, ClienteEliminar

rutas_clientes = APIRouter()
lista_clientes: list[Cliente] = []


#CRUD CLIENTES

#LISTAR CLIENTES
@rutas_clientes.get("/clientes")
async def listar_cliente():
    #creacion de sms mas adecuado al usuario
    if len(lista_clientes) > 0:
       return{"Existen clientes": lista_clientes}
    else:
        return{"No existen clientes"}
    

@rutas_clientes.get("/clientes/{id}")
async def listar_cliente(id:int):
    for cliente in lista_clientes:
        if cliente.id == id:
            return cliente

    

#CREAR CLIENTES

@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente:ClienteCrear):
    Cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    Cliente_val.id = len (lista_clientes) +1  #incremento de id
    lista_clientes.append(Cliente_val)
#    return {"Clientes": Cliente_val}
    return Cliente_val


#EDITAR CLIENTES 
@rutas_clientes.put("/cliente/{id}")
async def editar_clientes(id:int, datos_cliente:ClienteEditar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_val = Cliente.model_validate(datos_cliente.model_dump())
            cliente_val.id = id
            lista_clientes[i] = cliente_val
             
    return {"mensaje": "Se acualizo correctamente el cliente", "Cliente": cliente_val}


#ELIMINAR CLIENTES 
@rutas_clientes.delete("/cliente/{id}")
async def eliminar_clientes(id:int, datos_cliente:ClienteEliminar):
    for i, obj_cliente in enumerate(lista_clientes):
        if obj_cliente.id == id:
            cliente_eliminado = lista_clientes.pop(i)
    return {"Cliente": "Cliente elminado", "Cliente": cliente_eliminado}