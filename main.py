from models.arbol import Arbol, permutar #Traemos lo hecho en arbol, La clase Arbol y la función permutar
from views.grafica import visualizar_arbol #Traemos la forma de visualizar los arboles

#Ingreso de elementos del array
array = [(5,8), (1,13), (10,15), (20,12), (11,15), (14,8)] #Entre archivo JSON
arboles_individuales = set([]) #Eso es un conjunto para evitar repetidos
contador = 0 #Contador para saber la cantidad de arboles unicos
solucion = [] #Array solución

#Llamado a permutar el array ingresado
permutar(array, [], solucion)

### SOLUCIONAR ESTO TOCA HACER QUE DEVUELVA UNA LISTA CON LAS LISTAS QUE SON UNICAS

# Crear e insertar elementos en el árbol
for i in solucion:
    arbol = Arbol() #Se tiene que crear un nuevo arbol para cada uno
    tamaño = len(arboles_individuales) #Se saca el tamaño del conjunto antes de insertar el siguiente arbol
    for j in i:
        arbol.insertar(j[0], j[1])  #Se recorre la sublista y se sacan los valores x, y
    arboles_individuales.add(( #Insertamos los recorridos inorden y preorden del arbol para el conjunto, asi verificamos todos los casos posibles sin repetición 
        tuple(map(tuple, arbol.recorrido_inorden())),
        tuple(map(tuple,(arbol.recorrido_preorden()))) 
    ))
    if tamaño < len(arboles_individuales): #Verificamos si al insertar el nuevo valor, si se aumenta el tamaño, por lo que es un arbol nuevo
        print("----------------------------------------------------")
        print("Recorrido inorden:", arbol.recorrido_inorden())  #Mostramos recorridos  
        print("Recorrido preorden:", arbol.recorrido_preorden()) 
        print("----------------------------------------------------")
        # Visualizar el árbol con PyGame
        visualizar_arbol(arbol) #Vizualisamos el arbol
        contador +=1 #Y sumamos al contador para saber cuantos arboles en total salen (68)

print(contador)

