import copy
import math
class Nodo:
    def __init__(self, valor_x, valor_y, altura):
        valor = [valor_x, valor_y] #Se pone cada nodo un array, el primer elemento es la componente x, el segundo la y y el tercero la alineacion
        self.valor = valor 
        self.izquierda = None
        self.derecha = None
        self.altura = altura #Si la componente es par, es porque es alineación X, si es impar es porque es alineación Y

class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def insertar(self, valor_x, valor_y):
        if self.raiz is None:
            self.raiz = Nodo(valor_x, valor_y, 0)
        else:
            self._insertar(self.raiz, valor_x, valor_y, 0)

    def _insertar(self, nodo, valor_x, valor_y, height):
        #Tomando el caso de que se organice por valores de x
        #Buscamos el componente x para poder hallarlo en el arbol
        comp_x = nodo.valor[0]
        comp_y = nodo.valor[1]
        altura = self.nivel(comp_x, comp_y) #Saca la altura
        if (altura%2)==0: #Si es par, entonces se toma la componente en x
            ### Se toma respecto al nivel del padre.
            if valor_x < nodo.valor[0]:
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor_x, valor_y, height)
                else:
                    self._insertar(nodo.izquierda, valor_x, valor_y, height+1)
            elif valor_x >= nodo.valor[0]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor_x, valor_y, height)
                else:
                    self._insertar(nodo.derecha, valor_x, valor_y, height+1)
        else: #Se toma los impares, osea la componente es y
            ### Se toma respecto al nivel del padre.
            if valor_y < nodo.valor[1]: #Componentes y
                if nodo.izquierda is None:
                    nodo.izquierda = Nodo(valor_x, valor_y, height)
                else:
                    self._insertar(nodo.izquierda, valor_x, valor_y, height+1)
            elif valor_y >= nodo.valor[1]:
                if nodo.derecha is None:
                    nodo.derecha = Nodo(valor_x, valor_y, height)
                else:
                    self._insertar(nodo.derecha, valor_x, valor_y, height+1)

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
                    if nodo_x < raiz.valor[0]: #Por izquierda
                        return self._nivel(raiz.izquierda, nivel +1, nodo_x, nodo_y)
                    else:
                        return self._nivel(raiz.derecha, nivel+1, nodo_x, nodo_y)
                else: # El actual es impar por lo que el padre es par, entonces es x
                    if nodo_y < raiz.valor[1]: #Por izquierda
                        return self._nivel(raiz.izquierda, nivel +1, nodo_x, nodo_y)
                    else:
                        return self._nivel(raiz.derecha, nivel+1, nodo_x, nodo_y)
                    
if __name__ == "__main__":
    
    # Recibir lista en JSON
    def es_viable_permutacion(s,n):
        return len(s) <= n
    def es_valido_permutacion(s):
        return len(s) == len(set(s))
    
    def backtrack_permutacion(nums, n, s, solucion):
        if es_valido_permutacion(s):
            if es_viable_permutacion(s,n):
                if n == len(s):
                    solucion.append(copy.deepcopy(s)) #Se necesita copiarlo asi, porque si no, se guarda es la referencia
                if math.factorial(n) == len(solucion):
                    print(solucion)
                    print("El tamaño es: ", len(solucion))
                else:
                    for i in range(1, n+1):
                        s.append(i)
                        backtrack_permutacion(nums, n, s, solucion)
                        s.pop()
    backtrack_permutacion([1,2,3,4], 4, [], [])
    def lista_posibles(listaGrande):
        lista = []
    arbol = ArbolBinario()
    arbol.insertar(5, 8) #x
    arbol.insertar(1, 13) #y
    arbol.insertar(10, 15) # y
    arbol.insertar(20, 12) # x 
    arbol.insertar(11, 15) # x
    arbol.insertar(14,8) # y
    
    print("Recorrido inorden:", arbol.recorrido_inorden())  # Imprime: [10, 20, 30]
    
    

    
### PREGUNTAS
# 1. El arbol esta organizado de una manera rara, como lo tomamos? Respecto al x? al y? A la suma total?
# 2. Esta bien hasta el momento como esta funcionando el arbol?
# 3. Para hacer graficas, seria bueno matplotlib? => Se puede usar PyGame
# 4. Para la interfaz, es bueno el PyQt5? => Usar PyGame(Bueno) o Tkinter
# 5. Como serian todas las opciones posibles?   => Hojita, Ya resuelto
# 6. Hasta donde van las lineas? Ver ejemplo en las fotos que una linea va hasta al final y las otras no
# 7. Cuál es la más eficiente para mostrar? El parametro de Area? Cantidad de areas?