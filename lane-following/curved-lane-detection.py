import cv2
import numpy as np
import matplotlib.pyplot as plt

# Load the image
img = cv2.imread('test-images/lane.jpeg')

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

cv2.polylines(masked_edges, np.int32([ROIpoints]), True, (255,255,255))

# Display the resulting image
plt.imshow( masked_edges)
plt.show()

# max width and height of ROI lines

# Define the destination points for the bird's eye view
# or transformed ROI points

offsetInX = 20

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

# Display the resulting image
cv2.imshow("warped", warped)
cv2.waitKey(0)

# Apply Hough transform for curves
lines = cv2.HoughLines(masked_edges, rho=1, theta=np.pi/180, threshold=40, min_theta=0, max_theta=np.pi)

# Draw the lane curves on the original image
line_image = np.zeros((masked_edges.shape[0], masked_edges.shape[1], 3), dtype=np.uint8)

if lines is not None:

    for line in lines:
        rho, theta = line[0]
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(line_image, (x1, y1), (x2, y2), (0, 255, 0), 5)

    result = cv2.addWeighted(img, 0.8, line_image, 1, 0)

    
else:
    print("no lines detected")
