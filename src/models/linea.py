class Punto:
    def __init__(self, posicion): # Se recibe posicion y alineacion inicial de cada punto
        self.posicion = (posicion[0],posicion[1]) #Sacamos valores x, y
    
    def movimiento(self):
        pass
        
class Linea:
    def __init__(self, punto_posicion, orientacion):
        self.punto_inicial = None #PREGUNTAR ES ASI O SERIA COMO LO TENIAMOS ANTES, ANTES SIENDO QUE ESTABA PUNTO INICIAL Y FINAL COMO PARAMETRO Y LO AGREGABAMOS DIRECTAMENTE AHI
        self.punto_final = None
        self.punto_posicion = punto_posicion 
        self.orientacion = orientacion
        
    def interseccion():
        pass
    
    def limites():
        pass
    
