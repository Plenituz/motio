from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node

class Line(BaseClass):
    classNameStatic = "Line"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        print "Creating properties"
        #position point 1
        posFromProp = Props.VectorNodeProperty(self, "Start point position", "Start position")
        self.Properties.Add("posFrom", posFromProp, Geo.Vector2(0, 2))
        #position point 2
        posToProp = Props.VectorNodeProperty(self, "End point position", "End position")
        self.Properties.Add("posTo", posToProp, Geo.Vector2(0, -2))
        #thickness
        thicknessProp = Props.FloatNodeProperty(self, "Thickness of the line", "Thickness")
        self.Properties.Add("thickness", thicknessProp, 0.2)
        #action
        actionProp = Props.DropdownNodeProperty(self, "Choose what to do with existing shapes", "Action", ["Replace", "Merge"])
        self.Properties.Add("action", actionProp, "Replace")

    def evaluate_frame(self, frame, dataFeed):
        thickness = self.Properties.GetValue("thickness", frame)
        posFrom = self.Properties.GetValue("posFrom", frame)
        posTo = self.Properties.GetValue("posTo", frame)
        action = self.Properties.GetValue("action",frame)

        builder = Meshing.MeshBuilder()
        builder.AddLine(posFrom,posTo,thickness)
        mesh = builder.Mesh

        meshGroupInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        if action == "Merge":
            meshGroupInput.Add(mesh)
            meshGroup = meshGroupInput
        else:
            meshGroup = Meshing.MeshGroup(mesh)

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)