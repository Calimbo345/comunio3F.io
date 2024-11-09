from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# EL engine permite a SQL Alchemy comunicarse con la BBDD
# MAS INFORMACION: www.docs.sqlalchemy.org/en/14/engines.html
engine = create_engine("sqlite:///database/comunio_tercera_feb.db",
                       connect_args={"check_same_thread": False})#Create_engine cambia en funcion del gestor de BBDD => "sqlite"
# ADVERTENCIA: crear el engine no conecta inmediatamentea la BBDD

# Ahora crearemos la sesion lo que nos permite realizar transacciones a la BBDD
Session = sessionmaker(bind=engine)#Es una clase
session = Session()#Es un objeto

#Esta clase se encarga de mapear la info de las clase en las que Hereda y vincula us informacion a tablas de la BBDD
Base = declarative_base()

