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
            #Si la altura es impar es componente x
            if altura %2 != 0:
                self.validar(raiz,x,y,x,altura,0) 
            else: #Si la altura es par es componente y
                self.validar(raiz,x,y,y,altura,1)

    def validar(self,raiz,x,y,a,altura,posicion):                     #Determina respecto a su alineación, si se valida respecto a x o y.
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
    
    def recorrido_preorden_con_orientacion(self):
        elementos = []
        self._recorrido_preorden_con_orientacion(self.raiz, elementos)
        return elementos
    
    def _recorrido_preorden_con_orientacion(self,raiz, elementos):
        if raiz is not None:
           
            if raiz.altura % 2 != 0:
                elementos.append([raiz.valor[0],raiz.valor[1],0]) #0 es x
            else:
                elementos.append([raiz.valor[0],raiz.valor[1],1]) #0 es x
            self._recorrido_preorden_con_orientacion(raiz.izquierda, elementos)
            self._recorrido_preorden_con_orientacion(raiz.derecha, elementos)
                              
    


            
                            

                
            
