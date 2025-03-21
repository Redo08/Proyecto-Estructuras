from  linea import Linea, Punto
from  arbol import Arbol
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
        print(marco_x.posicion)
        print(marco_y.posicion)
        return marco_x, marco_y
       
    
    def generar_lineas(self):
        lineas_h = []  # (y, x_inicio, x_fin)
        lineas_v = []  # (x, y_inicio, y_fin)

        # Dibujar líneas con detección de intersecciones
        for x, y, alineacion in self.puntos:
            print(lineas_h)
            print(lineas_v)
            
            if alineacion == 0:  # Línea horizontal
                x
                # Verificar intersección con líneas verticales
                for lx, ly1, ly2 in lineas_v:
                    if ly1 <= y <= ly2:
                        if lx < x:
                            x_start = max(x_start, lx)
                        if lx > x:
                            x_end = min(x_end, lx)
                lineas_h.append((y, x_start, x_end))
                plt.pause(1)
                plt.plot([x_start, x_end], [y, y], color='blue', linestyle='--')
                
            else:  # Línea vertical
                y_start, y_end = min_y, max_y
                # Verificar intersección con líneas horizontales
                for ly, lx1, lx2 in lineas_h:
                    if lx1 <= x <= lx2:
                        if ly < y:
                            y_start = max(y_start, ly)
                        if ly > y:
                            y_end = min(y_end, ly)
                lineas_v.append((x, y_start, y_end))
                plt.pause(1)
                plt.plot([x, x], [y_start, y_end], color='green', linestyle='--')
    
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