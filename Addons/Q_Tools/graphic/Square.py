from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node

class Square(BaseClass):
    classNameStatic = "Square"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        print "Creating properties"
        #position
        posProp = Props.VectorNodeProperty(self, "Position of the square", "Position")
        self.Properties.Add("pos", posProp, Geo.Vector2(0, 0))
        #size
        sizeProp = Props.FloatNodeProperty(self, "Size of the square", "Size")
        self.Properties.Add("size", sizeProp, 2)
        #action
        actionProp = Props.DropdownNodeProperty(self, "Choose what to do with existing shapes", "Action", ["Replace", "Merge"])
        self.Properties.Add("action", actionProp, "Replace")

    def evaluate_frame(self, frame, dataFeed):
        size = self.Properties.GetValue("size", frame)
        pos = self.Properties.GetValue("pos", frame)
        action = self.Properties.GetValue("action",frame)
        points = [
            Geo.Vector2(size/2, size/2)+pos,
            Geo.Vector2(-size/2, size/2)+pos,
            Geo.Vector2(-size/2, -size/2)+pos,
            Geo.Vector2(size/2, -size/2)+pos,
        ]
        triangles = [
            0,1,2,
            0,2,3
        ]
        mesh = Meshing.Mesh()
        mesh.triangles = triangles
        mesh.points = points

        meshGroupInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        if action == "Merge":
            meshGroupInput.Add(mesh)
            meshGroup = meshGroupInput
        else:
            meshGroup = Meshing.MeshGroup(mesh)

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)