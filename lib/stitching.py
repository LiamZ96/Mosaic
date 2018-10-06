import cv2
import os
from matplotlib import pyplot as plt

"""
	Description: a class to deal with stitching images together and handling overlap of the images.
"""
class Stitching: 
	def __init__(self):
		self.images = []
		self.directory = ""
        

	"""
		Description: a function for creating a stitched image from ordered images.
		@return A stitched image.
	"""
	def stitchOrderedImages(self):
		# Create stitcher and stitch images
		stitcher = cv2.createStitcher()
		status, image = stitcher.stitch(self.images)

		if status == cv2.STITCHER_OK:
			# Get results directory 
			resultsDir = os.path.join(os.path.dirname(__file__), "..", "results")
			imagePath = os.path.join(resultsDir, "stitched_image.jpg")

			# Check if results directory exist, if not create it
			if not os.path.exists(resultsDir):
				os.makedirs(resultsDir)

			# Save image in results directory
			cv2.imwrite(imagePath, image)

			return image
		else:
			print('Error during stiching')
			return False

	"""
		Description: a function for creating a stitched image from unordered images.
		@return A stitched image.
	"""
	def stitchUnorderedImages(self):
		orb = cv2.ORB_create()
		bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		kpMap = {}
	
		# Iterate through images and detect keypoints for each image and store in dictonary
		for idx, img in enumerate(self.images):
			kp, desc = orb.detectAndCompute(img, None)
			kpMap["image" + str(idx)] = (kp, desc, img)
	
		while (len(kpMap) > 1):
			# Get first kpMap key
			parentKey = next(iter(kpMap))
			parentValue = kpMap[parentKey]
			allMatches = {}
				
			# Second Iteration to find all the matching keypoints for parentKeypoints
			for childKey, childValue in kpMap.items():
				## Add all the matching keypoint a list
				if (parentKey != childKey):
					good = []
					matches = bf.match(parentValue[1], childValue[1])

					# Get only good matches
					for m in matches:
						#print(m.distance)
						if m.distance < 7:
							good.append(m)

					#print(len(good))
					allMatches[childKey] = good
			
			# Find value with best match
			bestKeyPoints = (None, [])
			for matchKey, matchValue in allMatches.items():
				if (len(bestKeyPoints[1]) < len(matchValue)):
					bestKeyPoints = (matchKey, matchValue)

			# TODO: Handle too similar images
			bestMatch = kpMap[bestKeyPoints[0]]

			# Sort them in the order of their distance.
			matches = sorted(bestKeyPoints[1], key = lambda x:x.distance)

			# Draw first 10 matches.
			img3 = cv2.drawMatches(parentValue[2], parentValue[0], bestMatch[2], bestMatch[0], matches[:10], None, flags=2)

			plt.imshow(img3)
			plt.show()

			# Remove best matching image from kpMap and replace parentKey
			del kpMap[bestKeyPoints[0]]
			del kpMap[parentKey]

			# Stitch best matching image with parentImage
			stitchedImg = self.__stitchImages(parentValue, bestMatch)
			#print(stitchedImg)
			kpMap[parentKey] = stitchedImg

		# Get fully stitched
		stitchedImage = kpMap[next(iter(kpMap))][2]

		# Get results directory 
		resultsDir = os.path.join(os.path.dirname(__file__), "..", "results")
		imagePath = os.path.join(resultsDir, "stiched_image.jpg")

		# Check if results directory exist, if not create it
		if not os.path.exists(resultsDir):
			os.makedirs(resultsDir)

		# Save image in results directory
		cv2.imwrite(imagePath, stitchedImage)
		
		return stitchedImage

	"""
		Description: a function setting the directory for looking for images, this will only be used by a 
			commandline interface
		@param path - The directory in unix format
	"""
	def setDirectory(self, path):
		# Get directory of test images
		self.directory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))

		# Read images and append to image array
		for file in os.listdir(self.directory):
			self.images.append(cv2.imread(os.path.join(self.directory, file), cv2.IMREAD_COLOR))

	def __stitchImages(self, firstImage, secondImage):
		#print(firstImage, secondImage)
		# Create stitcher and stitch images
		stitcher = cv2.createStitcher()
		orb = cv2.ORB_create()
		bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		status, image = stitcher.stitch([firstImage[2], secondImage[2]])
		kp, desc = orb.detectAndCompute(image, None)
		#cv2.imshow('Image 1', firstImage[2])
		#cv2.imshow('Image 2', secondImage[2])
		cv2.imshow("Stitched Image", image)
		cv2.waitKey(0)
		cv2.destroyAllWindows()
		return (kp, desc, image)