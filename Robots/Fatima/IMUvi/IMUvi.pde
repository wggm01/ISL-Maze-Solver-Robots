//Cliente 
import java.io.IOException;
import processing.net.*; 
Client myClient;
String inString;
byte interesting = 115;
PShape pieta;
//long previousMillis=0; //Almacena la ultima vez que se cumplio el tiempo de muestreo
//long interval= 2000; //cada 2 segundos sera llamada la funcion para actualizar el valor de rotacion
float rotx,roty,rotz;
void setup() {
  size(640,480, P3D);
  pieta = loadShape("Frpi.obj");
  pieta.setFill(0xffff007f);
  myClient = new Client(this, "192.168.25.101", 5204);
}

void draw() {
  //long currentMillis=millis(); //Esta variable almacena la cuenta de millis.(no usado por el momento)
  background(0xffffffff);
  lights();
  camera(0,0,100 , 0, 0, 0, 0, -1, 0); //eje z positivo saliendo
  if (myClient.available() > 0) { 
  inString = myClient.readStringUntil(interesting);
  String[] rx = split(inString,',');
  //println(rx[0],rx[1],rx[2]);
  //convertir str a float
  rotx=float(rx[0]);
  roty=float(rx[1]); //conversion de data.
  rotz=float(rx[2]);
  //println(rotx,roty,rotz);
  }
  delay(5);
  shape(pieta);
  pieta.rotateX(rotx); pieta.rotateY(roty);
}
