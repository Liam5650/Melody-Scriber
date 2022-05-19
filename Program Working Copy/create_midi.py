from midiutil import MIDIFile

def createMidi(notes):
    
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