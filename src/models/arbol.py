import math
import copy
class Nodo:                                                     #Creación clase Nodo
    def __init__(self, x, y, altura):                           #coordenada en x, coordenada en y, y altura
        self.valor=[x,y]                                        #Atributo valor= valor en x, valor y
        self.izquierda=None                                     #Se inicializa izquierda y derecha en vacío
        self.derecha=None 
        self.altura=altura                                      # altura indicara la alineación, impar sera respecto a eje x, y par respecto al eje y
                           
                           
class Arbol: #Creación clase Arbol
    def __init__(self):
        self.raiz = None                                        #Se crea el arbol
    def insertar(self, x,y):
        if self.raiz is None:
            self.raiz= Nodo(x,y,1)                              #se inicializa en árbol conn el primer valor y con una altura de 1                        
            
        else:
            self._insertar(self.raiz,x,y,1)                     #Si el arbol tiene raiz, se ingresa a insertar el nodo hijo

    def _insertar(self,raiz,x,y,altura):                        #Se inserta según la condición de altura, ya sea validando el valor de x si la altura es impar, y en y si es par
        if raiz is not None:
            #Si la altura es impar
            if altura %2 != 0:
                self.validar(raiz,x,y,x,altura,0) 
            else: #Si la altura es par
                self.validar(raiz,x,y,y,altura,1)

    def validar(self,raiz,x,y,a,altura,posicion):                     #Determina respecto a su alineación, si se valida respecto a x o y.
                                                                #
        if raiz.valor[posicion]<=a:                           # Se mira por derecha
            if raiz.derecha is not None:
                self._insertar(raiz.derecha,x,y,altura+1)
            else:
                raiz.derecha=Nodo(x,y,altura+1)
        else: #Se mira por izquierda
            if raiz.izquierda is not None:
                self._insertar(raiz.izquierda,x,y,altura+1)
            else:
                raiz.izquierda=Nodo(x,y,altura+1)
 
    ################## RECORRIDOS ARBOL ######################
    def recorrido_inorden(self):
        elementos = []
        self._recorrido_inorden(self.raiz, elementos)
        return elementos
    
    def _recorrido_inorden(self, nodo, elementos):
        if nodo is not None:
            self._recorrido_inorden(nodo.izquierda, elementos)            
            elementos.append(nodo.valor)
            self._recorrido_inorden(nodo.derecha, elementos)
    
    def recorrido_preorden(self):
        elementos = []
        self._recorrido_preorden(self.raiz, elementos)
        return elementos
    
    def _recorrido_preorden(self, nodo, elementos):
        if nodo is not None:
            elementos.append(nodo.valor)
            self._recorrido_preorden(nodo.izquierda, elementos)
            self._recorrido_preorden(nodo.derecha, elementos)

######## FUNCIONES PROPIAS #######

#PERMUTACIÓN
def es_valido_permutar(s): #Es valido
    return len(set(s)) == len(s) #Si no estan repetidos
def es_viable_permutar(s, n):
    return len(s) <= n
def permutar(nums, s, solucion): #nums: Array inicial, s: Array vacio para cada solución individual, solucion: Array para las soluciones totales
    if es_valido_permutar(s):
        if es_viable_permutar(s, len(nums)):
            if len(nums) == len(s):
                solucion.append(copy.deepcopy(s)) #Se necesita copiarlo asi, porque si no, se guarda es la referencia
            if math.factorial(len(nums)) == len(solucion):
                return True
            else:
                for i in range(len(nums)):
                    s.append(nums[i]) #Se agrega cada valor de la lista
                    if permutar(nums, s, solucion):
                        return True
                    s.pop()
                              
    


            
                            

                
            
