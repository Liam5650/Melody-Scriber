from get_bars import getBars
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

# Create bar objects and update sheet

sheet.setBars(getBars(sheet.image))

# Create note objects and update sheet
'''
sortedStems = sortStems(bars, stemLines)
wholeNotes = getWholeNotes(img, sortedStems, bars)
notes = getNotes(img, bars, stemLines, notes = wholeNotes)

# Create and output the midi using the sheet object

createMidi(notes, bars, horizontalLines)
'''
end = timer()

print("\nExecution time: " + str(round(end - start, 4)) + " seconds.")