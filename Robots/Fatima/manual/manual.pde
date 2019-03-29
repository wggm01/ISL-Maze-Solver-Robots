import processing.net.*; 
Client myClient; 
int clicks;

void setup(){
myClient = new Client(this, "192.168.25.113", 6790);

}

void draw() {

 fill(255);
  rect(25, 25, 50, 50);
  if (!keyPressed){
  myClient.write("zs");
  }


}
//Dibujitos de controles.


void keyPressed() {
  
  if (key == 'w'){
  myClient.write("ws");
  }
  else if (key == 'a'){
  myClient.write("as");
  }
  else if (key == 'd'){
  myClient.write("ds");
  }
  else if (key == 'q'){
  myClient.write("qs");
  }
  else if (key == 'e'){
  myClient.write("es");
  }
  else if (key == 'x'){
  myClient.write("xs");//enviar letra x (detiene el programa, termina la coneccion)
  }
  else{
   myClient.write("zs");//evita que se mueva si presiono cualquier tecla(redundancia porque igual esto usando switch)
  }
 
}
