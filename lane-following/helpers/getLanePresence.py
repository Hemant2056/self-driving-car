import numpy as np
import cv2

def getLanePresence(lanePixels):

    isLeftLanePresent = True
    isRightLanePresent = True
    
    leftx, lefty, rightx, righty = lanePixels

    if (leftx.size < 500):
    
        isLeftLanePresent = False
    
    if(rightx.size < 500):
    
        isRightLanePresent = False

    return isLeftLanePresent, isRightLanePresent