from punto import Punto
from linea import Linea

def main():
    # 🎯 Creamos puntos y líneas
    punto1=Punto(0,13)
    punto1 = Punto(5, 8)
    punto2 = Punto(10, 3)

    
    linea1 = Linea(punto1, "vertical")
    linea2 = Linea(punto2, "horizontal")

    # 🔥 Mostramos las líneas
    print(linea1)
    print(linea2)

    # 🛠️ Calculamos la intersección
    interseccion = linea1.interseccion(linea2)

    # 📍 Mostramos la intersección
    if interseccion:
        print(f"¡Intersección en: {interseccion}!")
    else:
        print("No hay intersección entre estas líneas.")

if __name__ == "__main__":
    main()
