"""Difference from running average."""

import datetime
import sys
import cv2
import numpy as np
import time
import coils
import util
'''
DEVICE   = int(sys.argv[1])
WIDTH    = int(sys.argv[2])
HEIGHT   = int(sys.argv[3])
DURATION = float(sys.argv[4])  # In seconds.
'''
DURATION = 600
# Create the OpenCV video capture object.
cap = cv2.VideoCapture("/home/jcarpenter/Documents/school/Mosaic/test/resources/video_sample/short_clip.mp4")

'''
cap.set(3, WIDTH)
cap.set(4, HEIGHT)
'''
# Create the output window.
cv2.namedWindow('diff average 1', cv2.WINDOW_NORMAL)


# Maintain accumulation of thresholded differences.
image_acc = None  

# Keep track of previous iteration's timestamp.
tstamp_prev = None  

# Monitor framerates for the given seconds past.
framerate = coils.RateTicker((1,5,10))
frame_counter=0
# Run the loop for designated amount of time.
end = datetime.datetime.now() + datetime.timedelta(seconds=DURATION)
while end > datetime.datetime.now():
    
    # Take a snapshot and mark the snapshot time.
    hello, image = cap.read()

    # Compute alpha value.
    alpha, tstamp_prev = util.getAlpha(tstamp_prev)

    # Initalize accumulation if so indicated.
    if image_acc is None:
        image_acc = np.empty(np.shape(image))
        image_acc = image

    # Compute difference.
    image_diff = cv2.absdiff(
        image_acc.astype(image.dtype),
        image,
        alpha
        )

    # Accumulate.
    '''
    hello = cv2.accumulateWeighted(
        image,
        image_acc,
        alpha,
        )
'''
    # Write the framerate on top of the image.
    fps_text = '{:.2f}, {:.2f}, {:.2f} fps'.format(*framerate.tick())
    util.writeOSD(image_diff, (fps_text,))
    if(frame_counter%20 == 0):
        flat_img = image_diff.flatten()
        sample_size = int(flat_img.size / 4)
        pix_counter=0
        for i in range(0,sample_size):
            if flat_img[i] > 10:
                pix_counter +=1
        percent_diff = (float(pix_counter) / sample_size)
        print(percent_diff)
        if(percent_diff <= .8):
            print("image captured")
            image_acc = image
            imageName = ("/home/jcarpenter/Documents/school/Mosaic/img_group/" + str(time.strftime("%Y_%m_%d_%H_%M") + str(frame_counter)) + '.jpg')
            cv2.imwrite(imageName, image)

        # Display the image.
        cv2.imshow('diff average 1', image_diff)
    

    # Allow HighGUI to process event.
    cv2.waitKey(1)
    frame_counter +=1
