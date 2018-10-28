import cv2
import os
from matplotlib import pyplot as plt
import time
import sys
from PIL import Image
import shutil

"""
	Description: a class to deal with stitching images together and handling overlap of the images.
"""
class Stitching: 
	def __init__(self):
		self.images = []
		self.sourceDirectory = ""
		self.pSize = 800
		self.eThresh = 0
		self.resultsDirectory =""
		

	"""
		Description: a function for creating a stitched image from ordered images.
		@return A stitched image.
	"""
	def stitchOrderedImages(self):
		# Create stitcher and stitch images
		stitcher = cv2.createStitcher(True)
		status, image = stitcher.stitch(self.images)

		if status == cv2.STITCHER_OK:
			# Get results directory 
			#resultsDir = os.path.join(os.path.dirname(__file__), "..", "results")
			imagePath = os.path.join(resultsDir, "stiched_image.jpg")

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
	def collage(self,temp_path):
		images = []
		for file in os.listdir(temp_path):
			if(file.find('jpg') != -1 or file.find('JPG') != -1):
				images.append(Image.open(str(temp_path) + "/" + str(file)))
		widths, heights = zip(*(i.size for i in images))
		total_width = sum(widths)
		max_height = max(heights)

		new_im = Image.new('RGB', (total_width, max_height))

		x_offset = 0
		for im in images:
  			new_im.paste(im, (x_offset,0))
  			x_offset += im.size[0]
		
		new_im.save(self.resultsDirectory + 'map.jpg')
		shutil.rmtree(temp_path)


	def twoRoundStitch(self):
		completed_images = []
		print("begin first round")
		temp_dir = str(int(round(time.time())))
		temp_dir = temp_dir + "/"
		os.makedirs(temp_dir)
		self.pSize = 1000
		self.eThresh = 0
		first_round = []
		first_round = self.stitchUnorderedImages()
		self.images = [] #reset self.images to empty
		self.images = first_round
		self.pSize=200
		self.eThresh=200
		print("begin second round")
		final_images = self.stitchUnorderedImages()
		img_number =0
		for img in final_images:
			cv2.imwrite(str(temp_dir) + str(img_number) + ".jpg",img)
			img_number +=1
		self.collage(temp_dir)

	def stitchUnorderedImages(self):
		#if not os.path.exists(self.resultsDirectory):
		#	os.makedirs(self.resultsDirectory)

		orb = cv2.ORB_create(WTA_K=4, scaleFactor=1.1,patchSize=self.pSize,edgeThreshold=self.eThresh)
		bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)
		kpMap = {}
		matchLevel = 0
		matchThreshold =15
		parentKey = None
		completed_images = []
		
		# Iterate through images and detect keypoints for each image and store in dictonary
		for idx, img in enumerate(self.images):
			kp, desc = orb.detectAndCompute(img, None)
			if(len(kp) > 0):
				kpMap["image" + str(idx)] = (kp, desc, img)
			else:
				imagePath = os.path.join(self.resultsDirectory, "stiched_"+str(idx) +".jpg")
				completed_images.append(img)				
				#cv2.imwrite(imagePath,img)


		print("Initial count", len(kpMap))
		while (len(kpMap) > 1):
			# Get first kpMap key
			if(parentKey == None):
				parentKey = next(iter(kpMap))
			parentValue = kpMap[parentKey]
			allMatches = {}
			if(matchLevel > len(kpMap)):
				matchThreshold +=10
			# Second Iteration to find all the matching keypoints for parentKeypoints
			test = kpMap.items()
			for childKey, childValue in kpMap.items():
				## Add all the matching keypoint a list
				if (parentKey != childKey):
					good = []
					matches = bf.match(parentValue[1], childValue[1])

					# Get only good matches
					for m in matches:
						if m.distance < matchThreshold:
							good.append(m)
					allMatches[childKey] = good
			
			# Find value with best match
			bestKeyPoints = (None, [])
			for matchKey, matchValue in allMatches.items():
				if (len(bestKeyPoints[1]) < len(matchValue)):
					bestKeyPoints = (matchKey, matchValue)
			
			if (len(bestKeyPoints[1]) == 0):
				matchLevel +=1
				matchThreshold +=10
				continue
			

			bestMatch = kpMap[bestKeyPoints[0]]

			# Sort them in the order of their distance.
			matches = sorted(bestKeyPoints[1], key = lambda x:x.distance)
			# Stitch best matching image with parentImage
			stitchedImg = self.__stitchImages(parentValue, bestMatch, matches)
			if (len(stitchedImg) == 3):
				kpMap[parentKey] = stitchedImg
				matchLevel =0
				matchThreshold = 0
				del kpMap[bestKeyPoints[0]]
			else:
				matchLevel +=1
				#kpMap[bestKeyPoints[0]] = stitchedImg[0]
				#kpMap[parentKey] = stitchedImg[1]
			if(matchLevel > (len(kpMap)+ 25)):			 				
				matchLevel =0
				matchThreshold =15
				imagePath = os.path.join(self.resultsDirectory, "stiched_"+str(parentKey) +".jpg")				
				completed_images.append(kpMap[parentKey][2])
				#cv2.imwrite(imagePath,kpMap[parentKey][2])
				del kpMap[parentKey]
				parentKey = None
			
		# Check if results directory exist, if not create it
		

		
		return completed_images

	"""
		Description: a function setting the directory for looking for images, this will only be used by a 
			commandline interface
		@param path - The directory in unix format
	"""
	def setDirectory(self, path):
		# Get directory of test images
		self.sourceDirectory = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", path))

		# Read images and append to image array
		for file in os.listdir(self.sourceDirectory):
			if(file.find('jpg') != -1 or file.find('JPG') != -1):
				self.images.append(cv2.imread(os.path.join(self.sourceDirectory, file), cv2.IMREAD_COLOR))

	def __stitchImages(self, firstImage, secondImage, matches):
		#print(firstImage, secondImage)
		# Create stitcher and stitch images
		stitcher = cv2.createStitcher()
		orb = cv2.ORB_create(WTA_K=4, scaleFactor=1.1,patchSize=self.pSize, edgeThreshold=self.eThresh)
		bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)
		status, image = stitcher.stitch([firstImage[2], secondImage[2]])
		kp, desc = orb.detectAndCompute(image, None)

		#print(status)
		
		if (status == 0):
			# Draw first 10 matches.
			img3 = cv2.drawMatches(firstImage[2], firstImage[0], secondImage[2], secondImage[0], matches[:10], None, flags=2)
			return (kp, desc, image)
		else:
			return (firstImage, secondImage)