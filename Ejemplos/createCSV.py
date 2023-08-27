import csv 
import pandas as pd
import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server};Server=.\SIMULADOR;UID=root;PWD=7054705470;Database=CONTROLCCD;")
df = pd.read_sql_query("SELECT MC_ID,MC_CLAVE FROM [SCCD_C_MACROS] WHERE MC_ESTADO='A'", cnxn)
df.head()

rows=[]
for index, row in df.iterrows():
    _row=[ row["MC_CLAVE"],row["MC_ID"]]
    rows.append(_row)

# field names 
fields = ['MC_CLAVE', 'MC_ID'] 

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
