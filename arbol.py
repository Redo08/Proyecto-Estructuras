class Nodo:
    def __init__(self, valor_x, valor_y):
        valor = [valor_x, valor_y] #Se pone cada nodo un array, el primer elemento es la componente x, el segundo la y y el tercero la alineacion
        self.valor = valor 
        self.izquierda = None
        self.derecha = None
        self.alineacion = 0 # 0 es x, 1 es y

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor_x, valor_y):
        if self.raiz is None:
            self.raiz = Nodo(valor_x, valor_y)
        else:
            self._insertar(self.raiz, valor_x, valor_y)

    def _insertar(self, nodo, valor_x, valor_y):
        #Tomando el caso de que se organice por valores de x
        #Buscamos el componente x para poder hallarlo en el arbol
        comp_x = nodo.valor[0]
        altura = self.nivel(comp_x) #Saca la altura
        print(altura)
        if (altura%2)==0: #Si es par, entonces se toma la componente en x
            ### Se toma respecto al nivel del padre.
            if valor_x < nodo.valor[0]:
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor_x, valor_y)
                else:
                    self._insertar(nodo.izquierda, valor_x, valor_y)
            elif valor_x > nodo.valor[0]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor_x, valor_y)
                else:
                    self._insertar(nodo.derecha, valor_x, valor_y)
        else: #Se toma los impares, osea la componente es y
            ### Se toma respecto al nivel del padre.
            if valor_y < nodo.valor[1]: #Componentes y
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor_x, valor_y)
                else:
                    self._insertar(nodo.izquierda, valor_x, valor_y)
            elif valor_y > nodo.valor[1]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor_x, valor_y)
                else:
                    self._insertar(nodo.derecha, valor_x, valor_y)

    def recorrido_inorden(self):
        elementos = []
        self._recorrido_inorden(self.raiz, elementos)
        return elementos
    
    def _recorrido_inorden(self, nodo, elementos):
        if nodo is not None:
            self._recorrido_inorden(nodo.izquierda, elementos)
            elementos.append(nodo.valor)
            self._recorrido_inorden(nodo.derecha, elementos)
    
    def nivel(self, valor_x, valor_y):
        return self._nivel(self.raiz, 0, valor_x, valor_y)
    
    def _nivel(self, raiz, nivel, nodo_x, nodo_y):
        if raiz is not None:
            if raiz.valor[0] == nodo_x:
                return nivel
            else:
                if nivel%2 == 0: #El actual es par entonces el padre es impar por lo que es y
                    if nodo_y < raiz.valor[1]: #Por izquierda
                        return self._nivel(raiz.izquierda, nivel +1, nodo_x, nodo_y)
                    else:
                        return self._nivel(raiz.derecha, nivel+1, nodo_x, nodo_y)
        
    def verificacion(self): #Recorrido por anchura
        cola = []
        q = self.raiz
        cola.append(q)
        while cola:
            if cola[0].izquierda is not None:
                cola.append(cola[0].izquierda)
            if cola[0].derecha is not None:
                cola.append(cola[0].derecha)
            if cola:
                self.alineacion(cola.pop(0))
        return "Todo alineado"
            
    def alineacion(self, nodo):
        valor_x = nodo.valor[0]
        nivel = self.nivel(valor_x) #Valor x
        if nivel%2 == 0:
            nodo.alineacion = "Eje x"
            print(nodo.valor)
            print(nodo.alineacion)
        else:
            nodo.alineacion = "Eje y"
            print(nodo.valor)
            print(nodo.alineacion)
            
if __name__ == "__main__":
    arbol = ArbolBinario()
    arbol.insertar(5, 8) #x
    arbol.insertar(1, 13) #y
    arbol.insertar(10, 15) # y
    arbol.insertar(20, 12) # x 
    arbol.insertar(11, 15) # x
    arbol.insertar(14,8) # y
    
    print("Recorrido inorden:", arbol.recorrido_inorden())  # Imprime: [10, 20, 30]
    print(arbol.verificacion())
    
### PREGUNTAS
# 1. El arbol esta organizado de una manera rara, como lo tomamos? Respecto al x? al y? A la suma total?
# 2. Esta bien hasta el momento como esta funcionando el arbol?
# 3. Para hacer graficas, seria bueno matplotlib? => Se puede usar PyGame
# 4. Para la interfaz, es bueno el PyQt5? => Usar PyGame(Bueno) o Tkinter
# 5. Como serian todas las opciones posibles?   => Hojita, Ya resuelto
# 6. Hasta donde van las lineas? Ver ejemplo en las fotos que una linea va hasta al final y las otras no
