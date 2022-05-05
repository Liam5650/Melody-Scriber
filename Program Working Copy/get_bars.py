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



########## FIND HORIZONTAL LINES ##########



blackThreshold = 0.4 # The float value threshold in which we evaluate as a line
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
                
                leftHalfPixels.append((yIndex, xIndex))
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



########## FIND VERTICAL LINES / STEMS ##########



# The sheet layout could differ, ie only treble clef, bass clef + treble clef,
# so we need to try to take this into account by potentially searching multiple
# horizontal lines to find the bars and stems. 

verticalLines = [] # An array of lines represented by arrays of pixel coords
verticalThresh = 75 # The vertical length of pixels needed to be considered a line
stemLines = [] # An array of lines represented by arrays of pixel coords
stemThresh = 22 # The vertical length of pixels needed to be considered a stem
numHorizLines = len(horizontalLines) # The number of horizontal lines to process
currHorizLineIndex = 0 # The horizontal line to be processed
traversedImg = np.ones((yDim, xDim)) # An array to keep track of traversed pixels

while (currHorizLineIndex) < numHorizLines:
    
    xStart = horizontalLines[currHorizLineIndex][0][1] # X position of the start of the first line
    xEnd = horizontalLines[currHorizLineIndex][-1][1] # X position of the start of the first line
    yStart = horizontalLines[currHorizLineIndex][0][0] # Y position of the first line
    xIndex = xStart # Temp variable that can be changed during the loop
    
    # Start at first horizontal line. At each pixel, test to see if the pixel below
    # or above passes the black threshold. Also check that the Y value is within the bounds
    
    while (xIndex <= xEnd):
        
        yIndex = yStart # Temp variable that can be changed during the loop
        linePixels = [] # An array to hold the pixel coords of the line
        
        # Create the top half of the line
        
        topHalf = []
        
        while (img[yIndex,xIndex] < blackThreshold) and (yIndex > 0) and (traversedImg[yIndex,xIndex] == 1.0):
            
            # If it does, store pixel and keep looping down until a line is created

            topHalf.append((yIndex,xIndex))
            yIndex-=1
            
        # Create the bottom half of the line
        
        yIndex = yStart + 1
        bottomHalf = []
        
        while (img[yIndex,xIndex] < blackThreshold) and (yIndex < yDim) and (traversedImg[yIndex,xIndex] == 1.0):
            
            # If it does, store pixel and keep looping down until a line is created
            
            bottomHalf.append((yIndex,xIndex))
            yIndex+=1
        
        # Combine the halves
        
        for coord in reversed(topHalf):
            
            linePixels.append(coord)
            
        for coord in bottomHalf:
            
            linePixels.append(coord)
            
        # Once it has been traced up to down, check to see if the array size 
        # exceeds the verticalThresh to be considered a vertical line
        
        if (len(linePixels) > verticalThresh):
            
            # If it passes, keep the line and skip a few x pixels right. Also
            # add the pixels to the traversed list so they are not considered again.
           
            for coord in linePixels:
                traversedImg[coord] = 0.0
                traversedImg[coord[0], coord[1]+1] = 0.0
                
            verticalLines.append(linePixels)
        
        # Check to see if it is long enough for a note stem instead
        
        elif (len(linePixels) < verticalThresh) and len(linePixels) > stemThresh:
            
            # If it passes, keep the line and skip a few x pixels right. Also
            # add the pixels to the traversed list so they are not considered again.
           
            for coord in linePixels:
                traversedImg[coord] = 0.0
                traversedImg[coord[0], coord[1]+1] = 0.0
                
            stemLines.append(linePixels)
        
        xIndex += 1
           
    currHorizLineIndex += 1

# Add the lines to the test image to see if they line up with the original

for line in verticalLines:
    
    for pixel in line:
        
        testImg[pixel] = 0.0

for line in stemLines:
    
    for pixel in line:
        
        testImg[pixel] = 0.0



########## GET BARS ##########



# We are going to assume for now that a vertical line intersects 10 horizontal
# lines, ie. a standard treble + bass clef setup

# The format of a bar will be represented as an array of pixel coordinates in the format
# [[(TCTopLeftY,TCTopLeftX),(TCBottomRightY,TCBottomRightX)],[(BCTopLeftY,BCTopLeftX),(BCBottomRightY,BCBottomRightX)]]
# where TC reprents the treble clef upper half and BC represents the bass clef lower half.

horizLineIndex = 9 # Keep track of where we are in the horizontal line array. Index 9 is the 10th line, so the bottom of the first bar
vertLineIndex = 0 # Keep track of where we are in the vertical line array
bars = [] # the list containing bars in the format described above

# Loop through. We don't want to process the last line as the start of a bar, 
# so we stop at the length - 2 index to skip the ending dounle line. 

while (vertLineIndex < len(verticalLines)-2):
    
    # We only need to poll the horizontal lines at an interval of 5 as we can
    # get the rest of the coordinates simply from the vertical line. We must
    # check the Y length of each vertical line to see what set of horizontal
    # lines pair with them. Skip ahead when the max Y value of a vert line exceeds
    # the current horizontal line Y value. 
    
    if (verticalLines[vertLineIndex][-1][0] > horizontalLines[horizLineIndex][0][0]):
        
        horizLineIndex += 10
    
    # We also need to check if the vertical line is at the end of a line, as
    # these must be skipped
    
    if (verticalLines[vertLineIndex][-1][0] < verticalLines[vertLineIndex+1][-1][0]):
        
        vertLineIndex += 1
        
    # Otherwise, we create the bar
    
    else:
        
        bar = [] # Stores the treble and bass clef halves of the bar coords
        
        # Handle the treble clef half of the coords
        
        TCHalf = [] 
        TCHalf.append(verticalLines[vertLineIndex][0])
        TCHalf.append((horizontalLines[horizLineIndex-5][0][0], verticalLines[vertLineIndex+1][0][1]))

        # Handle the bass clef half of the coords
        
        BCHalf = []
        BCHalf.append((horizontalLines[horizLineIndex-4][0][0],verticalLines[vertLineIndex][0][1]))
        BCHalf.append(verticalLines[vertLineIndex+1][-1])
        
        # Create the bar
        
        bar.append(TCHalf)
        bar.append(BCHalf)
        
        # Save the bar
        
        bars.append(bar)
        
        # Proceed to next vertical line
        
        vertLineIndex +=1

# Output results 

print("Number of horizontal lines found: " + str(len(horizontalLines)))
print("Number of vertical lines found:   " + str(len(verticalLines)))
print("Number of staffs created:         " + str(len(bars)))
print("Number of note stems found:       " + str(len(stemLines)))

# Display test image 
    
plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)

end = timer()
print("\n Execution time: " + str(round(end - start, 4)) + " seconds.")