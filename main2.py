##from src.arbol import Arbol #Traemos lo hecho en arbol, La clase Arbol y la función permutar
from views import grafica_arbol
from src.models.utils import Utils
from src.models.arbol import Arbol
from src.models.plano import Plano

#Generar Utils
utils = Utils()

#Ingreso de elementos del arra y
array = [(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)] #Entre archivo JSON


arboles = utils.permutaciones_unique_arbol(array)
puntos = utils.permutaciones_unique_puntos(array)
arbol = utils.generar_arbol(array)

print(arbol.recorrido_anchura_con_orientacion())
recorrido_correcto = arbol.recorrido_anchura_con_orientacion()

#plano=Plano(recorrido_correcto)
#coordenadas_lineas, lineas_verticales, lineas_horizontales = plano.generar_lineas()
# print(coordenadas_lineas)
# print("----------------------------------------")
# print("Lineas verticales", lineas_verticales)
# print("----------------------------------------")
# print("Lineas horizontales", lineas_horizontales)
# print("Puntos intersección!")
# print(plano.puntos_areas(lineas_verticales, lineas_horizontales))
# print(len(plano.puntos_areas(lineas_verticales, lineas_horizontales)))

arbol_optimo, area_optima = utils.areas_optimas(puntos)

print(arbol_optimo.recorrido_anchura_con_orientacion())
plano = Plano(arbol_optimo.recorrido_anchura_con_orientacion())
lineas_verticales, lineas_horizontales = plano.generar_lineas()

print(plano.lineas)

# for i in coordenadas_lineas:
#    for j in coordenadas_lineas:
#       print(i[0])
#       print(j[0])
#       print(plano.distancia_entre_puntos(i[0], j[0]))


#print(len(arboles))
#print(len(puntos))
#print(puntos)


#for i in permutaciones[0]:
   #grafica_arbol.visualizar_arbol(i)

grafica_arbol.visualizar_arbol(arbol_optimo)
