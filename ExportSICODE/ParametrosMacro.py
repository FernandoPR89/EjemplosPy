import csv 
import pandas as pd
import pyodbc
import Modelo.Modelo as modelo
class ParametrosMacro(object):
    def __init__(self,indiceP,tipoUnifilar):
        super(ParametrosMacro, self).__init__()
        self.cnxn = pyodbc.connect("Driver={SQL Server};Server=.\SIMULADOR;UID=root;PWD=7054705470;Database=CONTROLCCD;")
        self.cuartoList = []
        self.octavoList = []
        self.indicePadre=indiceP
        self.mc_clave=""
        self.mc_id=""
        self.claveMCSig=""
        self.tipoUnifilar=tipoUnifilar

    def getParametros(self,mc_clave,mc_id,mc_ui):
        self.mc_clave=mc_clave
        self.mc_id=mc_id
        self.mc_ui=mc_ui #Asignado por el usuario
        self.claveMCSig=mc_clave+"011" #Obtener consecutivo
        self.tipoMacro(self.mc_clave)
        self.parametrosGenerales(self.mc_id)
        self.existenEqAsoc(self.mc_id)
        self.existenPHijos(self.mc_id)
        self.existenCambiosBool(self.mc_id)
        self.existenParametrosAdicionales(self.mc_clave,self.mc_id)
        self.existenParametrosZcar(self.mc_id)
        
        self.imprimeListaCuatro()
    
    def getParametrosCE(self,mc_clave,mc_id,mc_ui,clave_ce):
        self.clave_ce=clave_ce
        self.mc_clave=mc_clave
        self.mc_id=mc_id
        self.mc_ui=mc_ui #Asignado por el usuario
        self.claveMCSig=mc_clave+"011" #Obtener consecutivo
        self.tipoMacro(self.mc_clave)
        self.parametrosGenerales(self.mc_id)
        self.existenEqAsoc(self.mc_id)
        self.existenPHijos(self.mc_id)
        self.existenCambiosBool(self.mc_id)
        self.existenParametrosAdicionales(self.mc_clave,self.mc_id)
        self.existenParametrosZcar(self.mc_id)
        
        self.imprimeListaOctavo()

    def getUltimoIndice(self):
        return self.indicePadre
    
    def getCuartoListado(self):
        return self.cuartoList
    
    def getOctavoListado(self):
        return self.octavoList
    
    def imprimeListaCuatro(self):
        print("CUARTO LIST")
        for macro in self.cuartoList:
            print(macro.CVS, macro.MCI, macro.MUI,macro.MCC,macro.PRI,macro.VAL,macro.XML)

    def imprimeListaOctavo(self):
        print("OCTAVO LIST")
        for macro in self.octavoList:
            print(macro.CVC, macro.CEI,macro.MCI, macro.MUI,macro.MCC,macro.PRI,macro.VAL,macro.XML)

    def tipoMacro(self,mc_clave):
        df = pd.read_sql_query(f"SELECT MC_TIPO TMC, MC_ID MID FROM SCCD_C_MACROS WHERE MC_CLAVE='{mc_clave}'", self.cnxn)
        clase= df.at[0, 'TMC']
        if clase=='MacroControlSCCDBD':
            print(clase)       

    def parametrosGenerales(self,mc_id):
        print("--------- Parametros generales --------")
        df = pd.read_sql_query(f"SELECT B.PR_ID IDPR, B.PR_CLASE CLSE, B.PR_ETQTA ETQT, ISNULL(B.PR_VRBLE,'') VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID='{mc_id}'  AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PARAM'", self.cnxn)
        for  indicex,row in df.iterrows():
            idpr=row["IDPR"]
            clse = row["CLSE"]
            etqt= row["ETQT"]
            vble = row["VBLE"]
            vdef = row["VDEF"]
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            print(f'{idpr} {clse} {etqt} {vble} {vdef}')

    def existenEqAsoc(self,mc_id):
        # ***************** EXISTEN EQUIPOS ASOCIADOS *****************************************
        print("--------- EXISTEN EQUIPOS ASOCIADOS --------")
        df = pd.read_sql_query(f"SELECT B.PR_ID IDPR, B.PR_CLASE CLSE, B.PR_ETQTA ETQT, B.PR_VRBLE VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID ='{mc_id}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'EASO'", self.cnxn)
        for  indicex,row in df.iterrows():
            idpr=row["IDPR"]
            clse = row["CLSE"]
            etqt= row["ETQT"]
            vble = row["VBLE"]
            vdef = row["VDEF"]
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            print(f'{idpr} {clse} {etqt} {vble} {vdef}')
            
    def existenPHijos(self,mc_id):
        # ****************  EXISTEN PARÁMETROS HIJOS *****************************************
        print("--------- EXISTEN PARÁMETROS HIJOSS --------")
        df = pd.read_sql_query(f"SELECT B.PR_ID IDPR, B.PR_CLASE CLSE, B.PR_DESC PAT, B.PR_ETQTA ETQT, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID ='{mc_id}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PHIJO'", self.cnxn)
        for  indicex,row in df.iterrows():
            idpr=row["IDPR"]
            clse = row["CLSE"]
            etqt= row["PAT"]
            vble = row["ETQT"]
            vdef = row["VDEF"]
            if ('ICIRE' in etqt):
                etqt = etqt.replace("ICIRE", "" )
            if ('RESTE' in etqt):
                etqt = etqt.replace("RESTE", "" )

            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)

            print(f'{idpr} {clse} {etqt} {vble} {vdef}')

    def existenCambiosBool(self,mc_id):
        # ***************  EXISTEN CAMBIOS BOOLEANOS *****************************************
        print("--------- EXISTEN CAMBIOS BOOLEANOS --------")
        df = pd.read_sql_query(f"SELECT B.PR_ID IDPR, B.PR_CLASE CLSE, B.PR_ETQTA ETQT, B.PR_VRBLE VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID ='{mc_id}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'CBOOL'", self.cnxn)
        for  indicex,row in df.iterrows():
            idpr=row["IDPR"]
            clse = row["CLSE"]
            etqt= row["ETQT"]
            vble = row["VBLE"]
            vdef = row["VDEF"]
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,vble)
            print(f'{idpr} {clse} {etqt} {vble} {vdef}')

    def existenParametrosAdicionales(self,mc_clave,mc_id):
        cvmc='CRGE002'
        idmc='MC1006'

        print("--------- DETERMINAR LOS PARÁMETROS ACTIVOS PROPIOS DEL MACRO --------")
        df = pd.read_sql_query(f"SELECT '{mc_clave}'  MCVO, B.PR_ID IDPR, B.PR_CLASE CLSE, IIF(LEFT(B.PR_VRBLE,2)='PR',B.PR_ETQTA,IIF(LEFT(B.PR_VRBLE,4)='ZCAR',B.PR_ETQTA,CONCAT(B.PR_VRBLE,'.',B.PR_ETQTA))) ETQT, B.PR_VRBLE VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID ='{mc_id}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PADIC'", self.cnxn)
        for  indicex,row in df.iterrows():
            mcvo=row["MCVO"]
            idpr = row["IDPR"]
            clse= row["CLSE"]
            etqt = row["ETQT"]
            vble= row["VBLE"]
            vdef = row["VDEF"]
            print(f'{mcvo} {idpr} {clse} {etqt} {vble} {vdef}')
            if ('PARS' in etqt):
                etqt = etqt.replace("Subsistema", "Valor" )
            if ('PARF' in etqt):
                etqt = etqt.replace("Voltaje_Nominal", "Valor" )

            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)

    # SELECT PARA DETERMINAR LOS MACROS ELÉCTRICOS ACTIVOS AGREGADOS
        print("--------- DETERMINAR LOS MACROS ELÉCTRICOS ACTIVOS AGREGADOS --------")
        df = pd.read_sql_query(f"SELECT B.MC_ID IDMC, A.EC_CLAVE CVMC, B.MC_DIAG_TIPO TDG FROM SCCD_R_MAC_ELE_CTR A, SCCD_C_MACROS B WHERE A.MC_ID = '{mc_id}' AND EC_ESTADO = 'A' AND B.MC_CLAVE = LEFT(A.EC_CLAVE,LEN(A.EC_CLAVE)-3)", self.cnxn)
        for  indicex,row in df.iterrows():
            idmc=row["IDMC"]
            cvmc = row["CVMC"]
            tdg= row["TDG"]
            print(f'{idmc} {cvmc} {tdg}')
            self.parametrosPropiosMacroAgregado(cvmc,idmc)
            if 'CRGE' in cvmc:
                self.agregaCargaElectrica(cvmc)

    # SE DETERMINAN LOS PARAMETROS PROPIOS DEL MACRO ELECTRICO QUJE SE AGREGA
    def agregaCargaElectrica(self,cvmc):
        mcct ='MC1005' #Obtener el ID del macrocontrol de carga electrica trifasico 
        # Si es una carga electrica CRGE O FTRE se agrega su control
        print("--------- SE AGREGA LA CARGA ELECTRICA SI ES CRGE O FTRE --------")
        df = pd.read_sql_query(f"SELECT '{cvmc}' MCVO, B.PR_ID IDPR, B.PR_CLASE CLSE, CONCAT('{cvmc}.CRGC017.',B.PR_VRBLE,'.',B.PR_ETQTA) ETQT, B.PR_VRBLE VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID = '{mcct}' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PADIC'", self.cnxn)
        for  indicex,row in df.iterrows():
            mcvo=row["MCVO"]
            idpr = row["IDPR"]
            clse= row["CLSE"]
            etqt = row["ETQT"]
            vble= row["VBLE"]
            vdef= row["VDEF"]
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,mcvo,idpr,vdef,etqt)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,mcvo,idpr,vdef,etqt)
            print(f'{mcvo} {idpr} {clse} {etqt} {vble} {vdef}')
            
    def parametrosPropiosMacroAgregado(self,cvmc,idmc):
        print("--------- SE DETERMINAN LOS PARAMETROS PROPIOS DEL MACRO ELECTRICO QUE SE AGREGA --------")
        df = pd.read_sql_query(f"SELECT '{cvmc}' MCVO, B.PR_ID IDPR, B.PR_CLASE CLSE, IIF(LEFT(B.PR_VRBLE,2)='PR',CONCAT('{cvmc}.',B.PR_ETQTA),IIF(LEFT(B.PR_VRBLE,4)='ZCAR',CONCAT('{cvmc}.',B.PR_ETQTA),CONCAT('{cvmc}.',B.PR_VRBLE,'.',B.PR_ETQTA))) ETQT, B.PR_VRBLE VBLE, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID = '{idmc}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PADIC'", self.cnxn)
        for  indicex,row in df.iterrows():
            mcvo=row["MCVO"]
            idpr = row["IDPR"]
            clse= row["CLSE"]
            etqt = row["ETQT"]
            vble= row["VBLE"]
            vdef= row["VDEF"]
            if ('PARF' in etqt):
                etqt = etqt.replace("Factor_Participacion", "Valor" )
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,mcvo,idpr,vdef,etqt)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,mcvo,idpr,vdef,etqt)
            print(f'{mcvo} {idpr} {clse} {etqt} {vble} {vdef}')

    def existenParametrosZcar(self,MC_ID):
        #EXISTEN PARÁMTEROS ADICIONALES POR ZCAR
        print("--------- EXISTEN PARÁMTEROS ADICIONALES POR ZCAR --------")
        df = pd.read_sql_query(f"SELECT B.PR_ID IDPR, B.PR_CLASE CLSE, B.PR_ETQTA ETQT, ISNULL(B.PR_VALDEF,'') VDEF FROM SCCD_M_MAC_PARAM_REPOR A, SCCD_C_PARAM_REPOR B WHERE A.MC_ID='{MC_ID}' AND A.MR_ESTADO = 'A' AND A.PR_ID = B.PR_ID AND B.PR_CLASE = 'PZCAR'", self.cnxn)
        for  indicex,row in df.iterrows():
            idpr = row["IDPR"]
            clse= row["CLSE"]
            etqt = row["ETQT"]
            vdef = row["VDEF"]
            if  self.tipoUnifilar=="SE":
                self.guardarEnListaCuarto(self.indicePadre,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)
            else:
                self.guardarEnListaOctavo(self.indicePadre,self.clave_ce,self.mc_id,self.mc_ui,self.claveMCSig,idpr,vdef,etqt)
            print(f'{idpr} {clse} {etqt} {vdef}')

    def guardarEnListaCuarto(self,cvs,mci,mui,mcc,pri,val,xml):
            itemCuarto = modelo.SubCuarto(cvs,mci,mui,mcc,pri,val,xml)
            self.cuartoList.append(itemCuarto)
            self.indicePadre=self.indicePadre+1

    def guardarEnListaOctavo(self,cvc,cei,mci,mui,mcc,pri,val,xml):
            itemOctavo = modelo.SubOctavo(cvc,cei,mci,mui,mcc,pri,val,xml)
            self.octavoList.append(itemOctavo)
            self.indicePadre=self.indicePadre+1

        # self.cnxn = pyodbc.connect("Driver={SQL Server};Server=.\SIMULADOR;UID=root;PWD=7054705470;Database=CONTROLCCD;")
        # df = pd.read_sql_query(f"SELECT PR_ID FROM SCCD_M_MAC_PARAM_REPOR WHERE MC_ID='{mci}' AND MR_ESTADO='A'", self.cnxn)
        # df.head()
        
        # for  indicex,row in df.iterrows():
        #     pri=row["PR_ID"]
        #     df2 = pd.read_sql_query(f"SELECT PR_VRBLE, PR_VALDEF FROM SCCD_C_PARAM_REPOR WHERE PR_ID='{pri}'", self.cnxn)
        #     df2.head()
        #     # print(df2)
        #     for indicey, row2 in df2.iterrows():
        #         val=row2["PR_VALDEF"]
        #         variable=row2["PR_VRBLE"]
        #         print(f'{pri} -{variable} - {val}')
