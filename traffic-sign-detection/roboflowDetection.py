from roboflow import Roboflow
rf = Roboflow(api_key="pINvNud9Xpw37qPdbF9w")
project = rf.workspace().project("traffic-sign-and-lights-detector")
model = project.version(1).model

# infer on a local image
print(model.predict("test_images/lane1.png", confidence=40, overlap=30).json())