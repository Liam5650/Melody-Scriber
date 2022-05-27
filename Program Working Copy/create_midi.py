from midiutil import MIDIFile

def createMidi(notes, bars, horizontalLines):
    
    notes = ProcessNotes(notes, bars, horizontalLines)
    degrees = [60, 62, 64, 65, 67, 69, 71, 72] # MIDI note number
    track = 0
    channel = 0
    time = 0 # In beats
    duration = 1 # In beats
    tempo = 60 # In BPM
    volume = 100 # 0-127, as per the MIDI standard
    MyMIDI = MIDIFile(1) # One track, defaults to format 1 (tempo track
    # automatically created)
    MyMIDI.addTempo(track,time, tempo)
    for pitch in degrees:
        MyMIDI.addNote(track, channel, pitch, time, duration, volume)
        time = time + 1
    with open("./midi_output/major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)
        
def ProcessNotes(notes, bars, horizontalLines):
    
    processedNotes = [[],[]]
    
    for bar in notes:
        
        for staff in bar:
            
            for note in staff:
                
                pitch, channel = getPitch(note[0], bars, horizontalLines)
                
                processedNotes[channel].append((pitch, note[1]))
                
    return processedNotes

def getPitch(noteCoord, bars, horizontalLines):
    
    print(noteCoord)
    
    noteY = noteCoord[0]
    noteX = noteCoord[1]
    barIndex = 0
    
    while barIndex < len(bars):
        
        trebleTop = bars[barIndex][0][0][0]
        trebleBottom = bars[barIndex][0][1][0]
        trebleLeft = bars[barIndex][0][0][1]
        trebleRight = bars[barIndex][0][1][1]
        
        bassTop = bars[barIndex][1][0][0]
        bassBottom = bars[barIndex][1][1][0]
        bassLeft = bars[barIndex][1][0][1]
        bassRight = bars[barIndex][1][1][1]
        
        # Add a margin as notes may be outside these bounds (ex middle C)
        
        if (noteY > trebleTop and noteY < bassBottom):
            
            if (noteX > trebleLeft and noteX < bassRight):
                
                print(bars[barIndex])
                
                
                
                break
            
            else:
                
                barIndex += 1
        
        else:
            
            barIndex += 1
        
    
    return 0,0