from skimage import io
from skimage.color import rgb2gray
from skimage.transform import rescale
from skimage.metrics import mean_squared_error

def getWholeNotes(img, stemList, bars):
    
    # Takes in the image of sheet music to process as well as a list of the sorted
    # note stems by staff/bar as input. Also takes in the coords of the bars.
    # Returns the list after adding the centroid position of the whole notes 
    # found as well as length in beats. 
    
    # Import a grayscale image of a whole note
    
    wholeNoteImg = rgb2gray(io.imread('./note_images/whole1.png'))
    
    # Get the imported image dimensions
    
    noteDims = wholeNoteImg.shape # Tuple of the (Y,X) dims
    
    # Process each bar
    
    notes = [] # an array to hold the final notes discovered in the same format of the stemlist
    barIndex = 0 # keep track of what bar we are currently processing
    
    for bar in bars:
        
        barNotes = [[],[]] # Holds a list of the notes in the treble and bass staffs respectively
        
        # For each bar, check to see if the top or bottom stem is empty. 
        # Set the staff index to be searched, the top and bottom Y coordinates of
        # that staff, as well as the x position of the first note as a reference
        # for the search area to be checked later for the whole note.
        
        if (len(stemList[barIndex][0])>0 and stemList[barIndex][1] == []):
            
            staffIndex = 1 # store reference to know where to store the note later in the notes list
            xPos = stemList[barIndex][0][0][0][1] # the reference x position for our search
            staffTop = bar[staffIndex][0][0] # the top Y position of the staff
            staffBottom = bar[staffIndex][1][0] # the bottom Y position of the staff   
            
        elif (len(stemList[barIndex][1])>0 and stemList[barIndex][0] == []):
              
            staffIndex = 0 # store reference to know where to store the note later in the notes list
            xPos = stemList[barIndex][1][0][0][1] # the reference x position for our search
            staffTop = bar[staffIndex][0][0] # the top Y position of the staff
            staffBottom = bar[staffIndex][1][0] # the bottom Y position of the staff         
              
        else:
            
            # No reference point found, we need to search the top and bottom
            # Implement later if necessary. For now, just append an empty list of notes
            # for the bar. 
            
            notes.append(barNotes)
            barIndex += 1
            continue
        
        # Begin the search for a whole note. 
        
        # Define the upper and lower Y bounds of the search. This can extend a bit 
        # further than the staff bounds (ex middle c), so we add a quarter distance to make sure
        
        yLength = staffBottom-staffTop # the y length of the staff
        yStart = staffTop - (yLength//4) # where to start the Y search of the staff
        yEnd = staffBottom + (yLength//4) # where to end the Y search of the staff
        
        # Scale the size of our reference whole note image so that it matches
        # better to the image. The scale is 1/4 the yLength of a staff.
        
        noteScale = noteDims[0]/yLength
        noteRescaleFactor = round((1.0 / (noteScale/0.25)), 3)
        scaledNoteImg = rescale(wholeNoteImg, noteRescaleFactor, anti_aliasing=True)

        # Trace the empty staff up to down using the Y coordinates of the staff as a reference.
        
        yPos = yStart # reference to use for the current Y pos to be checked
        
        # The xPos is actually offset from the stem line to the left, move the reference
        # point accordingly
        
        xStart = xPos - scaledNoteImg.shape[1] # Start the search offset 1 note distance on the X axis
        xEnd = xStart + 10 # where to end the X search of the staff
        
        noteConfidence = [] # A list to track the best MSE confidence interval
        
        while yPos < yEnd:
            
            xPos = xStart # Reference for the X position of the search
            
            while xPos < xEnd:
                
                # Apply a gaussian blur to the test images as well as the window for better matching.
                
                # At each position, check the MSE of the pixel difference of the sheet image
                # and the image of the clef in the window.
                
                windowImg = img[yPos:yPos+scaledNoteImg.shape[0],xPos:xPos+scaledNoteImg.shape[1]]
                MSE = mean_squared_error(scaledNoteImg, windowImg)
                
                # Keep the confidence and position if it is the best so far
                
                if (noteConfidence == []):
                    
                    noteConfidence.append((MSE,(yPos,xPos)))
                    
                else:
                    
                    if (MSE < noteConfidence[0][0]):
                        
                        noteConfidence[0] = (MSE,(yPos,xPos))
                
                xPos += 1
                    
            yPos +=1
            
            # Skip a certain distance based on the distance between horizontal lines to be more efficient.
            # Immplement later if necessary.
        
        # Store the center position and note length to the notes array
        
        if (noteConfidence != []):

            center = (noteConfidence[0][1][0]+(scaledNoteImg.shape[0]//2), noteConfidence[0][1][1]+(scaledNoteImg.shape[1]//2))
            barNotes[staffIndex].append((center,4))
        
        barIndex += 1
        
        notes.append(barNotes)
    
    return notes