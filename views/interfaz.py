# mi_proyecto/interfaz_puntos.py
import tkinter as tk
from tkinter import filedialog
import json
import pygame
import ast  # Para evaluar la cadena como una lista
from src.models.utils import Utils
from src.models.arbol import Nodo, Arbol
from src.models.plano import Plano
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
        self.radio_punto = 1
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

        # Areas
        self.selected_area = None # Inicializamos el área seleccionada
        self.area_names = {} #Diccionario para almacenar nombres de las areas
        self.typing_name = False #Inicializa si el usuario esta escribiendo algo
        self.current_text = "" #Almacena el texto que el usuario esta haciendo

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
        
        self.punto_seleccionado = None

        # --- Nuevos botones para cm, in, ft ---
        self.cm_button_rect = pygame.Rect(self.input_rect_list.right + 10, self.input_rect_list.top, 50, 30)
        self.in_button_rect = pygame.Rect(self.cm_button_rect.right + 5, self.input_rect_list.top, 50, 30)
        self.ft_button_rect = pygame.Rect(self.in_button_rect.right + 5, self.input_rect_list.top, 50, 30)

        self.cm_button_text = self.font.render("cm", True, self.white)
        self.in_button_text = self.font.render("in", True, self.white)
        self.ft_button_text = self.font.render("ft", True, self.white)
        self.cm_active = False
        self.in_active = False
        self.ft_active = False

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
                print("⏮️ Botón Primero presionado")
                self.current_tree_index = 0
            elif self.prev_button_rect.collidepoint(event.pos):
                if self.current_tree_index > 0:
                    self.current_tree_index -= 1
                    print(f"⬅️ Botón Anterior, nuevo índice: {self.current_tree_index}")
            elif self.next_button_rect.collidepoint(event.pos):
                if 0 <= self.current_tree_index < len(self.tree_list) - 1:
                    self.current_tree_index += 1
                    print(f"➡️ Botón Siguiente, nuevo índice: {self.current_tree_index}")
            elif self.last_button_rect.collidepoint(event.pos):
                if self.tree_list:
                    self.current_tree_index = len(self.tree_list) - 1
                    print(f"⏭️ Botón Último, nuevo índice: {self.current_tree_index}")
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
                
            mouse_x, mouse_y = event.pos
            self.selected_area = None
            # --- Lógica para detectar clic en un área ---
            if self.optimal_tree_index is not None and self.current_tree_index == self.optimal_tree_index: #Para que siempre sea el optimo
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
                                # Imprimir los puntos escalados de cada área
                                polygon = pygame.draw.polygon(self.screen, (0, 0, 0), scaled_points, 0)
                                if polygon.collidepoint(mouse_x, mouse_y):
                                    self.selected_area = area_obj
                                    self.typing_name = True # Habilita el modo de escritura
                                    self.current_text = "" #Reinicia el texto
                                    print("Área seleccionada:", self.selected_area)
                                    break
                                                    
            # Nueva funcionalidad: verificar si se clickea un punto
            self.verificar_seleccion(event.pos)           
                  
        elif event.type == pygame.MOUSEMOTION:
            if self.punto_seleccionado is not None:  
                self.mover_punto(event.pos) 
        
        elif event.type == pygame.MOUSEBUTTONUP:
            if self.punto_seleccionado is not None:
                self.punto_seleccionado = None  
                self.actualizar_lista_puntos()  # Guarda la nueva posición y recalcula todo     
                 
        elif event.type == pygame.KEYDOWN:
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
                    print(f"🔠 Texto ingresado: {self.element_input_text}")  # Verifica qué texto ingresaste
                    print(f"📌 Área seleccionada: {self.selected_area}")  # ¿Es `None`?
                    
                    self.element_input_active = False
                    if self.element_input_text: #Evitar entradas vacias
                        first_letter = self.element_input_text[0].upper()
                        
                        for area_obj in self.optimal_areas:
                            print(f"🔍 Comparando con área: {area_obj}")  # Verifica si `selected_area` está en `optimal_areas`

                            if area_obj == self.selected_area:
                                print(f"✅ Guardando '{first_letter}' en {area_obj}")
                                if not area_obj.elementos_graficos:
                                    area_obj.elementos_graficos = []
                                area_obj.elementos_graficos.append(first_letter)
                                
                    self.element_input_text = ""
                        
                elif event.key == pygame.K_BACKSPACE:
                    self.element_input_text = self.element_input_text[:-1]
                else:
                    self.element_input_text += event.unicode
                    
            #---- Manejo de la entrada de texto para nombrar un area  
            elif self.typing_name:
                if event.key == pygame.K_RETURN:
                    self.typing_name = False
                    if self.current_text:
                        self.selected_area.nombre = self.current_text
                    self.current_text = ""
                    
                elif event.key == pygame.K_BACKSPACE:
                    self.current_text = self.current_text[:-1]
                else:
                    self.current_text += event.unicode  
                    
    def show_area_naming_dialog(self):
        if not self.selected_area:
            return
            
        # Configuración del diálogo
        font = pygame.font.Font(None, 32)
        input_box = pygame.Rect(300, 300, 400, 40)
        color_inactive = pygame.Color('lightskyblue3')
        color_active = pygame.Color('dodgerblue2')
        color = color_active
        active = True
        text = self.selected_area.elementos_graficos[0] if hasattr(self.selected_area, 'elementos_graficos') and self.selected_area.elementos_graficos else ""
        
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Guardar el texto en el área
                        if not hasattr(self.selected_area, 'elementos_graficos'):
                            self.selected_area.elementos_graficos = []
                        if len(self.selected_area.elementos_graficos) == 0:
                            self.selected_area.elementos_graficos.append(text)
                        else:
                            self.selected_area.elementos_graficos[0] = text
                        return
                    elif event.key == pygame.K_ESCAPE:
                        return
                    elif event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    else:
                        text += event.unicode
            
            # Dibujar
            self.screen.fill((240, 240, 240))
            txt_surface = font.render(text, True, color)
            width = max(400, txt_surface.get_width()+10)
            input_box.w = width
            self.screen.blit(font.render("Nombre del área:", True, (0,0,0)), (300, 270))
            self.screen.blit(txt_surface, (input_box.x+5, input_box.y+5))
            pygame.draw.rect(self.screen, color, input_box, 2)
            pygame.display.flip()                    

    def verificar_seleccion(self, pos):
        """Verifica si el usuario hizo clic en un punto"""
        x, y = self.transformar_coordenadas(pos)  # Convertimos coordenadas

        # Si la transformación falló, salimos
        if x is None or y is None:
            return  


        for i, (px, py) in enumerate(self.points):
            distancia = ((x - px) ** 2 + (y - py) ** 2) ** 0.5

            if distancia < self.radio_punto:
                self.punto_seleccionado = i
                return

        self.punto_seleccionado = None

    def actualizar_lista_puntos(self):
        if self.points:  
            # Enviar los nuevos puntos a la clase Plano
            plano = Plano(self.points)  
            plano.calcular_limites()

            # Obtener nuevos límites del plano
            x_min_plano = plano.x_min
            x_max_plano = plano.x_max
            y_min_plano = plano.y_min
            y_max_plano = plano.y_max

            # Actualizar la interfaz con los nuevos límites
            self.establecer_limites_plano(x_min_plano, x_max_plano, y_min_plano, y_max_plano)

            # Llamar nuevamente a los cálculos de árboles y líneas
            utils = Utils()
            arboles = utils.permutaciones_unique_arbol(self.points)
            puntos = utils.permutaciones_unique_puntos(self.points)
            lineas = utils.generar_todas_las_lineas_por_arbol(arboles)

            # Cargar y graficar nuevamente
            self.cargar_y_graficar_arboles(arboles, lineas)

            # Actualizar el árbol óptimo
            index, areas_optimas = utils.areas_optimas(puntos)
            
            self.optimal_areas = areas_optimas
            self.set_optimal_tree_index(index)
            
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
                    print(f"Area {area_obj} - Elementos graficos: {area_obj.elementos_graficos}")
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
                       # Solo dibuja el fondo si area_obj.color_fondo tiene un valor
                        if area_obj.color_fondo is not None:
                            fondo = area_obj.color_fondo
                             # Paso 15: Dibuja el polígono relleno en la pantalla utilizando los puntos escalados y el color de fondo.
                            pygame.draw.polygon(self.screen, fondo, scaled_points)
                        # Paso 14: Determina el color del borde del área de manera similar al color de fondo.
                        borde = area_obj.color_borde if area_obj.color_borde else (0, 0, 0) # Asegúrate de que el borde sea visible
                       
                        
                        # Paso 16: Dibuja el borde del polígono utilizando los mismos puntos escalados y el color del borde, con un grosor de 2 píxeles.
                        pygame.draw.polygon(self.screen, borde, scaled_points, 2)

                        center_x = int(self.grid_section_rect.left + 10 + (sum(p[0] for p in area_obj.limites) / len(area_obj.limites) - self.x_min) * scale_x)
                        center_y = int(self.grid_section_rect.bottom - 10 - (sum(p[1] for p in area_obj.limites) / len(area_obj.limites) - self.y_min) * scale_y)
                        
                        if hasattr(area_obj, 'nombre') and area_obj.nombre:
                            font = pygame.font.Font(None, 30)
                            name_surface = font.render(area_obj.nombre, True, (0,0,0))
                            name_rect = name_surface.get_rect(center=(center_x, center_y - 15))  # Ajuste para separar del elemento gráfico
                            self.screen.blit(name_surface, name_rect)
                            
                            if area_obj.elementos_graficos and isinstance(area_obj.elementos_graficos, list):
                                font = pygame.font.Font(None, 36)
                                y_offset = 15

                                for elemento in area_obj.elementos_graficos:
                                    if elemento:
                                        text_surface = font.render(elemento, True, (0, 0, 0))
                                        text_rect = text_surface.get_rect(center=(center_x, center_y + y_offset))
                                        self.screen.blit(text_surface, text_rect)
                                        y_offset += 20  # Ajusta este valor para el espaciado vertical entre elementos    
    
    def dibujar_lineas_plano(self):
        """Dibuja las líneas del plano y su primer punto en la sección derecha (cuadrícula)."""
        line_color = (0, 0, 0) # Negro para las líneas
        line_thickness = 2
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
                    lineas_actuales = self.all_lines_list[self.current_tree_index]
                    
                    #Inicializamos si el tiempo no existe
                    if not hasattr(self, '_primera_ejecucion'):
                        self._primera_ejecucion = True
                        self.line_animation_data = {
                            'start_time': pygame.time.get_ticks(),
                            'last_added_index': -1,
                            'visible_lines': []
                        }
                    
                    if self._primera_ejecucion:
                        # Lógica de animación solo para la primera vez
                        current_time = pygame.time.get_ticks()
                        elapsed = current_time - self.line_animation_data['start_time']
                        draw_interval = 1000  # .5 segundo

                        target_index = min(int(elapsed / draw_interval), len(lineas_actuales) - 1)

                        while self.line_animation_data['last_added_index'] < target_index:
                            next_index = self.line_animation_data['last_added_index'] + 1
                            punto, p_inicial, p_final = lineas_actuales[next_index]

                            x1 = self.grid_section_rect.left + padding + (p_inicial[0] - self.x_min) * scale_x
                            y1 = self.grid_section_rect.bottom - padding - (p_inicial[1] - self.y_min) * scale_y
                            x2 = self.grid_section_rect.left + padding + (p_final[0] - self.x_min) * scale_x
                            y2 = self.grid_section_rect.bottom - padding - (p_final[1] - self.y_min) * scale_y

                            self.line_animation_data['visible_lines'].append(((x1, y1), (x2, y2)))
                            self.line_animation_data['last_added_index'] = next_index

                            # Si llegamos al final, marcamos que ya no es la primera ejecución
                            if next_index >= len(lineas_actuales) - 1:
                                self._primera_ejecucion = False
                                break

                        # Dibujar solo las líneas animadas
                        for line in self.line_animation_data['visible_lines']:
                            pygame.draw.line(self.screen, line_color, 
                                           (int(line[0][0]), int(line[0][1])),
                                           (int(line[1][0]), int(line[1][1])), 
                                           line_thickness)
                    else:
                        # Modo normal: dibuja todas las líneas inmediatamente
                        for punto, p_inicial, p_final in lineas_actuales:
                            x1 = self.grid_section_rect.left + padding + (p_inicial[0] - self.x_min) * scale_x
                            y1 = self.grid_section_rect.bottom - padding - (p_inicial[1] - self.y_min) * scale_y
                            x2 = self.grid_section_rect.left + padding + (p_final[0] - self.x_min) * scale_x
                            y2 = self.grid_section_rect.bottom - padding - (p_final[1] - self.y_min) * scale_y

                            pygame.draw.line(self.screen, line_color, 
                                           (int(x1), int(y1)), 
                                           (int(x2), int(y2)), 
                                           line_thickness)
                        

                        
    def draw_points(self):
        """Dibuja los puntos en la sección derecha (cuadrícula)."""
        point_color = (255, 0, 0) # Rojo para los puntos
        point_radius = 3
        padding = 10

        if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
            range_x = self.x_max - self.x_min
            range_y = self.y_max - self.y_min
            if range_x > 0 and range_y > 0:
                scale_x = (self.grid_section_rect.width - 2 * padding) / range_x
                scale_y = (self.grid_section_rect.height - 2 * padding) / range_y

                for point in self.points:
                    x_point = self.grid_section_rect.left + padding + (point[0] - self.x_min) * scale_x
                    y_point = self.grid_section_rect.bottom - padding - (point[1] - self.y_min) * scale_y
                    pygame.draw.circle(self.screen, point_color, (int(x_point), int(y_point)), point_radius)

    def transformar_coordenadas(self, pos):
        """Convierte coordenadas de pantalla a coordenadas del gráfico"""
        if self.x_min is None or self.x_max is None or self.y_min is None or self.y_max is None:
            print("Error: Los límites del plano aún no han sido definidos.")
            return None, None

        x_pantalla, y_pantalla = pos

        # Transformación corregida
        x_grafico = (x_pantalla - self.grid_section_rect.left) * (self.x_max - self.x_min) / self.grid_section_rect.width + self.x_min
        y_grafico = self.y_max - ((y_pantalla - self.grid_section_rect.top) * (self.y_max - self.y_min) / self.grid_section_rect.height)

        print(f"Transformación: {pos} -> ({x_grafico}, {y_grafico})")  
        return x_grafico, y_grafico
    
    def mover_punto(self, pos):
        """Mueve el punto seleccionado al arrastrar el mouse"""
        if self.punto_seleccionado is None:
            return

        x, y = self.transformar_coordenadas(pos)  # Convertimos a coordenadas del gráfico

        # Asegurar que no se salga del rango permitido
        x = max(self.x_min, min(x, self.x_max))
        y = max(self.y_min, min(y, self.y_max))

        print(f"Moviendo punto {self.punto_seleccionado} a ({x}, {y})")  
        self.points[self.punto_seleccionado] = (x, y)

    
    def soltar_punto(self):
        """Se llama cuando el usuario suelta el mouse"""
        if self.punto_seleccionado is not None:
            print(f"Punto {self.punto_seleccionado} fijado en {self.points[self.punto_seleccionado]}")
            
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
                
                num_x_segments = int(self.x_max) # Puedes ajustar la cantidad de segmentos
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
                
                
                num_y_segments = int(self.y_max) # Puedes ajustar la cantidad de segmentos
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
        
        self.draw_points()
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
        self.screen.blit(self.outline_color_button_text, self.outline_color_button_text_rect) # Nuevo - Corregido a outline_color_button_text_rect
        
        # --- Nuevos botones para cm, in, ft al lado de "Anotar Elemento" ---
        button_y = self.element_input_rect.top  # La misma altura que el input de anotar elemento
        self.cm_button_rect = pygame.Rect(self.element_input_rect.right + 10, button_y, 50, 30)
        self.in_button_rect = pygame.Rect(self.cm_button_rect.right + 5, button_y, 50, 30)
        self.ft_button_rect = pygame.Rect(self.in_button_rect.right + 5, button_y, 50, 30)

        self.cm_button_text = self.font.render("cm", True, self.white)
        self.in_button_text = self.font.render("in", True, self.white)
        self.ft_button_text = self.font.render("ft", True, self.white)
        self.cm_active = False
        self.in_active = False
        self.ft_active = False
        
        # Dibujar entrada de texto para el elemento
        self.screen.blit(self.element_input_label, (self.element_input_rect.left - self.element_input_label.get_width() - 5, self.element_input_rect.centery - self.element_input_label.get_height() // 2)) # Nuevo
        pygame.draw.rect(self.screen, self.black, self.element_input_rect, 2) # Nuevo
        text_surface_element = self.font.render(self.element_input_text, True, self.black) # Nuevo
        self.screen.blit(text_surface_element, (self.element_input_rect.x + 5, self.element_input_rect.y + 5)) # Nuevo

        # --- Dibujar los botones de unidades (cm, in, ft) ---
        pygame.draw.rect(self.screen, self.blue, self.cm_button_rect)  # Fondo azul
        pygame.draw.rect(self.screen, self.black, self.cm_button_rect, 2) # Borde negro
        self.screen.blit(self.cm_button_text, self.cm_button_text.get_rect(center=self.cm_button_rect.center))

        pygame.draw.rect(self.screen, self.blue, self.in_button_rect)  # Fondo azul
        pygame.draw.rect(self.screen, self.black, self.in_button_rect, 2) # Borde negro
        self.screen.blit(self.in_button_text, self.in_button_text.get_rect(center=self.in_button_rect.center))

        pygame.draw.rect(self.screen, self.blue, self.ft_button_rect)  # Fondo azul
        pygame.draw.rect(self.screen, self.black, self.ft_button_rect, 2) # Borde negro
        self.screen.blit(self.ft_button_text, self.ft_button_text.get_rect(center=self.ft_button_rect.center))
        if self.element_input_active: # Nuevo
            pygame.draw.rect(self.screen, self.blue, self.element_input_rect, 3) # Nuevo
        pygame.display.flip()

    def get_points(self):
        return self.points