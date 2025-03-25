# mi_proyecto/interfaz_puntos.py
import tkinter as tk
from tkinter import filedialog
import json
import pygame
import random
import os 
import ast  # Para evaluar la cadena como una lista
from src.models.utils import Utils
from src.models.arbol import Nodo, Arbol
from views.grafica_arbol import dibujar_arbol
from tkinter import colorchooser # Importa el selector de color
from src.models.area import Area # Anexamos esta línea
class Interface:
    def __init__(self,tree_list=None,optimal_areas=None):
        pygame.init()
        
        self.screen_width = 1000
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Creador de Planos")

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 128, 128)
        self.font = pygame.font.Font(None, 22)
        self.font_small = pygame.font.Font(None, 16) # Fuente más pequeña para las etiquetas de la cuadrícula

        self.points =[]
        self.input_list_str = ""
        self.input_active_list = False
        self.input_rect_list = pygame.Rect(180, 50, 400, 30) #(x,y, ancho pix, larg pix)
        self.add_button_rect = pygame.Rect(600, 50, 150, 30)
        self.add_button_text = self.font.render("Ingresar Lista", True, self.white)
        self.add_button_text_rect = self.add_button_text.get_rect(center=self.add_button_rect.center)
        
         # Nuevo botón para cargar desde JSON
        self.load_json_button_rect = pygame.Rect(800, 50, 180, 30) # Colocarlo a la derecha de "Ingresar Lista"
        self.load_json_button_text = self.font.render("Cargar JSON", True, self.white)
        self.load_json_button_text_rect = self.load_json_button_text.get_rect(center=self.load_json_button_rect.center)

        # Nuevo botón para sacar el area otpima
        #self.load_json_button_rect = pygame.Rect()

        # Nueva sección para los árboles
        self.tree_list = tree_list if tree_list is not None else [] #Se almacena la lista de los arboles
        self.current_tree_index = 0  # Índice del árbol actual para mostrar

        # Definición de rectángulos para la sección de árboles y los botones
        self.trees_section_rect = pygame.Rect(20, 150, self.screen_width // 2 - 40, 400) # Mitad izquierda
        self.button_width = 80
        self.button_height = 30
        self.button_spacing = 10

        button_y = self.trees_section_rect.bottom + 20

        self.first_button_rect = pygame.Rect(20, button_y, self.button_width, self.button_height)
        self.prev_button_rect = pygame.Rect(20 + self.button_width + self.button_spacing, button_y, self.button_width, self.button_height)
        self.next_button_rect = pygame.Rect(20 + 2 * (self.button_width + self.button_spacing), button_y, self.button_width, self.button_height)
        self.last_button_rect = pygame.Rect(20 + 3 * (self.button_width + self.button_spacing), button_y, self.button_width, self.button_height)

        self.first_button_text = self.font.render("Primero", True, self.white)
        self.prev_button_text = self.font.render("Anterior", True, self.white)
        self.next_button_text = self.font.render("Siguiente", True, self.white)
        self.last_button_text = self.font.render("Último", True, self.white)

        # Recuadro para mostrar la lista de puntos
        self.points_display_rect = pygame.Rect(20, self.add_button_rect.bottom + 20, self.screen_width - 40, self.input_rect_list.height) # Debajo del botón, con espacio, toma las medidas de la caja donde se ingresan los datos
        # Nueva sección para la cuadrícula (parte derecha)
        self.grid_section_rect=pygame.Rect(self.screen_width//2+20,150,self.screen_width//2-40,400)

        # Atributos para almacenar los límites del plano
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None               
        self.root_tk = tk.Tk() # Inicializa tkinter
        self.root_tk.withdraw()
        self.running = True
        self.all_lines_list =[]# Inicializa self.all_lines_list aquí
         # Nuevo botón para mostrar el óptimo
        self.optimal_button_width = 150
        self.optimal_button_height = 30
        self.optimal_button_x = self.grid_section_rect.x + (self.grid_section_rect.width - self.optimal_button_width) // 2
        self.optimal_button_y = self.grid_section_rect.bottom + 20
        self.optimal_button_rect = pygame.Rect(self.optimal_button_x, self.optimal_button_y, self.optimal_button_width, self.optimal_button_height)
        self.optimal_button_text = self.font.render("Mostrar Óptimo", True, self.white)
        self.optimal_button_text_rect = self.optimal_button_text.get_rect(center=self.optimal_button_rect.center)

        # Colores para las áreas
        self.area_background_color = (200, 200, 200) # Gris claro por defecto - Nuevo atributo
        self.area_outline_color = (0, 0, 0)       # Negro por defecto - Nuevo atributo
        self.optimal_areas = optimal_areas if optimal_areas is not None else []# Inicializamos optimal_areas - Nuevo atributo


        self.optimal_areas = optimal_areas if optimal_areas is not None else[]# Inicializamos optimal_areas - Nuevo atributo
        self.selected_area = None # Inicializamos el área seleccionada

        # Botones para cambiar el color
        self.bg_color_button_rect = pygame.Rect(self.grid_section_rect.left + 20, self.grid_section_rect.bottom + 60, 180, 30) # Nuevo
        self.bg_color_button_text = self.font.render("Cambiar Fondo Área", True, self.white) # Nuevo
        self.bg_color_button_text_rect = self.bg_color_button_text.get_rect(center=self.bg_color_button_rect.center) # Nuevo

        self.outline_color_button_rect = pygame.Rect(self.grid_section_rect.right - 200, self.grid_section_rect.bottom + 60, 180, 30) # Nuevo
        self.outline_color_button_text = self.font.render("Cambiar Borde Área", True, self.white) # Nuevo
        self.outline_color_button_text_rect = self.outline_color_button_text.get_rect(center=self.outline_color_button_rect.center) # Nuevo

        # Entrada de texto para anotar elementos
        self.element_input_rect = pygame.Rect(self.grid_section_rect.left + 20, self.bg_color_button_rect.bottom + 20, 200, 30) # Nuevo
        self.element_input_text = "" # Nuevo
        self.element_input_active = False # Nuevo
        self.element_input_label = self.font.render("Anotar Elemento:", True, self.black) # Nuevo
        # Atributo para almacenar el índice del árbol óptimo
        self.optimal_tree_index = None

    # Nuevo método para establecer los límites del plano
    def establecer_limites_plano(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max
    def set_optimal_tree_index(self, index):
        """Establece el índice del árbol óptimo en la lista."""
        if self.tree_list is not None and 0 <= index < len(self.tree_list):
            self.optimal_tree_index = index
        else:
            print(f"Índice de árbol óptimo fuera de rango: {index}")
    def cargar_json_dialog(self):
        # raiz = tk.Tk()  <-- Elimina esta línea
        # raiz.withdraw()  <-- Elimina esta línea
        
        # Abrir el explorador de archivos y filtrar solo archivos JSON
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")],
            title="Seleccionar archivo JSON" # Opcional: título de la ventana
        )

        if file_path:  # Si el usuario seleccionó un archivo
            try:
                with open(file_path, "r", encoding="utf-8") as archivo_data:
                    data = json.load(archivo_data)
                    if isinstance(data, list) and all(isinstance(point, list) and len(point) == 2 for point in data):
                        self.points = [tuple(point) for point in data]
                        print(f"Puntos cargados desde JSON: {self.points}")
                    else:
                        print("El archivo JSON debe contener una lista de listas o tuplas con formato [[x, y], ...]")
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo en la ruta: {file_path}")
            except json.JSONDecodeError:
                print(f"Error: El archivo en la ruta: {file_path} no es un JSON válido.")
            except Exception as e:
                print(f"Ocurrió un error al cargar el JSON: {e}")
    def set_tree_list(self, new_tree_list,new_all_lines_list):
        """Actualiza la lista de árboles y resetea el índice."""
        self.tree_list = new_tree_list
        self.all_lines_list = new_all_lines_list
        self.current_tree_index = 0 

    def cargar_y_graficar_arboles(self, lista_de_arboles,lista_de_todas_las_lineas):
        """Carga la lista de árboles y fuerza un redibujado."""
        self.set_tree_list(lista_de_arboles, lista_de_todas_las_lineas)
        # Aquí podrías calcular los límites del plano basándote en las líneas del primer árbol
        
        pygame.display.flip() # Fuerza una actualización de la pantalla inmediatamente
        

    def cargar_mas_optimo(self, arbol_optimo, lineas_optimas):
        self.set_tree_list(arbol_optimo, lineas_optimas)
        pygame.display.flip()
        
    def handle_input(self, event):
        """Maneja los eventos de entrada del usuario."""
        utils = Utils()
        if event.type == pygame.MOUSEBUTTONDOWN:
            # --- Manejo de la activación del input de la lista de puntos ---
            if self.input_rect_list.collidepoint(event.pos):
                self.input_active_list = True
            else:
                self.input_active_list = False

            # --- Manejo del botón "Ingresar Lista" ---
            if self.add_button_rect.collidepoint(event.pos):
                self.process_point_list()
            # --- Manejo del botón "Cargar JSON" ---
            elif self.load_json_button_rect.collidepoint(event.pos):
                self.cargar_json_dialog() # Usar el texto del campo de entrada como ruta

            # --- Manejo de los botones de navegación de árboles ---
            if self.first_button_rect.collidepoint(event.pos):
                self.current_tree_index = 0
            elif self.prev_button_rect.collidepoint(event.pos):
                if self.current_tree_index > 0:
                    self.current_tree_index -= 1
            elif self.next_button_rect.collidepoint(event.pos):
                if 0 <= self.current_tree_index < len(self.tree_list) - 1:
                    self.current_tree_index += 1
            elif self.last_button_rect.collidepoint(event.pos):
                if self.tree_list:
                    self.current_tree_index = len(self.tree_list) - 1
            # --- Manejo del clic en el botón "Mostrar Óptimo" ---
            elif self.optimal_button_rect.collidepoint(event.pos):
                if self.optimal_tree_index is not None:
                    self.current_tree_index = self.optimal_tree_index
            # --- Manejo de los botones de cambio de color ---
            elif self.bg_color_button_rect.collidepoint(event.pos):
                color_code = colorchooser.askcolor(title="Seleccionar color de fondo")
                if color_code and self.selected_area:
                    self.selected_area.color_fondo = color_code[0]
            elif self.outline_color_button_rect.collidepoint(event.pos):
                color_code = colorchooser.askcolor(title="Seleccionar color de contorno")
                if color_code and self.selected_area:
                    self.selected_area.color_borde = color_code[0]
            # --- Manejo de la activación del input del elemento del área ---
            elif self.element_input_rect.collidepoint(event.pos):
                self.element_input_active = True
            else:
                self.element_input_active = False

            # --- Lógica para detectar clic en un área ---
            if self.optimal_tree_index is not None and self.current_tree_index == self.optimal_tree_index:
                mouse_x, mouse_y = event.pos
                print(f"Clic en: ({mouse_x}, {mouse_y})")
                for area_obj in self.optimal_areas:
                    
                    scaled_points =[]
                    if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
                        range_x = self.x_max - self.x_min
                        range_y = self.y_max - self.y_min
                        if range_x > 0 and range_y > 0:
                            scale_x = (self.grid_section_rect.width - 2 * 10) / range_x
                            scale_y = (self.grid_section_rect.height - 2 * 10) / range_y
                            for x, y in area_obj.limites:
                                scaled_x = self.grid_section_rect.left + 10 + (x - self.x_min) * scale_x
                                scaled_y = self.grid_section_rect.bottom - 10 - (y - self.y_min) * scale_y
                                scaled_points.append((int(scaled_x), int(scaled_y)))

                            if scaled_points:
                                print(f"Puntos escalados del área: {scaled_points}") # Imprimir los puntos escalados de cada área
                                polygon = pygame.draw.polygon(self.screen, (0, 0, 0), scaled_points, 0)
                                if polygon.collidepoint(mouse_x, mouse_y):
                                    self.selected_area = area_obj
                                    print("Área seleccionada:", self.selected_area)
                                    break
                    print(f"Puntos escalados para el área: {scaled_points}")
        if event.type == pygame.KEYDOWN:
            # --- Manejo de la entrada de texto para la lista de puntos ---
            if self.input_active_list:
                if event.key == pygame.K_RETURN:
                    self.input_active_list = False
                    self.process_point_list()
                elif event.key == pygame.K_BACKSPACE:
                    self.input_list_str = self.input_list_str[:-1]
                else:
                    self.input_list_str += event.unicode
            # --- Manejo de la entrada de texto para el elemento del área ---
            elif self.element_input_active:
                if event.key == pygame.K_RETURN:
                    self.element_input_active = False
                    if self.element_input_text:
                        first_letter = self.element_input_text[0].upper()
                        for area_obj in self.optimal_areas:
                            if area_obj == self.selected_area: # Aplicar solo al área seleccionada
                                area_obj.elementos_graficos = [first_letter]
                        self.element_input_text = ""
                elif event.key == pygame.K_BACKSPACE:
                    self.element_input_text = self.element_input_text[:-1]
                else:
                    self.element_input_text += event.unicode
    def process_point_list(self):
        try:
            # Evaluamos la cadena como una lista literal de Python
            point_list = ast.literal_eval(self.input_list_str)
            if isinstance(point_list, list) and all(isinstance(point, tuple) and len(point) == 2 for point in point_list):
                self.points = point_list
                self.input_list_str = ""
            else:
                print("Por favor, ingresa una lista válida de tuplas con formato [(x, y), ...]")
        except (SyntaxError, ValueError):
            print("Error al procesar la lista. Asegúrate de usar el formato correcto: [(x, y), ...]")
    def draw_areas(self):
        """Dibuja las áreas en la sección derecha (cuadrícula) solo si el árbol actual es el óptimo."""
        # Paso 1: Verifica si se debe dibujar el área.
         # Se asegura de que haya un índice de árbol óptimo establecido
        # y que el árbol que se está mostrando actualmente NO sea diferente del óptimo.
        # Si el árbol actual no es el óptimo, la función se detiene (retorna) sin dibujar nada.
        if self.optimal_tree_index is not None and self.current_tree_index != self.optimal_tree_index:
            #print("Contenido de self.optimal_areas para el árbol óptimo:", self.optimal_areas)
            return  # No dibujar áreas si el árbol actual no es el óptimo

        # Paso 2: Verifica si se tienen los límites del plano y la sección de la cuadrícula definidos.
        # Si alguna de estas variables no está definida, no se puede realizar el escalado ni el dibujo correctamente.
        if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
            # Paso 3: Calcula el rango de los valores en los ejes X e Y del plano.
            range_x = self.x_max - self.x_min
            range_y = self.y_max - self.y_min
            # Paso 4: Verifica que los rangos sean mayores que cero para evitar divisiones por cero.
           
            if range_x > 0 and range_y > 0:

                # Paso 5: Calcula los factores de escala para los ejes X e Y.
                # Estos factores se utilizan para mapear las coordenadas del plano a las coordenadas de píxeles dentro de la sección de la cuadrícula.
                # Se resta un padding de 20 (10 en cada lado) del ancho y alto para dejar un margen.
                scale_x = (self.grid_section_rect.width - 2 * 10) / range_x
                scale_y = (self.grid_section_rect.height - 2 * 10) / range_y
                # Paso 7: Itera sobre cada objeto 'area_obj' en la lista self.optimal_areas.
                # Se asume que cada 'area_obj' representa un área independiente.

                #print("Contenido de self.optimal_areas:", self.optimal_areas) 

                for area_obj in self.optimal_areas:
                    print(f"Propiedades del área: {area_obj.__dict__}")
                    # Paso 8: Inicializa una lista vacía para almacenar los puntos escalados del área actual.
                    scaled_points =[]
                     # Paso 9: Itera sobre cada punto (x, y) en la lista de límites del área actual.
                    # Se asume que 'area_obj.limites' es una lista de tuplas que definen los vértices del área.
                
                    for x, y in area_obj.limites:
                        # Paso 10: Calcula las coordenadas de píxeles escaladas para el punto actual.
                        # Para el eje X: se toma la coordenada x, se resta el mínimo valor de x del plano, se multiplica por el factor de escala en X y se añade un desplazamiento para ubicarlo dentro de la sección de la cuadrícula con un margen de 10 píxeles desde la izquierda.
                        scaled_x = self.grid_section_rect.left + 10 + (x - self.x_min) * scale_x
                        # Para el eje Y: similar al eje X, pero se resta el valor escalado de la parte inferior de la sección de la cuadrícula. Esto se debe a que el eje Y en Pygame crece hacia abajo, mientras que en un sistema de coordenadas típico crece hacia arriba.
                        scaled_y = self.grid_section_rect.bottom - 10 - (y - self.y_min) * scale_y
                        # Paso 11: Añade las coordenadas escaladas (convertidas a enteros) a la lista de puntos escalados.
                        scaled_points.append((int(scaled_x), int(scaled_y)))

                    # Paso 12: Verifica si hay puntos escalados para dibujar el área.
                    if scaled_points:
                        # Paso 13: Determina el color de fondo del área.
                        # Si el objeto 'area_obj' tiene un atributo 'color_fondo' establecido, se usa ese color; de lo contrario, se usa el color de fondo predeterminado de la interfaz.
                        if area_obj.color_fondo is None:
                            area_obj.color_fondo = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
                        fondo = area_obj.color_fondo
                        # Paso 14: Determina el color del borde del área de manera similar al color de fondo.
                        borde = area_obj.color_borde if area_obj.color_borde else (0, 0, 0) # Asegúrate de que el borde sea visible
                        # Paso 15: Dibuja el polígono relleno en la pantalla utilizando los puntos escalados y el color de fondo.
                        pygame.draw.polygon(self.screen, fondo, scaled_points)
                        # Paso 16: Dibuja el borde del polígono utilizando los mismos puntos escalados y el color del borde, con un grosor de 2 píxeles.
                        pygame.draw.polygon(self.screen, borde, scaled_points, 2)

                        # Paso 17: Verifica si el objeto 'area_obj' tiene elementos gráficos asociados (por ejemplo, una etiqueta).
                        if area_obj.elementos_graficos and isinstance(area_obj.elementos_graficos, list) and area_obj.elementos_graficos[0]:
                            # Paso 18: Configura la fuente para la etiqueta.
                            font = pygame.font.Font(None, 36)
                            # Paso 19: Obtiene el texto de la etiqueta del primer elemento de la lista.
                            label_text = area_obj.elementos_graficos[0]
                            # Paso 20: Renderiza el texto en una superficie.
                            text_surface = font.render(label_text, True, (0, 0, 0))
                            # Paso 21: Calcula las coordenadas centrales del área para ubicar la etiqueta.
                            center_x = int(self.grid_section_rect.left + 10 + (sum(p[0] for p in area_obj.limites) / len(area_obj.limites) - self.x_min) * scale_x)
                            center_y = int(self.grid_section_rect.bottom - 10 - (sum(p[1] for p in area_obj.limites) / len(area_obj.limites) - self.y_min) * scale_y)
                            # Paso 22: Obtiene el rectángulo que delimita la superficie del texto y lo centra en las coordenadas calculadas.
                            text_rect = text_surface.get_rect(center=(center_x, center_y))
                            # Paso 23: Dibuja la superficie del texto (la etiqueta) en la pantalla en la posición calculada.
                            self.screen.blit(text_surface, text_rect)
    def dibujar_lineas_plano(self):
        """Dibuja las líneas del plano y su primer punto en la sección derecha (cuadrícula)."""
        line_color = (0, 0, 0) # Negro para las líneas
        line_thickness = 2
        point_color = (255, 0, 0) # Rojo para el primer punto
        point_radius = 3
        padding = 10

        # Calcula la escala para ajustar las líneas dentro de grid_section_rect
        if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
            range_x = self.x_max - self.x_min
            range_y = self.y_max - self.y_min
            if range_x > 0 and range_y > 0:
                scale_x = (self.grid_section_rect.width - 2 * padding) / range_x
                scale_y = (self.grid_section_rect.height - 2 * padding) / range_y

                # Iterar sobre la lista correcta de líneas
                if self.all_lines_list and 0 <= self.current_tree_index < len(self.all_lines_list):
                    lineas_para_arbol_actual = self.all_lines_list[self.current_tree_index]
                    for linea in lineas_para_arbol_actual:
                        punto, punto_inicial, punto_final = linea

                        # Calcular las coordenadas en la cuadrícula
                        x1_line = self.grid_section_rect.left + padding + (punto_inicial[0] - self.x_min) * scale_x
                        y1_line = self.grid_section_rect.bottom - padding - (punto_inicial[1] - self.y_min) * scale_y
                        x2_line = self.grid_section_rect.left + padding + (punto_final[0] - self.x_min) * scale_x
                        y2_line = self.grid_section_rect.bottom - padding - (punto_final[1] - self.y_min) * scale_y

                        # Dibujar la línea
                        pygame.draw.line(self.screen, line_color, (int(x1_line), int(y1_line)), (int(x2_line), int(y2_line)), line_thickness)

                        # Dibujar el primer punto
                        x_point = self.grid_section_rect.left + padding + (punto[0] - self.x_min) * scale_x
                        y_point = self.grid_section_rect.bottom - padding - (punto[1] - self.y_min) * scale_y
                        pygame.draw.circle(self.screen, point_color, (int(x_point), int(y_point)), point_radius)
    
    def establecer_limites_plano(self, x_min, x_max, y_min, y_max):
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def draw_grid_with_labels(self, screen):

        """Dibuja la cuadrícula con etiquetas en la sección derecha."""
        grid_rect = self.grid_section_rect
        grid_color = (200, 200, 200)
        line_thickness = 1
        padding = 10  # Espacio alrededor de la cuadrícula dentro de su sección

        if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None:
            range_x = self.x_max - self.x_min
            range_y = self.y_max - self.y_min

            if range_x > 0 and range_y > 0:
                # Dibujar el borde de la sección de la cuadrícula
                pygame.draw.rect(screen, self.black, grid_rect, 2)

                # Calcular el espacio disponible para la cuadrícula dentro de la sección
                grid_inner_rect = pygame.Rect(grid_rect.left + padding, grid_rect.top + padding,
                                             grid_rect.width - 2 * padding, grid_rect.height - 2 * padding)

                # Dibujar líneas verticales y etiquetas del eje X
                
                num_x_segments = self.x_max # Puedes ajustar la cantidad de segmentos
                if num_x_segments > 0:
                    x_step = range_x / num_x_segments
                    for i in range(num_x_segments + 1):
                        x_val = self.x_min + i * x_step
                        x_pixel = grid_inner_rect.left + (x_val - self.x_min) * (grid_inner_rect.width / range_x)
                        pygame.draw.line(screen, grid_color, (int(x_pixel), grid_inner_rect.top), (int(x_pixel), grid_inner_rect.bottom), line_thickness)
                        # Mostrar etiquetas solo en ciertos intervalos para evitar superposición
                        if num_x_segments > 0 and (i % max(1, num_x_segments // 10) == 0 or i == 0 or i == num_x_segments): # Mostrar etiquetas aproximadamente
                            text = self.font_small.render(f"{x_val:.1f}", True, self.black)
                            text_rect = text.get_rect(midtop=(int(x_pixel), grid_rect.bottom - padding + 5))
                            screen.blit(text, text_rect)

                # Dibujar líneas horizontales y etiquetas del eje Y
                
                
                num_y_segments = self.y_max # Puedes ajustar la cantidad de segmentos
                if num_y_segments > 0:
                    y_step = range_y / num_y_segments
                    for i in range(num_y_segments + 1):
                        y_val = self.y_min + i * y_step
                        y_pixel = grid_inner_rect.bottom - (y_val - self.y_min) * (grid_inner_rect.height / range_y)
                        pygame.draw.line(screen, grid_color, (grid_inner_rect.left, int(y_pixel)), (grid_inner_rect.right, int(y_pixel)), line_thickness)
                        # Mostrar etiquetas solo en ciertos intervalos para evitar superposición
                        if num_y_segments > 0 and (i % max(1, num_y_segments // 10) == 0 or i == 0 or i == num_y_segments): # Mostrar etiquetas aproximadamente
                            text = self.font_small.render(f"{y_val:.1f}", True, self.black)
                            text_rect = text.get_rect(midright=(grid_rect.left + padding - 5, int(y_pixel)))
                            screen.blit(text, text_rect)

                # Dibujar los ejes X e Y más gruesos
                pygame.draw.line(screen, self.black, (grid_inner_rect.left, grid_inner_rect.bottom), (grid_inner_rect.right, grid_inner_rect.bottom), 2) # Eje X
                pygame.draw.line(screen, self.black, (grid_inner_rect.left, grid_inner_rect.top), (grid_inner_rect.left, grid_inner_rect.bottom), 2) # Eje Y
            else:
                # Dibujar el borde si no hay rango de datos
                pygame.draw.rect(screen, self.black, grid_rect, 2)
                no_data_text = self.font.render("No hay datos para la cuadrícula.", True, self.black)
                text_rect = no_data_text.get_rect(center=grid_rect.center)
                screen.blit(no_data_text, text_rect)
        else:
            # Dibujar el borde si los límites no están definidos
            pygame.draw.rect(screen, self.black, grid_rect, 2)
            no_limits_text = self.font.render("Límites del plano no definidos.", True, self.black)
            text_rect = no_limits_text.get_rect(center=grid_rect.center)
            screen.blit(no_limits_text, text_rect)
    def draw(self):
        self.screen.fill(self.white)

        # Campo de entrada para la lista
        pygame.draw.rect(self.screen, self.black, self.input_rect_list, 2)
        text_label = self.font.render("Lista de Puntos:", True, self.black)
        self.screen.blit(text_label, (self.input_rect_list.left-170, self.input_rect_list.centery - text_label.get_height() // 2))
        text_surface_list = self.font.render(self.input_list_str, True, self.black)
        self.screen.blit(text_surface_list, (self.input_rect_list.x + 5, self.input_rect_list.y + 5))

        if self.input_active_list:
            pygame.draw.rect(self.screen, self.blue, self.input_rect_list, 3)

        # Botón de ingresar lista
        pygame.draw.rect(self.screen, self.blue, self.add_button_rect)
        pygame.draw.rect(self.screen, self.black, self.add_button_rect, 2)
        self.screen.blit(self.add_button_text, self.add_button_text_rect)
        # Nuevo botón para cargar desde JSON
        pygame.draw.rect(self.screen, self.blue, self.load_json_button_rect)
        pygame.draw.rect(self.screen, self.black, self.load_json_button_rect, 2)
        self.screen.blit(self.load_json_button_text, self.load_json_button_text_rect)
         # Recuadro para mostrar la lista de puntos
        self.points_display_rect = pygame.Rect(20, self.add_button_rect.bottom + 20, self.screen_width - 2*20, self.input_rect_list.height) # Debajo del botón, con espacio, toma las medidas de la caja donde se ingresan los datos
        pygame.draw.rect(self.screen, self.black, self.points_display_rect, 2) # Dibujar el borde del recuadro

        current_x = self.points_display_rect.x + 10
        y_position = self.points_display_rect.y + 5
        spacing = 10  # Espacio entre los puntos
        
        for point in self.points:
            point_text = self.font.render(str(point), True, self.black)
            self.screen.blit(point_text, (current_x, y_position))
            current_x += point_text.get_width() + spacing # Espacio entre líneas


        # Sección de árboles generados
        pygame.draw.rect(self.screen, self.black, self.trees_section_rect, 2) # Borde del recuadro
        title_text = self.font.render("Árboles Generados", True, self.black)
        self.screen.blit(title_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 10))

        length_text = self.font.render(f"Cantidad: {len(self.tree_list)}", True, self.black)
        self.screen.blit(length_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 40))

        # Mostrar el árbol actual
        if self.tree_list:
            if 0 <= self.current_tree_index < len(self.tree_list):
                current_tree = self.tree_list[self.current_tree_index]
                # Calcula la posición y el espacio para dibujar el árbol dentro del recuadro
                tree_x = self.trees_section_rect.centerx
                tree_y = self.trees_section_rect.y + 80 # Ajusta la posición vertical inicial
                espacio_x = self.trees_section_rect.width // 4 # Ajusta el espacio horizontal inicial

                # Llama a la función para dibujar el árbol
                dibujar_arbol(self.screen, current_tree.raiz, int(tree_x), int(tree_y), int(espacio_x))
            else:
                index_error_text = self.font.render("Índice de árbol fuera de rango.", True, self.black)
                self.screen.blit(index_error_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 70))
        else:
            no_trees_text = self.font.render("No hay árboles en la lista.", True, self.black)
            self.screen.blit(no_trees_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 70))

        # Botones de navegación
        pygame.draw.rect(self.screen, self.blue, self.first_button_rect)
        pygame.draw.rect(self.screen, self.black, self.first_button_rect, 2)
        self.screen.blit(self.first_button_text, (self.first_button_rect.x + 10, self.first_button_rect.y + 5))

        pygame.draw.rect(self.screen, self.blue, self.prev_button_rect)
        pygame.draw.rect(self.screen, self.black, self.prev_button_rect, 2)
        self.screen.blit(self.prev_button_text, (self.prev_button_rect.x + 10, self.prev_button_rect.y + 5))

        pygame.draw.rect(self.screen, self.blue, self.next_button_rect)
        pygame.draw.rect(self.screen, self.black, self.next_button_rect, 2)
        self.screen.blit(self.next_button_text, (self.next_button_rect.x + 10, self.next_button_rect.y + 5))

        pygame.draw.rect(self.screen, self.blue, self.last_button_rect)
        pygame.draw.rect(self.screen, self.black, self.last_button_rect, 2)
        self.screen.blit(self.last_button_text, (self.last_button_rect.x + 10, self.last_button_rect.y + 5))
        
        # Sección derecha para la cuadrícula
        #print(f"Índice actual: {self.current_tree_index}, Índice óptimo: {self.optimal_tree_index}")
        #print(f"Contenido de self.all_lines_list: {self.all_lines_list}")
        self.draw_grid_with_labels(self.screen)
        self.dibujar_lineas_plano()
        self.draw_areas()
        # Dibujar el botón "Mostrar Óptimo"
        pygame.draw.rect(self.screen, self.blue, self.optimal_button_rect)
        pygame.draw.rect(self.screen, self.black, self.optimal_button_rect, 2)
        self.screen.blit(self.optimal_button_text, self.optimal_button_text_rect)
        # Dibujar botones de color
        pygame.draw.rect(self.screen, self.blue, self.bg_color_button_rect) # Nuevo
        pygame.draw.rect(self.screen, self.black, self.bg_color_button_rect, 2) # Nuevo
        self.screen.blit(self.bg_color_button_text, self.bg_color_button_text_rect) # Nuevo

        pygame.draw.rect(self.screen, self.blue, self.outline_color_button_rect) # Nuevo
        pygame.draw.rect(self.screen, self.black, self.outline_color_button_rect, 2) # Nuevo
        self.screen.blit(self.outline_color_button_text, self.bg_color_button_text_rect) # Nuevo - Corregido a outline_color_button_text_rect

        # Dibujar entrada de texto para el elemento
        self.screen.blit(self.element_input_label, (self.element_input_rect.left - self.element_input_label.get_width() - 5, self.element_input_rect.centery - self.element_input_label.get_height() // 2)) # Nuevo
        pygame.draw.rect(self.screen, self.black, self.element_input_rect, 2) # Nuevo
        text_surface_element = self.font.render(self.element_input_text, True, self.black) # Nuevo
        self.screen.blit(text_surface_element, (self.element_input_rect.x + 5, self.element_input_rect.y + 5)) # Nuevo
        if self.element_input_active: # Nuevo
            pygame.draw.rect(self.screen, self.blue, self.element_input_rect, 3) # Nuevo
        pygame.display.flip()

    def get_points(self):
        return self.points