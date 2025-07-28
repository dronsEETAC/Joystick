from JoystickVirtual import *
from Dron import Dron
import keyboard # instalar keyboard


dron = Dron ()
dron.connect ('tcp:127.0.0.1:5763', 115200)
print ("Conectado al dron")
joystick = Joystic (0, dron, 'http://127.0.0.1:8766')

while True:
    #time.sleep(1)
    if keyboard.is_pressed('p'):
        break
joystick.stop()
print ("Fin")