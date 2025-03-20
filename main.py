##from src.arbol import Arbol #Traemos lo hecho en arbol, La clase Arbol y la función permutar
from views import grafica_arbol
from src.models.utils import Utils
from src.models.arbol import Arbol

#Generar Utils
utils = Utils()

#Ingreso de elementos del arra y
array = [(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)] #Entre archivo JSON

permutaciones= utils.generar_permutaciones(array)

print(len(permutaciones))


#or i in permutaciones[0]:
   #grafica_arbol.visualizar_arbol(i)

grafica_arbol.visualizar_arbol(permutaciones[0])


    
