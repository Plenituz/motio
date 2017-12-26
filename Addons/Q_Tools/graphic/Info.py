from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node
import Motio.NodeImpl

class Info(BaseClass):
    classNameStatic = "Info"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        print "Creating properties"

    def evaluate_frame(self, frame, dataFeed):
        meshGroup = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        print(dataFeed.GetChannelData(Node.PATH_CHANNEL))
        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)