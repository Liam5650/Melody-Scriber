import numpy as np
from skimage import io
from skimage.color import rgb2gray, rgba2rgb
from skimage.transform import rescale
from skimage.metrics import mean_squared_error



def getBars(img):
    
    # This function takes in two arrays of lines represented as pixel coordinates
    # that represent horizontal lines and vertical lines of a bar.
    # It returns bar coordinates in the format below.
    
    horizontalLines = getHorizontalLines(img)
    verticalLines, stemLines = getVerticalLines(img, horizontalLines)
    clefs = getClefs(img, horizontalLines)
    
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



def getClefs(img, horizontalLines):
    
    # Takes a sheet music image and an array of the horizontal lines used in
    # staffs/bars. The lines are represented as an array of individual pixel 
    # coordinates. The function returns the clef signatures of the staffs as an 
    # array of chars, for example ['t','b','t','b','t','b','t','b'], where 't'
    # represents a staff being a treble clef, and 'b' represents the bass cleff.
    # each index represents the top-down order of the staffs in the sheet. 
    
    # Import a grayscale image of a treble clef and bass clef (potentially multiple of each).
    
    trebleImg = rgb2gray(io.imread('./clef_images/treble1.png'))
    bassImg = rgb2gray((rgba2rgb(io.imread('./clef_images/bass3.png'))))
    
    # Get the imported image dimensions
    
    trebleDims = trebleImg.shape # Tuple of the (Y,X) dims
    bassDims = bassImg.shape # Tuple of the (Y,X) dims

    # Go through the staffs sequentially (ie. separate each search into 5 horizontal
    # lines).
    
    numLines = len(horizontalLines) # The number of lines to form staffs
    numStaffs = numLines//5 # The number of complete staffs we can make
    clefs = [] # The final list of clefs to be returned
    
    for staffIndex in range(numStaffs):
        
        #print("\nCurrent staff being processed: " + str(staffIndex+1))
        
        # Measure the Y distance between the top line and bottom line in the staff.
    
        topLineIndex = 5 * staffIndex # The index of the first line in the staff
        bottomLineIndex = (5 * staffIndex) + 4 # The index of the last line in the staff
        
        deltaY = horizontalLines[bottomLineIndex][0][0] - horizontalLines[topLineIndex][0][0]
        
        # Transform the image template of the clefs to match the size of the staff.
        # This defines the window size for the search (it is the dims of the scaled
        # clef image).
        
        # The size of a treble clef is usually around 185% the size of the deltaY
        
        trebleScale = trebleDims[0]/deltaY
        trebleRescaleFactor = round((1.0 / (trebleScale/1.85)), 3)
        scaledTrebleImg = rescale(trebleImg, trebleRescaleFactor, anti_aliasing=True)
        
        # Set the bass clef to the same size
        
        bassScale = bassDims[0]/deltaY
        bassRescaleFactor = round((1.0 / (bassScale/1.85)), 3)
        scaledBassImg = rescale(bassImg, bassRescaleFactor, anti_aliasing=True)

        # Treble Clef Search Section -
        
        # Define the search area of the window. Treble clefs can variably extend
        # up to half the deltaY above the top line, so we need to check at a few
        # different Y positions. 
        
        # The start positions will represent the top left corner of the search 
        # window, with the rest of the size depending on the size of the scaled
        # clef image
        
        topLineYPos = horizontalLines[topLineIndex][0][0]
        
        yStart = topLineYPos - (deltaY//2) # The Y coord of the start of the search
        yEnd = yStart + 10
         
        xStart = horizontalLines[topLineIndex][0][1] # The X coord of the start of the search
        xEnd = xStart + 20 # The X coord of the end of the search of a row
        
        # Translate the window across the sheet music image within the search area. 
        
        yPos = yStart # Reference for the Y position of the search
        trebleConfidence = [] # A list to track the best MSE confidence interval
        
        while yPos < yEnd:
            
            xPos = xStart # Reference for the X position of the search
            
            while xPos < xEnd:
                
                # Apply a gaussian blur to the test images as well as the window for better matching.
                
                # At each position, check the MSE of the pixel difference of the sheet image
                # and the image of the clef in the window.
                
                windowImg = img[yPos:yPos+scaledTrebleImg.shape[0],xPos:xPos+scaledTrebleImg.shape[1]]
                MSE = mean_squared_error(scaledTrebleImg, windowImg)
                
                # Keep the confidence and position if it is the best so far
                
                if (trebleConfidence == []):
                    
                    trebleConfidence.append((MSE,(yPos,xPos)))
                    
                else:
                    
                    if (MSE < trebleConfidence[0][0]):
                        
                        trebleConfidence.pop()
                        trebleConfidence.append((MSE,(yPos,xPos)))
                        
                xPos += 1
                
            yPos += 1
            
        #print("Treble confidence: " + str(trebleConfidence)) 
        
        # Bass Clef Search Section -
        
        # Define the search area of the window. Bass clefs can variably extend
        # above the top line, so we need to check at a few different Y positions. 
        
        # The start positions will represent the top left corner of the search 
        # window, with the rest of the size depending on the size of the scaled
        # clef image
        
        topLineYPos = horizontalLines[topLineIndex][0][0]
        
        yStart = topLineYPos - (deltaY//2) # The Y coord of the start of the search
        yEnd = yStart + 10
         
        xStart = horizontalLines[topLineIndex][0][1] # The X coord of the start of the search
        xEnd = xStart + 20 # The X coord of the end of the search of a row
        
        # Translate the window across the sheet music image within the search area. 
        
        yPos = yStart # Reference for the Y position of the search
        bassConfidence = [] # A list to track the best MSE confidence interval
        
        while yPos < yEnd:
            
            xPos = xStart # Reference for the X position of the search
            
            while xPos < xEnd:
                
                # Apply a gaussian blur to the test images as well as the window for better matching.
                
                # At each position, check the MSE of the pixel difference of the sheet image
                # and the image of the clef in the window.
                
                windowImg = img[yPos:yPos+scaledBassImg.shape[0],xPos:xPos+scaledBassImg.shape[1]]
                MSE = mean_squared_error(scaledBassImg, windowImg)
                
                # Keep the confidence and position if it is the best so far
                
                if (bassConfidence == []):
                    
                    bassConfidence.append((MSE,(yPos,xPos)))
                    
                else:
                    
                    if (MSE < bassConfidence[0][0]):
                        
                        bassConfidence.pop()
                        bassConfidence.append((MSE,(yPos,xPos)))
                        
                xPos += 1
                
            yPos += 1
            
        #print("Bass confidence: " + str(bassConfidence)) 
        
        # Compare the confidences and append the appropriate clef
        
        if (trebleConfidence[0][0] < bassConfidence[0][0]):
            
            clefs.append('t')
            
        elif (trebleConfidence[0][0] > bassConfidence[0][0]):
            
            clefs.append('b')
    
    #print("\nExpected return: ['t', 'b', 't', 'b', 't', 'b', 't', 'b']")
    #print("Actual return:   " + str(clefs))
    
    return clefs