# CameraLink
CameraLink es una librería que pretende facilitar la captación y procesado de imágenes (fotografías y stream de vídeo)
en el contexto del Drone Engineering Ecosystem (DEE).    
En este repositorio puede encontrarse el código de la librería y algunos demostradores de su uso.    
En el reposotorio también puede encontrarse códigos de ejemplo que muestran cómo trasmitir el stream de video mediante websockets,
lo cual ofrece un resultado significativamente mejor que la trasmisión via MQTT, que es el mecanismo utilizado por os primeros módulos
del DEE.   
## La librería CameraLink    
CameraLink esta implementada en forma de clase (la clase Camera) con sus atributos y una variedad de métodos para operar con la cámara.     
Actualmente, son pocos los métodos disponibles (esencialmente captar fotos y captar el stream de vídeo). Esta previsto enriquecer
la librería con métodos para procesado de imagen (por ejemplo, detección de objetos, contornos de colores, etc.).     
Todo el código de la clase (definición de atributos y métodos) está en el fichero Camera.py, aunque con toda probabilidad se irán creando 
ficheros que agrupen los diferentes métodos, a medida que vayan creciendo.      
En la versión actual los métodos disponibles son los siguientes:   
```
    def TakePicture (self)
    # retorna ret,frame
    # ret indica si ha obtenido una imagen o no y frame contiene la imagen
    # El método bloquea al programa que hace la llamada hasta que retorna el resultado

    def setFrequency (self, frequency):
    # Cambia la frecuencia del stream de video
    # Se usa cuando queremos cambiar la frecuencia en medio de la trasmisión del stream de video

    def StartVideoStream (self, frequency, callback, params = None):
    # Pone en marcha el stream de video. Tomará n imagenes por segundo
    # siendo n el valor del parámetro frequency. Cada vez que tenga una nueva
    # imagen llamará a la función callback pasandole esa imagen como primer parámetro
    # y después los parametros que haya en params
    # El método no bloquea al programa que hace la llamada
     
    def StopVideoStream (self):
    # Detiene el stream de video

    def Close (self):
    # Cierra la cámara
```

Muchos de los métodos pueden activarse de forma bloqueante o de forma no bloqueante. En el primer caso, el control no se devuelve al programa que hace la llamada hasta que la operación ordenada haya acabado. Si la llamada es no bloqueante entonces el control se devuelve inmediatamente para que el programa pueda hacer otras cosas mientras se realiza la operación.

Un buen ejemplo de método con estas dos opciones es takeOff, que tiene la siguiente cabecera:
