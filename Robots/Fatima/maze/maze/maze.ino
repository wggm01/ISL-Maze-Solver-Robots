#include <Servo.h>
#include "MPU9250.h"
#include "math.h"
#define RAD_TO_DEG 57.295779513082320876798154814105
//MPU
MPU9250 IMU(Wire,0x68);
int status;
float gpitch,groll,gyaw;
float gyroRatex,gyroRatey,gyroRatez;
float accRatex,accRatey,accRatez;
float accpitch,accroll;
float pitch,roll,yaw;
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
   pinMode(LED_BUILTIN, OUTPUT); //Indicador de proceso de calibracion
  // initialize serial:
  Serial.begin(115200);
  //Servos
  txServo.attach(5);
  txServo.write(5);
  //Servos
  //HC-SR04
  pinMode(TRIG_PIN, OUTPUT); 
  pinMode(ECHO_PIN, INPUT); 
  //HC-SR04
  //MPU
 while(!Serial) {Serial.println("Problemas con IMU");}

  // start communication with IMU 
  status = IMU.begin();
   if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    while(1) {}
  }
  // setting the accelerometer full scale range to +/-8G 
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_2G);
  // setting the gyroscope full scale range to +/-500 deg/s
  IMU.setGyroRange(MPU9250::GYRO_RANGE_250DPS);
  // setting DLPF bandwidth to 20 Hz
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_20HZ);
  // setting SRD to 19 for a 50 Hz update rate (cada 20 ms)
  IMU.setSrd(19);//frecuencia de actualizacion de datos del imu (magnetometroData Output Rate = 8Hz)
 
  //Calibracion de Gyro
  int gC = IMU.calibrateGyro();
  if (gC>0){
    Serial.println("Gyro calibrado");
   for(int i=0; i<2; i++ ){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW); 
    }}else{Serial.println("Error Gyro");}
    
 //Calibracion de Acce
 int aC =IMU.calibrateAccel();
  if (aC>0){
    Serial.println("Acce calibrado");
   for(int i=0; i<3; i++ ){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW); 
    }}else{Serial.println("Error Gyro");}
  Serial.println("Mueva ligeramente el dispositivo");   
//Calibracion magnetometro
 int mC =IMU.calibrateAccel();
 if (mC>0){
    Serial.println("Mag calibrado");
   for(int i=0; i<4; i++ ){
    digitalWrite(LED_BUILTIN, HIGH);
    delay(500);
    digitalWrite(LED_BUILTIN, LOW); 
    }}else{Serial.println("Error Gyro");}
  //MPU
  //Confirmacion de idle
   for(int i=0; i<4; i++ ){
     Serial.println('1');
     delay(200);
    }
  //Confirmacion de idle
}

//--------Funciones--------------//
void radar(){
  
  for(int i=5;i<=180;i++){  
  txServo.write(i);
  delay(5);
  distance = calculateDistance();
  Serial.print("R");
  Serial.print(",");
  Serial.print("CCW"); 
  Serial.print(",");
  Serial.print(i);
  Serial.print(","); 
  Serial.println(distance); 
  //Serial.print(".");
  //Serial.println("\n");
  //CONTROL DE IMU
//uint32_t ts1 = micros();
if (flagIMU==1){
data_IMU();}}
//uint32_t ts1 = micros();
//Serial.println(ts2-ts1);
//CONTROL DE IMU 
  
 
  for(int i=180;i>5;i--){  
  txServo.write(i);
  delay(5);
  distance = calculateDistance();
  Serial.print("R");
  Serial.print(",");
  Serial.print("CW"); 
  Serial.print(","); 
  Serial.print(i);
  Serial.print(",");
  Serial.println(distance);
  //Serial.print(".");
  //Serial.print("\n");
  //CONTROL DE IMU
if (flagIMU==1){
data_IMU();}}
//CONTROL DE IMU 
  }
  
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
  // display the data
  gyroRatex=IMU.getGyroX_rads();
  gyroRatey=IMU.getGyroY_rads();
  gyroRatez=IMU.getGyroZ_rads();
  gpitch +=(gyroRatex/50)*RAD_TO_DEG;
  groll +=(gyroRatey/50)*RAD_TO_DEG;
  gyaw +=(gyroRatez/50)*RAD_TO_DEG;
  accRatex=IMU.getAccelX_mss();
  accRatey=IMU.getAccelY_mss();
  accRatez=IMU.getAccelZ_mss();
  accRatex=accRatex*0.10197162129779;
  accRatey=accRatey*0.10197162129779;
  accRatez=accRatez*0.10197162129779;
  accpitch= atan(accRatex/sqrt(pow(accRatey,2) + pow(accRatez,2)))*(RAD_TO_DEG);
  accroll= atan(accRatey/sqrt(pow(accRatex,2) + pow(accRatez,2)))*(RAD_TO_DEG);
  //Filtro complementario:
  pitch = 0.97402*gpitch + accpitch*0.02598;
  roll = 0.97402*groll + accroll*0.02598;
  yaw= gyaw;
  Serial.print("I");
  Serial.print(","); 
  Serial.print(pitch);
  Serial.print(",");
  Serial.print(roll);
  Serial.print(",");
  Serial.println(yaw);
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
            txServo.attach(5);}
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


  
