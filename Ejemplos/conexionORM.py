import pandas as pd
import pyodbc
import sqlalchemy
from sqlalchemy.engine import create_engine
from sqlalchemy import select
from sqlalchemy.orm import Session
import models
# pyodbc stuff for MS SQL Server Express
driver='{SQL Server}'
server='.\SIMULADOR'
database='CONTROLCCD'

# pyodbc connection string
connection_string = f'mssql+pyodbc://DRIVER={driver};SERVER={server};'
connection_string += f'UID=root; PWD=7054705470'
connection_string += f'DATABASE={database};'


# create sqlalchemy engine connection URL
connection_url = sqlalchemy.engine.URL.create("mssql+pyodbc",database=database, host=server, query = {'driver':'SQL Server'})

engine = sqlalchemy.create_engine(connection_url)

cnxn = engine.connect()

session = Session(engine)
# stmt = select(models.SCCD_C_MACROS).where(models.SCCD_C_MACROS.MC_CLAVE.in_(["PARF"]))
# stmt = select(models.SCCD_C_MACROS).where(models.SCCD_C_MACROS.MC_ESTADO.in_(["A"]))
# for macro in session.scalars(stmt):
#     print(macro.MC_CLAVE)

stmt = select(models.EQUIPOS).where(models.EQUIPOS.NOMBRE.in_(["49015"]))
print(stmt)
for equipo in session.scalars(stmt):
    print(f'{equipo.ID} - {equipo.NOMBRE} - {equipo.ALARMA} - {equipo.FALLACOM}')

stmt = select(models.PUNTOS_SCADA).where(models.PUNTOS_SCADA.EQUIPO.in_([5443]))
print(stmt)
for equipo in session.scalars(stmt):
    print(f'{equipo.ID} {equipo.TIPO_EVENTO}')
    # print(f'{equipo.ID} - {equipo.NOMBRE} - {equipo.DEI} - {equipo.ALARMA} -  {equipo.FALLACOM}')