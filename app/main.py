from datetime import datetime
from fastapi.responses import JSONResponse

from fastapi import FastAPI, HTTPException
from .enrutador import clientes
from .enrutador import facturas
from .enrutador import transacciones
from .conexion_bd import crear_tablas


app = FastAPI(lifespan=crear_tablas)


#SE INCLUYE RUTA DE CLIENTES 
app.include_router(clientes.rutas_clientes, tags=["Clientes"])

#SE INCLUYE RUTA DE FACTURAS
app.include_router(facturas.rutas_facturas, tags=["Facturas"])

#SE INCLUYE RUTA DE TRANSACCIONES 
app.include_router(transacciones.rutas_transacciones, tags=["Transacciones"])


    
    
        