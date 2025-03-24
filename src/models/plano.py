from  src.models.linea import Linea, Punto
from  src.models.arbol import Arbol
import copy
import math

class Plano:
    def __init__(self, lista_puntos):
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None
        self.lineas = None #Es una lista que se calcula aqui ##########Lo ponemos ya como atributo?
        self.puntos = lista_puntos
        self.areas = None #Es una lista que se calcula aqui
        
    def calcular_limites(self): 
    
        # El marco en realidad el minimo siempre seria 0
        marco_x = Punto([0, max(p[0] for p in self.puntos)+1]) #(min, max) x
        marco_y = Punto([0, max(p[1] for p in self.puntos)+1])# (min, max) y 
        
        # Y el maximo siempre seria el maximo de los 2, x o y
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
         
        #Insertamos las lineas iniciales del plano
        lineas_h.append((0, 0, self.x_max)) #Linea a lo largo del eje x
        lineas_v.append((0, 0, self.y_max)) #Linea a lo largo del eje y
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

                lineas_h.append((y, x_inicio, x_final)) 
                lineas_totales.append(((x,y),(x_inicio, y), (x_final, y)))
        
        #Agregamos al final las lineas que cierran el plano
        lineas_h.append((self.y_max, 0, self.x_max)) #Linea a lo largo del tope del plano
        lineas_v.append((self.x_max, 0, self.y_max)) # Linea a largo del final del plano
        lineas_h.sort() #Las ordenamos de menor a mayor
        lineas_v.sort() #Las ordenamos de menor a mayor
        self.lineas = lineas_totales
        return lineas_v, lineas_h
    
    def puntos_interseccion_lineas_areas(self, lineas_v, lineas_h):
        esquinas = [] #Esquinas de cada area
        esquinas_set = set([]) #Para evitar repetidos
        #Sacamos 2 lineas verticales(Como la lista esta ordenada no hay problema)
        
        #Primera Linea vertical
        for i in range(len(lineas_v)-1): #Hasta el penultimo para evitar salirnos de la lista
            x1, y_inicio1, y_final1 = lineas_v[i] 

            #Segunda Linea vertical
            for k in range(i+1, len(lineas_v)):
                x2, y_inicio2, y_final2 = lineas_v[k]
                
                #Sacamos 2 lineas horizontales
                
                #Primera linea horizontal
                for j in range(len(lineas_h)-1):
                    y1, x_inicio1, x_final1 = lineas_h[j]
                    
                    #Segunda linea horizontal
                    for z in range(j+1,len(lineas_h)):
                        y2, x_inicio2, x_final2 = lineas_h[z]

                        #Si las horizontales estan  entre el rango de  las 2 verticales
                        if (y_inicio1 <= y1 <= y_final1 and y_inicio1 <= y2 <= y_final1) and (y_inicio2 <= y1 <= y_final2 and y_inicio2 <= y2 <= y_final2):
                           # Si las verticales estan dentro del rango de las horizontales
                           if (x_inicio1 <= x1 <= x_final1 and x_inicio1 <= x2 <= x_final1) and (x_inicio2 <= x1 <= x_final2 and x_inicio2 <= x2 <= x_final2):
                                puntos_area = [(x1, y2), (x2, y2), (x2,y1), (x1, y1)] #Puntos de las esquinas del area
                                
                                solucion = frozenset(puntos_area) #Metemos los puntos a un conjunto inmutable para evitar repetidos
                                if solucion not in esquinas_set: #Si no esta repetido, lo agrega
                                    esquinas.append(puntos_area)
                                    esquinas_set.add(solucion)
        return esquinas
        
        
    def filtrar_areas(self, areas): #Areas seria el array de esquinas
        areas_perfectas = [] #Solución a retornr
        lista_areas = [(puntos, self.generar_areas(puntos)) for puntos in areas] # Creamos una lista que tiene como valores una tupla, siendo la primera los puntos de las esquinas, y de segundo valor el area correspondiente a ese espacio
        lista_areas.sort(key=lambda x: x[1], reverse=True) # Organiza la lista de mayor a menor. Toma el segundo valor para organizar, y el reverse es el que hace que sea de mayor a menor
            
        #Recorremos la lista
        for i in range(len(lista_areas)):
            #Area 1, sacamos los limites
            area_1 = lista_areas[i][0]
            min_x_1 = min(area_1[0][0], area_1[1][0], area_1[2][0], area_1[3][0]) #La minima componente en x
            max_x_1 = max(area_1[0][0], area_1[1][0], area_1[2][0], area_1[3][0]) #La maxima componente en x
            min_y_1 = min(area_1[0][1], area_1[1][1], area_1[2][1], area_1[3][1]) #La minima componente en y
            max_y_1 = max(area_1[0][1], area_1[1][1], area_1[2][1], area_1[3][1]) #La maxima componente en y
            
            #Creamos una variable booleana para despues hacer el filtrado
            es_contenedor = False
            
            for j in range(i+1,len(lista_areas)): #Se hace asi para que no se compruebe con el mismo
                
                #Area 2, sacamos los limites
                area_2 = lista_areas[j][0]
                min_x_2 = min(area_2[0][0], area_2[1][0], area_2[2][0], area_2[3][0]) #La minima componente en x    
                max_x_2 = max(area_2[0][0], area_2[1][0], area_2[2][0], area_2[3][0]) #La maxima componente en x
                min_y_2 = min(area_2[0][1], area_2[1][1], area_2[2][1], area_2[3][1]) #La minima componente en y
                max_y_2 = max(area_2[0][1], area_2[1][1], area_2[2][1], area_2[3][1]) #La maxima componente en y
                
                #Validación
                if min_x_1 <= min_x_2 and max_x_2 <= max_x_1 and min_y_1 <= min_y_2 and  max_y_2 <= max_y_1: #Si el area uno tiene sus limites conteniendo el area 2
                    es_contenedor = True #Se asigna como contenedor y se sale
                    break
                
            if not es_contenedor: #Si no es contenedor, se agrega
                areas_perfectas.append(copy.deepcopy(lista_areas[i]))    
        return areas_perfectas 
    
    
    def distancia_entre_puntos(self, punto_1, punto_2): #Recibe los 2 puntos
        return math.sqrt((punto_1[0] - punto_2[0])**2 + (punto_1[1] - punto_2[1])**2) #Formula de distancia euclediana
        
    def generar_areas(self, puntos_area):
        #Sacar puntos necesarios
        largo = self.distancia_entre_puntos(puntos_area[0], puntos_area[1]) #Se saca el largo
        ancho = self.distancia_entre_puntos(puntos_area[1], puntos_area[2]) #Se saca el ancho

        return largo*ancho
    
    def puntos_areas(self, lineas_v, lineas_h): #Función llamada por el usuario
        esquinas_sin_filtro = self.puntos_interseccion_lineas_areas(lineas_v, lineas_h) #Saca todas las esquinas

        return self.filtrar_areas(esquinas_sin_filtro) #Devuelve solo las que si son
    
    
