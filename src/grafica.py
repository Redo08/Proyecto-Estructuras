import matplotlib.pyplot as plt
import time

# Clase del nodo KD
class NodoKD:
    def __init__(self, punto):
        self.valor = punto
        self.izquierda = None
        self.derecha = None

# Clase del árbol KD
class ArbolKD:
    def __init__(self):
        self.raiz = None

    def insertar(self, x, y):
        nuevo_nodo = NodoKD((x, y))
        if not self.raiz:
            self.raiz = nuevo_nodo
        else:
            self._insertar_recursivo(self.raiz, nuevo_nodo, 0)

    def _insertar_recursivo(self, actual, nuevo_nodo, nivel):
        if actual is None:
            return nuevo_nodo

        coordenada = nivel % 2

        if nuevo_nodo.valor[coordenada] < actual.valor[coordenada]:
            actual.izquierda = self._insertar_recursivo(actual.izquierda, nuevo_nodo, nivel + 1)
        else:
            actual.derecha = self._insertar_recursivo(actual.derecha, nuevo_nodo, nivel + 1)

        return actual

# Nueva función para graficar progresivamente
def graficar_arbol_kd_progresivo(nodo, min_x, max_x, min_y, max_y, nivel=0):
    if nodo is None:
        return

    x, y = nodo.valor

    # Dibuja el punto actual
    plt.plot(x, y, 'o', color='orange')
    plt.text(x + 0.3, y + 0.3, f"({x},{y})", fontsize=10)

    # Según el nivel, decide si dibuja una línea vertical u horizontal
    if nivel % 2 == 0:
        # Línea vertical
        plt.plot([x, x], [min_y, max_y], 'orange', linestyle='--', linewidth=1)
    else:
        # Línea horizontal
        plt.plot([min_x, max_x], [y, y], 'orange', linestyle='--', linewidth=1)

    # Actualiza y espera un momento para ver el proceso
    plt.pause(1)

    # Llama a la recursión para los hijos (izquierda y derecha)
    if nivel % 2 == 0:
        graficar_arbol_kd_progresivo(nodo.izquierda, min_x, x, min_y, max_y, nivel + 1)
        graficar_arbol_kd_progresivo(nodo.derecha, x, max_x, min_y, max_y, nivel + 1)
    else:
        graficar_arbol_kd_progresivo(nodo.izquierda, min_x, max_x, min_y, y,6 nivel + 1)
        graficar_arbol_kd_progresivo(nodo.derecha, min_x, max_x, y, max_y, nivel + 1)

# Crear el árbol y agregar puntos
arbol = ArbolKD()
puntos = [(5, 8),(1,13), (10, 15), (20,12), (11, 15),(14,8)]


for x, y in puntos:
    arbol.insertar(x, y)

# Configurar la gráfica
plt.figure(figsize=(8, 8))
plt.title("Árbol KD con visualización progresiva")
plt.grid(True)
plt.xlim(0, 20)
plt.ylim(0, 20)

# Graficar el árbol paso a paso
graficar_arbol_kd_progresivo(arbol.raiz, 0, 20, 0, 20)

plt.show()
