import matplotlib.pyplot as plt

def graficar_puntos(lista_puntos):
    plt.figure(figsize=(8, 8))
    
    for conjunto in lista_puntos:
        x_values = [p[0] for p in conjunto]
        y_values = [p[1] for p in conjunto]
        plt.plot(x_values, y_values, marker='o', linestyle='-', label=f'{conjunto}')
    
    plt.xlabel("Eje X")
    plt.ylabel("Eje Y")
    plt.title("Gráfico de puntos conectados en líneas")
    plt.grid(True)
    plt.legend()
    plt.show()

# Lista de conjuntos de puntos
datos = [
    [(20, 12), (20, 0), (20, 21)], [(5, 8), (0, 8), (20, 8)], [(11, 15), (11, 8), (11, 21)], [(10, 15), (0, 15), (11, 15)], [(14, 8), (0, 8), (20, 8)], [(1, 13), (1, 8), (1, 15)]
]

graficar_puntos(datos)
