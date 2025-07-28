# Control por Joystick   
## 1. Presentación
La mayoría de las aplicaciones del Drone Engineering Ecosystem permiten controlar el dron mediante botoneras (botones para armar, despegar, volar en diferentes direcciones, cambiar orientación, aterrizar, etc.). El dron también puede controlarse mediante un Joystick, de manera similar a como lo hacemos desde la emisora de radio, lo cual puede hacer que la interacción con el dron sea más amigable. El Joystick puede ser real (por ejemplo, conectado al portátil via USB o de forma inalámbrica) o virtual (en forma de web app). En este repo hay información que permite ambas formas de control del dron via Joystick.    
    
## 2. Uso del Joystick via Mission Planner    
Mission Planner permite controlar el dron usando un Joystick. Esta web y el vídeo muestra cómo hacerlo.    
   
https://ardupilot.org/copter/docs/common-joystick.html     
      
https://www.youtube.com/watch?v=HYT_L5V1dA4      

De forma similar, la propia emisora de radio se puede conectar a Mission Planner en modo Joystick.    

Estas opciones tienen al menos dos aspectos interesantes:
1. Podemos controlar el dron real (a través de Mission Planner) de forma muy parecida a cómo lo haríamos con una emisora de rádio, pero usando un dispositivo (el Joystick) que puede ser muy barato (el que describimos mas adelante cuesta poco más de 4 euros).
2. Podemos practicar el vuelo con emisora o Joystick usando el simulador SITL, a través de Mission Planner

## 3. Control por programa usando un Joystick real         
La información proporcionada por el Joystick puede ser capurada por un programa en Python y realizar desde ese programa las acciones que queramos asociar a cada uno de los actuadrores del Joystick. Veamos aquí como hacerlo.    
    
Usaremos el Joystick que se muestra en la figura y que puede adquirirse aqui por poco más de 4 euros.     
    
https://es.aliexpress.com/item/1005005616793872.html      

<img width="400" height="300" alt="Imagen1" src="https://github.com/user-attachments/assets/ead600c7-5699-48ac-b045-13f11f5ed188" />

En la figura se identifican los diferentes actuadores (buttons, axis y hats). El script llamado test.py de este repositorio permite identificar cada uno de los actuadores del Joystick que conectemos a nuestro portátil.   
    
El fichero JoystickReal.py contiene la definición de la clase Joystick en Python que define las funcionalidades de un Joystick para controlar un dron. La figura siguiente muestra las acciones asociadas a algunos de los actuadores del Joystick. Por otra parte, el fichero testJoystick.py es un sencillo programa de prueba que usa un objeto de la clase Dron (de la librería DronLink) para conectarse al simulador SITL, y un objeto de la clase Joystick.     
      <img width="400" height="300" alt="Imagen2" src="https://github.com/user-attachments/assets/296c28ab-f331-4d11-a906-2e38e217d441" />

Al instanciar un objeto de la clase Joystick hay que indicarle un identificador para el dron (puede ser un número), el objeto de la clase Dron y el nombre de la función que queremos que se ejecute cuando se pulse el botón 4 del Joystick. La función recibirá como parámetro el identficador del dron (útil si vamos a usar varios drones y varios Joysticks).     
     
La definición de la clase Joystick se puede enriquecer haciendo que, por ejemplo, al instanciar e objeto se especifiquen funciones a ejecutar cuando acaben las funciones del dron que se activan de modo no bloqueante (por ejemplo, takeOff).     

## 4. Control mediante un Joystick virtual     
El dron también se puede controlar mediante un Joystick virtual, en forma de web app. El fichero JoystickVirtual.py contiene la definición de una clase que controla el dron mediante los comandos que recibe a través de un web socket, cuya url se especifica en el momento de instanciar el objeto de la clase Joystick. En esta versión limitada de la clase solo atiende comandos para despegar, aterrizar y comandos con los valores RC (throttle, yaw, pitch y roll), para mover el dron. También asume que los valores RC están en el rango [-1, 1] y los ajusta convenientemente al rango [1000,2000].    

El fihero serverJoystickVirtual.py contiene el código de un servidor en Flask que presenta en el dispositivo movil que se conecta la interfaz mostrada en la figura. Se trata de dos botones (para despegar y aterrizar) y dos controles para generar las señales RC imitando los ejes del Joystick. La web app emite  a través de un web sockect que crea en el puerto 8766 la información que recoge del usuario. La web app está disponible en el puerto 5000.     
   <img width="400" height="200" alt="Imagen3" src="https://github.com/user-attachments/assets/d15b38f6-2b3e-4a04-a008-fece47ce43c8" />

Finalmente, el fichero testJoystickVirtual.py contiene un sencillo programa de prueba que usa un objeto de la clase Dron (de la librería DronLink) para conectarse al simulador SITL, y un objeto de la clase Joystick (versión virtual). Al instanciar un objeto de la clase Joystick hay que indicarle un identificador para el dron (puede ser un número), el objeto de la clase Dron y la url del websocket al que debe conectarse el Joystick.






 
