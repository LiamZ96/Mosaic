import cv2

"""
    Description: a class to deal with stitching images together and handling overlap of the images.
"""
class VideoConvert: 
    def __init__(self):
        pass 
    
    """
        Description: a function to convert a video file into images
        @param videoPath - the path to a video file
        @return an array of images from the video file
    """
    def videoToImages(self,videoPath):
        vidFile = cv.CaptureFromFile(videoPath)
        nFrames = int(  cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FRAME_COUNT ) )
        fps = cv.GetCaptureProperty( vidFile, cv.CV_CAP_PROP_FPS )
        waitPerFrameInMillisec = int( 1/fps * 1000/1 )

        print 'Num. Frames = ', nFrames
        print 'Frame Rate = ', fps, ' frames per sec'

        for f in xrange( nFrames ):
            frameImg = cv.QueryFrame( vidFile )
            cv.ShowImage( "My Video Window",  frameImg )
            cv.WaitKey( waitPerFrameInMillisec  )
        pass
        