##from src.arbol import Arbol #Traemos lo hecho en arbol, La clase Arbol y la función permutar

from src.optimizador import Optimizador

#Ingreso de elementos del arra y
array = [(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)] #Entre archivo JSON

permutaciones=Optimizador(array)
conjunto=permutaciones.generar_permutaciones()
print(conjunto)
print(len(conjunto))
