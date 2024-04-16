import math

class Triangulo:
    def __init__(self, centro, radio, color_relleno, color_borde, ancho_borde, estilo_borde, name = "New", scale=1, rotation = 0):
        self.color_relleno = color_relleno
        self.color_borde = color_borde
        self.ancho_borde = ancho_borde
        self.estilo_borde = estilo_borde
        self.x = centro[0]
        self.y = centro[1]
        self.scale = scale
        self.rotation = rotation
        self.name = name
        self.radio = radio
        # Coordenadas locales del triángulo
        self.punto1_local = (0, 0)
        self.punto2_local = (radio, 0)
        self.punto3_local = (radio / 2, radio * math.sqrt(3) / 2)

        # Coordenadas globales del triángulo
        self.punto1 = (self.x, self.y)
        self.punto2 = (self.x + self.punto2_local[0], self.y + self.punto2_local[1])
        self.punto3 = (self.x + self.punto3_local[0], self.y + self.punto3_local[1])

    def trasladar(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.punto1 = (self.x, self.y)
        self.punto2 = (self.x + self.punto2_local[0], self.y + self.punto2_local[1])
        self.punto3 = (self.x + self.punto3_local[0], self.y + self.punto3_local[1])

    def escalar(self, factor):
        # Escalar las coordenadas locales
        self.punto2_local = (self.punto2_local[0] * factor, self.punto2_local[1] * factor)
        self.punto3_local = (self.punto3_local[0] * factor, self.punto3_local[1] * factor)
        # Actualizar las coordenadas globales
        self.punto2 = (self.x + self.punto2_local[0], self.y + self.punto2_local[1])
        self.punto3 = (self.x + self.punto3_local[0], self.y + self.punto3_local[1])

    def rotar(self, angulo):
        angulo_rad = math.radians(angulo)
        # Rotar punto2
        x_rotado = self.x + self.punto2_local[0] * math.cos(angulo_rad) - self.punto2_local[1] * math.sin(angulo_rad)
        y_rotado = self.y + self.punto2_local[0] * math.sin(angulo_rad) + self.punto2_local[1] * math.cos(angulo_rad)
        self.punto2 = (x_rotado, y_rotado)
        # Rotar punto3
        x_rotado = self.x + self.punto3_local[0] * math.cos(angulo_rad) - self.punto3_local[1] * math.sin(angulo_rad)
        y_rotado = self.y + self.punto3_local[0] * math.sin(angulo_rad) + self.punto3_local[1] * math.cos(angulo_rad)
        self.punto3 = (x_rotado, y_rotado)

    
    def cambiar_punto_control(self, nuevo_punto):
        self.x = nuevo_punto[0]
        self.y = nuevo_punto[1]
        self.punto1 = (self.x, self.y)

    def dibujar(self, imagen):
        self.escalar(self.scale)
        self.rotar(self.rotation)
        #self.draw_bresenham(int(self.punto1[0]),int(self.punto1[1]),int(self.punto2[0]),int(self.punto2[1]),self.color_relleno, imagen)
        #self.draw_bresenham(int(self.punto2[0]),int(self.punto2[1]),int(self.punto3[0]),int(self.punto3[1]),self.color_relleno, imagen)
        #self.draw_bresenham(int(self.punto3[0]),int(self.punto3[1]),int(self.punto1[0]),int(self.punto1[1]),self.color_relleno, imagen)
        patron = [1,1,1,1,0,0,0,0] if self.estilo_borde == "Segmented" else [1]
        self.scanline_fill(int(self.punto1[0]),int(self.punto1[1]),int(self.punto2[0]),int(self.punto2[1]),int(self.punto3[0]),int(self.punto3[1]), self.color_relleno,imagen)
        self.draw_bresenham(int(self.punto1[0]),int(self.punto1[1]),int(self.punto2[0]),int(self.punto2[1]),self.color_borde, imagen, patron, self.ancho_borde)
        self.draw_bresenham(int(self.punto2[0]),int(self.punto2[1]),int(self.punto3[0]),int(self.punto3[1]),self.color_borde, imagen, patron, self.ancho_borde)
        self.draw_bresenham(int(self.punto3[0]),int(self.punto3[1]),int(self.punto1[0]),int(self.punto1[1]),self.color_borde, imagen, patron, self.ancho_borde)
        #self.draw_bresenham(10,10,10,300,self.color_borde, imagen, "1", self.ancho_borde)


    def paint_cell(self, x, y, color, imagen):
        if (0<=x<700 and 0 <= y < 700):
            imagen.putpixel((x, y), color)

    def draw_bresenham(self, x0, y0, x1, y1, color, imagen, patron=[1], grosor=1):
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        steep = dy > dx
        if steep:
            x0, y0 = y0, x0
            x1, y1 = y1, x1
        if x0 > x1:
            x0, x1 = x1, x0
            y0, y1 = y1, y0
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        p = 2 * dy - dx
        incE = 2 * dy
        incNE = 2 * (dy - dx)
        y = y0

        index = 0
        for x in range(x0, x1 + 1):
            if patron[index]:
                if steep:
                    self.paint_cell(y, x, color, imagen)
                    #grosor de la linea
                    suma = 0 if grosor % 2 == 0 else 1
                    # grosor de la linea
                    mitad = grosor//2
                    for i in range(-mitad, mitad+suma):
                        self.paint_cell(y+i, x, color, imagen)

                else:
                    self.paint_cell(x, y, color, imagen)
                    suma = 0 if grosor % 2 == 0 else 1
                    # grosor de la linea
                    mitad = grosor//2
                    for i in range(-mitad, mitad+suma):
                        self.paint_cell(x, y + i, color, imagen)

            index += 1
            if index >= len(patron):
                index = 0

            if p < 0:
                p += incE
            else:
                if y0 < y1:
                    y += 1
                else:
                    y -= 1
                p += incNE


    def scanline_fill(self, x0, y0, x1, y1, x2, y2, color, imagen):
        vertices = [(x0, y0), (x1, y1), (x2, y2)]

        min_y = min(y0, y1, y2)
        max_y = max(y0, y1, y2)
        for y in range(min_y + 1, max_y):
            intersecciones = []

            for i in range(3):
                x1, y1 = vertices[i]
                x2, y2 = vertices[(i + 1) % 3]

                if y1 < y2:
                    x1, y1, x2, y2 = x2, y2, x1, y1
                if y1 >= y and y2 < y:
                    interseccion_x = x1 + (y - y1) * (x2 - x1) / (y2 - y1)
                    intersecciones.append(interseccion_x)
            intersecciones.sort()

            for i in range(0, len(intersecciones), 2):
                x_start = int(intersecciones[i])
                x_end = int(intersecciones[i + 1])
                # canvas.create_line(x_start,y,x_end,y,fill=color)
                self.draw_bresenham(x_start+1, y, x_end, y, color, imagen)