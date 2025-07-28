
import json
import threading
import time

# instalar Fask y Flask-SocketIO
from flask import Flask, render_template
from flask_socketio import SocketIO


app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

def map_axis(value):
    """
    Convierte valor del eje (-1 a 1) a rango RC (-100 a 100)
    """
    if value < 0:
        value = -value
        return int(-value * value * value * value * 100)
    else:
        return int(value * value * value * value * 100)
def joysticLoop ():
    global throttle, yaw, pitch, roll
    throttle = 0
    yaw = 0
    pitch = 0
    roll = 0
    while True:
        data = [throttle, yaw, pitch, roll]
        socketio.emit('rc', data)
        #drone.send_rc_control(roll, pitch, throttle, yaw)
        time.sleep(0.1)  # Pequeña pausa para no saturar la consola

@app.route('/')
def index():
    # la web app solo va a recibir una petición HTTP para cargar el indice.html
    print ('empezamos')
    return render_template('indexJoystick.html')

@socketio.on("sendTakeoff")
def handle_takeoff():
    socketio.emit ('takeoff')
    threading.Thread(target=joysticLoop).start()

@socketio.on("sendLand")
def handle_land():
    socketio.emit ('land')

@socketio.on("sendRC")
def handle_sendRC(data):
    data =json.loads(data)
    global throttle, yaw, pitch, roll

    if data['id'] == 'left':
        throttle = float(data['y'])
        yaw = float(data['x'])
    else:
        pitch =-float(data['y'])
        roll = float(data['x'])

if __name__ == '__main__':
    # hay que poner en marcha el servidor flask, al que se conectarán el navegador, y el websocket al que
    # se conectará la estación de tierra
    from threading import Thread
    # Pongo en marcha el servidor flask en un hilo separado
    # Uso el el puerto 5000 para el servidor en desarrollo
    flask_thread = Thread(target=lambda: app.run(host='0.0.0.0', port=5000, debug=True, use_reloader=False))

    flask_thread.start()
    # Pongo en marcha el websocket
    # Uso  el puerto 8766 para el servidor en desarrollo
    socketio.run(app, host='0.0.0.0', port=8766, allow_unsafe_werkzeug=True)