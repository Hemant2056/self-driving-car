from helpers.findLaneEdges import getPerspectiveTransformedLaneEdges
from helpers.fitPolynomial import  fit_polynomial
from helpers.findLanePixels import find_lane_pixels

import cv2

import matplotlib.pyplot as plt

from time import sleep


videoObj = cv2.VideoCapture('test-images/lane.mp4')

success = True


while success:
    
    success, image = videoObj.read()

    if success:

        #step 1

        laneEdges = getPerspectiveTransformedLaneEdges(image)

        #step 2

        lanePixels , out_img = find_lane_pixels(laneEdges)

        #step 3

        out_img = fit_polynomial(laneEdges, lanePixels, out_img)
        
        cv2.imshow("out_img", out_img)
        cv2.waitKey(1)