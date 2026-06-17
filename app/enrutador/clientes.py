from fastapi import APIRouter, HTTPException, status
from ..modelos.clientes import  Cliente, ClienteCrear, ClienteEditar, ClienteEliminar
from ..listas import lista_clientes
from ..conexion_bd import Sesion_dependencia
from sqlmodel import select

rutas_clientes = APIRouter()


#CRUD CLIENTES

#LISTAR CLIENTES
@rutas_clientes.get("/clientes")
async def listar_cliente(mi_sesion: Sesion_dependencia):
    cliente_lis = mi_sesion.exec(select(Cliente)).all()
    return cliente_lis
    
#LISTAR CLIENTES POR ID
@rutas_clientes.get("/clientes/{id}")
async def listar_cliente(id:int, mi_sesion: Sesion_dependencia):
    cliente_list = mi_sesion.get(Cliente, id)
    if not cliente_list:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Cliente no encontrado con el ID {id}")
    return cliente_list

#CREAR CLIENTES

@rutas_clientes.post("/clientes", response_model=Cliente)
async def crear_clientes(datos_cliente:ClienteCrear, mi_sesion: Sesion_dependencia):
    Cliente_val = Cliente.model_validate(datos_cliente.model_dump())
    mi_sesion.add(Cliente_val)
    mi_sesion.commit()
    mi_sesion.refresh(Cliente_val)
    return Cliente_val


#EDITAR CLIENTES 
@rutas_clientes.put("/cliente/{id}")
async def editar_clientes(id:int, datos_cliente:ClienteEditar, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente conID {id}, no existe")
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.add(cliente_bd)
    mi_sesion.commit()
    mi_sesion.refresh(cliente_bd)
             
    return cliente_bd


#ELIMINAR CLIENTES 
@rutas_clientes.delete("/cliente/{id}")
async def eliminar_clientes(id:int, datos_cliente:ClienteEliminar, mi_sesion: Sesion_dependencia):
    cliente_bd = mi_sesion.get(Cliente, id)

    if not cliente_bd:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"El cliente conID {id}, no existe")
    cliente_dict = datos_cliente.model_dump(exclude_unset=True)
    cliente_bd.sqlmodel_update(cliente_dict)
    mi_sesion.delete(cliente_bd)
    mi_sesion.commit()
    return cliente_bd