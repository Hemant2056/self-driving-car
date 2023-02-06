from ultralytics import YOLO

# Load a model
model = YOLO("weights/best-yolov8.pt")  # load a custom model

# Predict with the model
results = model("https://ultralytics.com/images/bus.jpg")  # predict on an image