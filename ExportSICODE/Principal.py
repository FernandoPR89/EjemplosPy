# *********************
# 02/05/2023
# Fernando Patiño Reyes
# *********************
import csv 
import Preprocesamiento
import Agrupacion
import CrearSCD
import os
import FilaCol 
from LibreriasUCM import Libreria
import Modelo.Modelo as modelo
import Modelo.ValoresDefecto as Equivalencia
import ValidarMacrosMCI as ValidarIndicesMacros
import ParametrosMacro as ParametrosM
class Principal(object):
    def run(self):
        #nombreUnifilar = 'S.E. PRUEBA01 (PBA)'
        nombreUnifilar='PBA-04011'
        # nombreUnifilar='CIH-04015'
        self.NombreArchivoSalida = nombreUnifilar
        self.Abrev="PBA"
        self.VNM=13.8
        self.VNA=115
        self.PAN=100
        self.FRE=60
        self.LRW=-1
        self.LRH=-1
        self.CVX=-1
        self.CVY=-1

        segundoList = []
        terceroList = []
        cuartoList = []
        quintoList = []
        sextoList = []
        septimoList = []
        octavoList = []
        novenoList = []
        decimoList = []
        # self.macrosIndices=[]

        # primero = modelo.Primero(self.NombreArchivoSalida,self.Abrev,self.VNM,self.VNA,self.PAN,self.FRE,self.LRW,self.LRH)
