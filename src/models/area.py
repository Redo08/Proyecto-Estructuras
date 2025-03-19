class Area:
    def __init__(self):
        pass
    
    puntos = [(2, 3, 0), (5, 7, 1), (8, 5, 0), (4, 6, 1),(7, 4, 1),(1,1,1),(3,3,1)]
    
    marco_x = Punto([min(p[0] for p in puntos), max(p[0] for p in puntos)]) #(min, max) x
    marco_y = Punto([min(p[1] for p in puntos), max(p[1] for p in puntos)])# (min, max) y
    
    print(marco_x.posicion)
    print(marco_y.posicion)
    
    def calcular_Plano(self, lista_puntos): 
        pass

class Plano:
    def __init__(self):
        pass
    