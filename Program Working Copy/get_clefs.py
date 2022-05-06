def getClefs(img, horizontalLines):
    
    # Takes a sheet music image and an array of the horizontal lines used in
    # staffs/bars. The lines are represented as an array of individual pixel 
    # coordinates. The function returns the clef signatures of the staffs as an 
    # array of chars, for example ['t','b','t','b','t','b','t','b'], where 't'
    # represents a staff being a treble clef, and 'b' represents the bass cleff.
    # each index represents the top-down order of the staffs in the sheet. 
    
    # Import an image of a treble clef and bass clef (potentially multiple of each).
    
    # Go through the staffs sequentially (ie. separate each search into 5 horizontal
    # lines).
    
    numLines = len(horizontalLines) # The number of lines to form staffs
    numStaffs = numLines//5 # The number of complete staffs we can make

    for staffIndex in range(numStaffs):
        
        # Measure the Y distance between the top line and bottom line in the staff.
    
        topLineIndex = 5 * staffIndex # The index of the first line in the staff
        bottomLineIndex = (5 * staffIndex) + 4 # The index of the last line in the staff
        
        deltaY = horizontalLines[bottomLineIndex][0][0] - horizontalLines[topLineIndex][0][0]
        
        # Transform the image template of the clefs to match the size of the staff.
        # This defines the window size for the search (it is the dims of the scaled
        # clef image).
        
        # The size of a treble clef is usually around 150% the size of the deltaY
        
        # The size of a bass clef is usually around 80% the size of the deltaY
        
        # Define the search area of the window.
        
        # Translate the window across the sheet music image within the search area. 
        
        # At each position, check the MSE of the pixel difference of the sheet image
        # and the images of the clefs in the window.
        
        # If we surpass a setable confidence interval, mark the staff as 't' or 'b'
        # and append the result to the staff clef signature list
    
    return ['t','b','t','b','t','b','t','b']