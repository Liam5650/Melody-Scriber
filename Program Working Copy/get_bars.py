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
  
# Display test image 

plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)



########## FIND VERTICAL LINES ##########



# The sheet layout could differ, ie only treble clef, bass clef + treble clef,
# so we need to try to take this into account by potentially searching multiple
# horizontal lines to find the bars. The number of bars a found vertical line
# intersects will be used to determine this and skip horizontal lines in the 
# searching process that have already been intersected.

verticalLines = [] # An array of lines represented by arrays of pixel coords
verticalThresh = 75 # The vertical length of pixels needed to be considered a line
numHorizLines = len(horizontalLines) # The number of horizontal lines to process
currHorizLineIndex = 0 # The horizontal line to be processed
skipPixels = 8 # The number of pixels to skip in the X search to avoid counting the same line twice

while (currHorizLineIndex) < numHorizLines:
    
    xStart = horizontalLines[currHorizLineIndex][0][1] # X position of the start of the first line
    xEnd = horizontalLines[currHorizLineIndex][-1][1] # X position of the start of the first line
    yStart = horizontalLines[currHorizLineIndex][0][0] # Y position of the first line
    xIndex = xStart # Temp variable that can be changed during the loop
    
    # Start at first horizontal line. At each pixel, test to see if the pixel below
    # passes the black threshold. Also check that the Y value is within the bounds
    
    while (xIndex <= xEnd):
        
        yIndex = yStart # Temp variable that can be changed during the loop
        linePixels = [] # An array to hold the pixel coords of the line
        
        while (img[yIndex,xIndex] < blackThreshold) and (yIndex < yDim):
            
            # If it does, store pixel and keep looping down until a line is created
            
            linePixels.append((yIndex,xIndex))
            yIndex+=1
            
        # Once it has been traced up to down, check to see if the array size 
        # exceeds the verticalThresh to be considered a vertical line
        
        if (len(linePixels) > verticalThresh):
            
            # If it passes, keep the line and skip a few x pixels right
            
            verticalLines.append(linePixels)
            xIndex += skipPixels

        # If it doesn't, start over at the next pixel in the line
        
        else:
        
            xIndex += 1
        
    # After the first line has been fully explored, if there is a vertical line found, 
    # test to see how many horizontal lines the vertical line passes through.
    # This will create a bar, and we can ignore doing the horizontal search
    # through any of the intersected lines
        
    # If we have foudn a vertical line, we need to test it

    if (len(linePixels) > 0):
        
        # We skip ahead through the Horizontal lines as long as the Y value of the 
        # found vertical line is greater than that of the horizontal line

        while (currHorizLineIndex < numHorizLines) and (linePixels[-1][0] >= horizontalLines[currHorizLineIndex][0][0]):

            currHorizLineIndex += 1
    
    # If we didnt find a vertical line, start again at the next horizontal line
    
    else:
        
        currHorizLineIndex += 1

# Add the lines to the test image to see if they line up with the original

for line in verticalLines:
    
    for pixel in line:
        
        testImg[pixel] = 0.0
  
# Display test image 

plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)



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
# so we stop at the length - 1 index. 

while (vertLineIndex < len(verticalLines)-1):
    
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



########## FIND NOTE STEMS ##########



# Trace through horizontal lines, and trace any through any intersected
# vertical line up and down. Ignore lines that have already been traversed. 

traversedImg = np.ones((yDim, xDim)) # The white canvas serving as the test image

# Add the traversed vertical lines to the array

for line in verticalLines:
    
    for pixel in line:
        
        traversedImg[pixel] = 0.0

noteStems = [] # An array of lines represented by arrays of pixel coords
stemThresh = 22 # The vertical length of pixels needed to be considered a line
numHorizLines = len(horizontalLines) # The number of horizontal lines to process
currHorizLineIndex = 0 # The horizontal line to be processed
skipPixels = 3 # The number of pixels to skip in the X search to avoid counting the same line twice

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
        
        # Top Half 
        
        topHalf = []
        
        while (img[yIndex,xIndex] < blackThreshold) and (yIndex > 0) and (traversedImg[yIndex,xIndex] == 1.0):
            
            # If it does, store pixel and keep looping down until a line is created
            
            traversedImg[yIndex,xIndex] = 0.0
            topHalf.append((yIndex,xIndex))
            yIndex-=1
            
        # Bottom Half 
        
        yIndex = yStart + 1
        bottomHalf = []
        
        while (img[yIndex,xIndex] < blackThreshold) and (yIndex < yDim) and (traversedImg[yIndex,xIndex] == 1.0):
            
            # If it does, store pixel and keep looping down until a line is created
            
            traversedImg[yIndex,xIndex] = 0.0
            bottomHalf.append((yIndex,xIndex))
            yIndex+=1
        
        # Combine the halves
        
        for coord in reversed(topHalf):
            
            linePixels.append(coord)
            
        for coord in bottomHalf:
            
            linePixels.append(coord)
            
        # Once it has been traced up to down, check to see if the array size 
        # exceeds the stemThresh to be considered a stem
        
        if (len(linePixels) > stemThresh) and (len(linePixels) < verticalThresh):
            
            # If it passes, keep the line and skip a few x pixels right
            
            noteStems.append(linePixels)
            xIndex += skipPixels

        # If it doesn't, start over at the next pixel in the line
        
        else:
        
            xIndex += 1
        
        
    currHorizLineIndex += 1

# Add the lines to the test image to see if they line up with the original

for line in noteStems:
    
    for pixel in line:
        
        testImg[pixel] = 0.0

# should be 66, some are getting double counted due to being 2 pixels wide

print(len(noteStems))

# Display test image 
    
plt.imshow(testImg, cmap='gray', vmin=0,vmax=1)

end = timer()
print("\n Execution time: " + str(round(end - start, 4)) + " seconds.")