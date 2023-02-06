from ultralytics import YOLO

model = YOLO('yolov8n.pt')

results = model('test_images/rtl.jpg')

print (results)