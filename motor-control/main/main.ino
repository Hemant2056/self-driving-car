
#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\distance-to-obstacle\distance-to-obstacle.ino";

/** 
  * distanceToRearObstacle()
  * distanceToFrontObstacle()
*/

#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\find-velocity-and-accelrn\find-velocity-and-accelrn.ino";


void setup() {
  // put your setup code here, to run once:
Serial.begin(9600);


  initializeDistanceWithCorrespondingTime();

}

float accelerationOfObstacle;

void loop() {
  
  // put your main code here, to run repeatedly:
  accelerationOfObstacle = findAverageAcceleration();

 

}
