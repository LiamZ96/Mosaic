import lib.stitching as stitching
import lib.counting as counting

def main():
    stitcher = stitching.Stitching()
    count = counting.Counting()

    stitcher.setDirectory("test/resources/sample3")
    #imagePath = stitcher.stitchOrderedImages()
    imagePath = stitcher.stitchUnorderedImages()
    #count.countBeads(imagePath)


if __name__ == "__main__":
    main()