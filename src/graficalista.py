import matplotlib.pyplot as plt
import time

class Arbol:
    def __init__(self):
        self.raiz = None

    def recorrido_inorden(self):
            elementos = []
            self._recorrido_inorden(self.raiz, elementos)
            return elementos
        
    def _recorrido_inorden(self, nodo, elementos):
            if nodo is not None:
                elementos.append(nodo.valor)
                self._recorrido_inorden(nodo.izquierda, elementos)            
                self._recorrido_inorden(nodo.derecha, elementos)



