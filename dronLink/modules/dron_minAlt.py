import threading

from pymavlink import mavutil
import time

import math


import math

class TransformadorNEDCanvasEscalado:
    def __init__(self, heading_inicial_deg, ancho_canvas_px, alto_canvas_px, ancho_fisico_m, alto_fisico_m):
        """
        heading_inicial_deg: heading del dron en grados (0° = Norte) al conectar.
        ancho_canvas_px, alto_canvas_px: dimensiones del canvas en píxeles.
        ancho_fisico_m, alto_fisico_m: dimensiones reales del área (en metros).
        """
        self.heading_inicial_rad = math.radians(heading_inicial_deg)

        self.ancho_canvas = ancho_canvas_px
        self.alto_canvas = alto_canvas_px

        self.ancho_fisico = ancho_fisico_m
        self.alto_fisico = alto_fisico_m

        # Centro del canvas en píxeles
        self.cx = ancho_canvas_px / 2.0
        self.cy = alto_canvas_px / 2.0

        # Escala (pixeles por metro)
        self.escala_x = ancho_canvas_px / ancho_fisico_m
        self.escala_y = alto_canvas_px / alto_fisico_m

    def ned_a_canvas(self, x_ned_m, y_ned_m):
        """
        Convierte posición NED (metros) a coordenadas canvas (píxeles)
        aplicando rotación, escalado y centrado.
        """
        # Rotar según heading inicial (transformar a referencia del dron)
        vertical_m =  x_ned_m * math.cos(self.heading_inicial_rad) + y_ned_m * math.sin(self.heading_inicial_rad)
        horizontal_m = -x_ned_m * math.sin(self.heading_inicial_rad) + y_ned_m * math.cos(self.heading_inicial_rad)

        # Escalar de metros a píxeles
        horizontal_px = horizontal_m * self.escala_x
        vertical_px = vertical_m * self.escala_y

        # Convertir a coordenadas canvas, con origen en centro y eje Y invertido para canvas
        canvas_x = self.cx + horizontal_px
        canvas_y = self.cy - vertical_px

        return canvas_x, canvas_y

    def canvas_a_ned(self, canvas_x_px, canvas_y_px):
        """
        Convierte coordenadas canvas (píxeles) a posición NED (metros)
        aplicando transformación inversa.
        """
        # Diferencia desde el centro del canvas
        horizontal_px = canvas_x_px - self.cx
        vertical_px = -(canvas_y_px - self.cy)

        # Escalar píxeles a metros
        horizontal_m = horizontal_px / self.escala_x
        vertical_m = vertical_px / self.escala_y

        # Rotación inversa para volver a NED
        x_ned_m = vertical_m * math.cos(self.heading_inicial_rad) - horizontal_m * math.sin(self.heading_inicial_rad)
        y_ned_m = vertical_m * math.sin(self.heading_inicial_rad) + horizontal_m * math.cos(self.heading_inicial_rad)

        return x_ned_m, y_ned_m





def punto_en_poligono(self, poligono, punto):
    """
    Determina si un punto está dentro de un polígono.

    Parámetros:
        poligono: lista de tuplas (x, y) representando los vértices del polígono.
        punto: tupla (x, y) del punto a evaluar.

    Retorna:
        True si el punto está dentro o en el borde del polígono, False si está fuera.
    """

    print ('voy a ver si esta dentro: ', punto)
    x, y = punto
    dentro = False
    n = len(poligono)

    for i in range(n):
        x1, y1 = poligono[i]
        x2, y2 = poligono[(i + 1) % n]  # siguiente vértice (cerrando polígono)

        # Comprobamos si el punto está en un borde
        if ((y - y1) * (x2 - x1) == (x - x1) * (y2 - y1) and
                min(x1, x2) <= x <= max(x1, x2) and
                min(y1, y2) <= y <= max(y1, y2)):
            return True  # está sobre un borde

        # Algoritmo ray casting
        intersecta = ((y1 > y) != (y2 > y)) and \
                     (x < (x2 - x1) * (y - y1) / (y2 - y1 + 1e-12) + x1)
        if intersecta:
            dentro = not dentro
    print ('resultado: ', dentro)
    return dentro





