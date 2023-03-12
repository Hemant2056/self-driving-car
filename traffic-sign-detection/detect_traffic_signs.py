import torch, json
from datetime import datetime

from time import sleep

#from picamera2 import Picamera2


# will convert the image to text string

import pytesseract  # pip install pytesseract

# then install tesseract from https://tesseract-ocr.github.io/tessdoc/

# then add full path of tesseract executable to the PATH
	# or put line like as the following one
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
pytesseract.pytesseract.tesseract_cmd = r'E:\\tesseract\\tesseract.exe'
#none of the above mentioned steps were required for raspberry pi i.e
# no need to add to path or define tesseract_cmd variable (for rp)


# adds image processing capabilities
from PIL import Image  

#from picamera2 import Picamera2
'''

picam2 = Picamera2()
picam2.configure(picam2.create_preview_configuration(main={"format": 'XRGB8888', "size": (640, 480)}))
picam2.start()

'''
# Model

from datetime import datetime

model = torch.hub.load('yolov5', 'custom', path='weights/best.pt', source='local')  # local model

#model = torch.hub.load('yolov5', 'custom', path='weights/traffic_sign.pt', source='local')  # local model


def cropImage(originalImage, eachResult):
	
	#bounding box for the detected sign e.g speed limit / trafficlight

	left = eachResult['xmin']
	top = eachResult['ymin']
	right = eachResult['xmax']
	bottom = eachResult['ymax']

	#originalImage = Image.open(imgPath)

			# crop the iamge so as to extract speed limit part
			# based on bounding box

	return originalImage.crop((left, top, right, bottom))

def detectTrafficSigns():

	trafficSignsDetected = 0

	#img = Image.fromarray(img)
	img = 'test_images/sl_80.webp' #from test_images dir
	img = Image.open(img)
	# Inference

	results = model(img)

	isStop = 0

	resultsInJson = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions
	
	print(resultsInJson)

	resultsInPython = json.loads(resultsInJson);
	
	'''
	for result in resultsInPython:
		#if result['name']=="sl_20":
			#isStop = 1
		print(result['name']+ " , ")
			
	if isStop:
		# in motor driver, set IN1, IN2 pins to LOW
		print("stop the car: , second part of time :  ",  datetime.now().second)
	
	'''

	for result in resultsInPython:
        
		if result['name'] == 'speedlimit':
			
			speedLimitInText = pytesseract.image_to_string(cropImage(img, result))
			
			print('speed limit detected, speed limit: ', speedLimitInText )

		if result['name'] == "stop":
			print("stop sign detected")




while 1:
	detectTrafficSigns()


	print(datetime.now().second)

	'''
	trapezoidRoi = np.int32([[width/2-50, height* 3/5], [width/4, height], [width-width/4, height], [width/2+50, height*3/5]])

	'''

#include <iostream>
using namespace std;

const int noOfDistanceTimeSamples = 10;

float distanceWithCorrespondingTime[noOfDistanceTimeSamples][2] = {{50, 10}, {49, 11 }, {47, 12}, {44, 13}, {40, 14}, {35, 15}, {29, 16}, {22, 17}, {21, 18}, {21, 19   }};

void putDistanceAndTimeOnIndex(int i){
  // change this line when rear ultrasonic sensor is added
  // change this later
  //distanceWithCorrespondingTime[i][0] =  calculateDistanceToFrontObstacle();
  distanceWithCorrespondingTime[i][0] = (20 -  i) * (i+1);

  //distanceWithCorrespondingTime[i][1] = millis() / 1000.0 ;
    distanceWithCorrespondingTime[i][1] = 20 + i;
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
    /*
    Serial.print("sample 1: dist, time: ");
    Serial.print(samples[i+1][0]);
    Serial.print(", ");
    Serial.print(samples[i+1][1]);
    Serial.println();
    Serial.print("sample 2: dist, time: ");
    Serial.print(samples[i][0]);
    Serial.print(", ");
    Serial.println(samples[i][1]);
    delay(2000);
    */
    float differenceInMagnitude = samples[i+1][0] - samples[i][0];
    float differenceInTime = samples[i+1][1] - samples[i][1];
   /*
    Serial.print("diff in mag: ");
    Serial.print(differenceInMagnitude);
    Serial.print(", diff in time: ");
    Serial.print(differenceInTime);
    

    Serial.print("derivative: ");
    Serial.print(derivative);
    Serial.println();
    */
    
    float derivative = differenceInMagnitude / differenceInTime;
    cout<<"mag1: "<<samples[i+1][0]<<", mag2:  "<<samples[i][0]<<endl<<"time1: "<<samples[i+1][1]<<", time2: "<<samples[i][1]<<endl<<"diff in mag: "<<differenceInMagnitude<<", diff in time: "<<differenceInTime<<endl<<  ", derivative: "<<derivative<<endl<<endl<<endl;

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

float sumOfAllVelocities, averageVelocity;
float findAverageVelocity(){
	sumOfAllVelocities = 0;
	for(int i = 0; i< noOfVelocitySamples; i++){
    	sumOfAllVelocities += velocitySamples[i][0];
    }
    return sumOfAllVelocities / (float)noOfVelocitySamples;
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




float findAverageAcceleration(){
//updateDistanceToRearObstacleWithCorrespondingTime();

cout<<"velocity portion: "<<endl<<endl;
findVelocitySamples();



cout<<endl<<endl<<endl<<" acceleration samples"<<endl;


findAcclerationSamples();

  sumOfAllAccelerations = 0;
  for(int i = 0; i < noOfAccelerationSamples; i++){
    sumOfAllAccelerations += accelerationSamples[i][0];
      cout<<"accelrn: "<<accelerationSamples[i][0]<< "sum: "<<sumOfAllAccelerations<<endl;

  }
  cout<<" total sum: "<<sumOfAllAccelerations<<endl;
   cout<<"avg accelrn: ";
  averageAcceleration = sumOfAllAccelerations  / 				(float)noOfAccelerationSamples;
  return averageAcceleration;

}

int main(){

averageAcceleration =  findAverageAcceleration() * -1;

averageVelocity = findAverageVelocity() * -1;



}
