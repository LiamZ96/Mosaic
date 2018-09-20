import cv2
import os

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, "resources/sample3/")
stitcher = cv2.createStitcher()
images = []


for file in os.listdir(path):
	images.append(cv2.imread(path + file, cv2.IMREAD_COLOR))


ret, pano = stitcher.stitch(images)

if ret == cv2.STITCHER_OK:
    cv2.imshow('panorama', pano)
    cv2.waitKey()

    cv2.destroyAllWindows()
else:
    print('Error during stiching')