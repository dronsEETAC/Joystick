from JoystickReal import *
from dronLink.Dron import Dron
import keyboard # instalar keyboard

def identifica (id):
    print ("Soy el joystick: ", id)


dron1= Dron ()
dron1.connect ('tcp:127.0.0.1:5763', 115200)
joystick1 = Joystick (dron1, identifica, 0)

dron2= Dron ()
dron2.connect ('tcp:127.0.0.1:5773', 115200)
joystick2 = Joystick (dron2, identifica, 1)

dron3= Dron ()
dron3.connect ('tcp:127.0.0.1:5783', 115200)
joystick3 = Joystick (dron3, identifica, 2)

while True:
    #time.sleep(1)
    if keyboard.is_pressed('p'):
        break
joystick1.stop()
joystick2.stop()
joystick3.stop()

dron1.disconnect()
dron2.disconnect()
dron3.disconnect()
print ("Fin")