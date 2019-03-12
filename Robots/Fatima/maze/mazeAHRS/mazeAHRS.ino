
#include <hcsr04.h>
#include <Servo.h>
#include "quaternionFilters.h"
#include "MPU9250.h"

//MPU
#define AHRS true         
#define SerialDebug true
#define I2Cclock 400000
#define I2Cport Wire
#define MPU9250_ADDRESS MPU9250_ADDRESS_AD0
int status;
MPU9250 myIMU(MPU9250_ADDRESS, I2Cport, I2Cclock);
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
float distance;
#define TRIG_PIN A1
#define ECHO_PIN A0
HCSR04 rad(TRIG_PIN, ECHO_PIN, 20, 400);

//HC-SR04

void setup() {
  // initialize serial:
  Serial.begin(115200);
  //MPU
  Wire.begin();
  while(!Serial){}; //Evita que el programa incie sin el puerto serial
  byte c = myIMU.readByte(MPU9250_ADDRESS, WHO_AM_I_MPU9250);
  Serial.print(F("MPU9250 I AM 0x"));
  Serial.print(c, HEX);
  Serial.print(F(" I should be 0x"));
  Serial.println(0x71, HEX);
  if (c == 0x71) // WHO_AM_I should always be 0x68
  {
    // Start by performing self test and reporting values
   myIMU.MPU9250SelfTest(myIMU.selfTest);
    // Calibrate gyro and accelerometers, load biases in bias registers
   myIMU.calibrateMPU9250(myIMU.gyroBias, myIMU.accelBias);
   
    // Initialize device for active mode read of magnetometer
	myIMU.initMPU9250();
	Serial.println("MPU9250 initialized for active data mode....");
	byte d = myIMU.readByte(AK8963_ADDRESS, WHO_AM_I_AK8963);
    Serial.print("AK8963 ");
    Serial.print("I AM 0x");
    Serial.print(d, HEX);
    Serial.print(" I should be 0x");
    Serial.println(0x48, HEX);
	if (d != 0x48)
    {
      // Communication failed, stop here
      Serial.println(F("Communication failed, abort!"));
      Serial.flush();
      abort();
    }
	// Get magnetometer calibration from AK8963 ROM
    myIMU.initAK8963(myIMU.factoryMagCalibration);
    // Initialize device for active mode read of magnetometer
    Serial.println("AK8963 initialized for active data mode....");
	  myIMU.getAres();
    myIMU.getGres();
    myIMU.getMres();
  } // if (c == 0x71)
  else
  {
    Serial.print("Could not connect to MPU9250: 0x");
    Serial.println(c, HEX);
	// Communication failed, stop here
    Serial.println(F("Communication failed, abort!"));
    Serial.flush();
    abort();
  }
  //MPU

  //Servos
  txServo.attach(5);
  txServo.write(5);
  //Servos
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
   float distancemm=rad.distanceInMillimeters();
  float distancep= distancemm*0.1; //cm
  
  return distancep;}

  void data_IMU(){
	  myIMU.readAccelData(myIMU.accelCount);  // Read the x/y/z adc values

    
    // Now we'll calculate the accleration value into actual g's
    // This depends on scale being set
    myIMU.ax = (float)myIMU.accelCount[0]*myIMU.aRes; // - accelBias[0];
    myIMU.ay = (float)myIMU.accelCount[1]*myIMU.aRes; // - accelBias[1];
    myIMU.az = (float)myIMU.accelCount[2]*myIMU.aRes; // - accelBias[2];

    myIMU.readGyroData(myIMU.gyroCount);  // Read the x/y/z adc values
    
    
    // Calculate the gyro value into actual degrees per second
    // This depends on scale being set
    myIMU.gx = (float)myIMU.gyroCount[0]*myIMU.gRes;
    myIMU.gy = (float)myIMU.gyroCount[1]*myIMU.gRes;
    myIMU.gz = (float)myIMU.gyroCount[2]*myIMU.gRes;

    myIMU.readMagData(myIMU.magCount);  // Read the x/y/z adc values
    

	  myIMU.mx = (float)myIMU.magCount[0] * myIMU.mRes
               * myIMU.factoryMagCalibration[0] - myIMU.magBias[0];
    myIMU.my = (float)myIMU.magCount[1] * myIMU.mRes
               * myIMU.factoryMagCalibration[1] - myIMU.magBias[1];
    myIMU.mz = (float)myIMU.magCount[2] * myIMU.mRes
               * myIMU.factoryMagCalibration[2] - myIMU.magBias[2];
    


  // Must be called before updating quaternions!
  myIMU.updateTime();

  MahonyQuaternionUpdate(myIMU.ax, myIMU.ay, myIMU.az, myIMU.gx*DEG_TO_RAD,
                         myIMU.gy*DEG_TO_RAD, myIMU.gz*DEG_TO_RAD, myIMU.my,
                         myIMU.mx, myIMU.mz, myIMU.deltat);

  if (!AHRS)
  {
    myIMU.delt_t = millis() - myIMU.count;
    if (myIMU.delt_t > 3)
    {
      if(SerialDebug)
      {
		   int i =1; //Bypass
       /* // IMPRESION DE VALORES SIN USAR AHRS
        Serial.print("X-acceleration: "); Serial.print(1000*myIMU.ax);
        Serial.print(" mg ");
        Serial.print("Y-acceleration: "); Serial.print(1000*myIMU.ay);
        Serial.print(" mg ");
        Serial.print("Z-acceleration: "); Serial.print(1000*myIMU.az);
        Serial.println(" mg ");

        // Print gyro values in degree/sec
        Serial.print("X-gyro rate: "); Serial.print(myIMU.gx, 3);
        Serial.print(" degrees/sec ");
        Serial.print("Y-gyro rate: "); Serial.print(myIMU.gy, 3);
        Serial.print(" degrees/sec ");
        Serial.print("Z-gyro rate: "); Serial.print(myIMU.gz, 3);
        Serial.println(" degrees/sec");

        // Print mag values in degree/sec
        Serial.print("X-mag field: "); Serial.print(myIMU.mx);
        Serial.print(" mG ");
        Serial.print("Y-mag field: "); Serial.print(myIMU.my);
        Serial.print(" mG ");
        Serial.print("Z-mag field: "); Serial.print(myIMU.mz);
        Serial.println(" mG");

        myIMU.tempCount = myIMU.readTempData();  // Read the adc values
        // Temperature in degrees Centigrade
        myIMU.temperature = ((float) myIMU.tempCount) / 333.87 + 21.0;
        // Print temperature in degrees Centigrade
        Serial.print("Temperature is ");  Serial.print(myIMU.temperature, 1);
        Serial.println(" degrees C");*/
      }
      myIMU.count = millis();
    } // if (myIMU.delt_t > 500)
  } // if (!AHRS)
  else
  {
    // Serial print at 0.5 s rate independent of data rates
    myIMU.delt_t = millis() - myIMU.count;

    if (myIMU.delt_t > 3)
    {
      if(SerialDebug)
      {
		    int i =1; //Bypass
       /* Serial.print("ax = "); Serial.print((int)1000*myIMU.ax);
        Serial.print(" ay = "); Serial.print((int)1000*myIMU.ay);
        Serial.print(" az = "); Serial.print((int)1000*myIMU.az);
        Serial.println(" mg");

        Serial.print("gx = "); Serial.print( myIMU.gx, 2);
        Serial.print(" gy = "); Serial.print( myIMU.gy, 2);
        Serial.print(" gz = "); Serial.print( myIMU.gz, 2);
        Serial.println(" deg/s");

        Serial.print("mx = "); Serial.print( (int)myIMU.mx );
        Serial.print(" my = "); Serial.print( (int)myIMU.my );
        Serial.print(" mz = "); Serial.print( (int)myIMU.mz );
        Serial.println(" mG");

        Serial.print("q0 = "); Serial.print(*getQ());
        Serial.print(" qx = "); Serial.print(*(getQ() + 1));
        Serial.print(" qy = "); Serial.print(*(getQ() + 2));
        Serial.print(" qz = "); Serial.println(*(getQ() + 3));*/
      }

      myIMU.yaw   = atan2(2.0f * (*(getQ()+1) * *(getQ()+2) + *getQ() *
                    *(getQ()+3)), *getQ() * *getQ() + *(getQ()+1) * *(getQ()+1)
                    - *(getQ()+2) * *(getQ()+2) - *(getQ()+3) * *(getQ()+3));
      myIMU.pitch = -asin(2.0f * (*(getQ()+1) * *(getQ()+3) - *getQ() *
                    *(getQ()+2)));
      myIMU.roll  = atan2(2.0f * (*getQ() * *(getQ()+1) + *(getQ()+2) *
                    *(getQ()+3)), *getQ() * *getQ() - *(getQ()+1) * *(getQ()+1)
                    - *(getQ()+2) * *(getQ()+2) + *(getQ()+3) * *(getQ()+3));
      myIMU.pitch *= RAD_TO_DEG;
      myIMU.yaw   *= RAD_TO_DEG;
      //    4.60° W  ± 0.31° (3-10-19) UTP Panama Declinacion
      // - http://www.ngdc.noaa.gov/geomag-web/#declination
      myIMU.yaw   -= 4.6;
      myIMU.roll  *= RAD_TO_DEG;

      if(SerialDebug)
      {
        Serial.print("I");
        Serial.print(", ");
        Serial.print(myIMU.yaw, 2);
        Serial.print(", ");
        Serial.print(myIMU.pitch, 2);
        Serial.print(", ");
        Serial.println(myIMU.roll, 2);

        /*Serial.print("rate = ");
        Serial.print((float)myIMU.sumCount/myIMU.sum, 2);
        Serial.println(" Hz");*/
      }

      myIMU.count = millis();
      myIMU.sumCount = 0;
      myIMU.sum = 0;
    } // if (myIMU.delt_t > 500)
  } // if (AHRS)
}
    
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


  
