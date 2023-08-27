import Equipos
equipos = Equipos.Equipos()
misEquipos =equipos.getEquipo()
for key,value in misEquipos.items():
    print(key)
	#print(value['categoriaP'])