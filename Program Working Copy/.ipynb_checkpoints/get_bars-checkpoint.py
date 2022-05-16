import numpy as np



def getHorizontalLines(img):

    # This function takes in an image of sheet music and returns an array of 
    # lines represented as an array of pixel coordinates. These lines represent
    # the horizontal line makeup of a bar

    xDim = img.shape[1] # The X dimension of the image
    yDim = img.shape[0] # The Y dimension of the image
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
    

    return horizontalLines



def getVerticalLines(img, horizontalLines):
    
    # This function takes in an image of sheet music and an array of lines
    # represented as pixel coordinates that represent horizontal lines of a bar.
    # It outputs vertical bar lines and note stem lines in the same pixel 
    # coordinate format.
    
    # The sheet layout could differ, ie only treble clef, bass clef + treble clef,
    # so we need to try to take this into account by potentially searching multiple
    # horizontal lines to find the bars and stems. 
    
    blackThreshold = 0.4 # The float value threshold in which we evaluate as a line
    xDim = img.shape[1] # The X dimension of the image
    yDim = img.shape[0] # The Y dimension of the image
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

    return verticalLines, stemLines



def getBars(verticalLines, horizontalLines):
    
    # This function takes in two arrays of lines represented as pixel coordinates
    # that represent horizontal lines and vertical lines of a bar.
    # It returns bar coordinates in the format below.
    
    # The format of a bar will be represented as an array of pixel coordinates in the format
    # [[(TCTopLeftY,TCTopLeftX),(TCBottomRightY,TCBottomRightX)],[(BCTopLeftY,BCTopLeftX),(BCBottomRightY,BCBottomRightX)]]
    # where TC reprents the treble clef upper half and BC represents the bass clef lower half.
    
    # We are going to assume for now that a vertical line intersects 10 horizontal
    # lines, ie. a standard treble + bass clef setup
    
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
    
    return bars