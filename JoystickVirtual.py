import threading
import time
import socketio # instalar python-socketio, requests, websocket-cient

class Joystic:
    def __init__(self, num, dron, connectionString):
        self.num = num

        self.dron = dron
        self.yaw = 1500
        self.throttle = 1500
        self.pitch = 1500
        self.roll = 1500

        print ("empezamos")

        sio = socketio.Client()
        # esto es para conectarme al websocket del servidor en desarrollo
        #sio.connect('http://localhost:8766')
        sio.connect(connectionString)
        print ("Conectado al socket")

        @sio.event
        def takeoff():
            self.dron.arm()
            print("Armado")
            self.dron.takeOff(5)
            print("En el aire")
            self.dron.setMode ('LOITER')
            threading.Thread(target=self.control_loop_virtual).start()

        @sio.event
        def land():
            self.dron.Land()
            print("En tierra")

        @sio.event
        def rc(data):
            self.yaw = self.map_axis(float(data[1]))
            self.throttle = self.map_axis(float(data[0]))
            self.pitch = self.map_axis(float(data[2]))
            self.roll = self.map_axis(float(data[3]))

    def control_loop_virtual (self):
        # con este parametro hacemos que el dron no exija que el throttle esté al mínimo para armar
        params = [{'ID': "PILOT_THR_BHV", 'Value': 1}]
        self.dron.setParams(params)
        self.working = True
        while self.working:
            self.dron.send_rc( self.roll, self.pitch, self.throttle, self.yaw)
            time.sleep(0.1)
        # Restauro el parámetro que cambié
        params = [{'ID': "PILOT_THR_BHV", 'Value': 0} ]
        self.dron.setParams(params)


    def map_axis(self, value):
        """Convierte valor del eje (-1 a 1) a rango RC (1000 a 2000)"""
        return int(1500 + value * 500)

    def map_axis_yaw(self, value):
        """Convierte valor del eje (-1 a 1) a rango RC (1000 a 2000)
        pero no de forma lineal, para que el dron gire poco con valores bajos del yaw"""
        return int(1500 + value * value * value * value * 500)

    def stop (self):
        self.working = False