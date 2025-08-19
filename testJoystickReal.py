from JoystickReal import *
from dronLink.Dron import Dron
import keyboard # instalar keyboard

def identifica (id):
    print ("Soy el joystick: ", id)


dron= Dron ()

dron.connect ('tcp:127.0.0.1:5763', 115200)

print ("Conectado al dron")
joystick = Joystick (dron, identifica, 2)


while True:
    #time.sleep(1)
    if keyboard.is_pressed('p'):
        break
joystick.stop()

print ("Fin")