from src.models.arbol import Arbol
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
            
            arboles_individuales.add(( #Insertamos el recorrido preorden del arbol para el conjunto, asi verificamos todos los casos posibles sin repetición 
                tuple(map(tuple,(arbol.recorrido_preorden()))) 
            ))
            
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
    def cargar_datos_json (self, ruta_archivo):
        pass
    def validar_puntos_usuario(self, puntos):
        pass