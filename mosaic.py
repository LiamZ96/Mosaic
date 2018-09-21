import lib.stitching as stitching
import lib.counting as counting

def countBeads():
    count = counting.Counting()
    path="./test/resources/sampleMaps/map.png"
    count.countBeads(path)


def main():
    stitch = stitching.Stitching()
    countBeads()
    


if __name__ == "__main__":
    
    main()
