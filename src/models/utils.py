from src.models.arbol import Arbol
import copy
import math
class Utils:
    def __init__(self):
        pass
    
    def generar_arbol(lista_valores): #Lista de puntos que generan arbol y retorna un objeto arbol
        pass
    
    
    def generar_permutaciones(self, lista_valores): #Retorna las permutaciones unicas
        permutaciones_all=[]
        self.permutar(lista_valores,[],permutaciones_all) #Saca todas las permutaciones
        return self.permutaciones_unique(permutaciones_all)

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

    def permutaciones_unique(self,solucion): # Sacamos las permutaciones unicas (No se repite la estructura del arbol)
        arboles_individuales=set([]) # Conjunto para evitar repetidos
        soluciones_unique=[] # Array en el que se van a almacenar soluciones unicas, se retorna
        for i in solucion: #Recorremos la lista de listas
            arbol = Arbol() #Se tiene que crear un nuevo arbol para cada uno
            tamaño = len(arboles_individuales) #Se saca el tamaño del conjunto antes de insertar el siguiente arbol
            for j in i: # Recorremos cada conjunto de puntos de la lista
                arbol.insertar(j[0], j[1])  #Se recorre la sublista y se sacan los valores x, y
            arboles_individuales.add(( #Insertamos el recorrido preorden del arbol para el conjunto, asi verificamos todos los casos posibles sin repetición 
                tuple(map(tuple,(arbol.recorrido_preorden()))) 
            ))
            if tamaño < len(arboles_individuales): #Verificamos si al insertar el nuevo valor, si se aumenta el tamaño, por lo que es un arbol nuevo
                soluciones_unique.append(copy.deepcopy(arbol))   #Vamos anexando soluciones ##PREGUNTA, MANDAMOS EL ARBOL O LA LISTA DE PUNTOS
                        
        return soluciones_unique
    