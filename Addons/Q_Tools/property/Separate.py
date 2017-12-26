from Motio.NodeImpl.PropertyAffectingNodes import PyPropertyAffectingNodeBase as BaseClass
from Motio.NodeImpl.NodePropertyTypes import *
from System import Type as Type
from Motio.NodeCore import Node
import Motio.Geometry as Geo
import Motio.NodeCommon

class Separate(BaseClass):
    classNameStatic = "Separate"
    def get_class_name(self):
        return self.classNameStatic

    def get_accepted_property_types(self):
        return [Geo.Vector2.__clrtype__()]

    def setup_properties(self):
        self.Properties.Add("xProp", FloatNodeProperty(self, "X component", "X"), 0)
        self.Properties.Add("yProp", FloatNodeProperty(self, "Y component", "Y"), 0)

    #use this function as a node constructor, this is optionnal
    def setup_node(self):
        print("setup node")

    def evaluate_frame(self, frame, dataFeed):
        if dataFeed.ChannelExists(Node.PROPERTY_OUT_CHANNEL):
            previousVal = dataFeed.GetChannelData(Node.PROPERTY_OUT_CHANNEL)

        self.Properties["xProp"].StaticValue = previousVal.X
        self.Properties["yProp"].StaticValue = previousVal.Y

        xProp = self.Properties.GetValue("xProp", frame)
        yProp = self.Properties.GetValue("yProp", frame)

        newVal = Geo.Vector2(xProp,yProp)
        dataFeed.SetChannelData(Node.PROPERTY_OUT_CHANNEL, newVal)
