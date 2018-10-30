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

    # 4x demo 
    count = Counting("./test/resources/sampleMaps/resultsmap.jpg")
    circles = count.getColorBeads(HoughConfig.OBJX4)
    printCircles(count,circles)
    
    # 10x demo 
    count = Counting("./test/resources/sampleMaps/bluemap.jpg")
    circles = count.getColorBeads(HoughConfig.OBJX4)
    printCircles(count,circles)

if __name__ == "__main__":
    main()
