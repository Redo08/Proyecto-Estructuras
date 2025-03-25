# main.py
from views.interfaz import Interface  # Asegúrate del nombre correcto
from src.models.utils import Utils
from src.models.plano import Plano
from src.models.arbol import Arbol
import pygame

if __name__ == "__main__":
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
                    #Calcular los límites del plano inicial con la lista de puntos
                    
                    plano=Plano(lista_de_puntos)
                    plano.calcular_limites()
                    
                    x_min_plano = plano.x_min
                    x_max_plano = plano.x_max
                    y_min_plano = plano.y_min
                    y_max_plano = plano.y_max
                    print(f"\nLímites iniciales del plano: x_min={x_min_plano}, x_max={x_max_plano}, y_min={y_min_plano}, y_max={y_max_plano}")

                # Enviar los límites a la interfaz para configurar la gráfica y la cuadrícula
                    interfaz.establecer_limites_plano(x_min_plano, x_max_plano, y_min_plano, y_max_plano)
                    utils = Utils()

                    arboles = utils.permutaciones_unique_arbol(lista_de_puntos)
                    # if event.type == pygame.MOUSEBUTTONDOWN:
                    #     if interfaz.boton_area_optima.collidepoint(event.pos):  # Si se presiona el botón
                    #         utils = Utils()
                    #         areas_optimas = utils.generar_areas(arboles)  # Obtiene áreas óptimas con sus índices
                    #         print("\nÍndices de árboles con sus áreas óptimas:")
                    #         for idx, area in areas_optimas:
                    #             print(f"Árbol {idx}: Área {area}")

                    # # Opcional: Actualizar la interfaz con el árbol y sus áreas óptimas
                    # interfaz.mostrar_area_optima(areas_optimas)
                    puntos = utils.permutaciones_unique_puntos(lista_de_puntos)
                    lineas=utils.generar_todas_las_lineas_por_arbol(arboles)
                    print("Las lineas son", lineas)
                    # Envía la lista de árboles a la interfaz usando el método cargar_y_graficar_arboles
                    interfaz.cargar_y_graficar_arboles(arboles,lineas)
                    # Cargar area optima
                    index,areas_optimas= utils.areas_optimas(puntos)
                    #print("las areas optimas son",areas_optimas)
                    interfaz.optimal_areas = areas_optimas
                    interfaz.set_optimal_tree_index(index)
                    trees_loaded = True
                    #print(f"\nSe generaron {len(arboles)} árboles únicos con sus líneas.")
                    #print(Arbol.recorrido_anchura_con_orientacion())
                    #recorrido_correcto = Arbol.recorrido_anchura_con_orientacion()
                    

            interfaz.draw()

    pygame.quit()