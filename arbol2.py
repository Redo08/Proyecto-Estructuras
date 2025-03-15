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
                else 
                    
    
            
            
