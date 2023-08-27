# import pypyodbc 
# import pandas as pd

import pandas as pd
import pyodbc

cnxn = pyodbc.connect("Driver={SQL Server};Server=.\SIMULADOR;UID=root;PWD=7054705470;Database=CONTROLCCD;")
df = pd.read_sql_query("SELECT * FROM SCCD_M_MAC_PARAM_REPOR WHERE MC_ID='MC1039' AND MR_ESTADO='A'", cnxn)
df.head()

print(df)
df2 = pd.read_sql_query("  SELECT  TOP (100) * FROM SCCD_C_PARAM_REPOR", cnxn)
df2.head()
print(df2)

# cnxn = pypyodbc.connect("Driver={SQL Server Native Client 11.0};"
#                       "Server=.\SIMULADOR;"
#                       "Database=CONTROLCCD;"
#                       "uid=root;pwd=7065705470")


# cursor = cnxn.cursor()
# cursor.execute('SELECT * FROM SCCD_C_MACROS')

# for row in cursor:
#     print('row = %r' % (row,))



#df = pd.read_sql_query('select * from table', cnxn)