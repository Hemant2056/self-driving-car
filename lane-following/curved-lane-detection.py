from helpers.findLaneEdges import getPerspectiveTransformedLaneEdges
from helpers.fitPolynomial import  fit_polynomial
from helpers.findLanePixels import find_lane_pixels

import matplotlib.pyplot as plt

laneImageLocation = 'test-images/lane.jpeg'; 

#step 1

laneEdges = getPerspectiveTransformedLaneEdges(laneImageLocation)

plt.imshow(laneEdges)
plt.show()

#step 2

lanePixels , out_img = find_lane_pixels(laneEdges)

#step 3

out_img = fit_polynomial(laneEdges, lanePixels, out_img)

plt.imshow(out_img)
plt.show()