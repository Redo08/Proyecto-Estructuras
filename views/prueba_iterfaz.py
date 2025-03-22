import pygame
import sys
from src.models.arbol import Arbol  # Asegúrate de que la clase Arbol esté en src/models/arbol.py
from src.models.plano import Plano # Importar la clase Plano

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 30
LINE_COLOR = (255, 255, 255)
NODE_COLOR = (0, 102, 255)
TEXT_COLOR = (255, 255, 255)
BUTTON_COLOR = (50, 50, 50)
BUTTON_HOVER_COLOR = (100, 100, 100)
BUTTON_TEXT_COLOR = (255, 255, 255)
FONT_SIZE = 20
SMALL_FONT_SIZE = 16  # Para textos más pequeños
INPUT_BOX_COLOR = (220, 220, 220)
INPUT_TEXT_COLOR = (0, 0, 0)
GRID_COLOR = (128, 128, 128)  # Color para la grilla

class InterfazArboles:
    def __init__(self, arboles=None):
        """
        Inicializa la interfaz para visualizar una lista de árboles KD.

        Args:
            arboles: Una lista de objetos Arbol KD.  Si no se proporciona, se usa una lista vacía.
        """
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Visualización de Árboles KD y Planos")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.small_font = pygame.font.Font(None, SMALL_FONT_SIZE)  # Fuente más pequeña

        # Inicializar atributos
        self.arboles = arboles if arboles is not None else []  # Lista para almacenar los árboles KD
        self.puntos_ingresados = []
        self.input_text = ''
        self.input_active = False  # Para controlar si el input está activo
        self.indice_arbol_actual = 0

        # Rectángulos para las áreas de la interfaz
        self.area_cargar_json_rect = pygame.Rect(10, 10, 200, 50)
        self.area_ingresar_puntos_rect = pygame.Rect(10, 70, 200, 100)
        self.area_mostrar_puntos_rect = pygame.Rect(10, 180, 200, 100)
        self.area_arbol_rect = pygame.Rect(220, 10, WIDTH - 230, HEIGHT // 2 - 20)
        self.area_plano_rect = pygame.Rect(220, HEIGHT // 2, WIDTH - 230, HEIGHT // 2 - 10)

        self.botones = self.crear_botones()  # Esto debe ir después de la inicialización de los rectángulos
        self.planos = self.generar_planos() # Generar los planos a partir de los árboles

        self.run()

    def crear_botones(self):
        """Crea los botones de la interfaz."""
        botones = {}
        button_width = 100
        button_height = 30
        margin = 10

        # Botón para "Cargar desde JSON"
        botones['cargar_json'] = {
            'rect': self.area_cargar_json_rect,
            'texto': 'Cargar desde JSON',
            'color': BUTTON_COLOR,
            'hovered': False,
        }

        # Botón para "Ingresar Puntos"
        botones['ingresar_puntos'] = {
            'rect': self.area_ingresar_puntos_rect,
            'texto': 'Ingresar Puntos',
            'color': BUTTON_COLOR,
            'hovered': False,
        }

        # Botones de navegación del árbol
        botones['primero'] = {
            'rect': pygame.Rect(
                self.area_arbol_rect.x + margin,
                self.area_arbol_rect.bottom + margin,
                button_width,
                button_height,
            ),
            'texto': 'Primero',
            'color': BUTTON_COLOR,
            'hovered': False,
        }
        botones['anterior'] = {
            'rect': pygame.Rect(
                self.area_arbol_rect.x + margin + button_width + margin,
                self.area_arbol_rect.bottom + margin,
                button_width,
                button_height,
            ),
            'texto': 'Anterior',
            'color': BUTTON_COLOR,
            'hovered': False,
        }
        botones['siguiente'] = {
            'rect': pygame.Rect(
                self.area_arbol_rect.right - 2 * button_width - margin - margin,
                self.area_arbol_rect.bottom + margin,
                button_width,
                button_height,
            ),
            'texto': 'Siguiente',
            'color': BUTTON_COLOR,
            'hovered': False,
        }
        botones['ultimo'] = {
            'rect': pygame.Rect(
                self.area_arbol_rect.right - button_width - margin,
                self.area_arbol_rect.bottom + margin,
                button_width,
                button_height,
            ),
            'texto': 'Último',
            'color': BUTTON_COLOR,
            'hovered': False,
        }
        return botones

    def dibujar_arbol(self, nodo, x, y, espacio_x, seccion_x, seccion_y):
        """
        Dibuja el árbol de manera recursiva en la sección especificada.

        Args:
            nodo: El nodo actual del árbol a dibujar.
            x: La coordenada x del nodo.
            y: La coordenada y del nodo.
            espacio_x: El espacio horizontal entre los nodos hijo.
            seccion_x: La coordenada x de la sección donde se dibuja el árbol.
            seccion_y: La coordenada y de la sección donde se dibuja el árbol.
        """
        if nodo is None:
            return

        if nodo.izquierda:
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (seccion_x + x, seccion_y + y),
                (seccion_x + x - espacio_x, seccion_y + y + 80),
                2,
            )
            self.dibujar_arbol(
                nodo.izquierda,
                x - espacio_x,
                y + 80,
                espacio_x // 2,
                seccion_x,
                seccion_y,
            )

        if nodo.derecha:
            pygame.draw.line(
                self.screen,
                LINE_COLOR,
                (seccion_x + x, seccion_y + y),
                (seccion_x + x + espacio_x, seccion_y + y + 80),
                2,
            )
            self.dibujar_arbol(
                nodo.derecha,
                x + espacio_x,
                y + 80,
                espacio_x // 2,
                seccion_x,
                seccion_y,
            )

        pygame.draw.circle(self.screen, NODE_COLOR, (seccion_x + x, seccion_y + y), NODE_RADIUS)
        font = pygame.font.Font(None, 24)
        text = font.render(str(nodo.valor), True, (255, 255, 255))
        self.screen.blit(text, (seccion_x + x - 15, seccion_y + y - 10))

    def dibujar_plano(self, plano, seccion_x, seccion_y):
        """
        Dibuja el plano en la sección especificada.

        Args:
            plano: El objeto Plano a dibujar.
            seccion_x: La coordenada x de la sección donde se dibuja el plano.
            seccion_y: La coordenada y de la sección donde se dibuja el plano.
        """
        if plano:
            for x, y_start, y_end in plano.lineas_v:
                pygame.draw.line(
                    self.screen,
                    (0, 255, 0),
                    (seccion_x + x, seccion_y + y_start),
                    (seccion_x + x, seccion_y + y_end),
                    2,
                )
            for (x, y), (x_start, y1), (x_end, y2) in plano.lineas_h:
                pygame.draw.line(
                    self.screen,
                    (0, 0, 255),
                    (seccion_x + x_start, seccion_y + y),
                    (seccion_x + x_end, seccion_y + y),
                    2,
                )

    def dibujar_botones(self):
        """Dibuja los botones en la pantalla."""
        for boton_nombre, boton_data in self.botones.items():
            pygame.draw.rect(self.screen, boton_data['color'], boton_data['rect'])
            texto = self.font.render(boton_data['texto'], True, BUTTON_TEXT_COLOR)
            texto_rect = texto.get_rect(center=boton_data['rect'].center)
            self.screen.blit(texto, texto_rect)

    def dibujar_info_arbol(self):
        """Muestra información sobre el árbol actual y la lista de árboles."""
        texto_longitud = self.font.render(
            f"Árbol {self.indice_arbol_actual + 1} de {len(self.arboles)}",
            True,
            TEXT_COLOR,
        )
        self.screen.blit(
            texto_longitud,
            (
                self.area_arbol_rect.x + (self.area_arbol_rect.width // 2) - texto_longitud.get_width() // 2,
                self.area_arbol_rect.y + 10,
            ),
        )

    def dibujar_areas(self):
        """Dibuja los rectángulos que representan las áreas de la interfaz."""
        pygame.draw.rect(self.screen, (128, 128, 128), self.area_cargar_json_rect, 1)  # Gris
        pygame.draw.rect(self.screen, (128, 128, 128), self.area_ingresar_puntos_rect, 1)  # Gris
        pygame.draw.rect(self.screen, (128, 128, 128), self.area_mostrar_puntos_rect, 1)  # Gris
        pygame.draw.rect(self.screen, (128, 128, 128), self.area_arbol_rect, 1)  # Gris
        pygame.draw.rect(self.screen, (128, 128, 128), self.area_plano_rect, 1)  # Gris

        # Etiquetas de las áreas
        cargar_json_label = self.small_font.render("Cargar desde JSON", True, TEXT_COLOR)
        ingresar_puntos_label = self.small_font.render("Ingresar Puntos", True, TEXT_COLOR)
        mostrar_puntos_label = self.small_font.render("Puntos Ingresados", True, TEXT_COLOR)
        arbol_label = self.small_font.render("Árbol KD", True, TEXT_COLOR)
        plano_label = self.small_font.render("Plano", True, TEXT_COLOR)

        self.screen.blit(
            cargar_json_label, (self.area_cargar_json_rect.x + 5, self.area_cargar_json_rect.y + 5)
        )
        self.screen.blit(
            ingresar_puntos_label,
            (self.area_ingresar_puntos_rect.x + 5, self.area_ingresar_puntos_rect.y + 5),
        )
        self.screen.blit(
            mostrar_puntos_label,
            (self.area_mostrar_puntos_rect.x + 5, self.area_mostrar_puntos_rect.y + 5),
        )
        self.screen.blit(arbol_label, (self.area_arbol_rect.x + 5, self.area_arbol_rect.y + 5))
        self.screen.blit(plano_label, (self.area_plano_rect.x + 5, self.area_plano_rect.y + 5))

        # Dibujar la caja de entrada de texto
        pygame.draw.rect(self.screen, INPUT_BOX_COLOR, self.input_box)
        text_surface = self.font.render(self.input_text, True, INPUT_TEXT_COLOR)
        self.screen.blit(text_surface, (self.input_box.x + 5, self.input_box.y + 5))

        # Mostrar los puntos ingresados
        puntos_text = ", ".join(map(str, self.puntos_ingresados))
        puntos_surface = self.small_font.render(puntos_text, True, TEXT_COLOR)
        self.screen.blit(
            puntos_surface,
            (self.area_mostrar_puntos_rect.x + 5, self.area_mostrar_puntos_rect.y + 20),  # Ajustar la posición vertical
        )

        # Dibujar la grilla en el área del plano
        self.dibujar_grilla(self.area_plano_rect)

    def dibujar_grilla(self, rect):
        """
        Dibuja una grilla dentro del rectángulo dado.

        Args:
            rect: Un objeto pygame.Rect que define el área donde dibujar la grilla.
        """
        # Dibujar líneas verticales
        for x in range(rect.left, rect.right, 50):  # Ejemplo: cada 50 píxeles
            pygame.draw.line(self.screen, GRID_COLOR, (x, rect.top), (x, rect.bottom), 1)
        # Dibujar líneas horizontales
        for y in range(rect.top, rect.bottom, 50):
            pygame.draw.line(self.screen, GRID_COLOR, (rect.left), (rect.right, y), 1)

    def handle_eventos(self):
        """Maneja los eventos de PyGame."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Clic izquierdo
                    for boton_nombre, boton_data in self.botones.items():
                        if boton_data['rect'].collidepoint(event.pos):
                            self.manejar_click_boton(boton_nombre)
                    if self.input_box.collidepoint(event.pos):
                        self.input_active = True
                    else:
                        self.input_active = False
            elif event.type == pygame.MOUSEMOTION:
                for boton_nombre, boton_data in self.botones.items():
                    if boton_data['rect'].collidepoint(event.pos):
                        boton_data['color'] = BUTTON_HOVER_COLOR
                        boton_data['hovered'] = True
                    else:
                        boton_data['color'] = BUTTON_COLOR
                        boton_data['hovered'] = False
            elif event.type == pygame.KEYDOWN:
                if self.input_active:
                    if event.key == pygame.K_RETURN:
                        try:
                            punto = eval(self.input_text)  # Evaluar la cadena como una tupla
                            if isinstance(punto, tuple) and len(punto) == 2:
                                self.puntos_ingresados.append(punto)
                                self.input_text = ''
                            else:
                                print(
                                    "Entrada inválida. Ingrese un punto como (x, y)"
                                )  # Mensaje de error
                        except Exception as e:
                            print(f"Error al evaluar la entrada: {e}")  # Imprimir el error
                            self.input_text = ''
                    elif event.key == pygame.K_BACKSPACE:
                        self.input_text = self.input_text[:-1]
                    else:
                        self.input_text += event.unicode

    def manejar_click_boton(self, boton_nombre):
        """Maneja los clics en los botones."""
        if boton_nombre == 'primero':
            self.indice_arbol_actual = 0
        elif boton_nombre == 'anterior':
            self.indice_arbol_actual = max(0, self.indice_arbol_actual - 1)
        elif boton_nombre == 'siguiente':
            self.indice_arbol_actual = min(len(self.arboles) - 1, self.indice_arbol_actual + 1)
        elif boton_nombre == 'ultimo':
            self.indice_arbol_actual = len(self.arboles) - 1
        elif boton_nombre == 'cargar_json':
            # Aquí iría la lógica para cargar puntos desde un archivo JSON
            print("Cargar desde JSON")
            self.arboles = self.cargar_arboles_desde_json() # Esto debería devolver una lista de Arbols
            if self.arboles:
                self.indice_arbol_actual = 0
                self.planos = self.generar_planos() # Generar planos basados en los árboles cargados.

        elif boton_nombre == 'ingresar_puntos':
            # Crear un árbol con los puntos ingresados.
            if len(self.puntos_ingresados) > 0:
                # Generar el árbol KD
                arbol_kd = self.generar_arbol_kd(self.puntos_ingresados)
                self.arboles = [arbol_kd]  # Actualiza la lista de árboles con el nuevo árbol
                self.indice_arbol_actual = 0  # Establecer el índice en 0 para mostrar el primer árbol
                self.planos = self.generar_planos() # Generar planos basados en el nuevo arbol.

    def cargar_arboles_desde_json(self):
        """
        Carga la lista de árboles desde un archivo JSON.

        Returns:
            Una lista de objetos Arbol cargados desde el archivo JSON,
            o una lista vacía si no se pudo cargar correctamente.
        """
        try:
            from src.utils.funciones_auxiliares import cargar_datos  # Importar localmente para evitar dependencia circular
            datos = cargar_datos()  # Cargar los datos desde el archivo JSON
            arboles = []
            for arbol_data in datos:
                puntos = arbol_data.get("puntos", [])  # Obtener la lista de puntos del diccionario
                if puntos:
                    arbol_kd = self.generar_arbol_kd(puntos)
                    arboles.append(arbol_kd)
            return arboles
        except Exception as e:
            print(f"Error al cargar árboles desde JSON: {e}")
            return []  # Devolver una lista vacía en caso de error

    def generar_planos(self):
        """
        Genera la lista de planos a partir de la lista de árboles KD.

        Returns:
            Una lista de objetos Plano.
        """
        planos = []
        if self.arboles:
            for arbol in self.arboles:
                planos.append(Plano(arbol.recorrido_preorden_con_orientacion()))
        return planos

    def run(self):
        """Bucle principal de la interfaz."""
        running = True
        while running:
            self.screen.fill((0, 0, 0))  # Fondo negro

            self.dibujar_areas()  # Dibujar areas

            # Dibujar el plano en la sección izquierda
            if self.planos and len(self.planos) > 0:
                plano_actual = self.planos[self.indice_arbol_actual]
                self.dibujar_plano(plano_actual, self.area_plano_rect.x, self.area_plano_rect.y)
            else:
                self.dibujar_grilla(self.area_plano_rect)

            # Dibujar el árbol actual en la sección derecha
            if self.arboles and len(self.arboles) > 0:
                arbol_actual = self.arboles[self.indice_arbol_actual]
                self.dibujar_arbol(
                    arbol_actual.raiz,
                    WIDTH // 4,
                    HEIGHT // 2,
                    WIDTH // 8,
                    self.area_arbol_rect.x,
                    self.area_arbol_rect.y,
                )
                self.dibujar_info_arbol()  # Mostrar info del arbol actual

            self.dibujar_botones()
            self.handle_eventos()
            pygame.display.flip()
