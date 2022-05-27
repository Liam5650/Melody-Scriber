import matplotlib.pyplot as plt
from skimage import io
from skimage.color import rgb2gray
from get_bars import getHorizontalLines, getVerticalLines, getBars
from get_clefs import getClefs
from get_notes import getNotes, sortStems
from get_whole_notes import getWholeNotes
from create_midi import createMidi
from timeit import default_timer as timer

start = timer()

# Load image

img = io.imread('./test_images/test_image_1.png')

# Convert the image to a 2D array representing pixels in grayscale from 0-1

img = rgb2gray(img)

# Display the image

fig = plt.figure()
fig.set_facecolor((0.8,0.8,0.8))
plt.imshow(img, cmap='gray')
plt.title("2D Array Representation of the Image in Grayscale")
plt.xlabel('X')
plt.ylabel('Y')
plt.colorbar();

# Get components

horizontalLines = getHorizontalLines(img)
verticalLines, stemLines = getVerticalLines(img, horizontalLines)
bars = getBars(verticalLines, horizontalLines)

#print("Number of horizontal lines found: " + str(len(horizontalLines)))
#print("Number of vertical lines found:   " + str(len(verticalLines)))
#print("Number of staffs created:         " + str(len(bars)))
#print("Number of note stems found:       " + str(len(stemLines)))

clefs = getClefs(img, horizontalLines)

#print("\nClef signature by staff index:    " + str(clefs))

sortedStems = sortStems(bars, stemLines)

#print(sortedStems[0])

wholeNotes = getWholeNotes(img, sortedStems, bars)

notes = getNotes(img, bars, stemLines, notes = wholeNotes)
print(notes[0])

createMidi(notes, bars, horizontalLines) # This writes a file in the "midi_output" folder

end = timer()
print("\nExecution time: " + str(round(end - start, 4)) + " seconds.")