# Procesa S.E. ---------------------------------------------------
        prepro = Preprocesamiento.Preprocesamiento(nombreUnifilar,)
        iconosMT=[]
        if prepro.validaJSON():
            prepro.eliminarHistorial()
            prepro.buscarEquipos()
            prepro.buscarEquiposElecConectados()
            prepro.buscarEquiposSinConectar()
            prepro.buscarNodosConectados()
            prepro.buscarNodosTexto()
            prepro.buscarLocEquiposyNodos()
            prepro.getEnlaces()
            prepro.buscarIconoMT()
            iconosMT = prepro.getIconosMT()
            # if  prepro.getEquiposSinconectar()>=1:
            #     prepro.conectarEquipo()
        else: print("JSON NO VALIDO")    
        enlacesPrincipales = prepro.getConexionesEquipos()
        prepro.resumenJson()
        nodos = prepro.getLocEquiposyNodos()
        # Se validan los indices de las macros
        validarIndicesM = ValidarIndicesMacros.ValidarMacrosMCI()
        # Se cargan los equipos
        equiposID = prepro.getEquiposID() # Se obtienen los equipos y los id de los unifilares

        macrosIndices=[]
        with open('macrosMCI.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        for equipo in equiposID:
                                if row['id']==equipo['id']:
                                        mcc=row['MC_CLAVE']
                                        mci=row['MC_ID']
                                        macrosIndices.append([mcc,mci])
        indicePadre=1
        clave_CE="CE0380"
        parametrosMacro = ParametrosM.ParametrosMacro(indicePadre,"CE")
        
        sig=11
        for macro in macrosIndices:
                if macro[0]=="CUCHE":
                      nombreConsecutivo=f'CUCHE{sig}'
                      sig=sig+1
                if macro[0]=="ICIRE":
                      nombreConsecutivo="43010"
                if macro[0]=="VIRT":
                      nombreConsecutivo="VIRT013"
                if macro[0]=="RESTE":
                      nombreConsecutivo=f'R0033'
                      sig=sig+1
                if macro[0]=="DESCE":
                      nombreConsecutivo="D0034"              
                parametrosMacro.getParametrosCE(macro[0],macro[1],nombreConsecutivo,clave_CE)
                indicePadre=parametrosMacro.getUltimoIndice()
                print(f'{macro[0]},{macro[1]}')

        cuartoList= parametrosMacro.getCuartoListado()
        #parametrosMacro.getParametros("ICIRE","MC1039","43010")
        #parametrosMacro.getParametros("CUCHE","MC1010","CUCHEPBB1")
        #parametrosMacro.getParametros("RESTE","MC1072","R0033")

        nodosTexto = prepro.getNodosTexto()
        # prepro.grafica(nodos,nodosTexto,enlacesPrincipales)
        fase2 = Agrupacion.Agrupacion(nodos,nodosTexto,iconosMT)
        #fase2.preAgrupa()
        fase2.agrupa()
        nodosAgrupados = fase2.get_nodosAgrupadosList()
        #fase2.grafica(nodos,nodosTexto,nodosAgrupados,enlacesPrincipales)
# END Procesa S.E. ---------------------------------------------------

# START PROCESA CE ---------------------------------------------------
        # nombreUnifilar = 'PBA-04011'
        # preproCE = Preprocesamiento.Preprocesamiento(nombreUnifilar)
        # iconosMT=[]
        # if preproCE.validaJSON():
        #     preproCE.eliminarHistorial()
        #     preproCE.buscarEquipos()
        #     preproCE.buscarEquiposElecConectados()
        #     preproCE.buscarEquiposSinConectar()
        #     preproCE.buscarNodosConectados()
        #     preproCE.buscarNodosTexto()
        #     preproCE.buscarLocEquiposyNodos()
        #     preproCE.getEnlaces()
        #     preproCE.buscarIconoMT()
        #     iconosMT = preproCE.getIconosMT()
        # else: print("JSON NO VALIDO")    
        # enlacesPrincipales = preproCE.getConexionesEquipos()
        # preproCE.resumenJson()
        # nodos = preproCE.getLocEquiposyNodos()
        # validarIndicesM = ValidarIndicesMacros.ValidarMacrosMCI()
        # equiposID = preproCE.getEquiposID() # Se obtienen

        # macrosIndices=[]
        # with open('macrosMCI.csv', newline='') as csvfile:
        #         reader = csv.DictReader(csvfile)
        #         for row in reader:
        #                 for equipo in equiposID:
        #                         if row['id']==equipo['id']:
        #                                 mcc=row['MC_CLAVE']
        #                                 mci=row['MC_ID']
        #                                 macrosIndices.append([mcc,mci])
        # indicePadre=1
        # parametrosMacro = ParametrosM.ParametrosMacro(indicePadre,"CE")
        # clave_CE="CE0380"
        # sig=11
        # for macro in macrosIndices:
        #         if macro[0]=="CUCHE":
        #               nombreConsecutivo=f'CUCHE{sig}'
        #               sig=sig+1
        #         if macro[0]=="VIRT":
        #               nombreConsecutivo="VIRT013"
        #         if macro[0]=="RESTE":
        #               nombreConsecutivo=f'R0033'
        #               sig=sig+1
        #         if macro[0]=="DESCE":
        #               nombreConsecutivo="D0034"              
        #         parametrosMacro.getParametrosCE(macro[0],macro[1],nombreConsecutivo,clave_CE)
        #         indicePadre=parametrosMacro.getUltimoIndice()
        #         print(f'{macro[0]},{macro[1]}')

        # octavoList= parametrosMacro.getOctavoListado()
# END Procesa CE ---------------------------------------------------
        # print(macrosIndices)
        #Se calcula la fila y columba de los equipos
        # filacol = FilaCol.FilaCol()
        # filacol.calcula(nodos)

        primero = modelo.Primero(self.NombreArchivoSalida,self.Abrev,self.VNM,self.VNA,self.PAN,self.FRE,self.LRW,self.LRH)
        # directorio=os.getcwd()+'/Unifilares_original/PBA/CTO'

        # numeroCircuitos = next(os.walk(directorio))[2] #dir is your directory path as string
        # cantidad=(len(numeroCircuitos))
        
        itemSegundo = modelo.SubSegundo(1,"CE0380","04010","04010","01",self.VNM,self.VNA,self.PAN,self.FRE,self.LRW,self.LRH)
        segundoList.append(itemSegundo)

        itemTercero = modelo.SubTercero(1,"MC0008","FREC","PARF008",1,12,"",self.CVX,self.CVY)
        terceroList.append(itemTercero)
        itemTercero = modelo.SubTercero(2,"MC1010","CUCHEPBB1","CUCHE011",5,3,"",self.CVX,self.CVY)
        terceroList.append(itemTercero)
        itemTercero = modelo.SubTercero(3,"MC1010","CUCHEPBB2","CUCHE012",7,3,"",self.CVX,self.CVY)
        terceroList.append(itemTercero)
        itemTercero = modelo.SubTercero(4,"MC1039","04010","ICIRE010",6,3,"",self.CVX,self.CVY)
        terceroList.append(itemTercero)

        # itemQuinto = modelo.SubQuinto(1,"MC1026","FVOLE4","MR1089","MR1173","72010","MC1047")
        # quintoList.append(itemQuinto)
        # quintoList.append(itemQuinto)

        # itemSexto = modelo.SubSexto(1,"","","","","","")
        # sextoList.append(itemSexto)
        # sextoList.append(itemSexto)
#NMC:(NÚMERO DE COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/
        itemSeptimo = modelo.SubSeptimo(1,"CE0380","MC0005","04010","VIRT013",6,3,"SEPRUEBAB.ICIRE010",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(2,"CE0380","MC0008","FREC","PARF008",1,12,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(3,"CE0380","MC0009","PAREA","PARE009",1,13,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(4,"CE0380","MC0009","PAREB","PARE010",1,14,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(5,"CE0380","MC0009","PAREC","PARE011",1,15,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(6,"CE0380","MC1068","PRF_CRGA","PRFIL012",2,12,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(7,"CE0380","MC1014","D0034","DESCE015",6,7,"",-1,-1)
        septimoList.append(itemSeptimo)
        itemSeptimo = modelo.SubSeptimo(8,"CE0380","MC1072","R0033","RESTE014",6,5,"",-1,-1)
        septimoList.append(itemSeptimo)

#NMC: NÚMERO DE VALORES DE LOS COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/


#NMC: NÚMERO DE VALORES DE LOS COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/
        itemNoveno = modelo.SubNoveno(1,"CE0380","MC1068","PRF_CRGA","MR1253","MR0022","PAREA","MC0009")
        novenoList.append(itemNoveno)
        itemNoveno = modelo.SubNoveno(1,"CE0380","MC1068","PRF_CRGA","MR1254","MR0022","PAREB","MC0009")
        novenoList.append(itemNoveno)
        itemNoveno = modelo.SubNoveno(1,"CE0380","MC1068","PRF_CRGA","MR1255","MR0022","PAREC","MC0009")
        novenoList.append(itemNoveno)


        segundo = modelo.Segundo(len(segundoList),segundoList)
        tercero = modelo.Tercero(len(terceroList),terceroList)
        cuarto = modelo.Cuarto(len(cuartoList),cuartoList)
        quinto = modelo.Quinto(len(quintoList),quintoList)
        sexto = modelo.Sexto(len(sextoList),sextoList)
        septimo = modelo.Septimo(len(septimoList),septimoList)
        octavo = modelo.Octavo(len(octavoList),octavoList)
        noveno = modelo.Noveno(len(novenoList),novenoList)
        decimo = modelo.Decimo(len(decimoList),decimoList)

        fase3 = CrearSCD.CrearSCD(nombreUnifilar+".scd")
        # fase3.crearArchivo(primero,segundo,tercero,cuarto,quinto,sexto,septimo,octavo,noveno,decimo)


#thisdir = "C://INEEL_code//Unifilares_original"

# for r, d, f in os.walk(thisdir):
#     for file in f:
#         if file.endswith(".desp"):
#             print(file[:-5])
#             nombreUnifilar = file[:-5]
#             prepro = Preprocesamiento.Preprocesamiento(nombreUnifilar)
#             prepro.eliminaHistorial()
#             prepro.procesa()

#nombreUnifilar='CTO-PMC-04045'

# libreria = Libreria.Libreria()
# elementossubestacion = libreria.getElementosRedMT()
# for elemento in elementossubestacion:
#     print(elemento)

if __name__ == '__main__':
    Principal().run()

