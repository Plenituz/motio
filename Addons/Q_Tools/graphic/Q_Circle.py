from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node

class Q_Circle(BaseClass):
    classNameStatic = "Q Circle"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        print "Creating properties"
        #position
        posProp = Props.VectorNodeProperty(self, "Position of the circle's center", "Position")
        self.Properties.Add("pos", posProp, Geo.Vector2(0, 0))
        #radius
        radiusProp = Props.FloatNodeProperty(self, "Circle's radius", "Radius")
        self.Properties.Add("radius", radiusProp, 5)
        #detail
        detailProp = Props.FloatNodeProperty(self, "Smoothness of the circle", "Detail")
        self.Properties.Add("detail", detailProp, 12)
        #action
        actionProp = Props.DropdownNodeProperty(self, "Choose what to do with existing shapes", "Action", ["Replace", "Merge"])
        self.Properties.Add("action", actionProp, "Replace")

    def evaluate_frame(self, frame, dataFeed):
        pos = self.Properties.GetValue("pos", frame)
        radius = self.Properties.GetValue("radius", frame)
        detail = self.Properties.GetValue("detail", frame)
        action = self.Properties.GetValue("action",frame)

        builder = Meshing.MeshBuilder()
        builder.AddCircle(pos,radius,detail)
        mesh = builder.Mesh

        meshGroupInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        if action == "Merge":
            meshGroupInput.Add(mesh)
            meshGroup = meshGroupInput
        else:
            meshGroup = Meshing.MeshGroup(mesh)

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)