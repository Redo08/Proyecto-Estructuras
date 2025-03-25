from src.models.arbol import Arbol
from src.models.plano import Plano
from src.models.area import Area  # Importa la clase Area
import copy
import math
class Utils:
    def __init__(self):
        
        pass
    
    def generar_arbol(self, lista_valores): #Lista de puntos que generan arbol y retorna un objeto arbol
        arbol = Arbol() #Creamos el arbol
        for i in lista_valores: #Recorremos los valores que se van a ingresar
            arbol.insertar(i[0], i[1])
        return arbol
    
    def generar_permutaciones(self, lista_valores, clasificador): #Retorna las permutaciones unicas
        permutaciones_all=[]
        self.permutar(lista_valores,[],permutaciones_all) #Saca todas las permutaciones
        return self.permutaciones_unique(permutaciones_all, clasificador)

    def es_valido_permutar(self,solucion): #Es valido
        return len(set(solucion)) == len(solucion) #Si no estan repetidos
    
    def es_viable_permutar(self,solucion, tamano_array):
        return len(solucion) <= tamano_array #Es viable cuando el tamaño de la solución es menor o igual al tamaño del array ingresado
    
    def permutar(self ,nums, solucion, array_resultado): #nums: Array inicial, solucion: Array vacio para cada solución individual, array_resultado: Array para las soluciones totales
        if self.es_valido_permutar(solucion):
            if self.es_viable_permutar(solucion, len(nums)):
                if len(nums) == len(solucion): #Caso Base cuando el tamaño de la solución es igual a la cantidad de datos ingresados
                    array_resultado.append(copy.deepcopy(solucion)) #Se necesita copiarlo asi, porque si no, se guarda es la referencia
                if math.factorial(len(nums)) == len(array_resultado): #Cuando el total de las permutaciones es igual al n! de la cantidad de datos
                    return True #Hacemos esto asi, para que se propague y termine apenas encuentre todas las permutaciones
                else:
                    for i in range(len(nums)): #Recorremos los datos
                        solucion.append(nums[i]) #Se agrega cada valor de la lista
                        if self.permutar(nums, solucion, array_resultado): #Hacemos llamados recursivos
                            return True
                        solucion.pop() #Se elimina para hacer el backtracking

  
    def permutaciones_unique(self,solucion, clasificador): # Sacamos las permutaciones unicas (No se repite la estructura del arbol)
        arboles_individuales=set([]) # Conjunto para evitar repetidos
        soluciones_unique=[] # Array en el que se van a almacenar soluciones unicas, se retorna
        for i in solucion: #Recorremos la lista de listas
            tamaño = len(arboles_individuales) #Se saca el tamaño del conjunto antes de insertar el siguiente arbol
            
            arbol = self.generar_arbol(i) # Generamos el arbol
            
            arboles_individuales.add(str(arbol.recorrido_preorden())) #Insertamos el recorrido preorden del arbol para el conjunto, asi verificamos todos los casos posibles sin repetición 
            
            if tamaño < len(arboles_individuales):  #Verificamos si al insertar el nuevo valor, si se aumenta el tamaño, por lo que es un arbol nuevo
                if clasificador == 0: #Arbol
                    soluciones_unique.append(copy.deepcopy(arbol))   #Vamos anexando soluciones ##PREGUNTA, MANDAMOS EL ARBOL O LA LISTA DE PUNTOS
                else: #Lista de puntos
                    soluciones_unique.append(copy.deepcopy(i))
                    
        return soluciones_unique
    
    # Permutaciones_unique que retorna arboles
    def permutaciones_unique_arbol(self, solucion_unicas_arboles):
        return self.generar_permutaciones(solucion_unicas_arboles, 0)
    
    # Permutaciones_unique que retorna lista de valores
    def permutaciones_unique_puntos(self, solucion_unicas_puntos):
        return self.generar_permutaciones(solucion_unicas_puntos, 1)
    
    
    def areas_optimas(self, listas_permutaciones_unique): # Lista de arboles únicos 
        area = []
        arbol_optimo = None
        index_final = 0
        index = 0
        for i in listas_permutaciones_unique:
            arbol = self.generar_arbol(i) #Insertamos los valores al arbol
            
            puntos_ordenados = arbol.recorrido_anchura_con_orientacion()
            
            plano = Plano(puntos_ordenados) #Creamos el plano
            
            lista_vertical, lista_horizontal = plano.generar_lineas()
            
            posibles_areas = plano.puntos_areas(lista_vertical, lista_horizontal)
            print("--------------------------------------------")
            print("Permutacion correspondiente", i)
            print("Areas posibles: ",posibles_areas)
            print("Tamaño areas posibles: ", len(posibles_areas))
            print("-------------------------------------------")
            if not area or len(posibles_areas) < len(area):
                area = posibles_areas
                arbol_optimo = arbol
                index_final = index

            index +=1
        
        lista_areas_optimas=self.lista_areas(area)
        
        
        print("El arbol optimo es:", arbol_optimo)
        print("El area final es:", area, "Con tamaño", len(area)) 
        return index_final, lista_areas_optimas
    
    def generar_todas_las_lineas_por_arbol(self, lista_de_arboles):
        """
        Genera una lista de listas de líneas, donde cada lista de líneas corresponde
        a un conjunto de puntos (que representa un árbol único).
        """
        
        todas_las_lineas =[]
        for arbol in lista_de_arboles:
            puntos_arbol = arbol.recorrido_anchura_con_orientacion() # Ajusta esto según el método correcto en tu clase Arbol
            plano = Plano(puntos_arbol) # Crear una instancia de Plano para cada conjunto de puntos
            plano.generar_lineas() # Generar las líneas para este conjunto de puntos
            todas_las_lineas.append(plano.lineas) # Guarda las líneas generadas para este conjunto de puntos
        return todas_las_lineas
    
    def lista_areas(self,lista_areas):
        areas=[]
        for area in lista_areas:
            limites=area[0]
            valor=area[1]
            area_obj=Area(limites,valor)
            areas.append(area_obj)
        return areas
