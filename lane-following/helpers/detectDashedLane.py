import cv2

import numpy as np

def detectDashedLane(laneEdges, lanePixels, laneLinesPresence):

	isLeftLaneLinePresent, isRightLaneLinePresent = laneLinesPresence

	leftx, lefty, rightx, righty = lanePixels

	lefty = np.sort(lefty)

	righty = np.sort(righty)

	noOfDarkPixelsToBeCountedAsLargeBreaks = 5 #may be required to  tune again on pi

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

	if((noOfLargeBreaksInRightLaneLine > 1) & (noOfLargeBreaksInLeftLaneLine > 1)):
		# means the vehicle is inside the middle lane
		isInsideRightLane = True
		isInsideLeftLane = True
	else:
		if(((noOfLargeBreaksInLeftLaneLine > 1) or ((noOfLargeBreaksInRightLaneLine < 2) & (isRightLaneLinePresent))) &  (noOfLargeBreaksInRightLaneLine <= noOfLargeBreaksInLeftLaneLine)):
			isInsideRightLane = True
			print("inside else if")
		else:
			if(((noOfLargeBreaksInRightLaneLine >= 2) or ((noOfLargeBreaksInLeftLaneLine < 2) & (isLeftLaneLinePresent))) & (noOfLargeBreaksInRightLaneLine >= noOfLargeBreaksInLeftLaneLine)):
				isInsideLeftLane = True;
				print("inside else else")

	return isInsideLeftLane, isInsideRightLane	