
import math
import copy
from src.arbol import Arbol

class Optimizador:
    def __init__(self,listapuntos):
        self.puntos=listapuntos
        
    def generar_permutaciones(self):
        permutaciones_all=[]
        self.permutar(self.puntos,[],permutaciones_all)
        return self.permutaciones_unique(permutaciones_all)

    def es_valido_permutar(self,solucion): #Es valido
        return len(set(solucion)) == len(solucion) #Si no estan repetidos
    
    def es_viable_permutar(self,solucion, tamano_array):
        return len(solucion) <= tamano_array
    
    def permutar(self ,nums, solucion, array_resultado): #nums: Array inicial, solucion: Array vacio para cada solución individual, array_resultado: Array para las soluciones totales
        if self.es_valido_permutar(solucion):
            if self.es_viable_permutar(solucion, len(nums)):
                if len(nums) == len(solucion):
                    array_resultado.append(copy.deepcopy(solucion)) #Se necesita copiarlo asi, porque si no, se guarda es la referencia
                if math.factorial(len(nums)) == len(array_resultado):
                    return True
                else:
                    for i in range(len(nums)):
                        solucion.append(nums[i]) #Se agrega cada valor de la lista
                        if self.permutar(nums, solucion, array_resultado):
                            return True
                        solucion.pop()

    def permutaciones_unique(self,solucion):
        arboles_individuales=set([]) ##Conjunto para evitar repetidos
        soluciones_unique=[]
        for i in solucion:
            arbol = Arbol() #Se tiene que crear un nuevo arbol para cada uno
            tamaño = len(arboles_individuales) #Se saca el tamaño del conjunto antes de insertar el siguiente arbol
            for j in i:
                arbol.insertar(j[0], j[1])  #Se recorre la sublista y se sacan los valores x, y
            arboles_individuales.add(( #Insertamos los recorridos inorden y preorden del arbol para el conjunto, asi verificamos todos los casos posibles sin repetición 
                
                tuple(map(tuple,(arbol.recorrido_preorden()))) 
            ))
            if tamaño < len(arboles_individuales): #Verificamos si al insertar el nuevo valor, si se aumenta el tamaño, por lo que es un arbol nuevo
                soluciones_unique.append(copy.deepcopy(i))
                  #Mostramos recorridos  
                
        return soluciones_unique
               