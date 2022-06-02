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
    