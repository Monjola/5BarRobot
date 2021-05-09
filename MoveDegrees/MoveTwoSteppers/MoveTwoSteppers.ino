#include <AccelStepper.h>
#include <stdio.h>
#include <string.h>

//Define objects
AccelStepper rightStepper(1, 7, 6);
AccelStepper leftStepper(1, 3, 4);

//Define variables
int pos = 0;

int ppr = 200;
int microstepping_factor = 32;
String msg;

int stepper0_angle = 0;
int stepper1_angle = 0;

String stepper0_angle_str = "";
String stepper1_angle_str = "";

int comma_position;

int angleToPulses(int angle) {
  float pulsecommand = (float(ppr) / 360) * microstepping_factor * angle;
  return (int)pulsecommand;
}

int parseMessage(String msg, int number)
{
  msg.remove(0, number);

  return msg.toInt();
}
void setup() {
  Serial.begin(500000);
  rightStepper.setMaxSpeed(1800);
  rightStepper.setAcceleration(1800000);
  leftStepper.setMaxSpeed(1800);
  leftStepper.setAcceleration(1800000);
};



void loop() {
  rightStepper.run();
  leftStepper.run();
  if (rightStepper.distanceToGo() == 0 && leftStepper.distanceToGo() == 0) {
    if (Serial.available() == 1) {
  }
  String data = Serial.readStringUntil('\n');
  //Serial.print(data);
  comma_position = data.indexOf(','); 
  stepper0_angle_str = data.substring(0,comma_position);
  stepper0_angle = stepper0_angle_str.toInt();
  data = data.substring(comma_position+1, data.length());
  comma_position = data.indexOf(','); 
  stepper1_angle_str = data.substring(0,comma_position);
  stepper1_angle = stepper1_angle_str.toInt();
  if (stepper0_angle != 0) {
    rightStepper.moveTo(angleToPulses(stepper1_angle));
    leftStepper.moveTo(angleToPulses(stepper0_angle));
  }
  
  
    
  }
  

  }
  
    
