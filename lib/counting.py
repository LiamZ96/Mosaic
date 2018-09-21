import cv2
import numpy as np

"""
    Description: a class to deal with counting microbeads in a stitched image.
"""
class Counting: 
    def __init__(self):
        pass 
    
    """
        Description: a function that takes a map of images and counts the beads.
        @param imageMap - a map (image) of the microscope images.
        @return a dictionary containing information collected during the counting process.
    """
    def countBeads(self,imageMap):
        img = cv2.imread(imageMap)
        gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

        sift = cv2.xfeatures2d.SIFT_create() #throws error telling you to rebuild opencv to include nofree sift functions
        kp = sift.detect(gray,None)

        img=cv2.drawKeypoints(gray,kp)

        cv2.imwrite('sift_keypoints.png',img)