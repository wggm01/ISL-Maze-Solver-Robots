//Cliente
import processing.net.*; 
import java.io.IOException;
Client myClient; 
String inString;
byte interesting = 115;
float iAngle,iDistance;
float pixsDistance;
String noObject;
PFont orcFont;
void setup() { 
  size (640, 480); //Ancho, alto
  smooth(); //Geometrica con bordes suaves Antialiasing
  orcFont = loadFont("OCRAExtended-30.vlw"); //Carga las fuentes en formato vlw y la lee como una imagen por letra o simbolo
  myClient = new Client(this, "192.168.25.113", 65436); 
} 
//0,0 esta en la esquina superior izquierda
//todo esta en  pixeles 
//Funciones
//Plantilla de Radar
void drawRadar() {
  pushMatrix(); //Guarda en el buffer como estaba antes el sistema de coordenada
  translate(width/2,height-height*0.074); // Origen trasladado a la mitad y hasta 444px de 480
  noFill(); // no puede ir junto con noStroke(); porque entonces no aparecera nada en la pantalla
  strokeWeight(2);
  stroke(98,245,31); //define el color de los bordes (por defecto esta en rgb porque no se uso colorMode())
  // draws the arc lines
  arc(0,0,(width-width*0.0625),(width-width*0.0625),PI,TWO_PI);
  arc(0,0,(width-width*0.27),(width-width*0.27),PI,TWO_PI);
  arc(0,0,(width-width*0.479),(width-width*0.479),PI,TWO_PI);
  arc(0,0,(width-width*0.687),(width-width*0.687),PI,TWO_PI);
  // draws the angle lines
  line(-width/2,0,width/2,0);
  line(0,0,(-width/2)*cos(radians(30)),(-width/2)*sin(radians(30)));
  line(0,0,(-width/2)*cos(radians(60)),(-width/2)*sin(radians(60)));
  line(0,0,(-width/2)*cos(radians(90)),(-width/2)*sin(radians(90)));
  line(0,0,(-width/2)*cos(radians(120)),(-width/2)*sin(radians(120)));
  line(0,0,(-width/2)*cos(radians(150)),(-width/2)*sin(radians(150)));
  //line((-width/2)*cos(radians(30)),0,width/2,0);
  popMatrix(); //restaura el sistema de coordenada usando pushmatrix.
}
//Lineas de animacion para el radar
void drawLine() {
  pushMatrix();
  strokeWeight(9);
  stroke(30,250,60);
  translate(width/2,height-height*0.074); // Origen trasladado a la mitad y hasta 444px de 480
  line(0,0,(height-height*0.12)*cos(radians(iAngle)),-(height-height*0.12)*sin(radians(iAngle)));//calcula las cordenadas rectangulares y las dibuja 
  popMatrix();
}

//Deteccion de objetos
void drawObject() {
  pushMatrix();
  translate(width/2,height-height*0.074); // moves the starting coordinats to new location
  strokeWeight(9);
  stroke(255,10,10); // red color
  pixsDistance = iDistance*((height-height*0.1666)*0.025); // covers the distance from the sensor from cm to pixels
  // limiting the range to 40 cms
  if(iDistance<40){
    // draws the object according to the angle and the distance
  line(pixsDistance*cos(radians(iAngle)),-pixsDistance*sin(radians(iAngle)),(width-width*0.505)*cos(radians(iAngle)),-(width-width*0.505)*sin(radians(iAngle)));
  }
  popMatrix();
}

//Texto en pantalla
void drawText() { // draws the texts on the screen
  
  pushMatrix();
  if(iDistance>40) {
  noObject = "Out of Range";
  }
  else {
  noObject = "In Range";
  }
  fill(0,0,0);
  noStroke();
  rect(0, height-height*0.0648, width, height);
  fill(98,245,31);
  textSize(25);
  
  text("10cm",width-width*0.3854,height-height*0.0833);
  text("20cm",width-width*0.281,height-height*0.0833);
  text("30cm",width-width*0.177,height-height*0.0833);
  text("40cm",width-width*0.0729,height-height*0.0833);
  textSize(20);
  text("Object: " + noObject, width-width*0.875, height-height*0.0277);
  text("Angle: " + iAngle +" °", width-width*0.48, height-height*0.0277);
  text("Distance: ", width-width*0.26, height-height*0.0277);
  if(iDistance<40) {
  text("        " + iDistance +" cm", width-width*0.225, height-height*0.0277);
  }
  textSize(25);
  fill(98,245,60);
  translate((width-width*0.4994)+width/2*cos(radians(30)),(height-height*0.0907)-width/2*sin(radians(30)));
  rotate(-radians(-60)); //la rotacion se hace con respecto al origen
  text("30°",0,0);
  resetMatrix();
  translate((width-width*0.503)+width/2*cos(radians(60)),(height-height*0.0888)-width/2*sin(radians(60)));
  rotate(-radians(-30));
  text("60°",0,0);
  resetMatrix();
  translate((width-width*0.507)+width/2*cos(radians(90)),(height-height*0.0833)-width/2*sin(radians(90)));
  rotate(radians(0));
  text("90°",0,0);
  resetMatrix();
  translate(width-width*0.513+width/2*cos(radians(120)),(height-height*0.07129)-width/2*sin(radians(120)));
  rotate(radians(-30));
  text("120°",0,0);
  resetMatrix();
  translate((width-width*0.5104)+width/2*cos(radians(150)),(height-height*0.0574)-width/2*sin(radians(150)));
  rotate(radians(-60));
  text("150°",0,0);
  popMatrix(); 
}

void draw() { 
  if (myClient.available() > 0) {  
    inString = myClient.readStringUntil(interesting);
    String[] rx = split(inString,',');
    //convertir str a float
   iAngle=float(rx[0]);
   iDistance=float(rx[1]); //conversion de data.
    //println(rx[0],rx[1]);
    println(rx[2],rx[3],rx[4]);
  }
    
 fill(98,245,31);
 textFont(orcFont);
 noStroke();
 fill(0,4); 
 rect(0, 0, width, height-height*0.065); 
 
 drawRadar(); 
 drawLine();
 drawObject();
 drawText();
 
 

 
} 
