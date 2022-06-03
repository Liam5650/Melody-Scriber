from skimage import io
from skimage.color import rgb2gray
from get_bars import getBars



class MusicSheet:
    
    def __init__(self, tempo = 120):
        
        self.tempo = tempo
        
    def setImage(self, path):
        
        image = rgb2gray(io.imread(path))
        self.image = image
        
    def createBars(self):
        
        self.barObjects = getBars(self.image)



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
 
    
    
class Chord:
    
    noteObjects = []
  
  
  
class Note:
    
    coord = ()
    headType = ''
    time = 0
    pitch = 0
    tails = 0
    dotted = False
 

    
class Rest:
    
    time = 0
    