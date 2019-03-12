#include <hcsr04.h>
#include <Servo.h>
#include "MPU9250.h"

//MPU
MPU9250 IMU(Wire,0x68);
int status;
//MPU
//Serial
char cmd[2];
int j=0;
boolean stringComplete = false;  // whether the string is complete
int flagSerial = 1; //control de envio de instrucciones
int flagIMU = 0;
int flagRadar = 0;
//Serial
//Servos
Servo txServo;
//Servos
//HC-SR04
#define TRIG_PIN A1
#define ECHO_PIN A0
HCSR04 rad(TRIG_PIN, ECHO_PIN, 20, 400);

//HC-SR04

void setup() {
  // initialize serial:
  Serial.begin(115200);
  //Servos
  txServo.attach(6);
  txServo.write(5);
  //Servos
  //HC-SR04
  pinMode(trigPin, OUTPUT); 
  pinMode(echoPin, INPUT);
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
  //delay(5);
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
  //delay(5);
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
  distancemm=rad.distanceInMillimeters()
  distance= distancemm*0.1; //cm
  return distance;}

  void data_IMU(){
 IMU.readSensor();
Serial.print("I");
Serial.print(",");
Serial.print(IMU.getGyroX_rads(),6);
Serial.print(",");
Serial.print(IMU.getGyroY_rads(),6);
Serial.print(",");
Serial.print(IMU.getGyroZ_rads(),6);
Serial.print(",");
Serial.print(IMU.getAccelX_mss(),6);
Serial.print(",");
Serial.print(IMU.getAccelY_mss(),6);
Serial.print(",");
Serial.print(IMU.getAccelZ_mss(),6);
Serial.print(",");
Serial.print(IMU.getMagX_uT(),6);
Serial.print(",");
Serial.print(IMU.getMagY_uT(),6);
Serial.print(",");
Serial.print(IMU.getMagZ_uT(),6);
Serial.print(",");
Serial.println(IMU.getTemperature_C(),6);}
    
//--------Funciones--------------//

void loop() {
//PROCESO DE INICIALIZACION
if (flagSerial == 0){  //Controlo que este bloque se ejecute con la bandera.
  if (stringComplete) {
       char cmd1 = cmd[0];
      if (cmd1== '1'){ //el numero 1 se utiliza como indicador de estado
       for(int i=0 ; i<4 ; i++){
      Serial.println(cmd1);}}//Mensaje de retorno
      else{
        if (cmd1== 'R'){ 
            flagIMU = 1; //Activa la transmision de data de imu
            flagRadar = 1;}
            //Serial.println(cmd1);}//Activa la transmision de data de radar
        else if(cmd1== 'E'){
            flagRadar = 0;
            flagIMU =0;//todo se desactiva
            flagSerial=0;}
            //Serial.println(cmd1);}
            }
      // clear the string:
      cmd[0]='0'; cmd[1]='0';j=0;flagSerial = 0;
      stringComplete = false;}}

//CONTROL DE RADAR
if(flagRadar == 1){
radar();
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


  
