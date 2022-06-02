from get_notes import getNotes, sortStems
from get_whole_notes import getWholeNotes
from create_midi import createMidi
from sheet_objects import MusicSheet
from timeit import default_timer as timer

start = timer()

# Create music sheet object

sheet = MusicSheet()

# Set the image path

sheet.setImage('./test_images/test_image_1.png')

# Create bar objects 

sheet.createBars()

bars = sheet.barObjects

for bar in bars:
    print(bar.cornerCoords)

'''
# Create note objects

sortedStems = sortStems(bars, stemLines)
wholeNotes = getWholeNotes(img, sortedStems, bars)
notes = getNotes(img, bars, stemLines, notes = wholeNotes)

# Create and output a midi file

createMidi(notes, bars, horizontalLines)
'''
end = timer()

print("\nExecution time: " + str(round(end - start, 4)) + " seconds.")