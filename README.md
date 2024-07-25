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

## Demostradores     
En la carpeta de demostradores pueden encontrarse dos.  

_consolaDirecta_ en un código en python muy simple que usa CameraLink para tomar dos fotos y mostrar el stream de video durante 15 segundos, tomando las imágenes de la cámara que tenga el ordenador en el que se ejecuta.   

Para poner en marcha este demostrador es necesario instalas la librería _opencv_python_.     

El segundo demostrador asume que el computador en el que se captura la imagen es diferente del computador en el que se visualiza. Este es el caso si queremos visualizar en tierra (en el portátil) las imágenes que captura el dron en el aire. En ese caso, el código que captura la image, que está en el fichero _Service.py_ se ejecutaría en la RPi de lleva el dron y la aplicación de estación de tierra, que está en el fichero _DashRemoto.py_ se ejecutaría en el portátil.    

El demostrador usa dos mecanismos diferentes para trasmitir el stream de video entre el servicio de a bordo y la estación de tierra. Uno de los mecanismos es usar un broker MQTT, que es el sistema habitual de comunicación entre los módulos del DEE y, por eso, es el usado en los primeros módulos que se desarrollaron. Sin embargo, este mecanismo no es muy adecuado para la trasmisión de video stream ya que incurre en frecuentes retrasos que reducen significativamente la calidad de la experiencia de usuario.   
   
El segundo mecanismo es la comunicació via websockets directa entre los dos módulos. Los brokers MQTT también usan websockets pero con una sobrecarga de gestión de las publicaciones y subscripciones responsable de esos retrasos antes mencionados. El uso de websockets directamente elimina esa sobrecarga y hace que la experiencia de usuario mejore significativamente. La aplicación de estación de tierra permite comparar el resultado de la transmisión via broker con la trasmisión via websockets.    

El script _Service.py_ tiene un parámetro que puede tomar el valor _simulation_ o _production_. Se usa el primer valor si quieremos probar el demostrador captando las imágenes de la cámara del portátil. Usaremos el segundo valor si _Service.py_ se ejecuta en la RPi abordo del dron.     

Para poner en marcha este demostrador es necesario instalar las librerías _paho_mqtt_ (ATENCIÓN: versión 1.6.1), _websockets_ y _netifaces_.
  
Este vídeo muestra el demostrador en funcionamiento, en modo _simulation_.     

## Transmisión del stream de vídeo via websocket    
Con frecuencia es necesario trasmitir el stream de vídeo desde el módulo en el que se captura hacia cualquier otro del DEE (ya sea una estación de tierra en python o una webApp o una aplicación en Flutter). De hecho, eso es exactamente lo que ocurre en el segundo demostrador que se ha mostrado en el apartado anterior.    

En las primeras implementaciones de módulos del DEE se usaba un broker MQTT para la trasmisión del stream de video. Los resultados no eran satisfactorios. El resultado mejora mucho si se usa una trasmisión directa mediante websocket (como se  hace en el demostrador mencionado).    
En la carpeta _webSocketDemo_ de este repositorio pueden encontrarse códigos que ejemplifican como implementar esta comunicación via websockets. El fichero _server.py_ contiene un script que espera conexión via websocket para enviar el stream de video al módulo que se ha conectado. El fichero _client.py_ es un ejemplo de cliente que se conecta al server y recibe el stream de video. Los códigos son los mismos que los usados en els segundo demostrador de apartado anterior.   

La carpeta _clientWebApp_ contiene una aplicación en Vue (webApp) que actua como cliente. Se conecta tambien al server y recibe el stream de video.    

El siguiente vídeo muestra estas aplicaciones en acción.   

Los detalles de cómo realizar la trasmisión de videostream entre un servidor en python y un módulo en Flutter pueden encontrarse en este repositorio:

