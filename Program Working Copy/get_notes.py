from skimage import io
from skimage.color import rgb2gray
from skimage.transform import resize
from skimage.metrics import mean_squared_error

#to be used for getHorizontalLines when makes initial y guess more precise
import get_bars

def getNotes(img, bars, stemLines,stemNum = 0, barNum = 0, notes = None):
    '''
    Scans adjacent to stems of notes within a bar, and compares them to known 
    images of notes at the top and bottom along the horizontal, getting the 
    orientation of the notes before scanning along the rest of the stem for chords
    
    Parameters
    ----------
    bars : Nx2x2x2 array
        The top left and bottom right corner of both staffs of a bar of music
    stemLines : NxMx2 array
        N:number of lines; M: length of line in pixels; 2: y, x coord of each pixel
    stemNum, barNum: 
        The index of the starting bars and stems
    Return: 
    -------
    notes:
    Array ((note, time)) where the index is the bar #
    '''
    
    #cut up staff into 4 to get the height of a note-head/lane-of-staff
    #This runs into issues with a small resolution image, should base 
    #implementation off of horizontal bars returned in get_bars
    headHeight = int(((bars[0][0][0][0] - bars[0][0][1][0])/4 )*(-1)) 
    
    # Import notes for CV 
    noteSolOn = rgb2gray(io.imread('./note_images/solOn.png'))#Solid
    noteSolOff = rgb2gray(io.imread('./note_images/solOff.png'))
    noteHolOff = rgb2gray(io.imread('./note_images/holOff.png')) #Hollow
    noteHolOn = rgb2gray(io.imread('./note_images/holOn.png')) 
    
    #Scale notes for comparison against music sheet
    noteHolOff, noteHolOn, noteSolOff, noteSolOn = scaleNote(noteHolOff,headHeight
            ),scaleNote(noteHolOn,headHeight), scaleNote(noteSolOff,headHeight), scaleNote(noteSolOn,headHeight)  
    
    #arrange in a list for easier passing between functions
    CVnotes = [noteSolOff, noteHolOff, noteSolOn, noteHolOn]
    
    #If a note list is not passed to getNotes, generate a note list to record them in
    if not (notes):
        notes = generateNoteList(bars)
    
    #Sort note stems for procedural evaluation of notes and ordered recording
    sortedStems = sortStems(bars,stemLines)
    
    #Loop through stems per bar until there are no more bars 
    #could modify to have terminal bar
    for i, bar in enumerate(sortedStems):
        for j, staff in enumerate(bar):
            
            #Takes a baseline y in the relevant staff used for as an origin
            staffTop = bars[i][j][0][0]
            
            for stem in staff:
                
                #get x position of stem, top of stem, and bottom of stem
                stemX, stemTop, stemBot = stem[0][1], stem[0][0], stem[((len(stem))-1)][0]

                #check top and bottom of stem for the expected steps (music term) from top of staff 
                topSteps = (stemTop - staffTop)//(headHeight/2) + 1 # +1 is adjustment factor till implementation with get horizontal lines
                botSteps = (stemBot - staffTop)//(headHeight/2) + 1
                
                #Get the note head guessed at the top and bottom of the stem (guess[0] = 0 if presumed none)
                topGuess = headCompare(img, staffTop, topSteps, stem, CVnotes, headHeight, 1)
                botGuess = headCompare(img, staffTop, botSteps, stem, CVnotes, headHeight, -1)
                
                #If a note head is detected at one endd of the stem, 
                if topGuess[0] != 0: #check the tails on the opposite end, then record the note
                    #check tail at bottom of stem
                    time = tailCompare()
                    notes[i][j].append(((topGuess[1],stemX),time))
                
                elif botGuess[0] != 0:
                    #check tail at top of stem
                    time = tailCompare()
                    notes[i][j].append(((botGuess[1],stemX),time))
                    
    return notes
    
        
def sortStems(bars,stemLines):
    '''
    Sorts the Stems of the notes in order and organizes them within the bars and staffs
    NOTE: Could return this in bars more efficiently
    
    Parameters
    ----------
    bars : Nx2x2x2 array
        The top left and bottom right corner of both staffs of a bar of music
    stemLines : NxMx2 array
        N:number of lines; M: length of line in pixels; 2: y, x coord of each pixel
    
    Returns 
    -------
    stemSort : Lx2xNxMx2
        L: number of Bars; 2:T or B staff; N: number of lines; M: length of line; 2: y,x coords of line
    '''
    
    #Array that will be used to hold The rest of the data
    stemSort = []

    for i in range(len(bars)): #iterate through each bar
    #print('bar ', i)
        
        stemSort.append([])
            
        for j in [0,1]: #iterate through top and bottom staffs
            
            stemSort[i].append([])

            for stem in stemLines: #go through the stems to figure out which is in each bar
         
                #print('staff ', j )
                stemEnd = len(stem) -1 #terminal y of given stem
                staffTop = bars[i][j][0][0] #More decipherable names for troubleshooting
                staffBot = bars[i][j][1][0]
                barLeft = bars[i][j][0][1]
                barRight = bars[i][j][1][1]
            
                #if top of stem is higher, and bottom of stem is lower than staff bounds (Y values inverted)
                if ((((staffTop < stem[0][0]) and (staffBot > stem[0][0])
            ) or ((staffTop < stem[stemEnd][0]) and (staffBot > stem[stemEnd][0]))
            #and if x of stem exists within bar
            ) and ((barLeft < stem[0][1]) and (barRight > stem[0][1]))):
                
                        stemSort[i][j].append(stem) #add element to sorted stems
                        #NOTE: would like to remove stems as iterating through for efficiency, but interferes with iteration   
                        #stemLines.remove(stem)
                        #place_cursor(stem[1][1],stem[1][0])
    
    #must now order the stems within the bar, sort using function to pull x values from stems
    for bar in range(len(stemSort)):
        for staff in [0,1]:
            stemSort[bar][staff].sort(key=note_x)
    
    return stemSort


