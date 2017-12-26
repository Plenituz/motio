from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node
import math

class Capsule(BaseClass):
    classNameStatic = "Capsule"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        print "Creating properties"
        #position point 1
        pos1Prop = Props.VectorNodeProperty(self, "First center position", "Position 1")
        self.Properties.Add("pos1", pos1Prop, Geo.Vector2(0, 2))
        #position point 2
        pos2Prop = Props.VectorNodeProperty(self, "Second center position", "Position 2")
        self.Properties.Add("pos2", pos2Prop, Geo.Vector2(0, -2))
        #thickness
        thicknessProp = Props.FloatNodeProperty(self, "Thickness of the capsule", "Thickness")
        self.Properties.Add("thickness", thicknessProp, 2)
        #detail
        detailProp = Props.FloatNodeProperty(self, "Definition of the rounded edges", "Detail")
        self.Properties.Add("detail", detailProp, 6)
        #action
        actionProp = Props.DropdownNodeProperty(self, "Choose what to do with existing shapes", "Action", ["Replace", "Merge"])
        self.Properties.Add("action", actionProp, "Replace")

    def evaluate_frame(self, frame, dataFeed):
        pos1 = self.Properties.GetValue("pos1", frame)
        pos2 = self.Properties.GetValue("pos2", frame)
        thickness = self.Properties.GetValue("thickness", frame)
        detail = self.Properties.GetValue("detail", frame)
        action = self.Properties.GetValue("action",frame)
        
        #normalize data
        detail = 1 if detail < 1 else int(detail)

        #calculate normal vector in both ways
        normal1 = Geo.Vector2.Normalize(Geo.Vector2(pos2.Y-pos1.Y,pos1.X-pos2.X))*Geo.Vector2(thickness/2)
        normal2 = Geo.Vector2.Normalize(Geo.Vector2(pos1.Y-pos2.Y,pos2.X-pos1.X))*Geo.Vector2(thickness/2)
        #angle between circle division
        divisionAngle = math.pi/detail

        #main rectangle points
        points = [
            pos1,
            pos2,
            pos1+normal1,
            pos1+normal2,
            pos2+normal1,
            pos2+normal2
        ]
        #circle points
        for i in range(detail-1):
            positionOnCircle1 = Geo.Vector2(thickness/2*math.cos(divisionAngle*(i+1)+math.atan2(normal1.Y, normal1.X)+math.pi),thickness/2*math.sin(divisionAngle*(i+1)+math.atan2(normal1.Y, normal1.X)+math.pi))
            points.append(positionOnCircle1+pos1)
            positionOnCircle2 = Geo.Vector2(thickness/2*math.cos(divisionAngle*(i+1)+math.atan2(normal1.Y, normal1.X)),thickness/2*math.sin(divisionAngle*(i+1)+math.atan2(normal1.Y, normal1.X)))
            points.append(positionOnCircle2+pos2)

        #main rectangle triangles
        triangles = [
            0,2,4,
            4,1,0,
            0,1,3,
            3,1,5
        ]
        #circle triangles border
        triangles.extend([
            0,3,6,
            1,4,7,
            0,detail*2+2,2,
            1,detail*2+3,5
        ])
        #circle triangles center
        for i in range(detail-2):
            triangles.extend([0,6+(2*i),8+(2*i)])
            triangles.extend([1,7+(2*i),9+(2*i)])
        

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