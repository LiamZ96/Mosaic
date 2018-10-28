import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import math
import itertools
from enum import Enum
from os import listdir, path

"""
    Description: an enum class to handle the HoughCircle configuration values that are used in cv2.HoughCircles().
"""
class HoughConfig(Enum): 

    # 4x magnification 
    OBJX4 = { "dp": 1,"minDist": 40,"param1": 50,"param2": 55,"minRadius": 0,"maxRadius": 75 }

    # 10x magnification 
    OBJX10 = { "dp": 1,"minDist": 60,"param1": 65,"param2": 68,"minRadius": 0,"maxRadius": 125 }

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
        @Param houghConfig - a HoughConfig object that contains the values for the HoughCircles() function
        @return an object containing information collected during the counting process.
    """
    def getColorBeads(self,houghConfig):
        houghConfig = houghConfig.value
        result = []
        
        img = self.grayScaleMap
        cimg = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
        circles = cv2.HoughCircles(img,cv2.HOUGH_GRADIENT,dp=houghConfig["dp"],minDist=houghConfig["minDist"],
                            param1=houghConfig["param1"],param2=houghConfig["param2"],minRadius=houghConfig["minRadius"],maxRadius=houghConfig["maxRadius"])

        circles = np.uint16(np.around(circles))
        for i in circles[0,:]:
            # i[0] is x coordinate, i[1] is y coordinate, i[2] is radius
            # draw the outer circle
            cv2.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
            # draw the center of the circle
            cv2.circle(cimg,(i[0],i[1]),2,(0,0,255),3)

            color = self.getBrightestColor(i)
            if(color[1] == False): # if the bead is a water bead, leave it out.
                self.colorBeads.append(color)
                result.append(color)
            else: 
                self.waterBeads.append(color)
        
        imagePath = '/'.join(self.imagePath.split('/')[:-2]) + '/results/'
        images = [file for file in listdir(imagePath) if path.isfile((imagePath+file))]
        fileNum = len(images)
        imagePath += 'result_image' + str(fileNum) +'.jpg'
        cv2.imwrite(imagePath, cimg)
        return result 
        
    """
        Description: a function that takes a cicle's RGB values and returns if it is water or not
        @param RGB - tuple containing the average red, green, and blue values of a circle
        @return a boolean that will be True if the circle is water
    """ 
    def isWater(self, RGB):
        red = RGB[0]
        green = RGB[1]
        blue = RGB[2]
        isWater = False

        
        maxRGBValue = 230
        minRGBValue = 3

        if red >= maxRGBValue and green >= maxRGBValue and blue >= maxRGBValue:
            isWater = True
        if red <= minRGBValue and green <= minRGBValue and blue <= minRGBValue:
            isWater = True 
        return isWater

    def getQuadrantRGBSamples(self, minX, minY, maxX, maxY, imgX, imgY):
        img = self.colorMap
        b, g, r = [], [], []
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
        return[r, g, b]
   
    """
        NOT CURRENTLY BEING USED BUT SHOULD BE LEFT FOR FUTURE USE (OPTIONAL) BY USER

        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns an array containing the bead's average RGB values and a boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @param imageMap - a map (image) of the microscope images in color.
        @return a tuple containing bead sample avg RGB values
    """        
    def getSampleAvgColor(self, circleInfo, imageMap):
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

        quadRGB = self.getQuadrantRGBSamples(minX, minY, maxX, maxY, imgX, imgY)
        r.append(quadRGB[0])
        g.append(quadRGB[1])
        b.append(quadRGB[2])

        # 2nd quadrant
        minX = x - (radius - buffer)
        maxX = x
        minY = y
        maxY = y + (radius - buffer)

        quadRGB = self.getQuadrantRGBSamples(minX, minY, maxX, maxY, imgX, imgY)
        r.append(quadRGB[0])
        g.append(quadRGB[1])
        b.append(quadRGB[2])

        # 3rd quadrant
        minX = x - (radius - buffer)
        maxX = x
        minY = y - (radius - buffer)
        maxY = y

        quadRGB = self.getQuadrantRGBSamples(minX, minY, maxX, maxY, imgX, imgY)
        r.append(quadRGB[0])
        g.append(quadRGB[1])
        b.append(quadRGB[2])

        # 4th quadrant
        minX = x
        maxX = x + (radius - buffer)
        minY = y
        maxY = y + (radius - buffer)

        quadRGB = self.getQuadrantRGBSamples(minX, minY, maxX, maxY, imgX, imgY)
        r.append(quadRGB[0])
        g.append(quadRGB[1])
        b.append(quadRGB[2])

        flatR = list(itertools.chain(*r))
        flatG = list(itertools.chain(*g))
        flatB = list(itertools.chain(*b))

        avgBlue = round(np.mean(flatB), 2)
        avgGreen = round(np.mean(flatG), 2)
        avgRed = round(np.mean(flatR), 2)
        averageRGB = (avgRed, avgGreen, avgBlue)

        return averageRGB

    """
        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns a list containing tuple with the bead's average RGB values of the top 10% and boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @param imageMap - a map (image) of the microscope images in color.
        @return a list containing tuple with average RGB values of top 10% from bead and boolean isWater
    """        
    def getBrightestColor(self, circleInfo):
        img = self.colorMap
        imgY = img.shape[0]
        imgX = img.shape[1]
        x = circleInfo[0]
        y = circleInfo[1]
        radius = circleInfo[2]
        reds, greens, blues = [], [], []

        points = self.getPointsInCircle(radius, x, y)
        colorsList = []
        coordinates = list(points)

        for xCoord, yCoord in coordinates:
            if (xCoord >= imgX) or (yCoord >= imgY):
                pass
            else:
                bgrValue = img[yCoord, xCoord]
                RGB = ( bgrValue[2], bgrValue[1], bgrValue[0] )
                colorsList.append(RGB)

        sortedByRed = sorted(colorsList, key=lambda tup: tup[0], reverse=True)
        sortedByGreen = sorted(colorsList, key=lambda tup: tup[1], reverse=True)
        sortedByBlue = sorted(colorsList, key=lambda tup: tup[2], reverse=True)

        # may need to be adjusted
        tenPercent = math.floor(0.10 * len(colorsList))

        for i in range(0, tenPercent):
            reds.append(sortedByRed[i][0])
            greens.append(sortedByGreen[i][1])
            blues.append(sortedByBlue[i][2])

        average = (round(np.mean(reds), 2), round(np.mean(greens), 2), round(np.mean(blues), 2))
        isWater = self.isWater(average)
        return [average, isWater]


    """
        Description: a function that takes a bead's radius and x and y coordinates of the center and returns coordinates of every point in
                    the bead
        @param radius - radius of bead
        @param centerX - X coordinate of the center of bead
        @param centerY - Y coordinate of the center of bead
        @return a zip of the coordinates within a circle
    """ 
    def getPointsInCircle(self, radius, centerX, centerY):
        a = np.arange(radius + 1)
        for x, y in zip(*np.where(a[:, np.newaxis]**2 + a**2 <= radius**2)):
            # x and y given here were assuming that the center was at 0,0 therefore you must add the actual center coordinates to give accurate ones back
            yield from set((( centerX + x, centerY + y), (centerX + x, centerY -y), (centerX -x, centerY + y), (centerX -x, centerY -y),))
                    
