<template>
 <ion-page>
      <ion-header>
        <ion-toolbar>
          <ion-title>WebSocket Video Example</ion-title>
        </ion-toolbar>
      </ion-header>
 
      <div class="video-container">
      <div class="video-item" v-if = "!showGal">
        <canvas id="mycanvas" class="thumbnail-video" width="350" height="400"></canvas>
      </div>
    </div>
    </ion-page>
</template>


<script lang="ts">
import { IonContent, IonHeader, IonPage, IonTitle, IonToolbar, IonButton,IonInput } from '@ionic/vue';
import { defineComponent, ref, onMounted } from 'vue';
import ExploreContainer from '@/components/ExploreContainer.vue';


export  default defineComponent({
  name: 'Tab1Page',
  components:{  
    IonContent,IonHeader,IonPage,IonTitle,IonToolbar, IonButton, IonInput
  },
  setup(){
     // Define la URL del WebSocket
    //const wsUrl = 'ws://10.4.113.107:8765';
    const wsUrl = 'ws://localhost:8765';
    const videoElement = ref<HTMLVideoElement | null>(null);

      // Crea una instancia de WebSocket
    const socket = new WebSocket(wsUrl);
    let mediaSource: MediaSource | null = null;

     // Maneja el evento de apertura de la conexión WebSocket
     socket.onopen = () => {
      console.log('Conexión establecida con el WebSocket');
    };

    socket.onmessage = (event) => {
   

           const image = "data:image/jpeg;base64," + event.data;

           //const canvas = document.createElement('canvas');
           //const canvas = document.getElementById('mycanvas');
           //const canvas = document.querySelector('.thumbnail') as HTMLCanvasElement;
           const canvas = document.getElementById('mycanvas') as HTMLCanvasElement;


           const ctx = canvas.getContext('2d');
           const img = new Image();

           if (!canvas) {
             console.error('Canvas not found');
             return;
           }

           //canvas.width = 350;         
           //canvas.height = 400;

           if (!ctx) {
             console.error('2D context not available');
             return;
           }

           img.onload = () => {
             canvas.width = img.width;         
             canvas.height = img.height;
             ctx.clearRect(0, 0, canvas.width, canvas.height);
             ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
             /**setInterval(() => {
               ctx.clearRect(0, 0, canvas.width, canvas.height);
               ctx.drawImage(img, 0, 0, canvas.width, canvas.height);
             },25);*/
           };
           img.src = image;
      };
    

 

    socket.onclose = () => {
      console.log('Conexión cerrada con el WebSocket');
      if (mediaSource) {
        mediaSource.endOfStream();
      }
    };

    socket.onerror = (error) => {
      console.error('Error en la conexión WebSocket:', error);
    };

    

    return{
      videoElement

    }
  }
});
</script>



<style scoped>
#container {
  text-align: center;
  position: absolute;
  top: 400px;
  left: 0;
  right: 0;
  top: 50%;
  transform: translateY(-50%);
}


#container strong {
  font-size: 20px;
  line-height: 26px;
}

#container p {
  font-size: 16px;
  line-height: 22px;
  
  color: #8c8c8c;
  
  margin: 0;
}

#container a {
  text-decoration: none;
}

.mensajeRecibido{
  position: absolute;
  top: 80px; 
  left: 10px; 
  color: white;
  font-size: 24px; 
}

.gallery{
  position: absolute;
  top:600px;
}

.descarga{
  position: absolute;
  top:600px;
  left:100px;
}

.gallery-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(100px, 1fr)); /* Define columnas automáticas */
  justify-content: center; /* Centra el contenido horizontalmente */
  gap: 10px; /* Espaciado entre imágenes */
  margin: 10px; /* Márgenes externos */
}

.video-container{
  margin-bottom: 200px;
}

.video-item {
  display: flex;
  align-items: center;
  justify-content: center;
}

.file-item {
    display: flex;
    align-items: center;
    justify-content: center;
  }

.thumbnail-video {
  max-width: 350px; /* Tamaño máximo de las miniaturas */
  max-height: 450px; /* Tamaño máximo de las miniaturas */
}

.thumbnail-file{
  max-width: 100px; /* Tamaño máximo de las miniaturas */
  max-height: 100px; /* Tamaño máximo de las miniaturas */
}
</style>
