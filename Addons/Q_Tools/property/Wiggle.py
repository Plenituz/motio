from Motio.NodeImpl.PropertyAffectingNodes import PyPropertyAffectingNodeBase as BaseClass
from Motio.NodeImpl.NodePropertyTypes import *
from System import Type as Type
from Motio.NodeCore import Node
import Motio.Geometry as Geo
from itertools import product
from math import sqrt, cos
from random import seed, uniform
import Motio.NodeCommon

class Wiggle(BaseClass):
    classNameStatic = "Wiggle"
    def get_class_name(self):
        return self.classNameStatic

    def get_accepted_property_types(self):
        #Geo.Vector2.__clrtype__()
        return [Type.GetType("System.Single")]

    def setup_properties(self):
        self.Properties.Add("type", DropdownNodeProperty(self, "Different type of movement", "Type", ["Periodic", "Perlin noise", "Random"]), "Periodic")
        self.Properties.Add("speedProp", FloatNodeProperty(self, "Speed of vibration", "Speed"), 1)
        self.Properties.Add("powerProp", FloatNodeProperty(self, "Power of vibration", "Power"), 1)
        self.Properties.Add("offsetProp", FloatNodeProperty(self, "Vibration's offset in time", "Offset"), 0)

    #use this function as a node constructor, this is optionnal
    def setup_node(self):
        print("setup node")

    def evaluate_frame(self, frame, dataFeed):
        if dataFeed.ChannelExists(Node.PROPERTY_OUT_CHANNEL):
            previousVal = dataFeed.GetChannelData(Node.PROPERTY_OUT_CHANNEL)

        noiseType = self.Properties.GetValue("type", frame)
        speed = self.Properties.GetValue("speedProp", frame)
        power = self.Properties.GetValue("powerProp", frame)
        offset = self.Properties.GetValue("offsetProp", frame)
        
        if noiseType == "Periodic":
            newVal = previousVal + cos((frame+offset)*speed)*power
        elif noiseType == "Perlin noise":
            noisePosition = abs(frame + offset)
            noiseScale = 1/float(speed)*5.0 if speed != 0 else 1000.0
            noiseVal = Get2DPerlinNoiseValue(float(noisePosition),float(noisePosition),noiseScale)*power
            newVal = previousVal + noiseVal
        else:
            seed(frame+offset)
            newVal = previousVal + ((uniform(-1,1)*2)+1)*power

        newVal = Motio.NodeCommon.ToolBox.ConvertToFloat(newVal)
        dataFeed.SetChannelData(Node.PROPERTY_OUT_CHANNEL, newVal)


#Perlin noise translated from C
#Original C from https://openclassrooms.com/courses/bruit-de-perlin
def Get2DPerlinNoiseValue(x, y, res):
    if x > 255:
        x = x - 255 * int(x / 255)
    if y > 255:
        y = y - 255 * int(y / 255)

    unit = 1.0/sqrt(2)
    gradient2 = [[unit,unit],[-unit,unit],[unit,-unit],[-unit,-unit],[1,0],[-1,0],[0,1],[0,-1]]
    perm =[
        151,160,137,91,90,15,131,13,201,95,96,53,194,233,7,225,140,36,103,30,69,
        142,8,99,37,240,21,10,23,190,6,148,247,120,234,75,0,26,197,62,94,252,219,
        203,117,35,11,32,57,177,33,88,237,149,56,87,174,20,125,136,171,168,68,175,
        74,165,71,134,139,48,27,166,77,146,158,231,83,111,229,122,60,211,133,230,220,
        105,92,41,55,46,245,40,244,102,143,54,65,25,63,161,1,216,80,73,209,76,132,
        187,208,89,18,169,200,196,135,130,116,188,159,86,164,100,109,198,173,186,3,
        64,52,217,226,250,124,123,5,202,38,147,118,126,255,82,85,212,207,206,59,227,
        47,16,58,17,182,189,28,42,223,183,170,213,119,248,152,2,44,154,163,70,221,
        153,101,155,167,43,172,9,129,22,39,253,19,98,108,110,79,113,224,232,178,185,
        112,104,218,246,97,228,251,34,242,193,238,210,144,12,191,179,162,241,81,51,145,
        235,249,14,239,107,49,192,214,31,181,199,106,157,184,84,204,176,115,121,50,45,
        127,4,150,254,138,236,205,93,222,114,67,29,24,72,243,141,128,195,78,66,215,61,
        156,180
    ]
    perm.extend(perm)

    #Adapter pour la resolution
    x /= res
    y /= res

    #On recupere les positions de la grille associee a (x,y)
    x0 = int(x)
    y0 = int(y)

    #Masquage
    ii = x0 & 255
    jj = y0 & 255

    #Pour recuperer les vecteurs
    gi0 = perm[ii + perm[jj]] % 8
    gi1 = perm[ii + 1 + perm[jj]] % 8
    gi2 = perm[ii + perm[jj + 1]] % 8
    gi3 = perm[ii + 1 + perm[jj + 1]] % 8

    #on recupere les vecteurs et on pondere
    tempX = x-x0
    tempY = y-y0
    s = gradient2[gi0][0]*tempX + gradient2[gi0][1]*tempY

    tempX = x-(x0+1)
    tempY = y-y0
    t = gradient2[gi1][0]*tempX + gradient2[gi1][1]*tempY

    tempX = x-x0
    tempY = y-(y0+1)
    u = gradient2[gi2][0]*tempX + gradient2[gi2][1]*tempY

    tempX = x-(x0+1)
    tempY = y-(y0+1)
    v = gradient2[gi3][0]*tempX + gradient2[gi3][1]*tempY


    #Lissage
    tmp = x-x0
    Cx = 3 * tmp * tmp - 2 * tmp * tmp * tmp

    Li1 = s + Cx*(t-s)
    Li2 = u + Cx*(v-u)

    tmp = y - y0
    Cy = 3 * tmp * tmp - 2 * tmp * tmp * tmp

    return Li1 + Cy*(Li2-Li1)