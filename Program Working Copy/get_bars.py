from get_bar_components import getHorizontalLines, getVerticalLines, getClefs



def getBars(img):
    
    # Takes in a grayscale image of sheet music. Computes and returns bar objects
    # as formated in the module sheet_objects.py.
    
    # Get the components necessary to create a bar
    
    horizontalLines = getHorizontalLines(img) # An array of lines which are an array of pixel x,y coords
    verticalLines, stemLines = getVerticalLines(img, horizontalLines) # An array of lines which are an array of pixel x,y coords
    clefs = getClefs(img, horizontalLines) # An ordered array of staff clef signatures represented as 't' or 'b'
    
    # Set up the reference indices for each component 
    
    vertLineIndex = 0 # Reference to track what vert line we are processing
    vertEndIndex = 0 # Reference to track how many vert lines correspond to a set of horiz lines
    horizLineIndex = 0 # Reference to track what horiz line we are processing
    horizEndIndex = 0 # Reference to track how many horiz lines correspond to a set of vert lines
    clefIndex = 0 # Reference to track where we are in the clef signature list

    # The following three variables are set static for now but may change as
    # we improve the algorithm for more complicated cases.
    
    buffer = 5 # Set an extension buffer of vert line Y ranges in case horiz lines are off by a few pixels
    numVertLines = len(verticalLines)-2 # Subtract two as the end-of-song vert line is counted extra times
    numHorizLines = len(horizontalLines) # Reference of how many horizontal lines we have

    bars = [] # The list to store the bar objects 
    
    # Begin the search sequentially through the set of vertical lines 
    
    while vertLineIndex < numVertLines:
        
        line = verticalLines[vertLineIndex] # The vertical line to test for intersecting horizontal lines
        lineTop = line[0][0]-buffer # Extending the lower Y bounds of the line
        lineBottom = line[-1][0]+buffer # Extending the upper Y bounds of the line
        
        # Iterate sequentially through the horizontal lines, using their first x,y
        # coordinate as a reference to see if it falls within the bounds of the 
        # vertical line. Update the ending horizontal index for tracking. 
        
        while (horizEndIndex < numHorizLines and lineBottom >= horizontalLines[horizEndIndex][0][0] >= lineTop):
            
            horizEndIndex += 1
        
        # Determine how many staffs can be created from the horiz lines found
        
        numStaffs = int((horizEndIndex - horizLineIndex)/5) # Sould be divisible by 5
        
        # Iterate sequentially through the vertical lines, using their first x,y
        # coordinate as a reference. The x coord will be tested against the final
        # x coord of a horizontal line belonging to the set, keeping track of 
        # how many vertical lines there are before the x values roughly converge.
        
        xEnd = horizontalLines[horizLineIndex][-1][1] # The final x position of a horiz line belonging to the vert set
        
        while (xEnd - verticalLines[vertEndIndex][0][1] > 10) :
            
            vertEndIndex += 1
        
        # Add one to include the end line found
        
        vertEndIndex += 1
        
        # Debugging

        print("Current vertical line: " + str(vertLineIndex))
        print("Vertical Lines that belong to this set: " + str(vertEndIndex - vertLineIndex))
        print("Horizontal start index: " + str(horizLineIndex))
        print("Horizontal end index: " + str(horizEndIndex))
        print("Number of staffs: " + str(numStaffs))
        
        # Create subsets or the verticle and horizontal lines to pass to the 
        # bar creation function.
        
        vertLineSubset = verticalLines[vertLineIndex:vertEndIndex]
        horizLineSubset = horizontalLines[horizLineIndex:horizEndIndex]
        clefSubset = clefs[clefIndex:numStaffs+1]
        
        # Create the new bars for this iteration and append to the full set 
        
        newBars = createBars(vertLineSubset, horizLineSubset, clefSubset)
        bars += newBars
        
        # Update the positions of the next lines to be searched
        
        clefIndex += numStaffs
        horizLineIndex = horizEndIndex
        vertLineIndex = vertEndIndex
        
        print("\n")
        
    return bars



def createBars(verticalLines, horizontalLines, clefs):
    
    # Takes in a set of corresponding vertical lines, horizontal lines, and
    # clefs. Creates and returns a list of bar objects made from these sets. 
    # The assumption is that these have already been properly divided, and 
    # vertical and horizontal lines intersect as expected. 
    
    # Iterate through the vertical lines to create separate staffs and bars
    
    vertIndex = 0 # Reference where we are in the vertical lines
    intersections = []
    
    while vertIndex < len(verticalLines):
        
        # Start at the top of the vertical line and trace down. We want to 
        # find where this line intersects the horizontal lines. The intersection
        # point is stored for processing.
        
        vertLine = verticalLines[vertIndex] # The starting vertical line of a bar
        horizIndex = 0 # Reference where we are in the horizontal lines
        currLineIntersections = [] # the pixel coords of intersection points found
    
        for pixel in vertLine:
            
            if pixel in horizontalLines[horizIndex]:
                
                currLineIntersections.append(pixel)
                horizIndex += 1
        
        intersections.append(currLineIntersections)
        vertIndex += 1
    
    # Reorganize or organization based on the Y value instead of the X 
    # for easier segment traversal across the x axis
    
    numHorizLines = len(horizontalLines)
    horizOrderedIntersections = []
    
    # Create a list of lists where each sub list index represents a horizontal line
    # and its respective intersection points with the vertical lines
    
    for i in range(numHorizLines):
        
        horizOrderedIntersections.append([])
    
    for lineIntersection in intersections:
        
        i = 0
        
        for pixel in lineIntersection:
            
            horizOrderedIntersections[i].append(pixel)
            i += 1
    
    print(horizOrderedIntersections)
    
    # Begin traversal across each horizontal line
    
    
    
    return []