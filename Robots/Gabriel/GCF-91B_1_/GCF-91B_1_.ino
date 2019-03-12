#include <Servo.h>

#define Servo_pin 10 //6 MEGA
#define servo_up 140
#define servo_down 47
#define err_pin 13
#define base_speed 90
const int sensor_number = 3;
const int sensor_data[sensor_number] = {A0,A1,A2}; //D-C-I
const int sensor_pwr[sensor_number] = {49,51,53};  //D-C-I
const int mot_pin[2][2] = {{3,5},{6,9}}; // 2,3-4,5 MEGA

Servo myservo; 

int mot_speed[2] = {0,0}; // 0 - 255

void move_servo(int pos){
  myservo.write(pos);
  digitalWrite(Servo_pin,LOW);
  delay(500);
}
void init_motors(void){
  int i = 0;
  int j = 0;
  while(j<2){
    i = 0;
    while(i<2){
      pinMode(mot_pin[j][i],OUTPUT);
      digitalWrite(mot_pin[j][i],LOW);
      i = i + 1;
    }
    j = j + 1;
  }  
}
void init_servo(void){
  pinMode(Servo_pin, OUTPUT);
  myservo.attach(Servo_pin);
  move_servo(servo_up);  
}
void init_sensors(void){
  int i = 0;
  while (i<sensor_number){
    pinMode(sensor_data[i],INPUT);
    pinMode(sensor_pwr[i],OUTPUT);
    digitalWrite(sensor_pwr[i],LOW);
    i = i + 1;
  }
}

float sensor_getdata(int sensor_n){ //D-C-I (1-2-3)
  int v = 0;
  int i = 0;
  if ((sensor_n > 0)&&(sensor_n <= sensor_number)){
    while (i<100){
      digitalWrite(sensor_pwr[sensor_n-1],HIGH);
      delayMicroseconds(250);
      v = v + analogRead(sensor_data[sensor_n-1]);
      delayMicroseconds(250);
      digitalWrite(sensor_pwr[sensor_n-1],LOW);
      delayMicroseconds(500);
      i = i + 1;
    }
    v = v/100;
    return v;
  }else{
    disp_err();
    return 0;
  }
}

void disp_err(void){
  motor_stop();
  while(true){ //Permanecerá aqui indicando que se produjo un error
    digitalWrite(err_pin,HIGH);
    delay(125);
    digitalWrite(err_pin,LOW);
    delay(125);
  }
}

void motor_rotation(int mot_n,int vel){
  if(vel<0){
    vel = -1*vel;
    analogWrite(mot_pin[mot_n-1][1],vel);
  }else{
    analogWrite(mot_pin[mot_n-1][0],vel);
  }
  delayMicroseconds(10);
}

void motor_ramp(int VF1,int VF2){
    int V0[2] = {mot_speed[0],mot_speed[1]};
    int a,b;
    if ((abs(VF1)>255)||(abs(VF2)>255)){
      disp_err();
    }
    while((V0[0]!=VF1)|(V0[1]!=VF2)){
      if(VF1>V0[0]){
        V0[0] = V0[0] + 1;
      }else if(VF1<V0[0]){
        V0[0] = V0[0] - 1;
      }
      if(VF2>V0[1]){
        V0[1] = V0[1] + 1;
      }else if(VF2<V0[1]){
        V0[1] = V0[1] - 1;
      }
      a = V0[0];
      b = V0[1];
      motor_rotation(1,a);
      motor_rotation(2,b);
    }
    mot_speed[0] = VF1;
    mot_speed[1] = VF2;
}   

void motor_stop(void){
  motor_ramp(0,0);
}

void turn(String dir){
  int R = 0;
  int L = 0;
  if (dir == "LEFT"){
    L = -1;
    R =  1;
  }else if (dir == "RIGHT"){
    L =  1;
    R = -1;
  }else{
    disp_err();
  }
  motor_stop();
  move_servo(servo_down);
  motor_ramp((L*base_speed),(R*base_speed));
  delay(400);
  motor_stop();
  move_servo(servo_up);
}

void setup() {
  // put your setup code here, to run once
  init_motors();
  init_servo();
  init_sensors();
  pinMode(err_pin, OUTPUT);
  Serial.begin(9600);
  motor_ramp(base_speed,base_speed);
}

float d = 0;
void loop() {
  // put your main code here, to run repeatedly:
  //d = sensor_getdata(3);
  //Serial.println(d);
  delay(300);
  motor_ramp(base_speed,base_speed);
  
 // delay(1500);
  //turn("RIGHT");
}
