import psycopg2
key = "CUE-307"
connection = psycopg2.connect(database="p_ucm_cfe", user="postgres", password="admin", host="localhost", port=5432)

cursor = connection.cursor()
# 37581573-b7f7-4af1-a87f-1c2d80293c2d
# 87e4de55-884f-4022-ad9f-085438d7624e
cursor.execute("SELECT * FROM public.equipo_electrico WHERE id='99c1f615-eed3-463c-9aa3-1f13d136b655';")
# Fetch all rows from database
record = cursor.fetchall()
for row in record:
    variable = row[2]
    print(f'{key} Equipo:: {variable}')

cursor.execute("SELECT * FROM public.puntos_ucm WHERE id='203f7757-771f-43d6-bdba-a8ed2d470a26';")
record = cursor.fetchall()
for row in record:
    variable = row[4]
    print(f'{key} Variable:: {variable}')