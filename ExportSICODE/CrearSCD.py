import Modelo.Modelo as modelo
class CrearSCD:
    def __init__(self,nombre):
        super(CrearSCD, self).__init__()
        self.NombreArchivo=nombre
        self.Contenido=[]
        #self.NombreArchivo = nombreArchivo
        # self.NombreArchivo = "Ejemplo.scd"
        # self.Abrev="LCH"
        # self.VNM=13.8
        # self.VNA=115
        # self.PAN=100
        # self.FRE=60
        # self.LRW=-1
        # self.LRH=-1

        # segundoList = []
        # terceroList = []
        # cuartoList = []
        # quintoList = []
        # sextoList = []
        # septimoList = []
        # octavoList = []
        # novenoList = []
        # decimoList = []

        # primero = modelo.Primero(self.NombreArchivo,self.Abrev,self.VNM,self.VNA,self.PAN,self.FRE,self.LRW,self.LRH)

        # itemSegundo = modelo.SubSegundo(1,"CE0360","04075","04075","01",self.VNM,self.VNA,self.PAN,self.FRE,self.LRW,self.LRH)
        # segundoList.append(itemSegundo)
        # segundoList.append(itemSegundo)

        # itemTercero = modelo.SubTercero(1,"MC0008","FREC","PARF008","",1,12,-1,-1)
        # terceroList.append(itemTercero)
        # terceroList.append(itemTercero)

        # itemCuarto = modelo.SubCuarto(1,"MC1022","FALME3","FALME016","PR0011","FALME3","ETQT")
        # cuartoList.append(itemCuarto)
        # cuartoList.append(itemCuarto)

        # itemQuinto = modelo.SubQuinto(1,"MC1026","FVOLE4","MR1089","MR1173","72010","MC1047")
        # quintoList.append(itemQuinto)
        # quintoList.append(itemQuinto)

        # # itemSexto = modelo.SubSexto(1,"","","","","","")
        # # sextoList.append(itemSexto)
        # # sextoList.append(itemSexto)

        # itemSeptimo = modelo.SubSeptimo(1,"CE0360","MC0005","04075","VIRT036",5,3,"SELCH.ICIRE014",-1,-1)
        # septimoList.append(itemSeptimo)
        # septimoList.append(itemSeptimo)

        # itemOctavo = modelo.SubOctavo(1,"CE0360","MC0005","04075","VIRT036","PR0032","04075","ETQT")
        # octavoList.append(itemOctavo)
        # octavoList.append(itemOctavo)

        # itemNoveno = modelo.SubNoveno(1,"CE0360","MC0005","04075","MR1130","MR1023","CRGE4","MC1006")
        # novenoList.append(itemNoveno)
        # novenoList.append(itemNoveno)

        # segundo = modelo.Segundo(len(segundoList),segundoList)
        # tercero = modelo.Tercero(len(terceroList),terceroList)
        # cuarto = modelo.Cuarto(len(cuartoList),cuartoList)
        # quinto = modelo.Quinto(len(quintoList),quintoList)
        # sexto = modelo.Sexto(len(sextoList),sextoList)
        # septimo = modelo.Septimo(len(septimoList),septimoList)
        # octavo = modelo.Octavo(len(octavoList),octavoList)
        # noveno = modelo.Noveno(len(novenoList),novenoList)
        # decimo = modelo.Decimo(len(decimoList),decimoList)

        # self.createOne(primero,segundo,tercero,cuarto,quinto,sexto,septimo,octavo,noveno,decimo)

    def crearArchivo(self,primero,segundo,tercero,cuarto,quinto,sexto,septimo,octavo,noveno,decimo):
        self.cargaPrimero(primero)
        self.cargaSegundo(segundo)
        self.cargaTercero(tercero)
        self.cargaCuarto(cuarto)
        self.cargaQuinto(quinto)
        self.cargaSexto(sexto)
        self.cargaSeptimo(septimo)
        self.cargaOctavo(octavo)
        self.cargaNoveno(noveno)
        self.cargaDecimo(decimo)
        self.saveFile()

    # PRIMERO, SE INSERTAN LOS DATOS GENERALES DE LA SUBESTACIÓN ELÉCTRICA
    def cargaPrimero(self,prim):
        self.Contenido.append(f"SED:{prim.Nombre},SEC:{prim.Abrev},VNM:{prim.VNM},VNA:{prim.VNA},PAN:{prim.PAN},FRE:{prim.FRE},LRW:{prim.LRW},LRH:{prim.LRH}/\n")
    
    # SEGUNDO, SE INSERTAN TODOS LOS CIRCUITOS ELÉCTRICOS ASOCIADOS A LA SUBESTACIÓN
    def cargaSegundo(self,seg):
        self.Contenido.append(f"NCE:{seg.NCE} (NÚMERO DE CIRCUITOS ELÉCTRICOS)/\n")
        if seg.NCE>0:
            for item in seg.SegundoList:
                self.Contenido.append(f"CCE:{item.CCE},CEI:{item.CEI},CED:{item.CED},CEC:{item.CEC},CLA:{item.CLA},VNM:{item.VNM},VNA:{item.VNA},PAN:{item.PAN},FRE:{item.FRE},LRW:{item.LRW},LRH:{item.LRH}/\n")
    
    # TERCERO, SE INSERTAN TODOS LOS MACROS ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA (QUE NO SEAN DEL TIPO COSA O COEN)
    def cargaTercero(self,ter):
        self.Contenido.append(f"NMS:{ter.NMS} (NÚMERO DE COMPONENTES ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA)/\n")
        if ter.NMS>0:
            for item in ter.TerceroList:
                self.Contenido.append(f"CMS:{item.CMS},MCI:{item.MCI},MUI:{item.MUI},MCC:{item.MCC},FIL:{item.FIL},COL:{item.COL},DES:{item.DES},CVX:{item.CVX},CVY:{item.CVY}/\n")
    
    # CUARTO, SE INSERTAN LOS PARÁMETROS DE LOS MACROS ASOCIADOS A LA SUBETACIÓN ELÉCTRICA (QUE NO SEAN DEL TIPO COSA O COEN) 
    def cargaCuarto(self,cuarto):
        self.Contenido.append(f"NVS:{cuarto.NVS} (NÚMERO DE VALORES DE LOS COMPONENTES ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA)/\n")
        if cuarto.NVS>0:  
            for item in cuarto.CuartoList:
                self.Contenido.append(f"CVS:{item.CVS},MCI:{item.MCI},MUI:{item.MUI},MCC:{item.MCC},PRI:{item.PRI},VAL:{item.VAL},XML:{item.XML}/\n")

    # QUINTO, SE INSERTAN LAS CONEXIONES DE LOS MACROS ASOCIADOS A LA SUBETACIÓN ELÉCTRICA (QUE NO SEAN DEL TIPO COSA O COEN)
    def cargaQuinto(self,quinto):
        self.Contenido.append(f"NCS:{quinto.NCS} (NÚMERO DE CONEXIONES DE LOS COMPONENTES ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA)/\n")
        if quinto.NCS>0:   
            for item in quinto.QuintoList:
                self.Contenido.append(f"CCS:{item.CCS},MCI:{item.MCI},MUI:{item.MUI},MRI:{item.MRI},MRD:{item.MRD},MUD:{item.MUD},MCD:{item.MCD}/\n")
    
    # SEXTO, SE INSERTAN LAS ETIQUETAS Y CONECTORES ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA
    def cargaSexto(self,sexto):
        self.Contenido.append(f"NAS:{sexto.NAS} (NÚMERO DE ELEMENTOS ADICIONALES ASOCIADOS A LA SUBESTACIÓN ELÉCTRICA)/\n")
        if sexto.NAS>0:        
            for item in sexto.SextoList:
                self.Contenido.append(f"CAS:{item.CAS},MCI:{item.MCI},MUI:{item.MUI},MCS:{item.MCS},VTI:{item.VTI},CVI:{item.CVI},CVX:{item.CVX},CVY:{item.CVY},LRG:{item.LRG},DCN:{item.DCN}/\n")

    # SÉPTIMO, SE INSERTAN TODOS LOS MACROS ASOCIADOS A LOS CIRCUITOS (QUE NO SEAN DEL TIPO COSA O COEN)
    def cargaSeptimo(self,septimo):
        self.Contenido.append(f"NMC:{septimo.NMC} (NÚMERO DE COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/\n")
        if septimo.NMC>0:
            for item in septimo.SeptimoList:
                self.Contenido.append(f"CMC:{item.CMC},CEI:{item.CEI},MCI:{item.MCI},MUI:{item.MUI},MCC:{item.MCC},FIL:{item.FIL},COL:{item.COL},DES:{item.DES},CVX:{item.CVX},CVY:{item.CVY}/\n")

    # OCTAVO, SE INSERTAN LOS PARÁMETROS DE LOS MACROS ASOCIADOS AL CIRCUITO ELÉCTRICO (QUE NO SEAN DEL TIPO COSA O COEN)
    def cargaOctavo(self,octavo):
        self.Contenido.append(f"NVC:{octavo.NVC} (NÚMERO DE VALORES DE LOS COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/\n")
        if octavo.NVC>0:
            for item in octavo.OctavoList:
                self.Contenido.append(f"CVC:{item.CVC},CEI:{item.CEI},MCI:{item.MCI},MUI:{item.MUI},MCC:{item.MCC},PRI:{item.PRI},VAL:{item.VAL},XML:{item.XML}/\n")

    # NOVENO, SE INSERTAN LAS CONEXIONES DE LOS MACROS ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS (QUE NO SEAN DEL TIPO COSA O COEN)
    def cargaNoveno(self,noveno):
        self.Contenido.append(f"NCC:{noveno.NCC} (NÚMERO DE CONEXIONES DE LOS COMPONENTES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/\n")
        if noveno.NCC>0:
            for item in noveno.NovenoList:
                self.Contenido.append(f"CCC:{item.CCC},CEI:{item.CEI},MCI:{item.MCI},MUI:{item.MUI},MRI:{item.MRI},MRD:{item.MRD},MUD:{item.MUD},MCD:{item.MCD}/\n")
    
    # DÉCIMO, SE INSERTAN LAS ETIQUETAS Y CONECTORES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS
    def cargaDecimo(self,decimo):
        self.Contenido.append(f"NAC:{decimo.NAC} (NÚMERO DE ELEMENTOS ADICIONALES ASOCIADOS A LOS CIRCUITOS ELÉCTRICOS)/\n")
        if decimo.NAC>0:
            for item in decimo.DecimoList:
                self.Contenido.append(f"CAC:{item.CAC},CEI:{item.CEI},MCI:{item.MCI},MUI:{item.MUI},MCS:{item.MCS},VTI:{item.VTI},CVI:{item.CVI},CVX:{item.CVX},CVY:{item.CVY},LRG:{item.LRG},DCN:{item.DCN}/\n")
    
    def saveFile(self):
        self.Contenido.append("FAD/")
        with open(self.NombreArchivo, "w") as file:
            file.writelines(self.Contenido)