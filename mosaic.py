from lib.stitching import Stitching 
from lib.counting import Counting 

def main():
    stitch = Stitching()
    count = Counting("./test/resources/sampleMaps/map.png")
    circles = count.getColorBeads()
    print(circles)
    print("Number of valid color beads found: "+str(len(circles)))
    print("---------------printing water beads---------------")
    print(count.waterBeads)
    print("Number of water beads found: "+str(len(count.waterBeads)))


if __name__ == "__main__":
    main()