import cv2
import os

"""
	Description: a class to deal with stitching images together and handling overlap of the images.
"""
class Stitching: 
	def __init__(self):
		self.images = []
		self.directory = ""
        

	"""
		Description: a function for creating a map of a collection of images.
		@param imageArray - an array of image objects.
		@return A stitched image.
	"""
	def createStitchedImage(self):
		stitcher = cv2.createStitcher()
		status, image = stitcher.stitch(self.images)

		if status == cv2.STITCHER_OK:
			tmpDir = os.path.join(os.path.dirname(__file__), "..", "tmp")
			imagePath = os.path.join(tmpDir, "stiched_image.jpg")
			if not os.path.exists(tmpDir):
				os.makedirs(tmpDir)
			cv2.imwrite(imagePath, image)
			return imagePath
		else:
			print('Error during stiching')

	"""
		Description: a function setting the directory for looking for images, this will only be used by a 
			commandline interface
		@param path - The directory in unix format
		@return No return
	"""
	def setDirectory(self, path):
		self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))
		for file in os.listdir(self.directory):
			self.images.append(cv2.imread(os.path.join(self.directory, file), cv2.IMREAD_COLOR))