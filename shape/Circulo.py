class Circulo:
    def __init__(self, centro, radio, color_relleno, color_borde, ancho_borde, estilo_borde, name="New", scale = 1, rotation=0):
        self.name = name
        self.x = centro[0]
        self.y = centro[1]
        self.centro = centro
        self.radio = radio
        self.color_relleno = color_relleno
        self.color_borde = color_borde
        self.ancho_borde = ancho_borde
        self.estilo_borde = estilo_borde
        self.scale = scale
        self.rotation = rotation

    def trasladar(self, dx, dy):
        self.x = self.x + dx
        self.y = self.y + dy
        self.centro = (self.x, self.y)

    def escalar(self, factor):
        self.radio *= factor
    
    def cambiar_punto_control(self, nuevo_centro):
        self.x = nuevo_centro[0]
        self.y = nuevo_centro[1]
        self.centro = nuevo_centro
    
    def dibujar(self, imagen):
        self.drawMidPoint(imagen, self.x, self.y, self.radio*self.scale, self.color_relleno)
        self.flood_fill(imagen, self.x, self.y, self.color_relleno, self.color_borde)
        self.draw_mid_point_grosor(imagen, self.x, self.y, self.radio, self.ancho_borde, self.estilo_borde, self.color_borde)

    def draw_pixel(self, imagen, x, y, color):
        if (0 <= x < 700) and (0 <= y < 700):
            imagen.putpixel((x, y), color)

    def drawMidPoint(self, imagen, xc, yc, radius, fill_color):
        x = 0
        y = radius
        p = 1 - radius
        while x <= y:
            self.draw_pixel(imagen, xc + x, yc + y, fill_color)
            self.draw_pixel(imagen, xc + x, yc - y, fill_color)
            self.draw_pixel(imagen, xc - x, yc + y, fill_color)
            self.draw_pixel(imagen, xc - x, yc - y, fill_color)
            self.draw_pixel(imagen, xc + y, yc + x, fill_color)
            self.draw_pixel(imagen, xc + y, yc - x, fill_color)
            self.draw_pixel(imagen, xc - y, yc + x, fill_color)
            self.draw_pixel(imagen, xc - y, yc - x, fill_color)
            if p <= 0:
                p = p + 2 * x + 1
            else:
                p = p + (2 * x) - (2 * y) + 1
                y -= 1
            x += 1

    def flood_fill(self, imagen, xi, yi, fill_color, border_color):
        stack = [(xi, yi)]
        visited = set()

        while stack:
            x, y = stack.pop()
            if (0 <= x < 700) and (0 <= y < 700) and (x, y) not in visited:
                current_color = imagen.getpixel((x, y))
                if current_color != fill_color and current_color != border_color:
                    self.draw_pixel(imagen, x, y, fill_color)
                    visited.add((x, y))
                    # Agregar solo los pixeles no visitados al stack
                    if (x, y + 1) not in visited:
                        stack.append((x, y + 1))
                    if (x - 1, y) not in visited:
                        stack.append((x - 1, y))
                    if (x + 1, y) not in visited:
                        stack.append((x + 1, y))
                    if (x, y - 1) not in visited:
                        stack.append((x, y - 1))

    # solo dibujar los bordesssss
    def draw_pixel_grosor(self, imagen, x, y, thickness, color):
        suma = 0 if (thickness%2==0) else 1
        half_thickness = int(thickness // 2)
        for dx in range(-half_thickness, half_thickness + suma):
            for dy in range(-half_thickness, half_thickness + suma):
                #draw.line([(x + dx, y + dy), (x + dx + 1, y + dy + 1)], fill=color, width=1)
                if ((0 < x < 700) and (0 < y < 700)):
                    imagen.putpixel((x + dx, y + dy), color)

    def draw_mid_point_grosor(self, imagen, xc, yc, radius, thickness, estilo, color):
        x = 0
        y = radius
        p = 1 - radius
        maskPos = 0
        while x <= y:
            if (mask[maskPos] or (estilo == "Continuous")):
                self.draw_pixel_grosor(imagen, xc + x, yc + y, thickness, color)
                self.draw_pixel_grosor(imagen, xc + x, yc - y, thickness,color)
                self.draw_pixel_grosor(imagen, xc - x, yc + y, thickness,color)
                self.draw_pixel_grosor(imagen, xc - x, yc - y, thickness,color)

                self.draw_pixel_grosor(imagen, xc + y, yc + x, thickness,color)
                self.draw_pixel_grosor(imagen, xc + y, yc - x, thickness,color)
                self.draw_pixel_grosor(imagen, xc - y, yc + x, thickness,color)
                self.draw_pixel_grosor(imagen, xc - y, yc - x, thickness,color)
            maskPos = (maskPos + 1) % len(mask)
            if p <= 0:
                p = p + 2 * x + 1
            else:
                p = p + (2 * x) - (2 * y) + 1
                y -= 1
            x += 1

mask = [0,0,0,0,0,1,1,0,0,0,0,0]