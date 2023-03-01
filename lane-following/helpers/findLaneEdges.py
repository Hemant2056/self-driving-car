import numpy as np
import cv2

def getPerspectiveTransformedLaneEdges(imageLoc):
		# Load the image
	img = cv2.imread(imageLoc)

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

	topLeft = (450, 331)
	bottomLeft = (170, imshape[0])
	bottomRight =  (imshape[1]-60, imshape[0])
	topRight = (525, 331)

	ROIpoints = [topLeft, bottomLeft, bottomRight, topRight]

	ROI = np.array([ROIpoints])
	cv2.fillPoly(mask, ROI, ignore_mask_color)
	masked_edges = cv2.bitwise_and(edges, mask)

	#cv2.polylines(masked_edges, np.int32([ROIpoints]), True, (255,255,255))

	# Display the resulting image
	#plt.imshow( masked_edges)
	#plt.show()

	# max width and height of ROI lines

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

	offset = 50

	return warped[transformedTopLeft[1]:transformedBottomLeft[1], transformedTopLeft[0]-offset:transformedTopRight[0]+offset]
