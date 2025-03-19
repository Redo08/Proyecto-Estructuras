
from punto import Punto

class Linea:
    def __init__(self, punto_inicial, punto_final, punto_posicion, orientacion):
        """Inicializa una línea desde un punto con una orientación ('vertical' o 'horizontal')."""
        self.punto_inicial = punto_inicial
        self.punto_final = punto_final
        self.punto = punto_posicion
        self.orientacion = orientacion

    def __repr__(self):
        """Texto bonito para la línea."""
        tipo = "Vertical" if self.orientacion == "vertical" else "Horizontal"
        return f"Línea {tipo} en {self.punto}"

    def interseccion(self, otra_linea):
        """Calcula la intersección entre dos líneas (si existe)."""
        # Si son del mismo tipo, no hay intersección (paralelas)
        if self.orientacion == otra_linea.orientacion:
            return None

        # Si esta línea es vertical y la otra es horizontal
        if self.orientacion == "vertical" and otra_linea.orientacion == "horizontal":
            return Punto(self.punto.x, otra_linea.punto.y)

        # Si esta línea es horizontal y la otra es vertical
        if self.orientacion == "horizontal" and otra_linea.orientacion == "vertical":
            return Punto(otra_linea.punto.x, self.punto.y)

        return None
