from get_bar_components import getHorizontalLines, getVerticalLines, getClefs



class Bar:
      
    def __init__(self, staffObjects, verticalLines, timeSig=(4,4)):
        
        self.timeSig = timeSig
        self.staffObjects = staffObjects
        self.vertLines = verticalLines
        self.cornerCoords = [staffObjects[0].cornerCoords[0], staffObjects[-1].cornerCoords[1]]
        
class Staff:
    
    noteStems = []
    noteObjects = []
    
    def __init__(self, clefSig, horizLines, keySig = ''):
        
        self.clefSig = clefSig
        self.keySig = keySig
        self.horizLines = horizLines
        self.cornerCoords = [horizLines[0][0], horizLines[-1][-1]]



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
        
        '''
        print("Current vertical line: " + str(vertLineIndex))
        print("Vertical Lines that belong to this set: " + str(vertEndIndex - vertLineIndex))
        print("Horizontal start index: " + str(horizLineIndex))
        print("Horizontal end index: " + str(horizEndIndex))
        print("Number of staffs: " + str(numStaffs))
        print("\n")
        '''
        
        # Create subsets or the verticle and horizontal lines to pass to the 
        # bar creation function.
        
        vertLineSubset = verticalLines[vertLineIndex:vertEndIndex]
        horizLineSubset = horizontalLines[horizLineIndex:horizEndIndex]
        clefSubset = clefs[clefIndex:clefIndex+numStaffs]

        # Create the new bars for this iteration and append to the full set 
        
        newBars = createBars(vertLineSubset, horizLineSubset, clefSubset)
        bars += newBars
        
        # Update the positions of the next lines to be searched
        
        clefIndex += numStaffs
        horizLineIndex = horizEndIndex
        vertLineIndex = vertEndIndex
        
    return bars



def createBars(verticalLines, horizontalLines, clefs):
    
    # Takes in a set of corresponding vertical lines, horizontal lines, and
    # clefs. Creates and returns a list of bar objects made from these sets. 
    # The assumption is that these have already been properly divided, and 
    # vertical and horizontal lines intersect as expected. 
    
    # Iterate through the horizontal lines to create separate staffs and bars
    
    horizIndex = 0 # Reference where we are in the horizontal lines
    lineSegments = [] # A list to store the horizontal line segments found
    
    while horizIndex < len(horizontalLines):
        
        # Start at the left side of the horizontal line and trace right, keeping 
        # track of traversed pixels. When we find an intersection point with a 
        # vertical line, we save the traversed line segment to be stored in a bar 
        # later. 
        
        horizLine = horizontalLines[horizIndex] # The starting horizontal line of a bar
        vertIndex = 1 # Reference where we are in the vertical lines. Skip the first line as it doesnt make a segment on its own
        currLineSegments = [] # the pixel coords of intersection points found for the current horizontal line
        numVertLines = len(verticalLines) # Used to make sure we do not check an invalid index
        pixelsTraversed = [] # A list of pixels we have traversed in the current segment
        
        for pixel in horizLine:
            
            if vertIndex < numVertLines and pixel in verticalLines[vertIndex]:
                
                currLineSegments.append(pixelsTraversed)
                pixelsTraversed = []
                vertIndex += 1
                
            else:
                
                pixelsTraversed.append(pixel)
                
        # Append horizontal line traversal results to the main list and continue
        
        lineSegments.append(currLineSegments)
        horizIndex += 1
        
    # Reorganize the segments so they are separated by bar
    
    # Handle the horizontal lines, ie 10 segments per bar
    
    numBars = len(verticalLines)-1
    organizedHorizSegments = []
    
    for i in range(numBars):
        
        organizedHorizSegments.append([])
    
    i = 0
    
    for horizLineSet in lineSegments:
        
        for segment in horizLineSet:
            
            organizedHorizSegments[i].append(segment)
            
            if i == numBars-1:
                
                i = 0
                
            else:
                
                i += 1
    
    # Handle the verticle lines, ie two segments per bar
    
    organizedVertSegments = []
    
    for i in range(numBars):
        
        organizedVertSegments.append([verticalLines[i], verticalLines[i+1]])

    # Create the bars from the segments
    
    bars = []
    
    for i in range(numBars):
        
        # Create the separate staff objects of the bar
        staffs = []
        
        for j in range(len(clefs)):
            
            staffClefSig = clefs[j]
            staffHorizLines = organizedHorizSegments[i][j*5:5+(j*5)]
            staff = Staff(staffClefSig, staffHorizLines)
            staffs.append(staff)
            
        bar = Bar(staffs, organizedVertSegments[i])
        bars.append(bar)
            
    return bars