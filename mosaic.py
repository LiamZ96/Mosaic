from lib.stitching import Stitching 
from lib.counting import Counting, HoughConfig
from matplotlib import pyplot as plt

def printCircles(counter,circles): 
    print("---------------------------------------------------------------------------")
    for i in circles:
        print(i)
    print("Number of valid color beads found: "+str(len(circles)))
    print("Number of water beads found: "+str(len(counter.waterBeads)))
    print("---------------------------------------------------------------------------")

def main():
    stitcher = Stitching()
    stitcher.setDirectory("test/resources/sample2")
    imageMap = stitcher.stitchUnorderedImages()

    # 4x demo 
    count = Counting("./test/resources/sampleMaps/map.png")
    circles = count.getColorBeads(HoughConfig.OBJX4)
    printCircles(count,circles)
    
    # 10x demo 
    count = Counting("./test/resources/sampleMaps/map_10x.jpg")
    circles = count.getColorBeads(HoughConfig.OBJX10)
    printCircles(count,circles)

if __name__ == "__main__":
    main()
