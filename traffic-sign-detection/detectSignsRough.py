import torch, json
from datetime import datetime
from time import sleep
from PIL import Image  

model = torch.hub.load('yolov5', 'custom', path='weights/best-own.pt', source='local')  # local model

img = 'test_images/lane1.png' #from test_images dir

img = Image.open(img)
# Inference

results = model(img)

isStop = 0

resultsInJson = results.pandas().xyxy[0].to_json(orient="records")  # JSON img1 predictions

print(resultsInJson)