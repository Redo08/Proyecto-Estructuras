import pygame
from src.models.arbol import Nodo, Arbol

# Configuración de pantalla
WIDTH, HEIGHT = 800, 600
NODE_RADIUS = 20
LINE_COLOR = (0, 0, 0)
NODE_COLOR = (0, 128, 128)
longitu_conexion=50

def dibujar_arbol(screen, nodo, x, y, espacio_x):
    """Dibuja el árbol de manera recursiva en PyGame"""
    if nodo is None:
        return

    if nodo.izquierda:
        pygame.draw.line(screen, LINE_COLOR, (x, y), (x - espacio_x, y + longitu_conexion), 2)
        dibujar_arbol(screen, nodo.izquierda, x - espacio_x, y + longitu_conexion, espacio_x // 2)

    if nodo.derecha:
        pygame.draw.line(screen, LINE_COLOR, (x, y), (x + espacio_x, y + longitu_conexion), 2)
        dibujar_arbol(screen, nodo.derecha, x + espacio_x, y + longitu_conexion, espacio_x // 2)

    pygame.draw.circle(screen, NODE_COLOR, (x, y), NODE_RADIUS)
    font = pygame.font.Font(None, 18)
    text = font.render(str(nodo.valor), True, (255, 255, 255))
    screen.blit(text, (x - 15, y - 10))
