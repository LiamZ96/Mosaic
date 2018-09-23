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
        img = cv2.imread(imageMap,0)
        fast = cv2.FastFeatureDetector_create()
        kp = fast.detect(img,None)
        img2 = cv2.drawKeypoints(img, kp,outImage=np.array([]), color=(255,0,0))
        plt.imshow(img2),plt.show()
