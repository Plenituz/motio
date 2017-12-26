from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node
import Motio.Graphics as Graphics

class Scale(BaseClass):
    classNameStatic = "Scale"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)


    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        #scale
        scaleProp = Props.VectorNodeProperty(self, "Scale of the object", "Scale")
        self.Properties.Add("scale", scaleProp, Geo.Vector2(1, 1))
        #uniformScale
        uniScaleProp = Props.FloatNodeProperty(self, "Scale of the object", "Uniform scale")
        self.Properties.Add("uniScale", uniScaleProp, 1)
        #center
        centerProp = Props.VectorNodeProperty(self, "Scale from this point", "Center")
        self.Properties.Add("center", centerProp, Geo.Vector2(0, 0))

    def evaluate_frame(self, frame, dataFeed):
        scaleNonUniform = self.Properties.GetValue("scale", frame)
        scaleUniform = self.Properties.GetValue("uniScale", frame)
        globalScale = scaleNonUniform*Geo.Vector2(scaleUniform,scaleUniform)
        center = self.Properties.GetValue("center", frame)

        meshInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        meshGroup = Meshing.MeshGroup()

        for mesh in meshInput:
            newPoints = []
            for point in mesh.points:
                newPoints.append((point-center)*globalScale+center)
            mesh.points = newPoints
            meshGroup.Add(mesh)

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)
