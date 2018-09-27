from lib.stitching import Stitching 
from lib.counting import Counting 

def main():
    stitch = Stitching()
    count = Counting("./test/resources/sampleMaps/map.png")
    circles = count.getColorBeads()
    for i in circles:
        print(i)
        print()
    print("Number of valid color beads found: "+str(len(circles)))
    print("Number of water beads found: "+str(len(count.waterBeads)))


if __name__ == "__main__":
    main()