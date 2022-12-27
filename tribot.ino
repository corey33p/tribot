#include <Adafruit_MotorShield.h>
#include <Servo.h> 
#include <stdlib.h> // for choosing random numbers
#include <math.h>

Adafruit_MotorShield AFMS = Adafruit_MotorShield();

Adafruit_DCMotor* motor1 = AFMS.getMotor(1);
Adafruit_DCMotor* motor2 = AFMS.getMotor(2);
Adafruit_DCMotor* motor3 = AFMS.getMotor(3);


void setup(){
  Serial.begin(9600);
  Serial.println("check0");

  if (!AFMS.begin()) {         // create with the default frequency 1.6KHz
  // if (!AFMS.begin(1000)) {  // OR with a different frequency, say 1KHz
    Serial.println("Could not find Motor Shield. Check wiring.");
    while (1);
  }
  Serial.println("Motor Shield found.");

  motor1->setSpeed(0);
//  motor1->run(FORWARD);
  motor1->run(RELEASE);
  motor2->setSpeed(0);
//  motor2->run(FORWARD);
  motor2->run(RELEASE);
  motor3->setSpeed(0);
// motor3->run(FORWARD);
  motor3->run(RELEASE);
}

void goDirection(int heading){
   float speed_multiplier = .425;
   float radians_heading = (heading + 90) * PI / 180;
   int m1_speed = (int) (speed_multiplier * 255 * sin(radians_heading + PI/6));
   int m2_speed = (int) (speed_multiplier * 255 * cos(radians_heading + PI/3));
   int m3_speed = (int) (speed_multiplier * 255 * cos(radians_heading));

   motor1->run(RELEASE);
   motor2->run(RELEASE);
   motor3->run(RELEASE);
   delay(10);

   Serial.print("m1_speed: ");Serial.println(m1_speed);
   Serial.print("m2_speed: ");Serial.println(m3_speed);
   Serial.print("m3_speed: ");Serial.println(m3_speed);
   
   if (m1_speed < 0){ m1_speed = -m1_speed; motor1->run(BACKWARD); }
   else             { motor1->run(FORWARD);}
   if (m2_speed < 0){ m2_speed = -m2_speed; motor2->run(BACKWARD); }
   else             { motor2->run(FORWARD);}
   if (m3_speed < 0){ m3_speed = -m3_speed; motor3->run(BACKWARD); }
   else             { motor3->run(FORWARD);}
   
   motor1->setSpeed(m1_speed);
   motor2->setSpeed(m2_speed);
   motor3->setSpeed(m3_speed);
}

void loop(){
  goDirection(90);
  int random_direction = rand() % 360;
  Serial.println(" --- --- --- ");
  Serial.print("random_direction: ");Serial.println(random_direction);
  goDirection(random_direction);
  delay(1000);
  Serial.print("random_direction: ");Serial.println(random_direction+180);
  goDirection(random_direction + 180);
  delay(1000);
}
