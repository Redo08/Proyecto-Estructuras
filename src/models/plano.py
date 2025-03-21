from  linea import Linea, Punto

class Plano:
    def __init__(self, lista_puntos):
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.lineas = None #Es una lista que se calcula aqui
        self.puntos = lista_puntos
        self.areas = None #Es una lista que se calcula aqui
        
    def calcular_limites(self): 
        # puntos = [(2, 3, 0), (5, 7, 1), (8, 5, 0), (4, 6, 1),(7, 4, 1),(1,1,1),(3,3,1)]

    
        # El marco en realidad el minimo siempre seria 0
        marco_x = Punto([0, max(p[0] for p in self.puntos) + 1]) #(min, max) x
        marco_y = Punto([0, max(p[1] for p in self.puntos) + 1])# (min, max) y
        print(marco_x.posicion)
        print(marco_y.posicion)
    
    def generar_lineas(self):
        pass
    
    def generar_areas(self):
        pass
    
    def areas_optimas(self, listas_permutaciones_unique): # Lista de arboles únicos 
        pass # Retorna el arbol que genera menor cantidad de areas
    
    def interseccion_lineas(self):
        pass
    
# Para comprobar funciones
if __name__ == '__main__':
    plano = Plano([(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)])
    plano.calcular_limites()