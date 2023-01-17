import torch, json
from datetime import datetime
# Model
model = torch.hub.load('ultralytics/yolov5', 'custom', path='weights/best11.pt')  # local model
#model = torch.hub.load('ultralytics/yolov5', 'yolov5n')  # local model

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
	

	resultsInPython = json.loads(resultsInJson);
	for result in resultsInPython:
		if result['name']=="stop sign":
			isStop = 1
		print(result['name']+ " , ")
			
	if isStop:
		# in motor driver, set IN1, IN2 pins to LOW
		print("stop the car: , second part of time :  ",  datetime.now().second)
	

