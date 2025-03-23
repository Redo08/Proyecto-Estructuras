# mi_proyecto/interfaz_puntos.py

import pygame
import ast  # Para evaluar la cadena como una lista
from src.models.arbol import Nodo, Arbol
from views.grafica_arbol import dibujar_arbol
class Interface:
    def __init__(self,tree_list=None):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 768
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Creador de Planos")

        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.blue = (0, 128, 128)
        self.font = pygame.font.Font(None, 22)

        self.points =[]
        self.input_list_str = ""
        self.input_active_list = False
        self.input_rect_list = pygame.Rect(180, 50, 400, 30) #(x,y, ancho pix, larg pix)
        self.add_button_rect = pygame.Rect(600, 50, 150, 30)
        self.add_button_text = self.font.render("Ingresar Lista", True, self.white)
        self.add_button_text_rect = self.add_button_text.get_rect(center=self.add_button_rect.center)

        # Nueva sección para los árboles
        self.tree_list = tree_list if tree_list is not None else []
        self.current_tree_index = 0 
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
        self.running = True
    #Nuevo procedimiento para arboles
    def set_tree_list(self, new_tree_list):
        """Actualiza la lista de árboles y resetea el índice."""
        self.tree_list = new_tree_list
        self.current_tree_index = 0 

    def cargar_y_graficar_arboles(self, lista_de_arboles):
        """Carga la lista de árboles y fuerza un redibujado."""
        self.set_tree_list(lista_de_arboles)
        pygame.display.flip() # Fuerza una actualización de la pantalla inmediatamente

    def handle_input(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.input_rect_list.collidepoint(event.pos):
                self.input_active_list = True
            else:
                self.input_active_list = False

            if self.add_button_rect.collidepoint(event.pos):
                self.process_point_list()
             # Manejo de los botones de navegación de árboles
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
        if event.type == pygame.KEYDOWN:
            if self.input_active_list:
                if event.key == pygame.K_RETURN:
                    self.input_active_list = False
                    self.process_point_list()
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
    def dibujar_cuadricula(self, screen):
        """Dibuja una cuadrícula en la sección derecha."""
        grid_rect = self.grid_section_rect
        grid_color = (200, 200, 200) # Color gris claro para la cuadrícula
        line_thickness = 1

        # Dibujar líneas verticales
        for x in range(grid_rect.left, grid_rect.right, 50): # Espacio de 50 píxeles entre líneas
            pygame.draw.line(screen, grid_color, (x, grid_rect.top), (x, grid_rect.bottom), line_thickness)

        # Dibujar líneas horizontales
        for y in range(grid_rect.top, grid_rect.bottom, 50): # Espacio de 50 píxeles entre líneas
            pygame.draw.line(screen, grid_color, (grid_rect.left, y), (grid_rect.right, y), line_thickness)

        # Dibujar el borde de la sección de la cuadrícula (opcional)
        pygame.draw.rect(screen, self.black, grid_rect, 2)
    
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
        self.dibujar_cuadricula(self.screen)

        pygame.display.flip()

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                self.handle_input(event)
            self.draw()
        pygame.quit()

    def get_points(self):
        return self.points