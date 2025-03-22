from  src.models.linea import Linea, Punto
from  src.models.arbol import Arbol
import matplotlib.pyplot as plt

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
        
        marco_superior = max(marco_x.posicion[1], marco_y.posicion[1])
        self.x_min = marco_x.posicion[0]
        self.x_max = marco_superior
        self.y_min = marco_y.posicion[0]
        self.y_max = marco_superior

    
    def generar_lineas(self):
        self.calcular_limites() # Para sacar limites del plano
        lineas_h = []  # (valor_y, x_inicio, x_fin)
        lineas_v = []  # (valor_x, y_inicio, y_fin)
        lineas_totales = []
        
        puntos = self.puntos #Sacamos el array de puntos
         
        #Definir limites de las rectas
        for i in puntos:
            x, y, alineacion = i[0], i[1], i[2] #Sacamos los valores de cada punto
            #Empezamos por las lineas verticales
            if alineacion == 0:
                y_inicio, y_final = self.y_min, self.y_max
                for j in lineas_h: #Recorremos lineas horizontales para encontrar choque
                    valor_y, x_inicio_linea_2, x_final_linea_2 = j[0], j[1], j[2]
                    if x_inicio_linea_2 < x < x_final_linea_2: #Si la recta esta dentro del rango de la otra linea
                        #Donde esta? 
                        #Arriba
                        if y > valor_y:
                            y_inicio = valor_y
                        
                        #Abajo
                        if y < valor_y:
                            y_final = valor_y

                        
                lineas_v.append((x,y_inicio, y_final))
                lineas_totales.append(((x,y),(x, y_inicio), (x, y_final)))

            #Empezamos las lineas horizontales
            else: #Alineacion igual a 1     
                x_inicio, x_final = self.x_min, self.x_max #Definimos los limites de la linea
                for j in lineas_v:
                    valor_x, y_inicio_linea_2, y_final_linea_2 = j[0], j[1], j[2]
                    if y_inicio_linea_2 < y < y_final_linea_2: #Si la linea esta dentro del rango de la otra
                        #Donde?
                        #Izquierda
                        if x < valor_x:
                            x_final = valor_x #Si esta en la izquierda, cambia el final
                        
                        #Derecha
                        if x > valor_x:
                            x_inicio = valor_x #Si esta a la derecha, se cambia el inicio

                        #En el mismo lugar
                        else:
                            pass #No cambia nada y se mantienen los limites
                lineas_h.append((y, x_inicio, x_final))
                lineas_totales.append(((x,y),(y, x_inicio), (y, x_final)))
                
        return lineas_totales
    
    def generar_areas(self):
        pass
    
    def areas_optimas(self, listas_permutaciones_unique): # Lista de arboles únicos 
        pass # Retorna el arbol que genera menor cantidad de areas
    
    def interseccion_lineas(self):
        pass
    
