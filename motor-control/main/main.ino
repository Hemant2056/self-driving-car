#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\motor-left-right\motor-left-right.ino";

/** 
  *
  * above file contains following functions:
  * turnLeft(), turnRight(), moveOrStop(), readSerialData(), reactToSerialMsg()   
  *    
*/

#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\distance-to-obstacle\distance-to-obstacle.ino";

/** 
  * distanceToRearObstacle()
  * distanceToFrontObstacle()
*/

#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\find-velocity-and-accelrn\find-velocity-and-accelrn.ino";


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);

// these pins are imported from motor-left-right.ino
pinMode(rearLeftWheel, OUTPUT);
pinMode(rearRightWheel, OUTPUT);
pinMode(frontLeftWheel, OUTPUT);
pinMode(frontRightWheel, OUTPUT);

// these pins are imported from distance-to-obstacle
pinMode(frontUltrasonicTrig, OUTPUT);
pinMode(frontUltrasonicEcho, INPUT);

pinMode(rearUltrasonicTrig, OUTPUT);
pinMode(rearUltrasonicEcho, INPUT);

moveOrStop(0);
  initializeDistanceWithCorrespondingTime();

}

float accelerationOfObstacle;

void loop() {
  
  // put your main code here, to run repeatedly:
  readSerialData(); //reads searial diata and reacts to the searial msg from master
  accelerationOfObstacle = findAverageAcceleration();

 

}
