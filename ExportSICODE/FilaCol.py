class FilaCol(object):
    def __init__(self):
        super(FilaCol, self).__init__()
        self.minimoX=0
        self.maximoX=0
        self.minimoX=0
        self.maximoY=0
        self.tamanoPorColumn=0
        self.tamanoPorFila=0
    
    def calcula(self, equipos):
        equiposFilCol=[]
        ejeX=[]
        ejeY=[]
        for equipo in equipos:
            ejeX.append(equipo[1])
            ejeY.append(equipo[2])

        self.minimoX = min(ejeX)
        self.maximoX = max(ejeX)
        self.minimoY = min(ejeY)
        self.maximoY = max(ejeY)

        tamanoEjeX = 0
        if self.minimoX<0:
            tamanoEjeX=abs(self.minimoX)+self.maximoX
        self.tamanoPorColumn=tamanoEjeX/15  #Columnas
        tamanoEjeY=0

        if self.minimoY<0:
            tamanoEjeY=abs(self.minimoY)+self.maximoY
        self.tamanoPorFila=tamanoEjeY/5 # Filas

        # print(f' Para el eje x el minimo x {minimoX} y el maximo x: {maximoX}')
        # print(f' Para el eje y el minimo y { self.minimoY} y el maximo y: {self.maximoY}')

        columnas = map(self.getCol,ejeX)
        if  self.minimoY == self.maximoY: 
            filas = map(self.getFilaDefecto,ejeY)
        else: 
            filas = map(self.getFila,ejeY)

        listadoColumnas=list(columnas)
        listadoFilas=list(filas)
        i=0
        for equipo in equipos:
            equiposFilCol.append([equipo[0],listadoColumnas[i],listadoFilas[i]])
            print(f' Equipo {equipo[0]} columna {listadoColumnas[i]} fila {listadoFilas[i]}')
            i=i+1
        
        # for y in filas:
        #     print(f' Filas en el eje y {y}')
    def getCol(self,posX):
        colValue=0
        # print(posX)
        if posX<=0:
            valPositivo=abs(posX)
            dato=abs(self.minimoX)-abs(valPositivo)
            # print(f'{dato},{valPositivo},{minValue}')
            if dato==0:
                colValue=1
            else:
                if dato>0 and dato<=self.tamanoPorColumn:
                    colValue=1
                else:
                    val=dato/self.tamanoPorColumn
                    colValue=round(val)
            # colValue=abs(minValue)/tamCol
        else:
            colValue=round((posX+abs(self.minimoX))/self.tamanoPorColumn)
        return colValue
    
    def getFila(self,poxY):
        filaValue=0
        # print(posX)
        if poxY<=0:
            valPositivo=abs(poxY)
            dato=abs(self.minimoY)-abs(valPositivo)
            # print(f'{dato},{valPositivo},{minValue}')
            if dato==0:
                filaValue=1
            else:
                if dato>0 and dato<=self.tamanoPorFila:
                    filaValue=1
                else:
                    val=dato/self.tamanoPorFila
                    filaValue=round(val)
            # filaValue=abs(minValue)/tamCol
        else:
            filaValue=round((poxY+abs(self.minimoY))/self.tamanoPorFila)
        filaValue=filaValue+1
        return filaValue
        
    def getFilaDefecto(self,posY):
        return 3