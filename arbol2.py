import math
import copy
class Nodo:
    def __init__(self, x, y, altura):
        self.valor=[x,y]
        self.izquiera=None
        self.derecha=None
        self.padre=None
        self.altura=altura
class Arbol:
    def __init__(self):
        self.raiz = None
    def insertar(self, x,y):
        if self.raiz is None:
            self.raiz= Nodo(x,y,1)
        else:
            self._insertar(self.raiz,x,y,1)

    def _insertar(self,raiz,x,y,altura):
        if raiz is not None:
            if altura %2 != 0:

                if raiz.valor[0]<=x:
                    if raiz.derecha is not None:
                        self.insertar(raiz.derecha,x,y,altura+1)
                    else:
                        raiz.derecha=Nodo(x,y,altura)
                else:
                    pass
                    
           
# Esto ya es main

def es_valido_permutar(s): #Es valido
    if len(set(s)) == len(s): #Si no estan repetidos
        return True
    
def es_viable_permutar(s, n):
    return len(s) <= n

def permutar(nums, n,  s, solucion): #nums: Array inicial, n: Tamaño array, s: Array vacio para cada solución individual, solucion: Array para las soluciones totales
    if es_valido_permutar(s):
        if es_viable_permutar(s, n):
            if n == len(s):
                solucion.append(copy.deepcopy(s)) #Se necesita copiarlo asi, porque si no, se guarda es la referencia
                if math.factorial(n) == len(solucion):
                    print(solucion)
                    print("El tamaño es: ", len(solucion))
                else:
                    for i in range(1, n+1):
                        s.append(i)
                        permutar(nums, n, s, solucion)
                        s.pop()

                
            