def catetos_semejantes(self, x, y, z):
    """
    Calcula los catetos de un triángulo semejante al dado,
    pero cuya hipotenusa mide z.

    Parámetros:
        x (float): Cateto 1 del triángulo original
        y (float): Cateto 2 del triángulo original
        z (float): Hipotenusa deseada del nuevo triángulo

    Retorna:
        (float, float): Catetos del nuevo triángulo
    """
    h_original = math.sqrt(x ** 2 + y ** 2)
    if h_original == 0:
        raise ValueError("Los catetos originales no pueden ser ambos cero.")

    factor_escala = z / h_original
    return x * factor_escala, y * factor_escala


# Ejemplo de uso


MIN_ALT = 4.0  # Altura mínima en metros

THROTTLE_UP = 1900  # Valor del canal 3 (throttle) para subir ligeramente
NEUTRAL = 1500       # Valor neutro para los canales

# Modos donde tiene sentido forzar altitud mínima
SAFE_MODES = ['GUIDED', 'LOITER', 'ALT_HOLD', 'POSHOLD']



def send_throttle_up(self):
    print("⚠️ Subiendo por debajo de altitud mínima.")
    self.vehicle.mav.rc_channels_override_send(
        self.vehicle.target_system,
        self.vehicle.target_component,
        NEUTRAL,  # Canal 1 (roll)
        NEUTRAL,  # Canal 2 (pitch)
        THROTTLE_UP,  # Canal 3 (throttle)
        NEUTRAL,  # Canal 4 (yaw)
        65535, 65535, 65535, 65535
    )

def clear_overrides(self):
    self.vehicle.mav.rc_channels_override_send(
        self.vehicle.target_system,
        self.vehicle.target_component,
        *[65535] * 8
    )

def _CheckMinAlt (self, escenario, aviso = None):

    while True:

        print('speeds: ', self.speeds[0], self.speeds[1])
        if self.alt is not None and self.flightMode is not None:
            print (self.alt, self.position[0])



            if self.alt < MIN_ALT and self.flightMode in SAFE_MODES:
                if aviso:
                    aviso (-1) # Aviso de que se ha detectado altura minima
                self.setFlightMode('GUIDED')
                self.move_distance('Up', 2)
                self.setFlightMode('LOITER')
        punto = (self.position[0], self.position[1])
        poligono = escenario[0]
        print ('voy a ver si estoy dentro del inclusion')
        if not self.punto_en_poligono (poligono, punto):
            print ('Alarma inclusion')
            if aviso:
                aviso(0)  # Aviso de que se ha detectado fence inclusiomn
            x = -self.speeds[0]
            y = -self.speeds[1]
            self.setFlightMode('GUIDED')

            z = 5
            step_x, step_y = self.catetos_semejantes (x,y,z)
            print ('atencion: ', -x,-y,step_x,step_y)
            self._move_distance_2 (step_x, step_y)


            #self.move_distance ('Back', 50)

            self.setFlightMode('LOITER')
        for i in range (1,len(escenario)):
            print('voy a ver si estoy dentro del exclusion ', i)
            poligono = escenario[i]
            if self.punto_en_poligono(poligono, punto):
                if aviso:
                    aviso(i)  # Aviso de que se ha detectado obstaculo i
                print('Alarma excusion')
                x = -self.speeds[0]
                y = -self.speeds[1]
                self.setFlightMode('GUIDED')

                z = 5
                step_x, step_y = self.catetos_semejantes(x, y, z)
                print('atencion: ', -x, -y, step_x, step_y)
                self._move_distance_2(step_x, step_y)

                # self.move_distance ('Back', 50)

                self.setFlightMode('LOITER')


        time.sleep(0.2)

def CheckMinAlt (self, escenario, aviso = None):
    threading.Thread(target=self._CheckMinAlt, args=[escenario, aviso ]).start()


