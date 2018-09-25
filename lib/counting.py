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
        return circles

        
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
