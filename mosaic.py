import lib.stitching as stitching
import lib.counting as counting

def main():
    stitch = stitching.Stitching()
    count = counting.Counting()
    circles = count.countBeads("./test/resources/sampleMaps/map.png")
    for i in circles[0,:]:
        beadInfo = count.getBrightestColor(i,"./test/resources/sampleMaps/map.png")
        print(beadInfo)

if __name__ == "__main__":
    main()