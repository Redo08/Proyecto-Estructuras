##from src.arbol import Arbol #Traemos lo hecho en arbol, La clase Arbol y la función permutar
from views import grafica_arbol
from src.models.utils import Utils
from src.models.arbol import Arbol

#Generar Utils
utils = Utils()

#Ingreso de elementos del arra y
array = [(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)] #Entre archivo JSON

arboles = utils.permutaciones_unique_arbol(array)
puntos = utils.permutaciones_unique_puntos(array)

print(len(arboles))
print(len(puntos))
print(puntos)


#or i in permutaciones[0]:
   #grafica_arbol.visualizar_arbol(i)

grafica_arbol.visualizar_arbol(arboles[0])


    
