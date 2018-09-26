import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import math

"""
    Description: a class to deal with counting microbeads in a stitched image.
"""
class Counting: 

    def __init__(self,imagePath):
        self.imagePath = imagePath
        self.grayScaleMap = cv2.imread(imagePath,0) # create grayscale cv2 img
        self.colorMap = cv2.imread(imagePath) # create color cv2 img
        self.colorBeads = []
        self.waterBeads = []

    """
        Description: a function that takes a map of images and counts the beads.
        @return an object containing information collected during the counting process.
    """
    def getColorBeads(self):
        result = []
        # TODO: REMOVE ME BEFORE MERGING WITH MASTER
        # This is super helpful. apparently opencv is garbo at documenting this.
        # https://www.pyimagesearch.com/2014/07/21/detecting-circles-images-using-opencv-hough-circles/
        img = self.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp=1,minDist=40,
                            param1=50,param2=55,minRadius=0,maxRadius=75)

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

            color = self.getAvgColor(i)
            if(color[1] == False): # if the bead is a water bead, leave it out.
                self.colorBeads.append(color)
                result.append(color)
            else: 
                self.waterBeads.append(color)

        plt.imshow(cimg),plt.show() # show the beads that have been detected
        return result 


    """
        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns an array containing the bead's average RGB values and a boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @return a list containing the RGB tuple and a boolean isWater
    """        
    def getAvgColor(self, circleInfo):
        random.seed(0)
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        r, g, b = [], [], []
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]

        # this might need to be adjusted
        # buffer is to eliminate the outside shadows factoring in on the edges of beads
        buffer = math.ceil(0.3 * radius)
        
        # 1st quadrant
        minX = x
        maxX = x + (radius - buffer)
        minY = y
        maxY = y + (radius - buffer)

        for i in range(0,50):
            randX = random.randint(minX, maxX)
            randY = random.randint(minY, maxY)
            if (randY >= imgY) or (randX >= imgX):
                pass
            else:
                bgr = img[randY, randX]
                b.append(bgr[0])
                g.append(bgr[1])
                r.append(bgr[2])

        # 2nd quadrant
        minX = x - (radius - buffer)
        maxX = x
        minY = y
        maxY = y + (radius - buffer)

        for i in range(0,50):
            randX = random.randint(minX, maxX)
            randY = random.randint(minY, maxY)
            if (randY >= imgY) or (randX >= imgX):
                pass
            else:
                bgr = img[randY, randX]
                b.append(bgr[0])
                g.append(bgr[1])
                r.append(bgr[2])

        # 3rd quadrant
        minX = x - (radius - buffer)
        maxX = x
        minY = y - (radius - buffer)
        maxY = y

        for i in range(0,50):
            randX = random.randint(minX, maxX)
            randY = random.randint(minY, maxY)
            if (randY >= imgY) or (randX >= imgX):
                pass
            else:
                bgr = img[randY, randX]
                b.append(bgr[0])
                g.append(bgr[1])
                r.append(bgr[2])

        # 4th quadrant
        minX = x
        maxX = x + (radius - buffer)
        minY = y
        maxY = y + (radius - buffer)

        for i in range(0,50):
            randX = random.randint(minX, maxX)
            randY = random.randint(minY, maxY)
            if (randY >= imgY) or (randX >= imgX):
                pass
            else:
                bgr = img[randY, randX]
                b.append(bgr[0])
                g.append(bgr[1])
                r.append(bgr[2])

        avgBlue = round(np.mean(b), 2)
        avgGreen = round(np.mean(g), 2)
        avgRed = round(np.mean(r), 2)
        averageRGB = (avgRed, avgGreen, avgBlue)
        isWater = self.__isWater(averageRGB)

        return [averageRGB, isWater]
        
    """
        Description: a function that takes a cicle's RGB values and returns if it is water or not
        @param RGB - tuple containing the average red, green, and blue values of a circle
        @return a boolean that will be True if the circle is water
    """ 
    def __isWater(self, RGB):
        red = RGB[0]
        green = RGB[1]
        blue = RGB[2]
        isWater = False

        # these may need to be adjusted, but a bead will either be white or blackish if small
        maxRGBValue = 230
        minRGBValue = 3

        if red >= maxRGBValue and green >= maxRGBValue and blue >= maxRGBValue:
            isWater = True
        if red <= minRGBValue and green <= minRGBValue and blue <= minRGBValue:
            isWater = True 
        return isWater
