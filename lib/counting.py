'''
MIT License

Copyright (c) 2018 LiamZ96

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
#Requirements in this file: 3.1.7, 3.1.8, 3.1.9, 3.1.10, 3.2.4, 3.2.5, 3.3.1
#Authors: Jacob Wakefield, McKenna Gates

import cv2
import numpy as np
from matplotlib import pyplot as plt
import random
import math
import itertools
import csv
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
        blur = cv2.GaussianBlur(img,(5,5),0)
        circles = cv2.HoughCircles(blur,cv2.HOUGH_GRADIENT,dp=houghConfig["dp"],minDist=houghConfig["minDist"],
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
        imagePath += 'result_image.jpg'#+ str(fileNum) +'.jpg'
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
   

    """
        Description: a function that takes an array representing a circle's[x-coord of center, y-coord of center, radius]
                    and returns a list containing tuple with the bead's average RGB values of the top 10% and boolean isWater
        @param circleInfo - array that contains a circle's x and y coordinates of the center and the radius of the circle
        @param imageMap - a map (image) of the microscope images in color.
        @return a list containing tuple with average RGB values of top 10% from bead, boolean isWater, and x,y,radius value of the bead.
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
        return [[average[0],average[1],average[2]], isWater, [circleInfo[0],circleInfo[1],circleInfo[2]]] #[[R,G,B], isWater, [x,y,radius]]


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
                    

    """
        Description: 
        @param 
        @param
        @param 
        @return 
    """ 
    def makeBeadsCSV(self):
        newPath = self.imagePath
        endIndex = newPath.rfind("/")
        newPath = newPath[:endIndex]
        newPath = newPath.replace("maps", "results")
        newPath = newPath + "/beads.csv"
        with open(newPath, mode='w', newline='') as beadFile:
            writer = csv.writer(beadFile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
            colNames = ['Bead Number', 'Red Val', 'Green Val', 'Blue Val', 'X-Coord', 'Y-Coord', 'Radius']
            writer.writerow(colNames)
            i = 1
            for bead in self.colorBeads:
                r = bead[0][0]
                g = bead[0][1]
                b = bead[0][2]
                x = bead[2][0]
                y = bead[2][1]
                radius = bead[2][2]
                beadNum = i
                writer.writerow([beadNum, r, g, b, x, y, radius])
                i += 1