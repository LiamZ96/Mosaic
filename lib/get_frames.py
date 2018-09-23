import cv2
import time
'''
vidFile = cv2.VideoCapture("short_clip.mp4")
nFrames = int(cv2.GetCaptureProperty( vidFile, cv2.CV_CAP_PROP_FRAME_COUNT ) )
fps = cv2.GetCaptureProperty( vidFile, cv2.CV_CAP_PROP_FPS )
waitPerFrameInMillisec = int( 1/fps * 1000/1 )
print 'Num. Frames = ', nFrames
print 'Frame Rate = ', fps, ' frames per sec'
for f in xrange( nFrames ):
    frameImg = cv.QueryFrame( vidFile )
    cv2.ShowImage( "My Video Window",  frameImg )
    cv2.WaitKey( waitPerFrameInMillisec  )
'''
def CaptureImage():
    imageName = 'DontCare.jpg' #Just a random string
    cap = cv2.VideoCapture("/home/jcarpenter/Documents/school/Mosaic/test/resources/video_sample/short_clip.mp4")
    num = 0
    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #For capture image in monochrome
        rgbImage = frame #For capture the image in RGB color space

        # Display the resulting frame
        cv2.imshow('image_viewer',rgbImage)
        #Wait to press 'q' key for capturing
        #Set the image name to the date it was captured
        if(num %2 == 0):
            imageName = ("/home/jcarpenter/Documents/school/Mosaic/img_group/" + str(time.strftime("%Y_%m_%d_%H_%M") + str(num)) + '.jpg')
        #Save the image
            cv2.imwrite(imageName, rgbImage)
        #break
        num +=1
    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()
    #Returns the captured image's name
    return imageName
CaptureImage()