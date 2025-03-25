import tkinter as tk
from tkinter import filedialog, colorchooser
import json
import pygame
import ast
from src.models.utils import Utils
from src.models.arbol import Nodo, Arbol
from src.models.plano import Plano
from views.grafica_arbol import dibujar_arbol
from src.models.area import Area
pygame.font.init()
class Colors:
    """Clase para centralizar la definición de colores."""
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    BLUE = (0, 128, 128)
    GRAY_LIGHT = (200, 200, 200)

class Fonts:
    """Clase para centralizar la definición de fuentes."""
    DEFAULT = pygame.font.Font(None, 22)
    SMALL = pygame.font.Font(None, 16)
    MEDIUM = pygame.font.Font(None, 32)
    LARGE = pygame.font.Font(None, 36)

class Interface2:
    def __init__(self, tree_list=None, optimal_areas=None):
        pygame.init()

        self.screen_width = 1000
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Creador de Planos")

        self.colors = Colors()
        self.fonts = Fonts()
        self.utils = Utils()
        self.plano = None  # Inicializar plano como None

        self.points =[]
        self.radio_punto = 5  # Aumentar el radio para facilitar la selección
        self.input_list_str = ""
        self.input_active_list = False
        self.input_rect_list = pygame.Rect(180, 50, 400, 30)
        self.add_button = Button(600, 50, 150, 30, "Ingresar Lista", self.fonts.DEFAULT, self.colors.WHITE)
        self.load_json_button = Button(800, 50, 180, 30, "Cargar JSON", self.fonts.DEFAULT, self.colors.WHITE)

        self.tree_list = tree_list if tree_list is not None else []
        self.current_tree_index = 0

        self.trees_section_rect = pygame.Rect(20, 150, self.screen_width // 2 - 40, 400)
        self.button_width = 80
        self.button_height = 30
        self.button_spacing = 10
        button_y = self.trees_section_rect.bottom + 20
        self.first_button = Button(20, button_y, self.button_width, self.button_height, "Primero", self.fonts.DEFAULT, self.colors.WHITE)
        self.prev_button = Button(20 + self.button_width + self.button_spacing, button_y, self.button_width, self.button_height, "Anterior", self.fonts.DEFAULT, self.colors.WHITE)
        self.next_button = Button(20 + 2 * (self.button_width + self.button_spacing), button_y, self.button_width, self.button_height, "Siguiente", self.fonts.DEFAULT, self.colors.WHITE)
        self.last_button = Button(20 + 3 * (self.button_width + self.button_spacing), button_y, self.button_width, self.button_height, "Último", self.fonts.DEFAULT, self.colors.WHITE)

        self.points_display_rect = pygame.Rect(20, self.add_button.rect.bottom + 20, self.screen_width - 40, self.input_rect_list.height)
        self.grid_section_rect = pygame.Rect(self.screen_width // 2 + 20, 150, self.screen_width // 2 - 40, 400)

        self.x_min = None
        self.x_max = None
        self.y_min = None
        self.y_max = None

        self.root_tk = tk.Tk()
        self.root_tk.withdraw()
        self.running = True
        self.all_lines_list =[]
        self.optimal_button = Button(
            self.grid_section_rect.x + (self.grid_section_rect.width - 150) // 2,
            self.grid_section_rect.bottom + 20,
            150, 30, "Mostrar Óptimo", self.fonts.DEFAULT, self.colors.WHITE
        )

        self.area_background_color = self.colors.GRAY_LIGHT
        self.area_outline_color = self.colors.BLACK
        self.optimal_areas = optimal_areas if optimal_areas is not None else []
        self.selected_area = None

        self.bg_color_button = Button(self.grid_section_rect.left + 20, self.grid_section_rect.bottom + 60, 180, 30, "Cambiar Fondo Área", self.fonts.DEFAULT, self.colors.WHITE)
        self.outline_color_button = Button(self.grid_section_rect.right - 200, self.grid_section_rect.bottom + 60, 180, 30, "Cambiar Borde Área", self.fonts.DEFAULT, self.colors.WHITE)

        self.element_input_rect = pygame.Rect(self.grid_section_rect.left + 20, self.bg_color_button.rect.bottom + 20, 200, 30)
        self.element_input_text = ""
        self.element_input_active = False
        self.element_input_label = self.fonts.DEFAULT.render("Anotar Elemento:", True, self.colors.BLACK)
        self.optimal_tree_index = None
        self.punto_seleccionado = None
        self._primera_ejecucion = True
        self.line_animation_data = {'start_time': 0, 'last_added_index': -1, 'visible_lines':[]}

    def establecer_limites_plano(self, x_min, x_max, y_min, y_max):
        """Establece los límites del plano."""
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
        """Abre un diálogo para cargar puntos desde un archivo JSON."""
        file_path = filedialog.askopenfilename(
            filetypes=[("Archivos JSON", "*.json")],
            title="Seleccionar archivo JSON"
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as archivo_data:
                    data = json.load(archivo_data)
                    if isinstance(data, list) and all(isinstance(point, list) and len(point) == 2 for point in data):
                        self.points = [tuple(point) for point in data]
                        print(f"Puntos cargados desde JSON: {self.points}")
                        self._recalcular_todo() # Recalcular todo al cargar nuevos puntos
                    else:
                        print("El archivo JSON debe contener una lista de listas o tuplas con formato [[x, y], ...]")
            except FileNotFoundError:
                print(f"Error: No se encontró el archivo en la ruta: {file_path}")
            except json.JSONDecodeError:
                print(f"Error: El archivo en la ruta: {file_path} no es un JSON válido.")
            except Exception as e:
                print(f"Ocurrió un error al cargar el JSON: {e}")

    def set_tree_list(self, new_tree_list, new_all_lines_list):
        """Actualiza la lista de árboles y resetea el índice y la animación."""
        self.tree_list = new_tree_list
        self.all_lines_list = new_all_lines_list
        self.current_tree_index = 0
        self._reset_line_animation()

    def cargar_y_graficar_arboles(self, lista_de_arboles, lista_de_todas_las_lineas):
        """Carga la lista de árboles y fuerza un redibujado."""
        self.set_tree_list(lista_de_arboles, lista_de_todas_las_lineas)
        pygame.display.flip()

    def cargar_mas_optimo(self, arbol_optimo, lineas_optimas):
        """Carga y grafica el árbol óptimo."""
        self.set_tree_list([arbol_optimo], [lineas_optimas]) # Envuelve en listas para mantener la estructura
        pygame.display.flip()

    def _reset_line_animation(self):
        """Resetea los datos de la animación de las líneas."""
        self._primera_ejecucion = True
        self.line_animation_data = {'start_time': pygame.time.get_ticks(), 'last_added_index': -1, 'visible_lines':[]}

    def _handle_input_text(self, event):
        """Maneja la entrada de texto para la lista de puntos y el elemento del área."""
        if self.input_active_list:
            if event.key == pygame.K_RETURN:
                self.input_active_list = False
                self._process_point_list()
            elif event.key == pygame.K_BACKSPACE:
                self.input_list_str = self.input_list_str[:-1]
            else:
                self.input_list_str += event.unicode
        elif self.element_input_active:
            if event.key == pygame.K_RETURN:
                self.element_input_active = False
                if self.element_input_text and self.selected_area:
                    if not hasattr(self.selected_area, 'elementos_graficos'):
                        self.selected_area.elementos_graficos =[]
                    self.selected_area.elementos_graficos.append(self.element_input_text[0].upper())
                self.element_input_text = ""
            elif event.key == pygame.K_BACKSPACE:
                self.element_input_text = self.element_input_text[:-1]
            else:
                self.element_input_text += event.unicode

    def _handle_mouse_button_down(self, event):
        """Maneja los eventos de clic del ratón."""
        if self.input_rect_list.collidepoint(event.pos):
            self.input_active_list = True
        else:
            self.input_active_list = False

        if self.add_button.is_clicked(event.pos):
            self._process_point_list()
        elif self.load_json_button.is_clicked(event.pos):
            self.cargar_json_dialog()
        elif self.first_button.is_clicked(event.pos):
            self.current_tree_index = 0
        elif self.prev_button.is_clicked(event.pos):
            if self.current_tree_index > 0:
                self.current_tree_index -= 1
        elif self.next_button.is_clicked(event.pos):
            if 0 <= self.current_tree_index < len(self.tree_list) - 1:
                self.current_tree_index += 1
        elif self.last_button.is_clicked(event.pos):
            if self.tree_list:
                self.current_tree_index = len(self.tree_list) - 1
        elif self.optimal_button.is_clicked(event.pos):
            if self.optimal_tree_index is not None:
                self.current_tree_index = self.optimal_tree_index
        elif self.bg_color_button.is_clicked(event.pos):
            self._change_area_color("fondo")
        elif self.outline_color_button.is_clicked(event.pos):
            self._change_area_color("borde")
        elif self.element_input_rect.collidepoint(event.pos):
            self.element_input_active = True
        else:
            self.element_input_active = False

        self._verificar_seleccion(event.pos)
        self._verificar_clic_en_area(event.pos)

    def _handle_mouse_motion(self, event):
        """Maneja los eventos de movimiento del ratón."""
        if self.punto_seleccionado is not None:
            self._mover_punto(event.pos)

    def _handle_mouse_button_up(self, event):
        """Maneja los eventos de liberación del botón del ratón."""
        if self.punto_seleccionado is not None:
            self.punto_seleccionado = None
            self._actualizar_lista_puntos()

    def handle_input(self, event):
        """Maneja todos los tipos de eventos."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            self._handle_mouse_button_down(event)
        elif event.type == pygame.MOUSEMOTION:
            self._handle_mouse_motion(event)
        elif event.type == pygame.MOUSEBUTTONUP:
            self._handle_mouse_button_up(event)
        elif event.type == pygame.KEYDOWN:
            self._handle_input_text(event)

    def _change_area_color(self, tipo="fondo"):
        """Abre un selector de color para cambiar el fondo o el borde del área seleccionada."""
        color_code = colorchooser.askcolor(title=f"Seleccionar color de {tipo}")
        if color_code and self.selected_area:
            if tipo == "fondo":
                self.selected_area.color_fondo = color_code[0]
            elif tipo == "borde":
                self.selected_area.color_borde = color_code[0]

    def _verificar_clic_en_area(self, pos):
        """Verifica si se hizo clic en un área óptima."""
        if self.optimal_tree_index is not None and self.current_tree_index == self.optimal_tree_index:
            mouse_x, mouse_y = pos
            for area_obj in self.optimal_areas:
                scaled_points = self._escalar_puntos_area(area_obj.limites)
                if scaled_points:
                    polygon = pygame.draw.polygon(self.screen, (0, 0, 0), scaled_points, 0)
                    if polygon.collidepoint(mouse_x, mouse_y):
                        self.selected_area = area_obj
                        print("Área seleccionada:", self.selected_area)
                        break

    def _escalar_puntos_area(self, puntos):
        """Escala los puntos de un área a las coordenadas de la pantalla."""
        if self.x_min is None or self.x_max is None or self.y_min is None or self.y_max is None or not self.grid_section_rect:
            return
        range_x = self.x_max - self.x_min
        range_y = self.y_max - self.y_min
        if range_x <= 0 or range_y <= 0:
            return
        scale_x = (self.grid_section_rect.width - 2 * 10) / range_x
        scale_y = (self.grid_section_rect.height - 2 * 10) / range_y
        scaled_points =[]
        for x, y in puntos:
            scaled_x = self.grid_section_rect.left + 10 + (x - self.x_min) * scale_x
            scaled_y = self.grid_section_rect.bottom - 10 - (y - self.y_min) * scale_y
            scaled_points.append((int(scaled_x), int(scaled_y)))
        return scaled_points

    def _transformar_coordenadas(self, pos):
        """Transforma las coordenadas de la pantalla a las coordenadas del plano."""
        if self.grid_section_rect and self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None:
            mouse_x, mouse_y = pos
            if self.grid_section_rect.collidepoint(mouse_x, mouse_y):
                padding = 10
                range_x = self.x_max - self.x_min
                range_y = self.y_max - self.y_min
                if range_x > 0 and range_y > 0:
                    scale_x = (self.grid_section_rect.width - 2 * padding) / range_x
                    scale_y = (self.grid_section_rect.height - 2 * padding) / range_y
                    x = self.x_min + (mouse_x - (self.grid_section_rect.left + padding)) / scale_x
                    y = self.y_max - (mouse_y - (self.grid_section_rect.top + padding)) / scale_y # Invertir para el eje Y
                    return x, y
        return None, None

    def _verificar_seleccion(self, pos):
        """Verifica si el usuario hizo clic en un punto."""
        x_clic, y_clic = self._transformar_coordenadas(pos)
        if x_clic is None or y_clic is None:
            return
        for i, (px, py) in enumerate(self.points):
            distancia = ((x_clic - px) ** 2 + (y_clic - py) ** 2) ** 0.5
            if distancia < self.radio_punto:
                self.punto_seleccionado = i
                return
        self.punto_seleccionado = None

    def _mover_punto(self, pos):
        """Mueve el punto seleccionado a la nueva posición."""
        if self.punto_seleccionado is not None:
            x, y = self._transformar_coordenadas(pos)
            if x is not None and y is not None:
                self.points[self.punto_seleccionado] = (x, y)

    def _actualizar_lista_puntos(self):
        """Actualiza la lista de puntos y recalcula los árboles y el plano."""
        if self.points:
            self.plano = Plano(self.points)
            self.plano.calcular_limites()
            self.establecer_limites_plano(self.plano.x_min, self.plano.x_max, self.plano.y_min, self.plano.y_max)
            arboles = self.utils.permutaciones_unique_arbol(self.points)
            puntos_permutados = self.utils.permutaciones_unique_puntos(self.points)
            lineas = self.utils.generar_todas_las_lineas_por_arbol(arboles)
            self.cargar_y_graficar_arboles(arboles, lineas)
            index, areas_optimas = self.utils.areas_optimas(puntos_permutados)
            self.optimal_areas = areas_optimas
            self.set_optimal_tree_index(index)
            self._reset_line_animation() # Resetear animación al actualizar puntos

    def _process_point_list(self):
        """Procesa la cadena de texto ingresada para crear la lista de puntos."""
        try:
            point_list = ast.literal_eval(self.input_list_str)
            if isinstance(point_list, list) and all(isinstance(point, tuple) and len(point) == 2 for point in point_list):
                self.points = [tuple(point) for point in point_list]
                self.input_list_str = ""
                self._recalcular_todo() # Recalcular todo al ingresar lista
            else:
                print("Por favor, ingresa una lista válida de tuplas con formato [(x, y), ...]")
        except (SyntaxError, ValueError):
            print("Error al procesar la lista. Asegúrate de usar el formato correcto: [(x, y), ...]")

    def _recalcular_todo(self):
        """Recalcula los límites, árboles, líneas y áreas óptimas."""
        if self.points:
            self.plano = Plano(self.points)
            self.plano.calcular_limites()
            self.establecer_limites_plano(self.plano.x_min, self.plano.x_max, self.plano.y_min, self.plano.y_max)
            arboles = self.utils.permutaciones_unique_arbol(self.points)
            puntos_permutados = self.utils.permutaciones_unique_puntos(self.points)
            lineas = self.utils.generar_todas_las_lineas_por_arbol(arboles)
            self.cargar_y_graficar_arboles(arboles, lineas)
            index, areas_optimas = self.utils.areas_optimas(puntos_permutados)
            self.optimal_areas = areas_optimas
            self.set_optimal_tree_index(index)
            self._reset_line_animation()

    def draw_areas(self):
        """Dibuja las áreas en la sección derecha (cuadrícula) si el árbol actual es el óptimo."""
        if self.optimal_tree_index is not None and self.current_tree_index == self.optimal_tree_index:
            if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
                range_x = self.x_max - self.x_min
                range_y = self.y_max - self.y_min
                if range_x > 0 and range_y > 0:
                    scale_x = (self.grid_section_rect.width - 2 * 10) / range_x
                    scale_y = (self.grid_section_rect.height - 2 * 10) / range_y
                    for area_obj in self.optimal_areas:
                        scaled_points =[]
                        for x, y in area_obj.limites:
                            scaled_x = self.grid_section_rect.left + 10 + (x - self.x_min) * scale_x
                            scaled_y = self.grid_section_rect.bottom - 10 - (y - self.y_min) * scale_y
                            scaled_points.append((int(scaled_x), int(scaled_y)))
                        if scaled_points:
                            fondo = area_obj.color_fondo if hasattr(area_obj, 'color_fondo') and area_obj.color_fondo else self.area_background_color
                            borde = area_obj.color_borde if hasattr(area_obj, 'color_borde') and area_obj.color_borde else self.area_outline_color
                            pygame.draw.polygon(self.screen, fondo, scaled_points)
                            pygame.draw.polygon(self.screen, borde, scaled_points, 2)
                            if hasattr(area_obj, 'elementos_graficos') and isinstance(area_obj.elementos_graficos, list):
                                font = self.fonts.LARGE
                                center_x = int(self.grid_section_rect.left + 10 + (sum(p[0] for p in area_obj.limites) / len(area_obj.limites) - self.x_min) * scale_x)
                                center_y = int(self.grid_section_rect.bottom - 10 - (sum(p[1] for p in area_obj.limites) / len(area_obj.limites) - self.y_min) * scale_y)
                                y_offset = 0
                                for elemento in area_obj.elementos_graficos:
                                    if elemento:
                                        text_surface = font.render(elemento, True, self.colors.BLACK)
                                        text_rect = text_surface.get_rect(center=(center_x, center_y + y_offset))
                                        self.screen.blit(text_surface, text_rect)
                                        y_offset += 20

    def dibujar_lineas_plano(self):
        """Dibuja las líneas del plano en la sección derecha (cuadrícula) con animación."""
        line_color = self.colors.BLACK
        line_thickness = 2
        padding = 10

        if self.x_min is not None and self.x_max is not None and self.y_min is not None and self.y_max is not None and self.grid_section_rect:
            range_x = self.x_max - self.x_min
            range_y = self.y_max - self.y_min
            if range_x > 0 and range_y > 0:
                scale_x = (self.grid_section_rect.width - 2 * padding) / range_x
                scale_y = (self.grid_section_rect.height - 2 * padding) / range_y

                if self.all_lines_list and 0 <= self.current_tree_index < len(self.all_lines_list):
                    lineas_actuales = self.all_lines_list[self.current_tree_index]

                    if self._primera_ejecucion:
                        current_time = pygame.time.get_ticks()
                        elapsed = current_time - self.line_animation_data['start_time']
                        draw_interval = 500  # Medio segundo por línea

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

                            if next_index >= len(lineas_actuales) - 1:
                                self._primera_ejecucion = False
                                break

                        for line in self.line_animation_data['visible_lines']:
                            pygame.draw.line(self.screen, line_color, line[0], line[1], line_thickness)
                    else:
                        # Dibujar todas las líneas si la animación ya terminó
                        for _, p_inicial, p_final in lineas_actuales:
                            x1 = self.grid_section_rect.left + padding + (p_inicial[0] - self.x_min) * scale_x
                            y1 = self.grid_section_rect.bottom - padding - (p_inicial[1] - self.y_min) * scale_y
                            x2 = self.grid_section_rect.left + padding + (p_final[0] - self.x_min) * scale_x
                            y2 = self.grid_section_rect.bottom - padding - (p_final[1] - self.y_min) * scale_y
                            pygame.draw.line(self.screen, line_color, (x1, y1), (x2, y2), line_thickness)

                    # Dibujar el primer punto del árbol actual
                    if lineas_actuales:
                        _, p_inicial, _ = lineas_actuales[0]
                        x_point = self.grid_section_rect.left + padding + (p_inicial[0] - self.x_min) * scale_x
                        y_point = self.grid_section_rect.bottom - padding - (p_inicial[1] - self.y_min) * scale_y
                        pygame.draw.circle(self.screen, self.colors.BLUE, (int(x_point), int(y_point)), 5)

    def dibujar_puntos(self):
        """Dibuja los puntos en la sección izquierda."""
        for point in self.points:
            pygame.draw.circle(self.screen, self.colors.BLACK, point, self.radio_punto)

    def dibujar_interfaz(self):
        """Dibuja todos los elementos de la interfaz."""
        self.screen.fill(self.colors.WHITE)

        # Sección de entrada de lista de puntos
        pygame.draw.rect(self.screen, self.colors.BLACK, self.input_rect_list, 2)
        text_surface = self.fonts.DEFAULT.render(self.input_list_str, True, self.colors.BLACK)
        self.screen.blit(text_surface, (self.input_rect_list.x + 5, self.input_rect_list.y + 5))
        self.add_button.draw(self.screen)
        self.load_json_button.draw(self.screen)

        # Recuadro para mostrar la lista de puntos
        pygame.draw.rect(self.screen, self.colors.BLACK, self.points_display_rect, 1)
        points_text = self.fonts.SMALL.render(f"Puntos: {self.points}", True, self.colors.BLACK)
        self.screen.blit(points_text, (self.points_display_rect.x + 5, self.points_display_rect.y + 5))

        # Sección de árboles
        pygame.draw.rect(self.screen, self.colors.BLACK, self.trees_section_rect, 2)
        title_text = self.fonts.DEFAULT.render("Árboles Generados", True, self.colors.BLACK)
        self.screen.blit(title_text, (self.trees_section_rect.x + 10, self.trees_section_rect.y + 10))

        if self.tree_list and 0 <= self.current_tree_index < len(self.tree_list):
            arbol_actual = self.tree_list[self.current_tree_index]
            dibujar_arbol(self.screen, arbol_actual, self.trees_section_rect, self.fonts.SMALL)
            index_text = self.fonts.SMALL.render(f"Árbol {self.current_tree_index + 1}/{len(self.tree_list)}", True, self.colors.BLACK)
            self.screen.blit(index_text, (self.trees_section_rect.x + 10, self.trees_section_rect.bottom - 20))
        elif not self.points:
            no_points_text = self.fonts.DEFAULT.render("Ingresa puntos para generar árboles", True, self.colors.BLACK)
            self.screen.blit(no_points_text, (self.trees_section_rect.centerx - no_points_text.get_width() // 2, self.trees_section_rect.centery - no_points_text.get_height() // 2))
        elif not self.tree_list:
            no_trees_text = self.fonts.DEFAULT.render("No se pudieron generar árboles", True, self.colors.BLACK)
            self.screen.blit(no_trees_text, (self.trees_section_rect.centerx - no_trees_text.get_width() // 2, self.trees_section_rect.centery - no_trees_text.get_height() // 2))

        self.first_button.draw(self.screen)
        self.prev_button.draw(self.screen)
        self.next_button.draw(self.screen)
        self.last_button.draw(self.screen)

        # Sección de la cuadrícula (plano)
        pygame.draw.rect(self.screen, self.colors.BLACK, self.grid_section_rect, 2)
        grid_title_text = self.fonts.DEFAULT.render("Plano Generado", True, self.colors.BLACK)
        self.screen.blit(grid_title_text, (self.grid_section_rect.x + 10, self.grid_section_rect.y + 10))

        if self.x_min is not None:
            self.dibujar_lineas_plano()
            self.draw_areas()
            self.optimal_button.draw(self.screen)
            self.bg_color_button.draw(self.screen)
            self.outline_color_button.draw(self.screen)

            # Entrada de texto para anotar elementos
            self.screen.blit(self.element_input_label, (self.element_input_rect.x, self.element_input_rect.y - 20))
            pygame.draw.rect(self.screen, self.colors.BLACK, self.element_input_rect, 2)
            element_text_surface = self.fonts.DEFAULT.render(self.element_input_text, True, self.colors.BLACK)
            self.screen.blit(element_text_surface, (self.element_input_rect.x + 5, self.element_input_rect.y + 5))

        elif self.points:
            no_plano_text = self.fonts.DEFAULT.render("Plano se mostrará aquí", True, self.colors.BLACK)
            self.screen.blit(no_plano_text, (self.grid_section_rect.centerx - no_plano_text.get_width() // 2, self.grid_section_rect.centery - no_plano_text.get_height() // 2))

        self.dibujar_puntos() # Dibujar puntos sobre todo

        pygame.display.flip()

    

class Button:
    """Clase para representar botones en la interfaz."""
    def __init__(self, x, y, width, height, text, font, color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.text_surface = font.render(text, True, color)
        self.text_rect = self.text_surface.get_rect(center=self.rect.center)

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)
        pygame.draw.rect(surface, (0, 0, 0), self.rect, 2) # Borde negro
        surface.blit(self.text_surface, self.text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

