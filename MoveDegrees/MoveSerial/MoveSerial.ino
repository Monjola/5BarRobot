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




//int parseLongMessage(String msg, int number)
//{
//  char str[40];
//  msg.toCharArray(str,40);
//  int init_size = strlen(str);
//  char delim[] = " ";
//  char arr[][40] ={};
//  int index = 0;
//  char *ptr = strtok(str, delim);
//
//  while(ptr != NULL)
//  {
//    printf("'%s'\n", ptr);
//    arr[index][0] = *ptr;
//    index++;
//    ptr = strtok(NULL, delim);
//  }
//  String returnMsg = *arr[1];
//  return (int) returnMsg;
//}

int angleToPulses(int angle) {
  float pulsecommand = (float(ppr) / 360) * microstepping_factor * angle;
  return (int)pulsecommand;
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
  msg = Serial.readString();
  switch (msg[0]) {

    case 's': //settings
      switch (msg[1]) {
        case 'p': // settings/pulse-per-revolution
          ppr = parseMessage(msg, 2);
          break;
        case 'm': // settings/microstepping
          microstepping_factor = parseMessage(msg, 2);
          break;
      }
      break;

    case 'c': //command
      switch (msg[1]) {
        case 'l': //command/left-motor
          pos = parseMessage(msg, 2);
          leftStepper.moveTo(angleToPulses(pos));
          leftStepper.run();
          Serial.print(pos);
          break;
        case 'r': //command/right-motor
          pos = parseMessage(msg, 2);
          rightStepper.moveTo(angleToPulses(pos));
          rightStepper.run();
          Serial.print(pos);
          break;
        case 'b': //command/both-motors
          //Serial.print(msg);
          //pos = parseLongMessage(msg, 2);
          //Serial.print(pos);
          //TODO
          break;
      }
      break;
  }
  }
    
  
}