def note_x(staff): ###Used as key for sorting notes within a staff###
    return staff[0][1] #this returns the x coordinate of the top of the stem of the note


def scaleNote(noteImage,newHeight):
    #Scales note images down for comparison
    noteDim = noteImage.shape
    scaledNote = resize(noteImage, (newHeight, round((noteDim[1] / noteDim[0]) 
                        * newHeight)), anti_aliasing = False)
    
    return scaledNote

    
def headCompare(img, staffTop, steps, stem, CVnotes, headHeight, side):
    '''
    
    Parameters
    ----------
    staffTop : integer
        The y coordinate of the top of the staff
    steps : int
        The number of steps from the note that would be intersecting with the top line of the staff
    stem : list of tuple
        the coordinates of each pixel of of a stem line 
    CVnotes : list of imgs
        reference images of both the solid and hollow notes on lines, then both off lines
    headHeight : int
        height in pixel of the space between staff lines
    side : int
        either -1 for left or 1 for right side of stem

    Returns 
    -------
    noteGuess: int
        0, 1, 2, 3, 4 for none, solid on, hollow on, solid off, hollow off note head at specified location
    yCenter: int
        the y coordinate of the center of the note
    '''
    windowRange = 10 #the range of starting y coordinates to be used for evaluating notes
    noteGuess = 0 #The return, which will be overwritten once minimum MSE is overcome
    maxErr = 0.2 #maximum MSE to be considered a viable guess
    confidence = 1 # a default degree of MSE confidence 
    yCenter = 1 #The center y of the detected note 
    
    #Test all of the notes within the CV note list (could be made more pythonic by simply iterating through the elements of CVnotes)
    for i in range(len(CVnotes)): #This
        #idxCV = idxStart + i
        idxCV = i
        
        #in case the proper step isn't precisely found, descend the comparison window a pixel at a time
        #Should introduce an x step as well of about 2 pixels
        for yStep in range(windowRange):
            
            #Left side of stem window
            if side == -1:
                windowImg = img[yStep+staffTop+ round(steps * headHeight/2)- headHeight
                :yStep + staffTop + round(steps * headHeight/2), 
                stem[0][1]+(CVnotes[idxCV].shape[1]*side):stem[0][1]]
            
            #Right side of stem window
            else: #need to swap order of x coordinates to generate image
                windowImg = img[yStep + staffTop+ round(steps * headHeight/2)- headHeight
                :yStep + staffTop + round(steps * headHeight/2), stem[0][1]:
                stem[0][1]+(CVnotes[idxCV].shape[1]*side)]
            
            #Error assignment and comparison
            MSE = mean_squared_error(CVnotes[idxCV], windowImg)
        
            if (MSE < maxErr) & (MSE < confidence):
                noteGuess = i + 1
                yCenter = round(yStep + staffTop + round(steps * headHeight/2) - headHeight/2)
                #print(windowImg.shape, CVnotes[idxCV].shape)
                #place_cursor(stem[0][1]+(CVnotes[idxCV].shape[1]*side),yCenter)
      
    return noteGuess, yCenter
    
def tailCompare():
    # checks at opposite end of where the terminal note head is to find a tail 
    # to deduce the time of the note
    
    return 1

def generateNoteList(bars):
    notes = []
    
    for bar in bars:
        notes.append([[],[]])
    
    return notes
    

'''
if given the top left and bottom right of the staff then you'll need to 
subdivide the staff into the seperate lines along which notes will be located
then you will want to scan across each line for anomalies in a 1 pixel wide 
range. This depends on the bias of the the image - there must be exclusively 
whitespace between the lines of the staff except for symbols and notes
will also have to check above and below the staff

    # Load image
    img = io.imread('./test_images/test_image_1.png')

    # Convert the image to a 2D array representing pixels in grayscale from 0-1

    img = rgb2gray(img)


    #print(yCenter)
    # fig = plt.figure()
    # fig.set_facecolor((0.8,0.8,0.8))
    # plt.imshow(img, cmap='gray')
    # plt.title("2D Array Representation of the Image in Grayscale")
    # plt.xlabel('X')
    # plt.ylabel('Y')
    # plt.colorbar();      

    def place_cursor(x,y):
        #Generates a cursor for identifying spots on the image, purely used for testing
        thickness = 2
        size = 9
        for i in range (x-size,x+size):
            for j in range (y-thickness,y+thickness):
                img[j][i] = 0
        for j in range (y-size,y+size):
            for i in range (x-thickness,x+thickness):
                img[j][i] = 0
'''