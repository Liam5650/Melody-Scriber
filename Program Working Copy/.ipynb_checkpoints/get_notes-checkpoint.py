###Copied from melody_scriber.py###
import numpy as np
import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray

# Load image
img = io.imread('./test_images/test_image_1.png')

# Convert the image to a 2D array representing pixels in grayscale from 0-1
img = rgb2gray(img) #1.0 is white, 0.0 is black

###End of copy###

#Code to test filling in parts of the sheet and altering it. 
#Just simple array stuff that I<m reminding myself of

#for i in range(len(img)):
#    for j in range(0,150): #len(img[1])):
#        img[i][j] = 0

#len(img)
#len(img[1])
#img[1][1]


def place_cursor(x,y):
    #Generates a cursor for identifying spots on the image 
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

def getNotes(barCoord):
    '''
    Parameters
    ----------
    barCoord : 2x2 array
        The top left and bottom right corner of both staffs of a bar of music

    Returns 1 on full bar, 0 on failure
    -------
    scans along all lines of a sheet of music for notes or symbols. When 
    encountered it identifies that symbol and jumps across it until it detect 
    another symbol along that line

    '''
    
    
    
    print(1)

# Display the image
fig = plt.figure()
fig.set_facecolor((0.8,0.8,0.8))
plt.imshow(img, cmap='gray')
plt.title("2D Array Representation of the Image in Grayscale")
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar();