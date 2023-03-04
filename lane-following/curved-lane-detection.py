from helpers.findLaneEdges import getPerspectiveTransformedLaneEdges, annotateFinalImage
from helpers.findLanePixels import find_lane_pixels
from helpers.getLanePresence import  getLanePresence
from helpers.detectDashedLane import detectDashedLane

import cv2
import matplotlib.pyplot as plt


videoObj = cv2.VideoCapture('test-images/lane3.mp4')

success = True

while success:

    success, image = videoObj.read()

    if success:

       # plt.imshow(image)
       # plt.show()

        #step 1

        laneEdges = getPerspectiveTransformedLaneEdges(image)

        #step 2

        laneEdges = cv2.flip(laneEdges, 1)

        lanePixels = find_lane_pixels(laneEdges)

        #step 3

        isLeftLaneLinePresent, isRightLaneLinePresent = getLanePresence(lanePixels)

        isInsideLeftLane, isInsideRightLane = detectDashedLane(laneEdges, lanePixels, [isLeftLaneLinePresent, isRightLaneLinePresent])

        out_img =  annotateFinalImage(laneEdges,  isInsideRightLane, isInsideLeftLane, isLeftLaneLinePresent, isRightLaneLinePresent)
        
        cv2.imshow("out_img", out_img)
        cv2.waitKey(1)