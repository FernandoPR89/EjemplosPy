import csv

# with open('names.csv', 'w', newline='') as csvfile:
#     fieldnames = ['first_name', 'last_name']
#     writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

#     writer.writeheader()
#     writer.writerow({'first_name': 'Baked', 'last_name': 'Beans'})
#     writer.writerow({'first_name': 'Lovely', 'last_name': 'Spam'})
#     writer.writerow({'first_name': 'Wonderful', 'last_name': 'Spam'})

# with open('macrosMCI.csv', newline='') as csvfile:
#     reader = csv.DictReader(csvfile)
#     for row in reader:
#         print(row['MC_CLAVE'], row['MC_ID'])
conjunto=[]
datos = {"nombre":"fernando","clave":"FPR","descripcion":"JAVA"}
datos2 = {"nombre":"Alondra","clave":"ANZ","descripcion":"C++"}
conjunto.append(datos)
conjunto.append(datos2)

print(conjunto)