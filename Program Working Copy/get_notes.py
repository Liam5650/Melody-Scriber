###Copied from melody_scriber.py###
import numpy as np
import matplotlib.pyplot as plt

from skimage import io
from skimage.color import rgb2gray
import get_bars

#Code to test filling in parts of the sheet and altering it. 
#Just simple array stuff that I<m reminding myself of

#for i in range(len(img)):
#    for j in range(0,150): #len(img[1])):
#        img[i][j] = 0

#len(img)
#len(img[1])
#img[1][1]

# Load image

img = io.imread('./test_images/test_image_1.png')

# Convert the image to a 2D array representing pixels in grayscale from 0-1

img = rgb2gray(img)

def place_cursor(x,y):
    #Generates a cursor for identifying spots on the image, purely used for testing
    thickness = 3
    size = 20
    for i in range (x-size,x+size):
        for j in range (y-thickness,y+thickness):
            img[j][i] = 0
    for j in range (y-size,y+size):
        for i in range (x-thickness,x+thickness):
            img[j][i] = 0

#place_cursor(391,245)


#Top left of the second bar is located at (241,140)
#Bottom right of the top half of the bar is located at (391,165)
#Top left of the bottom half of the second bar is at (241,207)
#Bottom left of the second bar is at (391,245)

'''
if given the top left and bottom right of the staff then you'll need to 
subdivide the staff into the seperate lines along which notes will be located
then you will want to scan across each line for anomalies in a 1 pixel wide 
range. This depends on the bias of the the image - there must be exclusively 
whitespace between the lines of the staff except for symbols and notes
will also have to check above and below the staff
'''

def getNotes(bars, stemLines,stemNum = 0, barNum = 0):
    '''
    Parameters
    ----------
    bars : Nx2x2x2 array
        The top left and bottom right corner of both staffs of a bar of music
    stemLines : NxMx2 array
        N:number of lines; M: length of line in pixels; 2: y, x coord of each pixel
    stemNum, barNum: 
        The index of the starting bars and stems
    Return: Array ((note, time)) where the index is the bar #
    -------
    scans adjacent to stems of notes within a bar, and compares them to known 
    images of notes at the top and bottom along the horizontal, getting the 
    orientation of the notes before scanning along the rest of the stem for chords

    '''
    stemSort = sortStems(bars,stemLines)
    
    #cut up the staff
    noteY = (bars[0][0][0][0] - bars[0][0][1][0])/4
    
    
    #for bar in stemSort:
        
    
    return stemSort
    
    #Scale notes for comparison
    
    #Loop through stems per bar until there are no more bars 
    #could modify to have terminal bar
    
    
    
        
def sortStems(bars,stemLines):
    '''
    

    Parameters
    ----------
    bars : Nx2x2x2 array
        The top left and bottom right corner of both staffs of a bar of music
    stemLines : NxMx2 array
        N:number of lines; M: length of line in pixels; 2: y, x coord of each pixel

    Returns 
    stemSort : Lx2xNxMx2
        L: number of Bars; 2:T or B staff; N: number of lines; M: length of line; 2: y,x coords of line
    -------
    '''
    
    stemX = 0
    stemNum = 0
    stemSort = []
    
    #Sort stems into staffs
    #Get staff top and bottom y values coordinates so that stems can be sorted into them
    #NOTE could return this in bars more efficiently
    
    for i in range(len(bars)): #iterate through each bar
    #print('bar ', i)
        
        stemSort.append([])
            
        for j in [0,1]: #iterate through top and bottom staffs
            
            stemSort[i].append([])

            for stem in stemLines: #go through the stems to figure out which is in each bar
         
                #print('staff ', j )
                stemEnd = len(stem) -1 #terminal y of given stem
                staffTop = bars[i][j][0][0]
                staffBot = bars[i][j][1][0]
                barLeft = bars[i][j][0][1]
                barRight = bars[i][j][1][1]
                # print('stafftop' ,staffTop, 'staffbot' ,staffBot, 'barLeft', barLeft, 'barRight',barRight)
                # print('stemtop',stem[0][0], 'stembot',stem[stemEnd][0], 'stemX', stem[0][1])
            
                #if top of stem is higher, and bottom of stem is lower than staff bounds (Y values inverted)
                if ((((staffTop < stem[0][0]) and (staffBot > stem[0][0])
            ) or ((staffTop < stem[stemEnd][0]) and (staffBot > stem[stemEnd][0]))
            #and if x of stem exists within bar
            ) and ((barLeft < stem[0][1]) and (barRight > stem[0][1]))):
                
                        stemSort[i][j].append([stem]) #add element to sorted stems
                        #NOTE: would like to remove stems as iterating through for efficiency, but interferes with iteration   
                        #stemLines.remove(stem)
                        #place_cursor(stem[1][1],stem[1][0])
    
    #must now order the stems within the bar, sort using function to pull x values
    for bar in range(len(stemSort)):
        for staff in [0,1]:
            stemSort[bar][staff].sort(key=note_x)
    
    
    return stemSort

def note_x(staff): #Used as key for sorting notes within a staff
    return staff[0][0][1] #this returns the x coordinate of the top of the stem of the note

'''        
    for bar in bars: 
        #go till stem index is out of bar check top and bottom of the line given
        for stem in stemLines:

            if (stem[0][1] > bar[1][1][1] #the next stem is on a new bar
                )  or (stemX > stem[0][1]) : #we've wrapped the page
                
                stemX = stem[0][1]
                break
            
            
            
            stemNum += 1
            print(2)
        print(1)
    
    return stemSort 
 '''       
def headCompare():
    
    #import hollow and solid note heads NOTE: may need to distinguish more 
    #effectively given that notes aren't identical in appearence given which 
    #side of the stem they,re found on
    
    holOn = rgb2gray(io.imread('./note_images/holOn.png'))
    holOff = rgb2gray(io.imread('./note_images/holOff.png'))
    solOff = rgb2gray(io.imread('./note_images/solOn.png'))
    
def tailCompare():
    return
    # checks at opposite end of where the terminal note head is to find a tail 
    # to deduce the time of the note