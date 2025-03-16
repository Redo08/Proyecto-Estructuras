from src.arbol import Arbol
from views.grafica import visualizar_arbol

# Crear e insertar elementos en el árbol
arbol = Arbol()
arbol.insertar(5, 8)
arbol.insertar(1, 13)
arbol.insertar(10, 15)
arbol.insertar(20, 12)
arbol.insertar(11, 15)
arbol.insertar(14, 8)

print("Recorrido inorden:", arbol.recorrido_inorden())

# Visualizar el árbol con PyGame
visualizar_arbol(arbol)
