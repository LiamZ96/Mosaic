import stitching
import cv2

demo = stitching.Stitching()
demo.setDirectory('/home/jcarpenter/Documents/school/Mosaic/test/resources/sample3/')
temp = demo.stitchUnorderedImages()
'''
writer = cv2
writer.cv2.imshow("final",temp)
writer.cv2.imwrite('/home/jcarpenter/Documents/school/Mosiac/test/resources/sample2/final.jpg',temp)
'''


