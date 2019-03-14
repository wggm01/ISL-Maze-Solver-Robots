#include <Servo.h>
#include "MPU9250.h"
#define RAD_TO_DEG 57.295779513082320876798154814105
//MPU
MPU9250 IMU(Wire,0x68);
int status;
float intex = 0;
float intey = 0;
float intez = 0;
//MPU
//Serial
char cmd[2];
int j=0;
boolean stringComplete = false;  // whether the string is complete
int flagSerial = 1; //control de envio de instrucciones
int flagIMU = 0;
int flagRadar = 0;
int servoattach=1;
//Serial
//Servos
Servo txServo;
//Servos

//HC-SR04
float distance; //crea la variable "distancia"
float tiempo; //crea la variable tiempo (como float)
#define TRIG_PIN A1
#define ECHO_PIN A0
//HC-SR04

void setup() {
  // initialize serial:
  Serial.begin(115200);
  //Servos
  txServo.attach(6);
  txServo.write(5);
  //Servos
  //HC-SR04
  pinMode(TRIG_PIN, OUTPUT); 
  pinMode(ECHO_PIN, INPUT); 
  //HC-SR04
  //MPU
  while(!Serial) {}
  // start communication with IMU 
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  } 
  //MPU
}

//--------Funciones--------------//
void radar(){
  
  for(int i=5;i<=181;i++){  
  txServo.write(i);
  delay(5);
  distance = calculateDistance();
  Serial.print("R");
  Serial.print(",");
  Serial.print("CCW"); 
  Serial.print(",");
  Serial.print(i);
  Serial.print(","); 
  Serial.print(distance); 
  //Serial.print(".");
  Serial.println("\n");
  //CONTROL DE IMU
if (flagIMU==1){
data_IMU();}
//CONTROL DE IMU 
  }
 
  for(int i=181;i>5;i--){  
  txServo.write(i);
  delay(5);
  distance = calculateDistance();
  Serial.print("R");
  Serial.print(",");
  Serial.print("CW"); 
  Serial.print(","); 
  Serial.print(i);
  Serial.print(",");
  Serial.print(distance);
  //Serial.print(".");
  Serial.print("\n");
  //CONTROL DE IMU
if (flagIMU==1){
data_IMU();}
//CONTROL DE IMU 
  }}
  
int calculateDistance(){ 
  digitalWrite(TRIG_PIN,LOW);
  delayMicroseconds(5);
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  tiempo = pulseIn(ECHO_PIN, HIGH,2915);
  int distancep = 0.01715*tiempo;
  if (distancep < 1){distancep=80;}
  return distancep;}

  void data_IMU(){
 IMU.readSensor();
 float gx = IMU.getGyroX_rads();
 float gy = IMU.getGyroY_rads();
 float gz = IMU.getGyroZ_rads();
 float ax = IMU.getAccelX_mss();
 float ay = IMU.getAccelY_mss();
 float az = IMU.getAccelZ_mss();
 intex +=gx*RAD_TO_DEG;
 intey +=gy*RAD_TO_DEG;
 intez +=gz*RAD_TO_DEG;
 float axg = map(ax, -9, 9,-1,1);
 float ayg = map(ay, -9, 9,-1,1);
 float azg = map(az, -9, 9,-1,1);
 float angx= 0.98*intex +0.02*axg;
 float angy= 0.98*intey +0.02*ayg;
 float angz= intez;
Serial.print("I");
Serial.print(",");
Serial.print(angx,6);
Serial.print(",");
Serial.print(angy,6);
Serial.print(",");
Serial.println(angz,6);
} 
//--------Funciones--------------//

void loop() {
//PROCESO DE INICIALIZACION
if(servoattach==1){txServo.detach();}
if (flagSerial == 0){  //Controlo que este bloque se ejecute con la bandera.
  if (stringComplete) {
       char cmd1 = cmd[0];
      if (cmd1== '1'){ //el numero 1 se utiliza como indicador de estado
       for(int i=0 ; i<4 ; i++){
      Serial.println(cmd1);}}//Mensaje de retorno
      else{
        if (cmd1== 'R'){ 
            flagIMU = 1; //Activa la transmision de data de imu
            flagRadar = 1;
            servoattach=0;
            txServo.attach(6);}
            //Serial.println(cmd1);}//Activa la transmision de data de radar
        else if(cmd1== 'E'){
            flagRadar = 0;
            flagIMU =0;//todo se desactiva
            servoattach=0;
            flagSerial=0;}
            //Serial.println(cmd1);}
            }
      // clear the string:
      cmd[0]='0'; cmd[1]='0';j=0;flagSerial = 0;
      stringComplete = false;}}

//CONTROL DE RADAR
if(flagRadar == 1){
  
radar();
//data_IMU();
  }}




void serialEvent() {
  while (Serial.available()) {
    char inChar = (char)Serial.read();
    //ACTIVA EL CODIGO EN EL LOOP
    flagSerial=0;
    // do something about it:
    cmd[j]=inChar;
    j = j+1;
    if (inChar == 's') {
      stringComplete = true;}}}


  
