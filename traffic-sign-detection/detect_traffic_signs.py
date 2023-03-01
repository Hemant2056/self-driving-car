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