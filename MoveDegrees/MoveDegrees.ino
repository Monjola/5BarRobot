#include <AccelStepper.h>

// Define a stepper and the pins it will use
AccelStepper stepper(1,7,6); // Defaults to AccelStepper::FULL4WIRE (4 pins) on 2, 3, 4, 5
AccelStepper stepper2(1,3,4);
int pos = 0;
int movepos = 305;
int ppr = 200;
int microstepping_factor = 32;
String msg;

void setup(){  
  Serial.begin(500000);
  stepper.setMaxSpeed(1800);
  stepper.setAcceleration(1800000);
  stepper2.setMaxSpeed(1800);
  stepper2.setAcceleration(1800000);
}

int angleToPulses(int angle) {
  float pulsecommand = (float(ppr)/360)*microstepping_factor*angle;
  return pulsecommand;
  }

void loop()
{
    if (stepper2.distanceToGo() == 0)
    {

	delay(1000);
  
  if (pos == movepos)
    pos = 0;
    else {
      pos = movepos;
      }
  
  
	stepper2.moveTo(angleToPulses(pos));
    }
    stepper2.run();
}
