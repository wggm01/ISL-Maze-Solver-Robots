//Cliente
import processing.net.*; 
import java.io.IOException;
Client myClient;
String inString;
byte interesting = 115;
PShape pieta;
//long previousMillis=0; //Almacena la ultima vez que se cumplio el tiempo de muestreo
//long interval= 2000; //cada 2 segundos sera llamada la funcion para actualizar el valor de rotacion
float rotx,roty,rotz;
void setup() {
  size(640,480, P3D);
  myClient = new Client(this, "192.168.25.113", 65435);
  pieta = loadShape("Frpi.obj");
  pieta.setFill(0xffff007f);
}

void draw() {
  //long currentMillis=millis(); //Esta variable almacena la cuenta de millis.(no usado por el momento)
  background(0xffffffff);
  lights();
  camera(0,0,100 , 0, 0, 0, 0, -1, 0); //eje z positivo saliendo
  if (myClient.available() > 0) {  
    inString = myClient.readStringUntil(interesting);
    String[] rx = split(inString,',');
    //convertir str a float
   rotx=float(rx[2]);
   roty=float(rx[3]); //conversion de data.
   rotz=float(rx[4]);
    //println(rx[0],rx[1]);}
  delay(0.5);
  shape(pieta);
  pieta.rotateX(rotx); pieta.rotateY(roty); pieta.rotateZ(rotz);
  
}
