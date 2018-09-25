import cv2
import numpy as np
from matplotlib import pyplot as plt
import random

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

    def getAvgColors(circleArry, imageMap):
        random.seed(0)
        circleArry = [(514, 290, 40), (1106, 962, 40), (465, 280, 40)]
        img = cv2.imread(imageMap)
        averages = []       

        print(img.shape)
        print(img[1106, 962])
        
        '''
        for circle in circleArry:
            r = []
            g = []
            b = []
            x = circle[0]
            y = circle[1]
            radius = circle[2]

            print(x,y,radius)
            print(img[x,y])
            print(img[x,y][0])
            #plot points?
            minX = x - (radius - 10)
            maxX = x + (radius - 10)
            minY = y - (radius - 10)
            maxY = y + (radius - 10)
            for i in range (0,50):
                randX = random.randint(minX, maxX)
                randY = random.randint(minY, maxY)
                rgb = img[randX, randY]
                r.append(rgb[0])
                g.append(rgb[1])
                b.append(rgb[2])
            avgRed = np.mean(r)
            avgGreen = np.mean(g)
            avgBlue = np.mean(b)
            print(r)
            print(avgRed)
            averages.append([avgRed, avgGreen, avgBlue])
        print(averages)
        '''