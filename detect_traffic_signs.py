import torch, json
from datetime import datetime

from colorthief import ColorThief

# will convert the image to text string

import pytesseract  # pip install pytesseract

# then install tesseract from https://tesseract-ocr.github.io/tessdoc/

# then add full path of tesseract executable to the PATH
	# or put line like as the following one
# pytesseract.pytesseract.tesseract_cmd = r'<full_path_to_your_tesseract_executable>'
pytesseract.pytesseract.tesseract_cmd = r'E:\\tesseract\\tesseract.exe'


# adds image processing capabilities
from PIL import Image  

# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/traffic_sign.pt')  # local model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # local model


def cropImage(imgPath, eachResult):
	
	#bounding box for the detected sign e.g speed limit / trafficlight

	left = eachResult['xmin']
	top = eachResult['ymin']
	right = eachResult['xmax']
	bottom = eachResult['ymax']

	originalImage = Image.open(imgPath)

			# crop the iamge so as to extract speed limit part
			# based on bounding box

	return originalImage.crop((left, top, right, bottom))


while 1:
	#Image
	#later taken from the pi camera
	#img = 'https://images.hindustantimes.com/rf/image_size_640x362/HT/p1/2015/02/02/Incoming/Pictures/1312893_Wallpaper2.jpg'; #or each frame

	#img = 'test_images/green_traffic_light.jpg';

	#img = 'test_images/stop_sign.webp';

	#img = camera.frame()

	img = 'test_images/tlg.jpg'

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

		if result['name'] == "trafficlight":
			print(ColorThief(cropImage(img, result)).get_color(quality=1))
			
	break