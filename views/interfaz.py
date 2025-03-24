# mi_proyecto/interfaz_puntos.py
import tkinter as tk
from tkinter import filedialog
import json
import pygame
import os 
import ast  # Para evaluar la cadena como una lista
from src.models.utils import Utils
from src.models.arbol import Nodo, Arbol
from views.grafica_arbol import dibujar_arbol
class Interface:
    def __init__(self,tree_list=None):
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
        utils = Utils()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect_list.collidepoint(event.pos):
                self.input_active_list = True
            else:
                self.input_active_list = False

            if self.add_button_rect.collidepoint(event.pos):
                self.process_point_list()
            elif self.load_json_button_rect.collidepoint(event.pos):
                self.cargar_json_dialog() # Usar el texto del campo de entrada como ruta


                
            # Manejo de los botones de navegación de árboles (sin cambios)
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
             # Manejo del clic en el botón "Mostrar Óptimo"
            elif self.optimal_button_rect.collidepoint(event.pos):
                if self.optimal_tree_index is not None:
                    self.current_tree_index = self.optimal_tree_index

        if event.type == pygame.KEYDOWN:
            if self.input_active_list:
                if event.key == pygame.K_RETURN:
                    self.input_active_list = False
                    # Aquí podríamos verificar si se presionó Enter después de ingresar una lista o una ruta de JSON
                    # Podrías agregar lógica adicional si quieres que Enter active alguna de las dos funciones
                    self.process_point_list() # Por ahora, Enter solo procesa la lista manual
                elif event.key == pygame.K_BACKSPACE:
                    self.input_list_str = self.input_list_str[:-1]
                else:
                    self.input_list_str += event.unicode

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
        #print(f"Índice del árbol actual: {self.current_tree_index}")
        #print(f"Contenido de self.all_lines_list: {self.all_lines_list}")
        self.draw_grid_with_labels(self.screen)
        self.dibujar_lineas_plano()
        # Dibujar el botón "Mostrar Óptimo"
        pygame.draw.rect(self.screen, self.blue, self.optimal_button_rect)
        pygame.draw.rect(self.screen, self.black, self.optimal_button_rect, 2)
        self.screen.blit(self.optimal_button_text, self.optimal_button_text_rect)
        pygame.display.flip()

    def get_points(self):
        return self.points