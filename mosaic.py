from lib.stitching import Stitching 
from lib.counting import Counting, HoughConfig
from matplotlib import pyplot as plt

def main():
    stitcher = Stitching()
    stitcher.setDirectory("test/resources/sample4")
    imageMap = stitcher.stitchOrderedImages()
    #plt.imshow(imageMap),plt.show() # show the beads that have been detected

    #count = Counting("./test/resources/sampleMaps/map.png")
    #circles = count.getColorBeads(HoughConfig.OBJX4)
    #for i in circles:
       # print(i)
  #  print("Number of valid color beads found: "+str(len(circles)))
   # print("Number of water beads found: "+str(len(count.waterBeads)))




if __name__ == "__main__":
    main()