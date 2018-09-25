import cv2
import numpy as np
from matplotlib import pyplot as plt

"""
    Description: a class to deal with counting microbeads in a stitched image.
"""
class Counting: 

    def __init__(self):
        pass

    """
        Description: a function that takes a map of images and counts the beads.
        @param imageMap - a map (image) of the microscope images.
        @return an object containing information collected during the counting process.
    """
    def countBeads(self,imageMap):
        # TODO: REMOVE ME BEFORE MERGING WITH MASTER
        # This is super helpful. apparently opencv is garbo at documenting this.
        # https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
        img = cv2.imread(imageMap,0)
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp=1,minDist=40,
                            param1=50,param2=55,minRadius=0,maxRadius=75)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

        plt.imshow(cimg),plt.show()
        
