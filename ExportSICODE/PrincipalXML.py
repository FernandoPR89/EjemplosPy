# *********************
# 12/06/2023
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
import ExportAgrademos.CrearArchivosXML as crearArchivosXML

class PrincipalXML(object):
    def run(self):
        nombreUnifilar = 'S.E. JUAREZ (ETJ)'
        #nombreUnifilar = 'ETJ-04022'
        #nombreUnifilar = 'S.E. PRUEBA01 (PBA)'
        #nombreUnifilar='PBA-04011'
        # nombreUnifilar='CIH-04015'
        self.NombreArchivoSalida = nombreUnifilar
        self.Abrev="ETJ"
        self.ClaveSE=""
        self.VNM=13.8
        self.VNA=115
        self.PAN=100
        self.FRE=60
        self.LRW=-1
        self.LRH=-1
        self.CVX=-1
        self.CVY=-1
        # self.macrosIndices=[]

# Procesa S.E. ---------------------------------------------------
        prepro = Preprocesamiento.Preprocesamiento(nombreUnifilar)
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
        # validarIndicesM = ValidarIndicesMacros.ValidarMacrosMCI()
        # Se cargan los equipos
        equiposID = prepro.getEquiposID() # Se obtienen los equipos y los id de los unifilares
        # for _equipo in equiposID:
        #     print(_equipo['id'],_equipo['mainCategory'],_equipo['nombre'],_equipo['key'])

        macrosIndices=[]
        with open('macrosMCI.csv', newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                        for equipo in equiposID:
                            if row['id']==equipo['id']:
                                    mcc=row['MC_CLAVE']
                                    _key = equipo['key'].split("-")
                                    tam=len(_key)
                                    _id=_key[tam-1]
                                    macrosIndices.append([mcc,equipo['id'],_id])

        # for macro in macrosIndices:
        #     print(f'{macro[0]},{macro[1]},{macro[2]}')

        nodosTexto = prepro.getNodosTexto() # Etiquetas sin asociar a los equipos

        # for nodo in nodosTexto:
        #     print(nodo[3])
            
        #prepro.grafica(nodos,nodosTexto,enlacesPrincipales)
        fase2 = Agrupacion.Agrupacion(nodos,nodosTexto,iconosMT)
        #fase2.preAgrupa()
        fase2.agrupa()
        nodosAgrupados = fase2.get_nodosAgrupadosList()
        # print("Enlaces principales")
        # print(enlacesPrincipales)
        # print("Nodos agrupados")
        # print(nodosAgrupados)
        fase2.grafica(nodos,nodosTexto,nodosAgrupados,enlacesPrincipales)
        datosUnifilar = prepro.getDatosUnifilar()
        _nombre=datosUnifilar['nombre']
        _abrev = datosUnifilar['abrev']
        _clave = datosUnifilar['clave'] #SEETJ
        _descripcion = datosUnifilar['descripcion']
        _divison="DG"

        self.ClaveSE=_clave
        # print(_nombre," ",_clave," ",_descripcion," ",_abrev)
        nivel="SE"
        archivoSis=[
            {"nombre":self.ClaveSE,"ndia":"349","descripcionCorta":self.ClaveSE,"descripcionLarga":_descripcion,"activo":"true","td":"Electrico","contador":"73","macro":"false","macroGlobal":"false","macroBase":"false","ideSistema":self.ClaveSE},
            {"nombre":"ETJ04022","ndia":"350","descripcionCorta":"ETJ04022","descripcionLarga":"ETJ04022","activo":"true","td":"Electrico","contador":"8","macro":"false","macroGlobal":"false","macroBase":"false","ideSistema":self.ClaveSE}
            ]
        macrosSE=[]
        #Llenado de macros
        indice=1
        nodosSE=[] # Apartado nodos del archivo gra
        for macro in macrosIndices:
            if 'ICIRE' in macro[0]:
                nombreConsecutivo=self.getNombreConsecutivo(macro[0],indice)
                etiquetas=self.getEtiquetasAsociadasAlEquipo(macro[2],nodosTexto,nodosAgrupados)
                # print(etiquetas)
                datos = {"ideComponente":nombreConsecutivo,"Equipo":f"I{etiquetas[0]}","IdEquipo":indice,"Descripcion":etiquetas[0],"Divison":_divison,"SE":_abrev,"DEIDisp":etiquetas[0],"tipo":"MacroControlSCCDBD","nivel":nivel}
                macrosSE.append(datos)
                macroXY=self.getXYNodo(macro[2],nodos)
                # print(macroXY)
                nodosSE.append([nombreConsecutivo,macroXY[0],macroXY[1]])
                indice=indice+1
            # print(f'{macro[0]},{macro[1]}')
        # for macro in macrosSE:
        #     print(macro['ideComponente'])
        # print(nodosSE)

        # macrosSE=[
        #     {"ideComponente":"ICIRE001","Equipo":"I43000","IdEquipo":"1000","Descripcion":"PUENTE DE IXTLA","Divison":_divison,"SE":_abrev,"DEIDisp":"43045","tipo":"MacroControlSCCDBD","nivel":nivel},
        #     {"ideComponente":"ICIRE002","Equipo":"I43002","IdEquipo":"1002","Descripcion":"AMACUZAC","Divison":_divison,"SE":_abrev,"DEIDisp":"43046","tipo":"MacroControlSCCDBD","nivel":nivel}
        #     ]
        datosGeneralesSE={"nombre":_clave,"tipoDiagrama":"Electrico","descCorta":_abrev,"descLarga":_descripcion}
        conexionesSE=[]


# END Procesa S.E. ---------------------------------------------------
# START Procesa C.E. -------------------------------------------------
        nombreUnifilar = 'ETJ-04022'
        prepro2 = Preprocesamiento.Preprocesamiento(nombreUnifilar)
        iconosMT=[]
        if prepro2.validaJSON():
            prepro2.eliminarHistorial()
            prepro2.buscarEquipos()
            prepro2.buscarEquiposElecConectados()
            prepro2.buscarEquiposSinConectar()
            prepro2.buscarNodosConectados()
            prepro2.buscarNodosTexto()
            prepro2.buscarLocEquiposyNodos()
            prepro2.getEnlaces()
            prepro2.buscarIconoMT()
            iconosMT = prepro2.getIconosMT()
            # if  prepro2.getEquiposSinconectar()>=1:
            #     prepro2.conectarEquipo()
        else: print("JSON NO VALIDO")    
        enlacesPrincipales = prepro2.getConexionesEquipos()
        print(enlacesPrincipales)
        prepro2.resumenJson()
        nodos = prepro2.getLocEquiposyNodos()
        
        self.procesaNodosEnEnlaces(enlacesPrincipales,nodos)
        # Se validan los indices de las macros ------------------------------
        # validarIndicesM = ValidarIndicesMacros.ValidarMacrosMCI()
        # Se cargan los equipos ------------------------------
        equiposID = prepro2.getEquiposID() # Se obtienen los equipos y los id de los unifilares
        # for _equipo in equiposID:
        #     print(_equipo['id'],_equipo['mainCategory'],_equipo['nombre'],_equipo['key'])
        # print(nodos)
        macrosIndices=[]
        with open('macrosMCI.csv', newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                for equipo in equiposID:
                    if row['id']==equipo['id']:
                        mcc=row['MC_CLAVE']
                        mci=row['MC_ID']
                        _key = equipo['key'].split("-")
                        tam=len(_key)
                        _id=_key[tam-1]
                        macrosIndices.append([mcc,equipo['id'],_id])
        # for macro in macrosIndices:
        #     print(f'{macro[0]},{macro[1]},{macro[2]}')

        nodosTexto = prepro2.getNodosTexto()
        comentariosCE =nodosTexto
        # print(comentariosCE)
        #prepro2.grafica(nodos,nodosTexto,enlacesPrincipales)
        fase2 = Agrupacion.Agrupacion(nodos,nodosTexto,iconosMT)
        #fase2.preAgrupa()
        fase2.agrupa()
        nodosAgrupados = fase2.get_nodosAgrupadosList()

        fase2.grafica(nodos,nodosTexto,nodosAgrupados,enlacesPrincipales)
# END Procesa C.E. ---------------------------------------------------
        # Crear archivos para los CE
        nivel="CE"
        macrosCE=[]
        nodosCE=[]
        nombreClave="ETJ04022"

        for macro in macrosIndices:
            nombreConsecutivo=self.getNombreConsecutivo(macro[0],indice)
            etiquetas=self.getEtiquetasAsociadasAlEquipo(macro[2],nodosTexto,nodosAgrupados)
            minimaEtiqueta=self.getEtiquetaCorta(etiquetas)
            # print(etiquetas)
            if 'ICIRE' in macro[0]:
                datos = {"ideComponente":nombreConsecutivo,"Equipo":f"I{minimaEtiqueta}","IdEquipo":indice,"Descripcion":minimaEtiqueta,"Divison":_divison,"SE":_abrev,"DEIDisp":minimaEtiqueta,"tipo":"MacroControlSCCDBD","nivel":nivel}
            else:
                 datos = {"ideComponente":nombreConsecutivo,"Equipo":f"{minimaEtiqueta}","IdEquipo":indice,"Descripcion":minimaEtiqueta,"Divison":_divison,"SE":_abrev,"DEIDisp":minimaEtiqueta,"tipo":"MacroControlSCCDBD","nivel":nivel}
            macrosCE.append(datos)
            macroXY=self.getXYNodo(macro[2],nodos)
            # print(macroXY)
            nodosCE.append([nombreConsecutivo,macroXY[0],macroXY[1]])
            indice=indice+1

        datosGeneralesCE={"nombre":nombreClave,"tipoDiagrama":"Electrico","descCorta":nombreClave,"descLarga":nombreClave}
        comentariossE=[] # Sin comentarios para la se

        conexionesCE=[{"fromID":"VIRT005","toId":"CUCHE004"},{"fromID":"VIRT005","toId":"DESCE008"},{"fromID":"DESCE008","toId":"CUCHE002"},{"fromID":"CUCHE002","toId":"CUCHE003"},{"fromID":"CUCHE003","toId":"RESTE007"},{"fromID":"CUCHE003","toId":"CUCHE001"},
        {"fromID":"CUCHE001","toId":"RESTE006"}]
        # nodosCE=["VIRT000","RESTE001","DESCE002"]

        crearArchivos = crearArchivosXML.CrearArchivosXML(archivoSis,datosGeneralesSE,macrosSE,conexionesSE,nodosSE,datosGeneralesCE,macrosCE,conexionesCE,nodosCE,_descripcion,self.ClaveSE,comentariosCE,comentariossE)
        crearArchivos.crearArchivos(self.ClaveSE)

        crearArchivos.crearArchivosCE(nombreClave)
        # fase2.grafica(nodos,nodosTexto,nodosAgrupados,enlacesPrincipales)

        #fase3 = CrearSCD.CrearSCD(nombreUnifilar+".scd")
        # fase3.crearArchivo(primero,segundo,tercero,cuarto,quinto,sexto,septimo,octavo,noveno,decimo)
    def procesaNodosEnEnlaces(self, enlacesPrincipales,nodosLoc):
        grupos=[]
        subgrupo=[]
        soloNodos=[]
        sinEnlaces=[]
        for enlace in enlacesPrincipales:
            if 'Nodo' in enlace[2] or 'Nodo' in enlace[3]:
                soloNodos.append(enlace)
            else:
                sinEnlaces.append(enlace)
        sig=1       
        for nodo in soloNodos:
            if nodo[0]==soloNodos[sig][0] or nodo[0]==soloNodos[sig][1]:
                subgrupo.append(nodo)
                # print("subgrupo")
                sig=sig+1
            else:
                subgrupo.append(nodo)
                grupos.append(subgrupo)
                subgrupo=[]
        sig=1
        base=""
        for nodo in soloNodos:
            base=nodo[1]
            if base==soloNodos[sig][1] or base==soloNodos[sig][0]:
                base=nodo[1]
                subgrupo.append(nodo)
                # print("subgrupo")
                sig=sig+1
            else:
                #subgrupo.append(nodo)
                grupos.append(subgrupo)
                subgrupo=[]
                # print("otro subgrupo")
        #Conocer el nodo mas a la izquierda de cada subgrupo
        for subgrupo in grupos:
            minimo=1000
            for grupo in subgrupo:
                actual = self.getLoc(grupo,nodosLoc)
                if actual < minimo:
                    minimo=actual
            print(minimo)
                # print(grupo)
        
        # print(grupos)
    def getLoc(self,idNodo, nodosLoc):
        minimo=1000
        for nodo in nodosLoc:
            if nodo[0]==idNodo[0]:
                actual = nodo[1]
                if actual < minimo:
                    minimo=actual
                    # print(idNodo[0],nodo[1],nodo[2])
            elif nodo[0]==idNodo[1]:
                actual = nodo[1]
                if actual < minimo:
                    minimo=actual
                    # print(idNodo[1],nodo[1],nodo[2])
        return minimo
    # Se va a tomar solo una etiqueta por el momento despues debe tomar dos una con numero y otra con texto
    def getEtiquetasAsociadasAlEquipo(self,idNodo,etiquetas,nodosAgrupados):
        datos = []
        for nodoA in nodosAgrupados:
            if idNodo==nodoA[0]:
                # print(idNodo,nodoA[0])
                _texto = self.getNombreEtiqueta(nodoA[1],etiquetas)
                datos.append(_texto)
        return datos

    def getXYNodo(self,idNodo, posicionXY):
        for nodo in posicionXY:
            #  print(nodo)
             if idNodo==nodo[0]:
                  xy=[nodo[1],nodo[2]*-1]
                  break
        return xy

    def getNombreEtiqueta(self,idNodo,etiquetas):
        texto = ""
        for etiqueta in etiquetas:
            if idNodo==etiqueta[0]:
                texto = etiqueta[3]
                break
        return texto    
    def getNombreConsecutivo(self,macro,index):
        _nombreMacro =""
        if  index<=9:
            _nombreMacro = f'{macro}00{index}'
        elif index>9 and index <=99:
            _nombreMacro = f'{macro}0{index}'
        else:
            _nombreMacro = f'{macro}{index}'
        return _nombreMacro
    def getEtiquetaCorta(self,etiquetas):  
        dato = ""
        minimoE=100
        tam=len(etiquetas)
        if tam==1:
            dato=etiquetas[0]
        else:
            for eti in etiquetas:
                tamano = len(eti)
                if tamano<minimoE:
                    dato=eti
                    minimoE=tamano
        return dato
                        
                    
                        
              
         
         

if __name__ == '__main__':
    PrincipalXML().run()