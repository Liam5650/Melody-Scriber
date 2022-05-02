###Copied from melody_scriber.py###

import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
from timeit import default_timer as timer

start = timer()

# Load image

img = io.imread('./test_images/test_image_1.png')

# Convert the image to a 2D array representing pixels in grayscale from 0-1

img = rgb2gray(img) #1.0 is white, 0.0 is black

"""
# Display the image

fig = plt.figure()
fig.set_facecolor((0.8,0.8,0.8))
plt.imshow(img, cmap='gray')
plt.title("2D Array Representation of the Image in Grayscale")
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar();
"""

###End of copy###

# The final function will take in a music sheet img as input. It will output an
# array of bar coordinates of the sheet, where each coord is represented in the
# form [[TCTopLeft,TCBottomRight],[BCTopLeft,BCBottomRight]]. "TC" represents
# the treble clef bar, and "BC" represents the bass clef bar.

# Create a white image that is the same size as our sheet. We will color the
# line pixels found black on this image and display it to compare to the 
# original sheet and track progress. 

xDim = img.shape[1] # The X dimension of the image
yDim = img.shape[0] # The Y dimension of the image

testImg = np.ones((yDim, xDim)) # The white canvas serving as the test image

"""
# Display test image 

plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)
"""

#### FIND HORIZONTAL LINES ####

blackThreshold = 0.2 # The float value threshold in which we evaluate as a line
horizontalThresh = 100 # The horizontal length of pixels needed to be considered a line

# Start from middle of the page, trace down from top

horizontalLines = [] # An array of lines represented by arrays of pixel coords
yIndex = 0 # Start from top
skipPixels = 3 # The number of pixels to skip in the Y search to avoid counting the same line twice

while (yIndex < yDim):

    xIndex = xDim//2 # Begin search from the middle
    
    # At each pixel, test to see if it passes the blackThreshold. If it doesnt, 
    # ignore. If it does, we need to test if it is a line
    
    if (img[yIndex,xIndex] < blackThreshold):
        
        
        # Trace horizontally from the pixel left and right, adding traced pixels to an
        # array containing their coordinates if they also pass the blackThreshold. 
        
        linePixels = [] # An array to hold the pixel coords of the line
        
        # Right-half loop
        
        rightHalfPixels = [] # Store the right half
        
        while xIndex < xDim:
            
            if (img[yIndex,xIndex] < blackThreshold):
                
                rightHalfPixels.append((yIndex, xIndex))
                xIndex +=1
            
            else:
                
                break
                
        # Left-half loop
        
        leftHalfPixels = [] # Store the left half
        
        xIndex = xDim//2 - 1 # Reset x position 1 pixel left of center
        
        while xIndex >= 0:
            
            if (img[yIndex,xIndex] < blackThreshold):
                
                rightHalfPixels.append((yIndex, xIndex))
                xIndex -=1
            
            else:
                
                break
        
        # Combine the halves
        
        for coord in reversed(leftHalfPixels):
            
            linePixels.append(coord)
            
        for coord in rightHalfPixels:
            
            linePixels.append(coord)

        # Once it has been traced left and right, check to see if the array size exceeds
        # the horizontalThresh to be considered a horizontal line
        
        if (len(linePixels) > horizontalThresh):
            
            # If it passes, keep the line and skip a few Y pixels down
            
            horizontalLines.append(linePixels)
            yIndex += skipPixels

    # Continue loop
    
    yIndex += 1;


# Add the lines to the test image to see if they line up with the original

for line in horizontalLines:
    
    for pixel in line:
        
        testImg[pixel] = 0.0
  
# Display test image 

plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)

    
end = timer()
print(end - start)