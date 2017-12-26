from Motio.NodeImpl.GraphicsAffectingNodes import PyGraphicsAffectingNodeBase as BaseClass
import Motio.NodeImpl.NodePropertyTypes as Props
import Motio.Meshing as Meshing
import Motio.Geometry as Geo
from Motio.NodeCore import Node
import Motio.Graphics as Graphics

class Border(BaseClass):
    classNameStatic = "Border"
    def get_class_name(self):
        return self.classNameStatic
    def __new__(cls, *args):
        return BaseClass.__new__(cls, *args)

    def setup_node(self):
        print "Setting up"

    def setup_properties(self):
        #alignment
        alignmentProp = Props.DropdownNodeProperty(self, "How to place the line around the shape", "Alignment", ["Inside", "Middle", "Outside"])
        self.Properties.Add("alignment", alignmentProp, "Middle")
        #thickness
        thicknessProp = Props.FloatNodeProperty(self, "Thickness of the border", "Thickness")
        self.Properties.Add("thickness", thicknessProp, 0.2)
        #color
        colorProp = Props.ColorNodeProperty(self, "Color of the border", "Color")
        self.Properties.Add("color", colorProp, Graphics.Color.Blue)
        #rounded
        roundedProp = Props.BoolNodeProperty(self, "Round between line", "Rounded")
        self.Properties.Add("rounded", roundedProp, 1)
        #keepShape
        keepShapeProp = Props.BoolNodeProperty(self, "Add the border to the original shape", "Keep original shape")
        self.Properties.Add("keepShape", keepShapeProp, 0)

    def evaluate_frame(self, frame, dataFeed):
        thickness = self.Properties.GetValue("thickness", frame)
        borderColor = self.Properties.GetValue("color", frame)

        meshGroupInput = dataFeed.GetChannelData(Node.MESH_CHANNEL)
        
        meshGroup = Meshing.MeshGroup()

        for mesh in meshGroupInput:
            builder = Meshing.MeshBuilder()
            points=mesh.points
            
            #triangle to segments
            segments = []
            for i in range(0,len(mesh.triangles),3):
                segments.append(sorted([mesh.triangles[i], mesh.triangles[i+1]]))
                segments.append(sorted([mesh.triangles[i+1],mesh.triangles[i+2]]))
                segments.append(sorted([mesh.triangles[i+2],mesh.triangles[i]]))

            #remove duplicate
            segments.sort()
            borderEdges = []
            skip = False
            for i in range(len(segments)):
                if skip:
                    skip = False
                    continue
                if i==len(segments)-1:
                    borderEdges.append(segments[i])
                    break
                if segments[i] != segments[i+1]:
                    borderEdges.append(segments[i])
                else:
                    skip = True

            #stroke border segments
            for borderEdge in borderEdges:
                builder.AddLine(points[borderEdge[0]],points[borderEdge[1]],thickness)

            mesh = builder.Mesh
            if mesh.material is None:
                mesh.material = Graphics.MeshMaterial()
            mesh.material.color = borderColor
            meshGroup.Add(mesh)

        dataFeed.SetChannelData(Node.MESH_CHANNEL, meshGroup)