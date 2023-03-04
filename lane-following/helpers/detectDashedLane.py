import cv2

import numpy as np

def detectDashedLane(laneEdges, lanePixels, laneLinesPresence):

	isLeftLaneLinePresent, isRightLaneLinePresent = laneLinesPresence

	leftx, lefty, rightx, righty = lanePixels

	lefty = np.sort(lefty)

	righty = np.sort(righty)

	noOfDarkPixelsToBeCountedAsLargeBreaks = 20 #may be required to  tune again on pi

	noOfLargeBreaksInLeftLaneLine = 0

	noOfLargeBreaksInRightLaneLine = 0


	if isLeftLaneLinePresent:

		for i in range(len(lefty)):
			if(i > 0):
				if(lefty[i] - lefty[i-1] > noOfDarkPixelsToBeCountedAsLargeBreaks):
					noOfLargeBreaksInLeftLaneLine += 1

	if isRightLaneLinePresent:
		for i in range(len(righty)):
			if(i > 0):
				if(righty[i] - righty[i-1] > noOfDarkPixelsToBeCountedAsLargeBreaks):
					noOfLargeBreaksInRightLaneLine += 1

	isInsideLeftLane = False

	isInsideRightLane = False

	print("NBL: ", noOfLargeBreaksInLeftLaneLine, ", NBR: ", noOfLargeBreaksInRightLaneLine)

	# may need to tweak '2' and '3' from lines below

	if((isLeftLaneLinePresent & noOfLargeBreaksInLeftLaneLine >= 2 & noOfLargeBreaksInRightLaneLine < noOfLargeBreaksInLeftLaneLine) or ((noOfLargeBreaksInRightLaneLine < 2) & (isRightLaneLinePresent))):
		isInsideRightLane = True

	if((isRightLaneLinePresent & noOfLargeBreaksInRightLaneLine >= 2 & noOfLargeBreaksInRightLaneLine > noOfLargeBreaksInLeftLaneLine) or ((noOfLargeBreaksInLeftLaneLine < 2) & (isLeftLaneLinePresent))):
		isInsideLeftLane = True;

	return isInsideLeftLane, isInsideRightLane	