class Nodo:
    def __init__(self, x, y, altura):
        self.valor=[x,y]
        self.izquierda=None
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
                self.validar(raiz,x,y,x,altura,1)
            else:
                self.validar(raiz,x,y,y,altura,1)

    def validar(self,raiz,x,y,a,altura,posicion):
        if raiz.valor[posicion]<=a:
            if raiz.derecha is not None:
                self._insertar(raiz.derecha,x,y,altura+1)
            else:
                raiz.derecha=Nodo(x,y,altura+1)
        else:
            if raiz.izquierda is not None:
                self._insertar(raiz.izquierda,x,y,altura+1)
            else:
                raiz.izquierda=Nodo(x,y,altura+1)

    def recorrido_inorden(self):
        elementos = []
        self._recorrido_inorden(self.raiz, elementos)
        return elementos
    
    def _recorrido_inorden(self, nodo, elementos):
        if nodo is not None:
            elementos.append(nodo.valor)
            print(nodo.altura)
            self._recorrido_inorden(nodo.izquierda, elementos)            
            self._recorrido_inorden(nodo.derecha, elementos)
                            
            
if __name__ == "__main__":
    arbol = Arbol()
    arbol.insertar(5, 8) #x
    arbol.insertar(1, 13) #y
    arbol.insertar(10, 15) # y
    arbol.insertar(20, 12) # x 
    arbol.insertar(11, 15) # x
    arbol.insertar(14,8) # y
    
    print("Recorrido inorden:", arbol.recorrido_inorden())  # Imprime: [10, 20, 30]   
            

            
            
