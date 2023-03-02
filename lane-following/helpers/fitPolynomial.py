import numpy as np
import cv2
import matplotlib.pyplot as plt


def fit_polynomial(binary_warped, lanePixels, out_img):
    
    leftx, lefty, rightx, righty = lanePixels

    print("left size: ", leftx.size, "rightx size: ", rightx.size)


    # Create an output image to draw on and visualize the result
    # Fit a second order polynomial to each using `np.polyfit`
    if not(leftx.size <500 or rightx.size <500):


        left_fit = np.polyfit(lefty, leftx, 2)
        right_fit = np.polyfit(righty, rightx, 2)

        # Generate x and y values for plotting
        ploty = np.linspace(0, binary_warped.shape[1]-1, binary_warped.shape[0] )
        try:
            left_fitx = left_fit[0]*ploty**2 + left_fit[1]*ploty + left_fit[2]
            right_fitx = right_fit[0]*ploty**2 + right_fit[1]*ploty + right_fit[2]
        except TypeError:
            # Avoids an error if `left` and `right_fit` are still none or incorrect
            print('The function failed to fit a line!')
            left_fitx = 1*ploty**2 + 1*ploty
            right_fitx = 1*ploty**2 + 1*ploty

        ## Visualization ##
        # Colors in the left and right lane regions
        out_img[lefty, leftx] = [255, 0, 0]
        out_img[righty, rightx] = [0, 0, 255]


        # Plots the left and right polynomials on the lane lines
        plt.plot(left_fitx, ploty, color='yellow')
        plt.plot(right_fitx, ploty, color='yellow')

        y_eval = np.max(ploty)
    
        # Calculation of R_curve (radius of curvature)
        left_curverad = ((1 + (2*left_fitx[0]*y_eval + left_fitx[1])**2)**1.5) / np.absolute(2*left_fitx[0])
        right_curverad = ((1 + (2*right_fitx[0]*y_eval + right_fitx[1])**2)**1.5) / np.absolute(2*right_fitx[0])

        print("left_curverad: ", left_curverad, " right_curverad: ", right_curverad)

    elif (leftx.size < 500):
        print("left lane not seen")
    elif(rightx.size < 500):
        print("right lane not seen")

    return out_img