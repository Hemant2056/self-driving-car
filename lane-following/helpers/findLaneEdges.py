import numpy as np
import cv2
import matplotlib.pyplot as plt

def getPerspectiveTransformedLaneEdges(img):

	copiedImg = np.copy(img)

	# Convert the image to grayscale
	gray = cv2.cvtColor(copiedImg, cv2.COLOR_BGR2GRAY)

	# Apply Gaussian blur
	blur = cv2.GaussianBlur(gray, (5, 5), 0)

	# Apply Canny edge detection
	edges = cv2.Canny(blur, 50, 150)


	# Define the ROI
	mask = np.zeros_like(edges)
	ignore_mask_color = 255
	imshape = img.shape

	#ROI Points

	offsetY = 0
	#'''
	#Roi for test video

	topLeft = (601, 444)
	bottomLeft = (180, imshape[0]-offsetY)
	bottomRight =  (1160, imshape[0]-offsetY)
	topRight = (934, topLeft[1])
	
	'''
	#roi for lane.jpeg

	topLeft = (435, 338)
	bottomLeft = (175, imshape[0] - offsetY)
	bottomRight =  (905, imshape[0] - offsetY)
	topRight = (540, topLeft[1])	

	'''

	ROIpoints = [topLeft, bottomLeft, bottomRight, topRight]

	ROI = np.array([ROIpoints])
	cv2.fillPoly(mask, ROI, ignore_mask_color)
	masked_edges = cv2.bitwise_and(edges, mask)

	copiedMaskedEdges = np.copy(masked_edges)

#	cv2.polylines(copiedMaskedEdges, np.int32([ROIpoints]), True, (255,255,255))

#	cv2.imshow("copied masked edges", copiedMaskedEdges)
#	cv2.waitKey(0)

	# Define the destination points for the bird's eye view
	# or transformed ROI points

	offsetInX = 10

	transformedTopLeft = (topLeft[0] - offsetInX, topLeft[1])
	transformedBottomLeft  = (transformedTopLeft[0], imshape[0])
	transformedBottomRight = (topRight[0] + offsetInX, imshape[0])
	transformedTopRight = (transformedBottomRight[0], topRight[1])

	dst =np.float32([[transformedTopLeft, transformedBottomLeft, transformedBottomRight, transformedTopRight]])

	# Define the source points for the bird's eye view
	#src = np.float32([[(100,imshape[0]),(400, 340), (567, 320), (imshape[1],imshape[0])]])

	src = np.float32(ROIpoints)

	# Use the cv2.getPerspectiveTransform() function to get the transformation matrix
	M = cv2.getPerspectiveTransform(src, dst)

	# Use the cv2.warpPerspective() function to apply the transformation matrix to the original image and get the bird's eye view
	warped = cv2.warpPerspective(masked_edges, M, (img.shape[1], img.shape[0]), flags=cv2.INTER_LINEAR)

	offset = 10
#left_curverad:  1780756078028722.5  right_curverad:  2467522555118308.0

	return warped[transformedTopLeft[1]:transformedBottomLeft[1], transformedTopLeft[0]-offset:transformedTopRight[0]+offset]


def annotateFinalImage(out_img,isOnRightLane, isOnLeftLane, isLeftLanePresent, isRightLanePresent):
	if isOnRightLane:
	    text = "on RL"
	elif isOnLeftLane:
	    text = "on LL"
	elif isOnLeftLane & isOnRightLane:
		text = "on midL"
	else:
	    text = "on N/a "

	# font
	font = cv2.FONT_HERSHEY_SIMPLEX
	  
	# org
	org = (100, 70)
	  
	# fontScale
	fontScale = 1
	   
	# Red color in BGR
	color = (255, 255, 255)
	  
	# Line thickness of 2 px
	thickness = 1
	   
	# Using cv2.putText() method
	out_img = cv2.putText(out_img, text, org, font, fontScale, color, thickness, cv2.LINE_AA, False)
	  
	if (isLeftLanePresent & isRightLanePresent):
	    text = "BL Prsnt"
	elif isLeftLanePresent:
	    text = "LL Prsnt"
	elif isRightLanePresent:
	    text = "RL Prsnt"
	else:
	    text = "NL Prsnt"

	org = (100, 120)

	out_img = cv2.putText(out_img, text, org, font, fontScale, 
	                 color, thickness, cv2.LINE_AA, False)

	return out_img