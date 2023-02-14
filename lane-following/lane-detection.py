import cv2

import numpy as np

import matplotlib.pyplot as plt

def applyCannyTo(image):

	laneImageInGrayScale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)

	#to reduce noise in the image
	gaussianBlurredImage = cv2.GaussianBlur(laneImageInGrayScale, (5,5), 0)

	return cv2.Canny(gaussianBlurredImage, 50, 150)

def regionOfInterestFor(image):

	height = image.shape[0]

	width = image.shape[1]

	leftTop = (width/2 - 75, height * 3/5)

	bottomLeft = (width/8, height)

	bottomRight = (width-width/8, height)

	topRight = (width/2+75, height*3/5)
	

	#trapezoidRoi = np.array([[ (400, 342), (150, height), (950, height), (575, 342)]])

	trapezoidRoi = np.int32([[ leftTop, bottomLeft, bottomRight, topRight]])


#np.int32([[width/2-50, height* 3/5], [width/4, height], [width-width/4, height], [width/2+50, height*3/5]])


	mask = np.zeros_like(image)

	cv2.fillPoly(mask, trapezoidRoi, (255, 255, 255))

	cv2.imshow("mask", mask)

	maskedImage = cv2.bitwise_and(image, mask)

	cv2.imshow("maskedImage", maskedImage)

	return maskedImage

def makeCoordinates(forParameters, onImage):
	
	slope, yIntercept = forParameters

	y2 = onImage.shape[0]

	y1 = int(y2 * 3/5)

	x1 = int((y1 - yIntercept)/slope)

	x2 = int((y2 - yIntercept)/slope)

	return np.array([x1, y1, x2, y2])


def displayLines(lines, referenceImage):
	lineImage = np.zeros_like(referenceImage)

	leftLanes = []
	rightLanes = []

	noLeftLane = 0
	noRightLane = 0

	if lines is not None:
		for line in lines:
			x1, y1, x2, y2 = line[0]

			slope, yIntercept = np.polyfit((x1, x2), (y1, y2), 1)

			if slope<0:
				leftLanes.append((slope, yIntercept))
			
			else:
				rightLanes.append((slope, yIntercept))


		if(len(leftLanes)>0):

			averageSlopeAndYinterceptOfLeftLanes = np.average(leftLanes, axis = 0)
			
			x1, y1, x2, y2 = makeCoordinates(averageSlopeAndYinterceptOfLeftLanes, referenceImage)

			cv2.line(lineImage, (x1, y1), (x2, y2), 255, 10)


		else:
			noLeftLane = 1


		if(len(rightLanes)>0):

			averageSlopeAndYinterceptOfRightLanes = np.average(rightLanes, axis = 0)

			x1, y1, x2, y2 = makeCoordinates(averageSlopeAndYinterceptOfRightLanes, referenceImage)

			cv2.line(lineImage, (x1, y1), (x2, y2), 255, 10)

		else:	

			noRightLane = 1


	return lineImage


laneImage = cv2.imread('test-images/download.webp')

copiedLaneImage = np.copy(laneImage)

edgesInImage = applyCannyTo(copiedLaneImage)

cv2.imshow('edgesInImage', edgesInImage)

maskedImage = regionOfInterestFor(edgesInImage)

houghLines = cv2.HoughLinesP(maskedImage, 2, np.pi/180, 100)

lineImage = displayLines(houghLines, copiedLaneImage)

cv2.imshow("lineImage" , lineImage)

comboImage = cv2.addWeighted(copiedLaneImage, 1, lineImage, 0.3, 1)

cv2.imshow("comboImage", comboImage)

cv2.waitKey(0)
'''
[{"xmin":151.2482910156,"ymin":44.690952301,"xmax":190.1858520508,"ymax":107.3635940552,"confidence":0.551926434,"class":0,"name":"stop"},{"xmin":149.2155609131,"ymin":40.0123977661,"xmax":192.7724151611,"ymax":112.8377151489,"confidence":0.2979212105,"class":5,"name":"trafficlight"}]
stop sign detected
'''