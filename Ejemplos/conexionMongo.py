import pymongo
from bson.json_util import dumps, loads
from pprint import pprint
import bson
import os
import shutil
import json

#Algoritmo para extraer los json de cada se y sus circutios asociados
class conexionMongo(object):
    def run(self):
# myclient = pymongo.MongoClient("mongodb://10.0.113.225:27017/")
# mydb = myclient["bd_unifilares_ucm"]
# despliegues = mydb['despliegues']

        myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
        mydb = myclient["despliegues_cue"]
        despliegues = mydb['unifilares_cue']

        # pprint(despliegues.find_one({'nombre': 'TBH 5015'}))
        #{clave:{ $regex : /^SE-/ }}
        cursor = despliegues.find({'nombre':{ '$regex' : '^S.E.' }})
        # print(cursor)
        # unifilares = loads(dumps(cursor))
        list_cur = list(cursor)
        # Converting to the JSON
        json_data = dumps(list_cur, indent = 2)

        # with open('data.json', 'w') as file:
        #     file.write(json_data)
        # unifilar = despliegues.find_one({'_id': bson.ObjectId('60ee46e558ea75ef4e601b94')})
        # print(unifilares)

        directorioActual=os.getcwd()
        nombreDirectorio="Division"
        divisionPath = os.path.join(directorioActual, nombreDirectorio)
        print(divisionPath)

        os.mkdir(divisionPath)
        # Crear archivo csv para leerlo en el principal que contenga la SE y sus CTO
        for unifilar in list_cur:
            # print(unifilar['clave'])
            _nombre = unifilar['nombre']
            clave=unifilar['clave']
            _clave = _nombre.split("(")
            nombreSE = _clave[1].replace(")","")
            if len(nombreSE)==3:
                print()
                nombreSEPath=os.path.join(divisionPath, nombreSE)
                directorioCTO=os.path.join(nombreSEPath,"CTO")
                os.mkdir(nombreSEPath)
                os.mkdir(directorioCTO)
                nuevoArchivo=os.path.join(nombreSEPath, clave+'.json')
                data = {}
                # data['_id'] = 
                data['nombre'] = unifilar['nombre'] # se trata del nombre en el json
                data['clave'] = unifilar['clave']
                data['descripcion'] = unifilar['descripcion']
                data['nodeDataArray'] = unifilar['modelo']['nodeDataArray']
                data['linkDataArray'] = unifilar['modelo']['linkDataArray']
                with open(nuevoArchivo, 'w') as file:
                    json.dump(data, file)
                procesaCTO(nombreSE,directorioCTO)

def procesaCTO(clave,path):
    myclient = pymongo.MongoClient("mongodb://127.0.0.1:27017/")
    mydb = myclient["bd_unifilares_ucm"]
    despliegues = mydb['despliegues']
    buscar=f'^{clave}'
    print(buscar)
    cursor = despliegues.find({'nombre':{ '$regex' : buscar }})
    list_cur = list(cursor)
    for circuito in list_cur:
        nombre=circuito['nombre']
        nuevoArchivo=os.path.join(path, nombre+'.json')
        data = {}
        # data['_id'] = 
        data['nombre'] = circuito['nombre'] # se trata del nombre en el json
        data['clave'] = circuito['clave']
        data['descripcion'] = circuito['descripcion']
        data['nodeDataArray'] = circuito['modelo']['nodeDataArray']
        data['linkDataArray'] = circuito['modelo']['linkDataArray']
        with open(nuevoArchivo, 'w') as file:
            json.dump(data, file)
# for db_info in mydb.list_collection_names():
#    print(db_info)
#mycol = mydb["despliegues"]
#list_database_names

# def crearDirectorio(self,nombreDirectorio):
#     os.mkdir(nombreDirectorio)

if __name__ == '__main__':
    conexionMongo().run()