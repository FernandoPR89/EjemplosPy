#Debe tomar el archivo de equivalencia para crear el archivo de equivalencia con IDs
import csv 
import pandas as pd
import pyodbc
import Modelo.ValoresDefecto as EquivalenciaA

class ValidarMacrosMCI(object):
    def __init__(self):
        super(ValidarMacrosMCI, self).__init__()
        self.crearArchivoEquivalencia()

    def crearArchivoEquivalencia(self):
        equivale = EquivalenciaA.ValoresDefecto()
        equivalencia = equivale.getEquivalencia()
        
        cnxn = pyodbc.connect("Driver={SQL Server};Server=.\SIMULADOR;UID=root;PWD=7054705470;Database=CONTROLCCD;")
        df = pd.read_sql_query("SELECT MC_ID,MC_CLAVE FROM SCCD_C_MACROS WHERE MC_ESTADO='A'", cnxn)
        df.head()
        # field names 
        
        fields = ['id','nombre','categoria','MC_CLAVE', 'MC_ID'] 
        rows=[]

        for equipo in equivalencia:
            claveEquipo=equipo['equivalencia']
            for index, row in df.iterrows():
                if claveEquipo==row["MC_CLAVE"]:
                    _id=equipo['id']
                    _nombre=equipo['nombre']
                    _categoriaP=equipo['categoriaP']
                    _row=[_id,_nombre,_categoriaP, row["MC_CLAVE"],row["MC_ID"]]
                    rows.append(_row)
                    break

        # name of csv file 
        filename = "macrosMCI.csv"
            
        # writing to csv file 
        with open(filename, 'w',newline='') as csvfile: 
            # creating a csv writer object 
            csvwriter = csv.writer(csvfile) 
                
            # writing the fields 
            csvwriter.writerow(fields) 
                
            # writing the data rows 
            csvwriter.writerows(rows)
