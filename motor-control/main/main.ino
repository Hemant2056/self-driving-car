
#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\motor-left-right\motor-left-right.ino"

/** 
  *
  * above file contains following functions:
  * turnLeft(), turnRight(), moveOrStop(), readSerialData(), reactToSerialMsg()   
  *    
*/

#include "E:\BE\8th_sem\major_project\sd-car\motor-control\helpers\distance-to-obstacle\distance-to-obstacle.ino"

/** 
  * distanceToRearObstacle()
  * distanceToFrontObstacle()
*/

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

}

float distanceWithCorrespondingTime = [][];

const int noOfDistanceTimeSamples = 10;

void putDistanceAndTimeOnIndex(int i){
  // change this line when rear ultrasonic sensor is added  
  distanceWithCorrespondingTime[noOfDistanceTimeSamples-1][0] =  calculateDistanceToFrontObstacle();
  
  distanceWithCorrespondingTime[noOfDistanceTimeSamples-1][1] = millis() / 1000 ;  
}

void updateDistanceToRearObstacleWithCorrespondingTime(){
  
  // shift the values to left so as to retain the recent samples only
  for(int i  = 0; i < noOfDistanceTimeSamples-1 ; i++ ){
    distanceWithCorrespondingTime[i][0] =  distanceWithCorrespondingTime[i+1][0];
    distanceWithCorrespondingTime[i][1] =  distanceWithCorrespondingTime[i+1][1];       
  }
  
  // update latest value
  putDistanceAndTimeOnIndex(noOfDistanceTimeSamples-1);
  
}

void initializeDistanceWithCorrespondingTime(){
  for (int i = 0 ; i< noOfDistanceTimeSamples; i++){
    putDistanceAndTimeOnIndex(i);
  }
}

float derivative, differenceInMagnitude , differenceInTime;

float findDerivative(int sampleLength, float[] samples){

float derivativeWithCorrespondingTime = [][];

float[] findDerivative(sampleLength, samples){

  for(i = 0; i < sampleLength - 1; i++){

    differenceInMagnitude = samples[i+1][0] - samples[i][0];
    differenceInTime = samples[i+1][1] - samples[i][1];

    derivative = differenceInDistance / differenceInTime;

    derivativeWithCorrespondingTime[i][0] = derivative;
    derivativeWithCorrespondingTime[i][1] = samples[i+1][1];
  
  }
  
  return derivativeWithCorrespondingTime;

}

float velocitySamples = [][];
const int noOfVelocitySamples =  noOfDistanceTimeSamples - 1;

void findVelocitySamples(){
  velocitySamples =  findDerivative(noOfDistanceTimeSamples, distanceWithCorrespondingTime)  
}

float accelerationSamples = [][];

void findAcclerationSamples(){
  accelerationSamples = findDerivative(noOfVelocitySamples, velocitySamples)
}

const int noOfAccelerationSamples = noOfVelocitySamples - 1;

float averageAcceleration, sumOfAllAccelerations;

void findAverageAcceleration(){
  sumOfAllAccelerations = 0;
  for(var i = 0; i < noOfAccelerationSamples; i++){
    sumOfAllAccelerations += accelerationSamples[i][0];
  }   
  averageAcceleration = averageAcceleration  / noOfAccelerationSamples;

  Serial.print("avg accelern: ");
  Serial.print(averageAcceleration);
}

void loop() {
  
  // put your main code here, to run repeatedly:
  readSerialData(); //reads searial diata and reacts to the searial msg from master


}
