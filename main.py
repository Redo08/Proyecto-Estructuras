# main.py
from views.interfaz import Interface  # Asegúrate del nombre correcto
from src.models.utils import Utils
from src.models.plano import Plano
from src.models.arbol import Arbol
import pygame

if __name__ == "_main_":
    pygame.init()
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Creador de Planos")

    interfaz = Interface()  # Inicializamos la interfaz

    running = True
    trees_loaded = False  # Bandera para controlar si los árboles ya se cargaron

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            interfaz.handle_input(event)

            # Ejemplo de cómo podrías generar los árboles después de ingresar los puntos
            if event.type == pygame.KEYDOWN:  # Puedes usar otro evento o condición
                if event.key == pygame.K_SPACE and not trees_loaded: # Ejemplo: al presionar ESPACIO
                    lista_de_puntos = interfaz.get_points()
                    print("\nLista de puntos obtenida desde la interfaz:")
                    for punto in lista_de_puntos:
                        print(punto)

                    utils = Utils()
                    arboles = utils.permutaciones_unique_arbol(lista_de_puntos)

                    # Envía la lista de árboles a la interfaz usando el método cargar_y_graficar_arboles
                    interfaz.cargar_y_graficar_arboles(arboles)
                    trees_loaded = True
                    print("\nLista de árboles enviada a la interfaz.")
                    print(Arbol.recorrido_anchura_con_orientacion())
                    recorrido_correcto = Arbol.recorrido_anchura_con_orientacion()

        interfaz.draw()

    pygame.quit()
    
