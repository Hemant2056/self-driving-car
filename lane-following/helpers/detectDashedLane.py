import cv2

import numpy as np

def detectDashedLane(laneEdges, lanePixels, laneLinesPresence):

	isLeftLaneLinePresent, isRightLaneLinePresent = laneLinesPresence

	leftx, lefty, rightx, righty = lanePixels

	lefty = np.sort(lefty)


	righty = np.sort(righty)
	#print("lefty size: ", lefty.size, ", righty size: ", righty.size)

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

	#print("NBR: ", noOfLargeBreaksInRightLaneLine, ", NBL: ", noOfLargeBreaksInLeftLaneLine)

	# may need to tweak '2' and '3' from lines below

	#print("llp: ", isLeftLaneLinePresent, "rlp: ", isRightLaneLinePresent)

	if((noOfLargeBreaksInRightLaneLine > 1) & (noOfLargeBreaksInLeftLaneLine > 1)):
		# means the vehicle is inside the middle lane
		isInsideRightLane = True
		isInsideLeftLane = True
		#print("inside if")
	else:
		if(((noOfLargeBreaksInLeftLaneLine > 1) or ((noOfLargeBreaksInRightLaneLine < 2) & (isRightLaneLinePresent))) &  (noOfLargeBreaksInRightLaneLine <= noOfLargeBreaksInLeftLaneLine)):
			isInsideRightLane = True
			#print("inside if else ")
		else:
			if(((noOfLargeBreaksInRightLaneLine >= 2) or ((noOfLargeBreaksInLeftLaneLine < 2) & (isLeftLaneLinePresent))) & (noOfLargeBreaksInRightLaneLine >= noOfLargeBreaksInLeftLaneLine)):
				isInsideLeftLane = True;
				#print("inside if else else ")

	return isInsideLeftLane, isInsideRightLane	