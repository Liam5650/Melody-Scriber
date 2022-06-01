from skimage import io
from skimage.color import rgb2gray

class MusicSheet:
    
    def __init__(self, tempo = 120):
        
        self.tempo = tempo
        
    def setImage(self, path):
        
        image = rgb2gray(io.imread(path))
        self.image = image
        
    def setBars(self, bars):
        
        self.barObjects = bars


class Bar:
    
    stafObjects = []
    cornerCoords = []
    
    def __init__(self, timeSig=(4,4)):
        
        self.timeSig = timeSig
        
class Staff:
    
    clefSig = ''
    keySig = ''
    cornerCoords = []
    horizLines = []
    vertLines = []
    noteStems = []
    noteObjects = []
    
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
    