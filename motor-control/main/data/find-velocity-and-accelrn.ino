const int noOfDistanceTimeSamples = 10;

float distanceWithCorrespondingTime[noOfDistanceTimeSamples][2];

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

float** findDerivative(int sampleLength, float samples[][2]){
  float** derivativeWithCorrespondingTime = (float**) malloc(sizeof(float*) * sampleLength);

  for(int i = 0; i < sampleLength - 1; i++){
    float* row = (float*) malloc(sizeof(float) * 2);

    float differenceInMagnitude = samples[i+1][0] - samples[i][0];
    float differenceInTime = samples[i+1][1] - samples[i][1];

    float derivative = differenceInMagnitude / differenceInTime;

    row[0] = derivative;
    row[1] = samples[i+1][1];

    derivativeWithCorrespondingTime[i] = row;
  }

  return derivativeWithCorrespondingTime;
}

const int noOfVelocitySamples =  noOfDistanceTimeSamples - 1;
float velocitySamples[noOfVelocitySamples][2]; // changed type to float (*)[2]

void freeAllocatedMemoryForPointerToDerivative(float** pointer, int noOfSamples){
  for(int row = 0; row < noOfSamples; row++ ){
    delete[] pointer[row];
  }
  delete[] pointer;
}

void findVelocitySamples(){
  float** pointerToDerivative =  findDerivative(noOfDistanceTimeSamples, distanceWithCorrespondingTime) ;   

  for(int i =0 ; i<noOfVelocitySamples; i++){
    velocitySamples[i][0] = pointerToDerivative[i][0];
    velocitySamples[i][1] = pointerToDerivative[i][1];
  }

  freeAllocatedMemoryForPointerToDerivative(pointerToDerivative, noOfVelocitySamples);         
}

const int noOfAccelerationSamples = noOfVelocitySamples - 1;

float accelerationSamples[noOfAccelerationSamples][2];

void findAcclerationSamples(){  
  float** pointerToDerivative = findDerivative(noOfVelocitySamples, velocitySamples);
  for(int i = 0 ; i < noOfAccelerationSamples; i++ ){
    accelerationSamples[i][0] =  pointerToDerivative[i][0];
    accelerationSamples[i][1] =  pointerToDerivative[i][1];
  }
  freeAllocatedMemoryForPointerToDerivative(pointerToDerivative, noOfAccelerationSamples);
}

float averageAcceleration, sumOfAllAccelerations;

void findAverageAcceleration(){
  sumOfAllAccelerations = 0;
  for(int i = 0; i < noOfAccelerationSamples; i++){
    sumOfAllAccelerations += accelerationSamples[i][0];
  }   
  averageAcceleration = averageAcceleration  / noOfAccelerationSamples;

  Serial.print("avg accelern: ");
  Serial.print(averageAcceleration);
}