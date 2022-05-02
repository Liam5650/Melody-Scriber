###Copied from melody_scriber.py###
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray

# Load image
img = io.imread('./test_images/test_image_1.png')

# Convert the image to a 2D array representing pixels in grayscale from 0-1
img = rgb2gray(img) #1.0 is white, 0.0 is black

# Display the image
fig = plt.figure()
fig.set_facecolor((0.8,0.8,0.8))
plt.imshow(img, cmap='gray')
plt.title("2D Array Representation of the Image in Grayscale")
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar();

###End of copy###

# The final function will take in a music sheet img as input. It will output an
# array of bar coordinates of the sheet, where each coord is represented in the
# form [[TCTopLeft,TCBottomRight],[BCTopLeft,BCBottomRight]]. "TC" represents
# the treble clef bar, and "BC" represents the bass clef bar.

# Create a white image that is the same size as our sheet. We will color the
# line pixels found black on this image and display it to compare to the 
# original sheet and track progress. 

#### FIND HORIZONTAL LINES ####

blackThreshold = 0.2 # The float value threshold in which we evaluate as a line
horizontalThresh = 100 # The horizontal length of pixels needed to be considered a line

# Start from middle of the page, trace down from top

# At each pixel, test to see if it passes the blackThreshold. If it doesnt, 
# ignore. If it does, we need to test if it is a line

# Trace horizontally from the pixel left and right, adding traced pixels to an
# array containing their coordinates if they also pass the blackThreshold. 

# Once it has been traced left and right, check to see if the array size exceeds
# the horizontalThresh to be considered a horizontal line. 