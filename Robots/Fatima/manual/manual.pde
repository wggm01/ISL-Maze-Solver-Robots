import processing.net.*; 
Client myClient; 
int clicks;

void setup(){
myClient = new Client(this, "192.168.25.113", 65435);

}

void draw() {
//Dibujitos de controles.
  
if (keyPressed){
  continue;}
else{
myClient.write("zs");//evita que se mueva y mantiene la conexion activa
}}

void keyPressed() {
  switch(key){
    case 'w':
      //enviar letra w
      myClient.write("ws");
    case 'a': 
      //enviar letra a
      myClient.write("as");
    case 'd':
      //enviar letra d
      myClient.write("ds");
    case 'q':
      //enviar letra q
      myClient.write("qs");
    case 'e':
      //enviar letra e
      myClient.write("es");
    case 'x':
      //enviar letra x (detiene el programa, termina la coneccion)
      myClient.write("xs");
    default:
      //evita que se mueva si presiono cualquier tecla(redundancia porque igual esto usando switch)
      myClient.write("zs");
}
