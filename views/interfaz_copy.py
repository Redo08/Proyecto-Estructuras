# Importación de librerías necesarias
import tkinter as tk
from tkinter import filedialog
import json
import pygame
import ast  # Para evaluar cadenas como estructuras de datos
from src.models.utils import Utils
from src.models.arbol import Nodo, Arbol
from src.models.plano import Plano
from views.grafica_arbol import dibujar_arbol
from tkinter import colorchooser  # Para selección de colores
from src.models.area import Area  # Clase para manejar áreas

class Interface:
    def __init__(self, tree_list=None, optimal_areas=None):
        """
        Inicializa la interfaz gráfica del creador de planos.
        
        Args:
            tree_list: Lista preexistente de árboles (opcional)
            optimal_areas: Áreas óptimas precalculadas (opcional)
        """
        # Inicialización de Pygame
        pygame.init()
        
        # Configuración de la ventana principal
        self.screen_width = 1000
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Creador de Planos")

        # Paleta de colores
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 128, 128)
        
        # Configuración de fuentes
        self.font = pygame.font.Font(None, 22)  # Fuente principal
        self.font_small = pygame.font.Font(None, 16)  # Fuente para etiquetas pequeñas

        # Variables para manejo de puntos
        self.points = []  # Almacena los puntos del plano
        self.radio_punto = 1  # Radio visual de los puntos
        self.input_list_str = ""  # Texto ingresado para lista de puntos
        self.input_active_list = False  # Estado del campo de entrada
        self.punto_seleccionado = None  # Punto seleccionado para mover

        # Geometría de elementos de la UI
        self.input_rect_list = pygame.Rect(180, 50, 400, 30)  # Campo de entrada
        self.add_button_rect = pygame.Rect(600, 50, 150, 30)  # Botón "Ingresar Lista"
        self.load_json_button_rect = pygame.Rect(800, 50, 180, 30)  # Botón "Cargar JSON"
        self.points_display_rect = pygame.Rect(20, 80, 960, 30)  # Área de visualización de puntos

        # Configuración de árboles
        self.tree_list = tree_list if tree_list is not None else []  # Lista de árboles
        self.current_tree_index = 0  # Índice del árbol actual mostrado
        self.optimal_tree_index = None  # Índice del árbol óptimo
        self.optimal_areas = optimal_areas if optimal_areas is not None else []  # Áreas óptimas
        self.all_lines_list = []  # Almacena todas las líneas de los árboles

        # Definición de áreas de visualización
        self.trees_section_rect = pygame.Rect(20, 150, 460, 400)  # Sección izquierda (árboles)
        self.grid_section_rect = pygame.Rect(500, 150, 460, 400)  # Sección derecha (cuadrícula)

        # Límites del plano (se establecen después con establecer_limites_plano)
        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        # Configuración de botones de navegación
        button_y = self.trees_section_rect.bottom + 20
        self.first_button_rect = pygame.Rect(20, button_y, 80, 30)
        self.prev_button_rect = pygame.Rect(110, button_y, 80, 30)
        self.next_button_rect = pygame.Rect(200, button_y, 80, 30)
        self.last_button_rect = pygame.Rect(290, button_y, 80, 30)

        # Botones para áreas óptimas
        self.optimal_button_rect = pygame.Rect(500, 560, 150, 30)
        self.bg_color_button_rect = pygame.Rect(520, 600, 180, 30)  # Color de fondo
        self.outline_color_button_rect = pygame.Rect(720, 600, 180, 30)  # Color de borde

        # Configuración para anotaciones
        self.element_input_rect = pygame.Rect(520, 640, 200, 30)
        self.element_input_text = ""
        self.element_input_active = False
        self.element_input_label = self.font.render("Anotar Elemento:", True, self.black)

        # Configuración para nombres de áreas
        self.selected_area = None  # Área seleccionada actualmente
        self.area_names = {}  # Diccionario de nombres de áreas
        self.typing_name = False  # Modo edición de nombre
        self.current_text = ""  # Texto siendo editado

        # Configuración de unidades de medida
        self.current_unit = 'm'  # Unidad por defecto (metros)
        self.cm_button_rect = pygame.Rect(self.element_input_rect.right + 10, self.element_input_rect.top, 50, 30)
        self.in_button_rect = pygame.Rect(self.cm_button_rect.right + 5, self.element_input_rect.top, 50, 30)
        self.ft_button_rect = pygame.Rect(self.in_button_rect.right + 5, self.element_input_rect.top, 50, 30)

        # Inicialización de tkinter para diálogos de archivo
        self.root_tk = tk.Tk()
        self.root_tk.withdraw()
        self.running = True  # Control del bucle principal

    def cargar_json_dialog(self):
        """Muestra un diálogo para cargar puntos desde un archivo JSON"""
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")],
            title="Seleccionar archivo JSON"
        )

        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as archivo_data:
                    data = json.load(archivo_data)
                    if isinstance(data, list):
                        self.points = [tuple(point) for point in data]
            except Exception as e:
                print(f"Error al cargar JSON: {e}")

    def process_point_list(self):
        """Procesa la lista de puntos ingresada como texto"""
        try:
            point_list = ast.literal_eval(self.input_list_str)
            if isinstance(point_list, list):
                self.points = point_list
                self.input_list_str = ""
        except (SyntaxError, ValueError):
            print("Error en formato de lista")

    def establecer_limites_plano(self, x_min, x_max, y_min, y_max):
        """Establece los límites del plano de dibujo"""
        self.x_min = x_min
        self.x_max = x_max
        self.y_min = y_min
        self.y_max = y_max

    def set_tree_list(self, new_tree_list, new_all_lines_list):
        """Actualiza la lista de árboles y sus líneas asociadas"""
        self.tree_list = new_tree_list
        self.all_lines_list = new_all_lines_list
        self.current_tree_index = 0

    def cargar_y_graficar_arboles(self, lista_de_arboles, lista_de_todas_las_lineas):
        """Carga nuevos árboles y actualiza la visualización"""
        self.set_tree_list(lista_de_arboles, lista_de_todas_las_lineas)
        pygame.display.flip()

    def set_optimal_tree_index(self, index):
        """Establece el índice del árbol óptimo"""
        if 0 <= index < len(self.tree_list):
            self.optimal_tree_index = index

    def handle_input(self, event):
        """Maneja todos los eventos de entrada del usuario"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.procesar_clics(event)
        elif event.type == pygame.MOUSEMOTION:
            self.procesar_movimiento(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self.procesar_soltar()
        elif event.type == pygame.KEYDOWN:
            self.procesar_teclado(event)

    def procesar_clics(self, event):
        """Maneja eventos de clic del mouse"""
        # Manejo de campos de entrada
        if self.input_rect_list.collidepoint(event.pos):
            self.input_active_list = True
        else:
            self.input_active_list = False

        # Manejo de botones principales
        if self.add_button_rect.collidepoint(event.pos):
            self.process_point_list()
        elif self.load_json_button_rect.collidepoint(event.pos):
            self.cargar_json_dialog()

        # Navegación de árboles
        if self.first_button_rect.collidepoint(event.pos):
            self.current_tree_index = 0
        elif self.prev_button_rect.collidepoint(event.pos):
            self.current_tree_index = max(0, self.current_tree_index - 1)
        elif self.next_button_rect.collidepoint(event.pos):
            self.current_tree_index = min(len(self.tree_list) - 1, self.current_tree_index + 1)
        elif self.last_button_rect.collidepoint(event.pos):
            self.current_tree_index = len(self.tree_list) - 1 if self.tree_list else 0

        # Botones de áreas
        if self.optimal_button_rect.collidepoint(event.pos) and self.optimal_tree_index is not None:
            self.current_tree_index = self.optimal_tree_index
        elif self.bg_color_button_rect.collidepoint(event.pos) and self.selected_area:
            color_code = colorchooser.askcolor(title="Seleccionar color de fondo")
            if color_code:
                self.selected_area.color_fondo = color_code[0]
        elif self.outline_color_button_rect.collidepoint(event.pos) and self.selected_area:
            color_code = colorchooser.askcolor(title="Seleccionar color de contorno")
            if color_code:
                self.selected_area.color_borde = color_code[0]

        # Selección de puntos y áreas
        self.verificar_seleccion(event.pos)
        self.detectar_seleccion_area(event.pos)

    def procesar_movimiento(self, event):
        """Maneja eventos de movimiento del mouse"""
        if self.punto_seleccionado is not None:
            self.mover_punto(event.pos)

    def procesar_soltar(self):
        """Maneja eventos de soltar mouse"""
        if self.punto_seleccionado is not None:
            self.punto_seleccionado = None
            self.actualizar_lista_puntos()

    def procesar_teclado(self, event):
        """Maneja eventos de teclado"""
        if self.input_active_list:
            self.procesar_entrada_puntos(event)
        elif self.element_input_active:
            self.procesar_entrada_elementos(event)
        elif self.typing_name:
            self.procesar_nombre_area(event)

    def verificar_seleccion(self, pos):
        """Verifica si se hizo clic en un punto"""
        x, y = self.transformar_coordenadas(pos)
        if x is None or y is None:
            return

        for i, (px, py) in enumerate(self.points):
            if ((x - px) ** 2 + (y - py) ** 2) ** 0.5 < self.radio_punto:
                self.punto_seleccionado = i
                return

        self.punto_seleccionado = None

    def mover_punto(self, pos):
        """Mueve el punto seleccionado"""
        if self.punto_seleccionado is None:
            return

        x, y = self.transformar_coordenadas(pos)
        x = max(self.x_min, min(x, self.x_max))
        y = max(self.y_min, min(y, self.y_max))

        self.points[self.punto_seleccionado] = (x, y)

    def transformar_coordenadas(self, pos):
        """Convierte coordenadas de pantalla a coordenadas del plano"""
        if None in (self.x_min, self.x_max, self.y_min, self.y_max):
            return None, None

        x_pantalla, y_pantalla = pos
        x_grafico = (x_pantalla - self.grid_section_rect.left) * (self.x_max - self.x_min) / self.grid_section_rect.width + self.x_min
        y_grafico = self.y_max - ((y_pantalla - self.grid_section_rect.top) * (self.y_max - self.y_min) / self.grid_section_rect.height)
        return x_grafico, y_grafico

    def draw(self):
        """Dibuja todos los componentes de la interfaz"""
        self.screen.fill(self.white)
        self.dibujar_cabecera()
        self.dibujar_seccion_arboles()
        self.dibujar_cuadricula()
        self.dibujar_botones_adicionales()
        pygame.display.flip()

    def dibujar_cabecera(self):
        """Dibuja la sección superior con campos de entrada"""
        pygame.draw.rect(self.screen, self.black, self.input_rect_list, 2)
        text_label = self.font.render("Lista de Puntos:", True, self.black)
        self.screen.blit(text_label, (self.input_rect_list.left-170, self.input_rect_list.centery - 11))
        
        text_surface = self.font.render(self.input_list_str, True, self.black)
        self.screen.blit(text_surface, (self.input_rect_list.x + 5, self.input_rect_list.y + 5))
        
        if self.input_active_list:
            pygame.draw.rect(self.screen, self.blue, self.input_rect_list, 3)

        # Botones principales
        for rect, text in [(self.add_button_rect, "Ingresar Lista"), 
                          (self.load_json_button_rect, "Cargar JSON")]:
            pygame.draw.rect(self.screen, self.blue, rect)
            pygame.draw.rect(self.screen, self.black, rect, 2)
            text_surf = self.font.render(text, True, self.white)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Muestra lista de puntos actual
        pygame.draw.rect(self.screen, self.black, self.points_display_rect, 2)
        x_pos = self.points_display_rect.x + 10
        for point in self.points:
            point_text = self.font.render(str(point), True, self.black)
            self.screen.blit(point_text, (x_pos, self.points_display_rect.y + 5))
            x_pos += point_text.get_width() + 10

    def dibujar_seccion_arboles(self):
        """Dibuja la sección izquierda con el árbol actual"""
        pygame.draw.rect(self.screen, self.black, self.trees_section_rect, 2)
        title_text = self.font.render("Árboles Generados", True, self.black)
        self.screen.blit(title_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 10))

        # Dibuja el árbol actual si existe
        if self.tree_list and 0 <= self.current_tree_index < len(self.tree_list):
            dibujar_arbol(self.screen, self.tree_list[self.current_tree_index].raiz, 
                         self.trees_section_rect.centerx, self.trees_section_rect.y + 80, 
                         self.trees_section_rect.width // 4)

        # Botones de navegación
        for rect, text in [(self.first_button_rect, "Primero"), 
                          (self.prev_button_rect, "Anterior"),
                          (self.next_button_rect, "Siguiente"),
                          (self.last_button_rect, "Último")]:
            pygame.draw.rect(self.screen, self.blue, rect)
            pygame.draw.rect(self.screen, self.black, rect, 2)
            text_surf = self.font.render(text, True, self.white)
            self.screen.blit(text_surf, (rect.x + 10, rect.y + 5))

    def dibujar_cuadricula(self):
        """Dibuja la sección derecha con la cuadrícula y elementos gráficos"""
        self.draw_grid_with_labels(self.screen)
        self.dibujar_lineas_plano()
        self.draw_areas()
        self.draw_points()

    def draw_grid_with_labels(self, screen):
        """Dibuja la cuadrícula con etiquetas de ejes"""
        if None in (self.x_min, self.x_max, self.y_min, self.y_max):
            return

        # Dibuja el borde de la cuadrícula
        pygame.draw.rect(screen, self.black, self.grid_section_rect, 2)

        # Configuración de la cuadrícula interna
        padding = 10
        inner_rect = pygame.Rect(
            self.grid_section_rect.left + padding,
            self.grid_section_rect.top + padding,
            self.grid_section_rect.width - 2 * padding,
            self.grid_section_rect.height - 2 * padding
        )

        # Dibuja líneas verticales y etiquetas X
        for i in range(11):  # 10 divisiones
            x_val = self.x_min + (self.x_max - self.x_min) * i / 10
            x_pos = inner_rect.left + inner_rect.width * i / 10
            pygame.draw.line(screen, (200, 200, 200), (x_pos, inner_rect.top), (x_pos, inner_rect.bottom), 1)
            if i % 2 == 0:  # Etiquetas cada 2 divisiones
                text = self.font_small.render(f"{x_val:.1f}", True, self.black)
                screen.blit(text, (x_pos - 15, inner_rect.bottom + 5))

        # Dibuja líneas horizontales y etiquetas Y
        for i in range(11):  # 10 divisiones
            y_val = self.y_min + (self.y_max - self.y_min) * i / 10
            y_pos = inner_rect.bottom - inner_rect.height * i / 10
            pygame.draw.line(screen, (200, 200, 200), (inner_rect.left, y_pos), (inner_rect.right, y_pos), 1)
            if i % 2 == 0:  # Etiquetas cada 2 divisiones
                text = self.font_small.render(f"{y_val:.1f}", True, self.black)
                screen.blit(text, (inner_rect.left - 40, y_pos - 10))

        # Dibuja ejes principales
        pygame.draw.line(screen, self.black, (inner_rect.left, inner_rect.bottom), (inner_rect.right, inner_rect.bottom), 2)
        pygame.draw.line(screen, self.black, (inner_rect.left, inner_rect.top), (inner_rect.left, inner_rect.bottom), 2)

    def dibujar_lineas_plano(self):
        """Dibuja las líneas de partición del árbol actual"""
        if not self.all_lines_list or not (0 <= self.current_tree_index < len(self.all_lines_list)):
            return

        line_color = (0, 0, 0)
        line_thickness = 2
        padding = 10

        if None in (self.x_min, self.x_max, self.y_min, self.y_max):
            return

        scale_x = (self.grid_section_rect.width - 2 * padding) / (self.x_max - self.x_min)
        scale_y = (self.grid_section_rect.height - 2 * padding) / (self.y_max - self.y_min)

        for punto, p_inicial, p_final in self.all_lines_list[self.current_tree_index]:
            x1 = self.grid_section_rect.left + padding + (p_inicial[0] - self.x_min) * scale_x
            y1 = self.grid_section_rect.bottom - padding - (p_inicial[1] - self.y_min) * scale_y
            x2 = self.grid_section_rect.left + padding + (p_final[0] - self.x_min) * scale_x
            y2 = self.grid_section_rect.bottom - padding - (p_final[1] - self.y_min) * scale_y

            pygame.draw.line(self.screen, line_color, (int(x1), int(y1)), (int(x2), int(y2)), line_thickness)

    def draw_areas(self):
        """Dibuja las áreas óptimas si el árbol actual es el óptimo"""
        if self.optimal_tree_index is None or self.current_tree_index != self.optimal_tree_index:
            return

        if None in (self.x_min, self.x_max, self.y_min, self.y_max):
            return

        padding = 10
        scale_x = (self.grid_section_rect.width - 2 * padding) / (self.x_max - self.x_min)
        scale_y = (self.grid_section_rect.height - 2 * padding) / (self.y_max - self.y_min)

        for area_obj in self.optimal_areas:
            scaled_points = []
            for x, y in area_obj.limites:
                scaled_x = self.grid_section_rect.left + padding + (x - self.x_min) * scale_x
                scaled_y = self.grid_section_rect.bottom - padding - (y - self.y_min) * scale_y
                scaled_points.append((int(scaled_x), int(scaled_y)))

            if scaled_points:
                # Dibuja el área
                if area_obj.color_fondo:
                    pygame.draw.polygon(self.screen, area_obj.color_fondo, scaled_points)
                pygame.draw.polygon(self.screen, area_obj.color_borde or (0, 0, 0), scaled_points, 2)

                # Dibuja etiquetas
                self.dibujar_etiquetas_area(area_obj, scaled_points, scale_x, scale_y)

    def dibujar_etiquetas_area(self, area_obj, scaled_points, scale_x, scale_y):
        """Dibuja nombres, elementos y área de una región"""
        # Calcula el centro del área
        center_x = sum(p[0] for p in scaled_points) // len(scaled_points)
        center_y = sum(p[1] for p in scaled_points) // len(scaled_points)

        # Dibuja el nombre del área si existe
        if hasattr(area_obj, 'nombre') and area_obj.nombre:
            font = pygame.font.Font(None, 30)
            name_surface = font.render(area_obj.nombre, True, (0, 0, 0))
            self.screen.blit(name_surface, (center_x - name_surface.get_width() // 2, center_y - 30))

        # Dibuja elementos gráficos
        if hasattr(area_obj, 'elementos_graficos') and area_obj.elementos_graficos:
            font = pygame.font.Font(None, 36)
            y_offset = 0
            for elemento in area_obj.elementos_graficos:
                if elemento:
                    text_surface = font.render(elemento, True, (0, 0, 0))
                    self.screen.blit(text_surface, (center_x - text_surface.get_width() // 2, center_y + y_offset))
                    y_offset += 25

        # Dibuja el área en la unidad seleccionada
        if hasattr(area_obj, 'area'):
            area_value = area_obj.area
            if self.current_unit == 'cm':
                area_value *= 10000
                unit = "cm²"
            elif self.current_unit == 'ft':
                area_value *= 10.7639
                unit = "ft²"
            else:  # metros por defecto
                unit = "m²"

            font = pygame.font.Font(None, 24)
            area_text = f"{area_value:.2f} {unit}"
            text_surface = font.render(area_text, True, (0, 0, 0))
            
            # Posiciona el texto en la parte superior del área
            min_y = min(p[1] for p in scaled_points) + 10
            self.screen.blit(text_surface, (center_x - text_surface.get_width() // 2, min_y))

    def draw_points(self):
        """Dibuja los puntos en la cuadrícula"""
        if not self.points or None in (self.x_min, self.x_max, self.y_min, self.y_max):
            return

        padding = 10
        scale_x = (self.grid_section_rect.width - 2 * padding) / (self.x_max - self.x_min)
        scale_y = (self.grid_section_rect.height - 2 * padding) / (self.y_max - self.y_min)

        for x, y in self.points:
            x_pos = self.grid_section_rect.left + padding + (x - self.x_min) * scale_x
            y_pos = self.grid_section_rect.bottom - padding - (y - self.y_min) * scale_y
            pygame.draw.circle(self.screen, (255, 0, 0), (int(x_pos), int(y_pos)), 3)

    def dibujar_botones_adicionales(self):
        """Dibuja botones inferiores y campos de entrada"""
        # Botón de área óptima
        pygame.draw.rect(self.screen, self.blue, self.optimal_button_rect)
        pygame.draw.rect(self.screen, self.black, self.optimal_button_rect, 2)
        self.screen.blit(self.optimal_button_text, self.optimal_button_text_rect)

        # Botones de color
        for rect, text in [(self.bg_color_button_rect, "Cambiar Fondo Área"),
                         (self.outline_color_button_rect, "Cambiar Borde Área")]:
            pygame.draw.rect(self.screen, self.blue, rect)
            pygame.draw.rect(self.screen, self.black, rect, 2)
            text_surf = self.font.render(text, True, self.white)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

        # Campo de entrada para elementos
        self.screen.blit(self.element_input_label, (self.element_input_rect.left - 150, self.element_input_rect.centery - 11))
        pygame.draw.rect(self.screen, self.black, self.element_input_rect, 2)
        text_surface = self.font.render(self.element_input_text, True, self.black)
        self.screen.blit(text_surface, (self.element_input_rect.x + 5, self.element_input_rect.y + 5))

        # Botones de unidades
        for rect, text, active in [(self.cm_button_rect, "cm", self.current_unit == 'cm'),
                                 (self.in_button_rect, "m", self.current_unit == 'm'),
                                 (self.ft_button_rect, "ft", self.current_unit == 'ft')]:
            color = self.blue if active else (150, 150, 150)
            pygame.draw.rect(self.screen, color, rect)
            pygame.draw.rect(self.screen, self.black, rect, 2)
            text_surf = self.font.render(text, True, self.white)
            self.screen.blit(text_surf, text_surf.get_rect(center=rect.center))

    def get_points(self):
        """Devuelve la lista actual de puntos"""
        return self.points