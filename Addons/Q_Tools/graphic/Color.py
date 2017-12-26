from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node
import Motio.Graphics as Graphics
import random

class Color(BaseClass):
    classNameStatic = "Color"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"
    '''
    def dropDownCallback(self,sender,args):
        if args.PropertyName == "StaticValue":
            self.updateInterface()
    
    def updateInterface(self):
        displayState = True if self.Properties.GetValue("type",0) == "Constant" else False
        self.Properties["color"].Visible = displayState
        self.Properties["seed"].Visible = not displayState
    '''

    def setup_properties(self):
        #type
        typeProp = Props.DropdownNodeProperty(self, "Choose how to apply the color", "Type", ["Constant", "Random (uniform)", "Random (per shape)"])
        self.Properties.Add("type", typeProp, "Constant")
        #color
        colorProp = Props.ColorNodeProperty(self, "Color of the object", "Color")
        self.Properties.Add("color", colorProp, Graphics.Color.Red)
        #seed
        seedProp = Props.FloatNodeProperty(self, "Seed for random", "Seed")
        self.Properties.Add("seed", seedProp, 1)

        #event callbacks
        #typeProp.PropertyChanged += self.dropDownCallback
        #self.updateInterface()

    def evaluate_frame(self, frame, dataFeed):
        colorType = self.Properties.GetValue("type", frame)

        if colorType == "Random (uniform)":
            globalColor = self.random_color(self.Properties.GetValue("seed", frame),frame)
        else:
            globalColor = self.Properties.GetValue("color", frame)

        meshInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        meshGroup = Meshing.MeshGroup()
        i = 0
        for mesh in meshInput:
            if mesh.material is None:
                mesh.material = Graphics.MeshMaterial()

            if colorType == "Random (per shape)":
                mesh.material.color = self.random_color(self.Properties.GetValue("seed", frame)+i,frame)
            else :
                mesh.material.color = globalColor
            meshGroup.Add(mesh)
            i+=1

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)

    def random_color(self, seed, frame):
        randomColor = Graphics.Color.White
        random.seed(seed)
        randomColor.R = random.randint(0,255)
        randomColor.G = random.randint(0,255)
        randomColor.B = random.randint(0,255)
        return randomColor
