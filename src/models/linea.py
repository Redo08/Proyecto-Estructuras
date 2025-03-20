class Punto:
    def __init__(self, posicion): # Se recibe posicion y alineacion inicial de cada punto
        self.posicion = (posicion[0],posicion[1]) #Sacamos valores x, y
    
    def movimiento(self): #Para cuando el usuario mueva un punto de la interfaz  ??????????? Se pone en el plano
        pass
        
class Linea:
    def __init__(self,  punto_inicial, punto_posicion, punto_final, orientacion):
        self.punto_inicial = punto_inicial 
        self.punto_posicion = punto_posicion 
        self.punto_final = punto_final
        # self.orientacion = orientacion ###???? Se puede obviar, puesto que se puede graficar con 2 puntos o más
        
    
    
