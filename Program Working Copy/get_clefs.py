from skimage import io
from skimage.color import rgb2gray, rgba2rgb
from skimage.transform import rescale
from skimage.metrics import mean_squared_error

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
        
        print("\nCurrent staff being processed: " + str(staffIndex+1))
        
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
            
        print("Treble confidence: " + str(trebleConfidence)) 
        
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
            
        print("Bass confidence: " + str(bassConfidence)) 
        
        # Compare the confidences and append the appropriate clef
        
        if (trebleConfidence[0][0] < bassConfidence[0][0]):
            
            clefs.append('t')
            
        elif (trebleConfidence[0][0] > bassConfidence[0][0]):
            
            clefs.append('b')
    
    print("\nExpected return: ['t', 'b', 't', 'b', 't', 'b', 't', 'b']")
    print("Actual return:   " + str(clefs))
    
    return clefs