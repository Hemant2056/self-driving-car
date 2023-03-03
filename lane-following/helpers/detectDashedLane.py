import cv2

import numpy as np

from helpers.findLanePixels import retMpLbRb

def detectDashedLane(laneEdges, lanePixels, laneLinesPresence):

	isLeftLaneLinePresent, isRightLaneLinePresent = laneLinesPresence

	leftx, lefty, rightx, righty = lanePixels


	lefty = lefty.sort()

	righty = righty.sort()

	
	noOfDarkPixelsToBeCountedAsLargeBreaks = 30 #may be required to  tune again on pi

	noOfLargeBreaksInLeftLaneLine = 0

	noOfLargeBreaksInRightLaneLine = 0

	if lefty is not None:

		for i in range(len(lefty)):
			if(i > 0):
				if(lefty[i] - lefty[i-1] > noOfDarkPixelsToBeCountedAsLargeBreaks):
					noOfLargeBreaksInLeftLaneLine += 1

	if righty is not None:

		for i in range(len(righty)):
			if(i > 0):
				if(righty[i] - righty[i-1] > noOfDarkPixelsToBeCountedAsLargeBreaks):
					noOfLargeBreaksInRightLaneLine += 1

	isInsideLeftLane = False

	isInsideRightLane = False

	# may need to tweak '2' and '3' from lines below

	if((isLeftLaneLinePresent & noOfLargeBreaksInLeftLaneLine > 2 & noOfLargeBreaksInRightLaneLine < noOfLargeBreaksInLeftLaneLine) or (noOfLargeBreaksInRightLaneLine < 3 & isRightLaneLinePresent)):
		isInsideRightLane = True

	if((isRightLaneLinePresent & noOfLargeBreaksInRightLaneLine > 2 & noOfLargeBreaksInRightLaneLine > noOfLargeBreaksInLeftLaneLine) or (noOfLargeBreaksInLeftLaneLine < 3 & isLeftLaneLinePresent)):
		isInsideLeftLane = True;

	return isInsideLeftLane, isInsideRightLane