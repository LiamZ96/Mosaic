import lib.stitching as stitching
import lib.counting as counting

def main():
    stitch = stitching.Stitching()
    count = counting.Counting()
    circles = count.countBeads("./test/resources/sampleMaps/map.png")
    validBeads = 0
    for i in circles[0,:]:
        beadInfo = count.getAvgColor(i,"./test/resources/sampleMaps/map.png")
        
        if beadInfo[1] == False:
            validBeads += 1
    print("Valid beads detected: " + str(validBeads))


if __name__ == "__main__":
    main()
