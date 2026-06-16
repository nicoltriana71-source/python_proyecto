from fastapi import FastAPI, Depends
from typing import Annotated
from sqlmodel import Session, SQLModel, create_engine

nombre_bd = "bd_clientes.sqlite3"
url_bd = f"sqlite:///{nombre_bd}"

#MOTOR BD
motor_bd = create_engine(url_bd)


#METODO DE TABLAS 
def crear_tablas(app: FastAPI):
    SQLModel.metadata.create_all(motor_bd)
    yield 


#METODO DE SESION 
def obtener_sesion():
    with Session(motor_bd) as mi_sesion:
        yield mi_sesion
        
#INYECCION DE DEPENDENCIAS 

#REGISTRO DE SESION 

Sesion_dependencia = Annotated[Session, Depends(obtener_sesion)]