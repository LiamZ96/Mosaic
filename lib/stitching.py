import cv2
import os
from matplotlib import pyplot as plt
import time
import sys
from PIL import Image
import shutil
import multiprocessing as mp

"""
        Description: a class to deal with stitching images together and handling overlap of the images.
"""
class Stitching: 
	def __init__(self):
		self.images = []
		self.sourceDirectory = ""
		#pSize = 800
		#eThresh = 0
		self.resultsDirectory =""
		#wtak = 0
		self.results = []
		

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
	def collage(self,temp_path,file_name):
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
		
		new_im.save(self.resultsDirectory + file_name)
		shutil.rmtree(temp_path)


	def twoRoundStitch(self, sourceDirectory, resultsDirectory):
		output = mp.Queue()
		#first we run the two rounds with WTA_K set to 4
		self.resultsDirectory = resultsDirectory
		self.setDirectory(sourceDirectory)
		'''
		wtak = 4
		completed_images = []
		print("begin first round")
		temp_dir = str(int(round(time.time())))
		temp_dir = temp_dir + "/"
		os.makedirs(temp_dir)
		pSize = 1000
		eThresh = 0
		first_round = []
		#first_round = self.stitchUnorderedImages(4,1000,0,self.images)
		'''
	
		pl = mp.Pool(processes=2)
		first_round = pl.starmap(self.stitchUnorderedImages, [(4,1000,0,self.images), (2, 1000, 0, self.images)])	
		'''
		processes = [mp.Process(target = self.stitchUnorderedImages, args =(4,1000,0,self.images, 0)), mp.Process(target=self.stitchUnorderedImages, args=(2, 1000, 0, self.images, 1))]
		for p in processes:
			p.start()
		for p in processes:
			p.join()
		'''
		final_images = pl.starmap(self.stitchUnorderedImages, [(4, 200, 200, first_round[0]), (2, 200, 200, first_round[1])])
		
		'''
		processes = [mp.Process(target = self.stitchUnorderedImages, args =(4,200,200,self.results[0],2)), mp.Process(target=self.stitchUnorderedImages, args=(2, 200, 200, self.results[1],3))]
		for p in processes:
			p.start()
		for p in processes:
			p.join()
		'''	


		'''
		pSize=200
		eThresh=200
		print("begin second round")
		#final_images = self.stitchUnorderedImages(4, 200,200,first_round)
		'''
		temp_dir = str(int(round(time.time())))
		temp_dir = temp_dir + "/"		
		os.makedirs(temp_dir)

		img_number =0
		for img in final_images[0]:
			cv2.imwrite(str(temp_dir) + str(img_number) + ".jpg",img)
			img_number +=1
		self.collage(temp_dir,"resultA.jpg")

		#now we run two round again but with WTA_K set to 2
		#self.setDirectory(self.sourceDirectory)
		'''
		wtak = 2
		completed_images = []
		print("begin first round")
		temp_dir = str(int(round(time.time())))
		temp_dir = temp_dir + "/"
		os.makedirs(temp_dir)
		pSize = 1000
		eThresh = 0
		first_round = []
		first_round = self.stitchUnorderedImages(2, 1000, 0, self.images)
		#print(len(first_round))
		self.images = first_round
		pSize=200
		eThresh=200
		print("begin second round")
		final_images = self.stitchUnorderedImages(2, 200, 200, first_round)
		'''
		temp_dir = str(int(round(time.time())))
		temp_dir = temp_dir + "/"		
		os.makedirs(temp_dir)
		
		img_number =0
		for img in final_images[1]:
			cv2.imwrite(str(temp_dir) + str(img_number) + ".jpg",img)
			img_number +=1
		self.collage(temp_dir,"resultB.jpg")

	def stitchUnorderedImages(self, wtak, pSize, eThresh, images):
		#if not os.path.exists(self.resultsDirectory):
		#	os.makedirs(self.resultsDirectory)

		orb = cv2.ORB_create(WTA_K=wtak, scaleFactor=1.1,patchSize=pSize,edgeThreshold=eThresh)
		if(wtak == 4):
			bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)
		else:
			bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
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
			stitchedImg = self.__stitchImages(parentValue, bestMatch, matches, wtak, pSize, eThresh)
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

	def setResultsDirectory(self,path):
		self.resultsDirectory = path

	def __stitchImages(self, firstImage, secondImage, matches, wtak, pSize, eThresh):
		#print(firstImage, secondImage)
		# Create stitcher and stitch images
		stitcher = cv2.createStitcher()
		orb = cv2.ORB_create(WTA_K=wtak, scaleFactor=1.1,patchSize=pSize, edgeThreshold=eThresh)
		if(wtak == 4):
			bf = cv2.BFMatcher(cv2.NORM_HAMMING2, crossCheck=True)
		else:
			bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
		try:
			status, image = stitcher.stitch([firstImage[2], secondImage[2]])
		except:
			return(firstImage,secondImage)
		kp, desc = orb.detectAndCompute(image, None)

		#print(status)
		
		if (status == 0):
			# Draw first 10 matches.
			img3 = cv2.drawMatches(firstImage[2], firstImage[0], secondImage[2], secondImage[0], matches[:10], None, flags=2)
			return (kp, desc, image)
		else:
			return (firstImage, secondImage)
