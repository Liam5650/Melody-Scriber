from midiutil import MIDIFile


def createMidi(notes, bars, horizontalLines):
    
    '''
    Takes in a list of note coords and lengths as well as bar coords, and 
    outputs a midi file to play the song. The horizontal lines data may be
    helpful once we get to an actual img but is unused for now. 
    '''
    
    # Set up the default params for the midiutil module
    tempo = 144
    volume = 100
    track = 0
    time = 0
    MyMIDI = MIDIFile(1)
    MyMIDI.addTempo(track,time, tempo)
    
    # Process the notes to a format readable by the midiutil
    
    notes = ProcessNotes(notes, bars, horizontalLines)
    
    # Go through the set of treble notes and bass notes and separate based on channel
    
    trebleNotes = notes[0]
    trebleChannel = 0

    for note in trebleNotes:
        MyMIDI.addNote(track, trebleChannel, note[0], time, note[1], volume)
        time = time + note[1]

    bassNotes = notes[1]
    bassChannel  = 1
    time = 0
    
    for note in bassNotes:
        MyMIDI.addNote(track, bassChannel, note[0], time, note[1], volume)
        time = time + note[1]
 
    # Write the file
 
    with open("./midi_output/output.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
        
    
def ProcessNotes(notes, bars, horizontalLines):
    
    '''
    Takes in a set of note coords and durations, as well as bar coords 
    (horizontalLines is unused for now). Returns the list of the processed notes
    to be used by the miniutil module to create the midi file. The format is a list
    of notes, where each note is a tuple containing the integer midi pitch number as 
    well as the integer note duration. 
    '''
    
    processedNotes = [[],[]] # Separate notes based on treble and bass channels
    barIndex = 0 # The bar of notes to be processed
    
    
    # Iterate through every set of bars and their respective notes
    
    while barIndex < len(bars):
        
        trebleCoords = bars[barIndex][0]
        trebleNotes = notes[barIndex][0]
        
        # Send each note and staff coords to the getPitch func for further processing
        
        for note in trebleNotes:
            
            noteCoord = note[0]
            notePitch = getPitch(noteCoord, trebleCoords, 0)
            noteDuration = note[1]
            noteChannel = 0
            processedNotes[noteChannel].append((notePitch, noteDuration))
        
        bassCoords = bars[barIndex][1]
        bassNotes = notes[barIndex][1]
        
        for note in bassNotes:
            
            noteCoord = note[0]
            notePitch = getPitch(noteCoord, bassCoords, 1)
            noteDuration = note[1]
            noteChannel = 1
            processedNotes[noteChannel].append((notePitch, noteDuration))
        
        barIndex += 1
        
    return processedNotes
 
    
def getPitch(noteCoord, staffCoords, clefSignature=0):
    
    '''
    Takes a note coord, staff coords, and clef signature as input. Uses the note coord
    within the specified type of staff in order to compute the integer pitch representation
    needed by the midiutil module. Outputs a note as a tuple containing the integer pitch
    as well as the integer duration of the note. 
    '''
    
    # Set up parameters for the note positional search in the staff
    
    noteY = noteCoord[0] # The notes Y pos
    staffTop = staffCoords[0][0] # The top of the staff
    staffBottom = staffCoords[1][0] # The bottom of the staff
    deltaY = staffBottom - staffTop # The Y length of the staff
    lineDistance = deltaY/4 # The approximate horizontal line distance within the staff
    staffExtendedTop = staffTop - (lineDistance*2) # Extend the staff to take very high notes into account
    staffExtendedBottom = staffBottom + (lineDistance*2) # Extend the staff to take very low notes into account
    stepSize = lineDistance/2 # Set the rough step size of a note
    
    # Begin the search through the Y axis where the note is located
    
    yPos = staffExtendedBottom # Start at the "bottom" (technically highest Y) and trace up
    stepIndex = 0 # Track how many steps we have taken
    
    while stepIndex <= 16:
        
        # If our yPos is very close to the note, we are at the right step and break out
        if yPos - noteY < 2:
            break
        
        yPos -= stepSize
        stepIndex += 1
    
    # Map the stepIndex to a list of pitches, depending on the specified clef signature
    
    if clefSignature == 0:
        trebleMap = [57, 59, 60, 62, 64, 65, 67, 69, 71, 72, 74, 76, 77, 79, 81, 83, 84]
        notePitch = trebleMap[stepIndex]
    
    elif clefSignature == 1:
        bassMap =   [36, 38, 40, 41, 43, 45, 47, 48, 50, 52, 53, 55, 57, 59, 60, 62, 64]
        notePitch = bassMap[stepIndex]
        
    return notePitch