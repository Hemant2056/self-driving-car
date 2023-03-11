const int frontUltrasonicTrig = 2;
const int frontUltrasonicEcho = 3;

const int rearUltrasonicTrig = 8;
const int rearUltrasonicEcho = 9;


float duration;

float calculateDistance(int trigPin, int echoPin){
  Serial.println("calculating distance.../");
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);

  duration = pulseIn(echoPin, HIGH);


  return (duration * .0343)/2;
  
}

float calculateDistanceToFrontObstacle(){
  return  calculateDistance(frontUltrasonicTrig, frontUltrasonicEcho);
}

float calculateDistanceToRearObstacle(){
  return calculateDistance(rearUltrasonicTrig, rearUltrasonicEcho);
}


