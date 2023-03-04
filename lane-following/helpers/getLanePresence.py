import numpy as np
import cv2

def getLanePresence(lanePixels):

    isLeftLanePresent = True
    isRightLanePresent = True
    
    leftx, lefty, rightx, righty = lanePixels

    minPointsRequiredToFormLane = 300

    if (leftx.size < minPointsRequiredToFormLane):
    

        isLeftLanePresent = False
    
    if(rightx.size < minPointsRequiredToFormLane):
    
        isRightLanePresent = False

    return isLeftLanePresent, isRightLanePresent