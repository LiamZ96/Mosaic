import lib.stitching as stitching
import lib.counting as counting

def main():
    stitch = stitching.Stitching()
    count = counting.Counting()
    count.countBeads("./test/resources/sampleMaps/map.png")
    count.getAvgColors("./test/resources/sampleMaps/map.png")


if __name__ == "__main__":
    main()