import matplotlib.pyplot as plt

# Datos de ejemplo: (x, y, alineacion)
puntos = [(1, 13, 1), (5,8,0), (10, 15,1), (11,15,0),(20,12,1),(14,8,0)]

# Extraer límites del plano
min_x = min(p[0] for p in puntos)
max_x = max(p[0] for p in puntos)
min_y = min(p[1] for p in puntos)
max_y = max(p[1] for p in puntos)

# Dibujar los puntos
plt.scatter([p[0] for p in puntos], [p[1] for p in puntos], color='red')

# Almacenar líneas dibujadas
lineas_h = []  # (y, x_inicio, x_fin)
lineas_v = []  # (x, y_inicio, y_fin)

# Dibujar líneas con detección de intersecciones
for x, y, alineacion in puntos:
    print(lineas_h)
    print(lineas_v)
    
    if alineacion == 0:  # Línea horizontal
        x_start, x_end = min_x, max_x
        # Verificar intersección con líneas verticales
        for lx, ly1, ly2 in lineas_v:
            if ly1 <= y <= ly2:
                if lx < x:
                    x_start = max(x_start, lx)
                if lx > x:
                    x_end = min(x_end, lx)
        lineas_h.append((y, x_start, x_end))
        plt.pause(1)
        plt.plot([x_start, x_end], [y, y], color='blue', linestyle='--')
        
    else:  # Línea vertical
        y_start, y_end = min_y, max_y
        # Verificar intersección con líneas horizontales
        for ly, lx1, lx2 in lineas_h:
            if lx1 <= x <= lx2:
                if ly < y:
                    y_start = max(y_start, ly)
                if ly > y:
                    y_end = min(y_end, ly)
        lineas_v.append((x, y_start, y_end))
        plt.pause(1)
        plt.plot([x, x], [y_start, y_end], color='green', linestyle='--')

# Configurar el plano
plt.xlim(min_x - 1, max_x + 1)
plt.ylim(min_y - 1, max_y + 1)
plt.grid(True)
plt.show()