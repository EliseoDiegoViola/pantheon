import sys
for module in sys.modules.keys():
    if sys.modules[module] and module not in sys.builtin_module_names and "pantheonModules" in str(sys.modules[module]) :
        del(sys.modules[module])

import MaxPlus
from pantheonModules.pantheonUtilities import modulesLoader
from pantheonModules.exporter.abstraction import exportableScene
from pantheonModules.exporter.abstraction import exportable
from pantheonModules.exporter.abstraction.exportable import EXPORTABLE_TYPE
from PySide import QtGui
from PySide import QtCore
from math import ceil

reload(modulesLoader)
loader = modulesLoader.ModulesLoader()

boundsTitle = "BOUNDS CHECKER 0.2 (hardcoded)"

def enumeratePoints(bounds,density=1):
    print "ENUMARATE!!!"
    points = []
    #externalPoints
    points.append(bounds.GetMin())
    points.append(bounds.GetMax())
    for axis in range(0,3):
        point = bounds.GetMin()
        if axis%3 == 0:
            point.SetX(point.GetX() + bounds.GetWidth().GetX())
        elif axis%3 == 1:
            point.SetY(point.GetY() + bounds.GetWidth().GetY())
        elif axis%3 == 2:
            point.SetZ(point.GetZ() + bounds.GetWidth().GetZ())
        points.append(point)
        point = bounds.GetMax()
        if axis%3 == 0:
            point.SetX(point.GetX() - bounds.GetWidth().GetX())
        elif axis%3 == 1:
            point.SetY(point.GetY() - bounds.GetWidth().GetY())
        elif axis%3 == 2:
            point.SetZ(point.GetZ() - bounds.GetWidth().GetZ())
        points.append(point)

    bMin = [bounds.GetMin().GetX(),bounds.GetMin().GetY(),bounds.GetMin().GetZ()]
    bMax = [bounds.GetMax().GetX(),bounds.GetMax().GetY(),bounds.GetMax().GetZ()]
    for axis in range(0,3*(density-1)):
        # print ceil(density-(axis/3)) , "+ - -"
        # print "- ",ceil(density-(axis/3)),"+ -"
        # print "- - ",ceil(density-(axis/3)),"+"
        # print ceil(density-(axis/3)) , "- + +"
        # print "+ ",ceil(density-(axis/3)),"- +"
        # print "+ + ",ceil(density-(axis/3)),"-"

        point = [0,0,0]
        point[0] = ceil(density-(axis/3))*bMax[0]
        point[1] = bMax[1]
        point[2] = bMax[2]
        points.append(point)

        point = [0,0,0]
        point[0] = ceil(density-(axis/3))*bMax[0]
        point[1] = bMax[1]
        point[2] = bMax[2]
        points.append(point)

        point = [0,0,0]
        point[0] = ceil(density-(axis/3))*bMax[0]
        point[1] = bMax[1]
        point[2] = bMax[2]
        points.append(point)

        point = [0,0,0]
        point[0] = ceil(density-(axis/3))*bMax[0]
        point[1] = bMax[1]
        point[2] = bMax[2]
        points.append(point)


        # point.SetX(point.GetX() + bounds.GetWidth().GetX()/ceil(density-(axis/3)))


        point.SetX(point.GetX() + bounds.GetWidth().GetX()/ceil(density-(axis/3)))
        point.SetY(point.GetY() + bounds.GetWidth().GetY()/ceil(density-(axis/3)))
        point.SetZ(point.GetZ() + bounds.GetWidth().GetZ()/ceil(density-(axis/3)))
        points.append(point)

        point = [bounds.GetMax().GetX(),bounds.GetMax().GetY(),bounds.GetMax().GetZ()]
        point.SetX(point.GetX() - bounds.GetWidth().GetX()/ceil(density-(axis/3)))
        point.SetY(point.GetY() - bounds.GetWidth().GetY()/ceil(density-(axis/3)))
        point.SetZ(point.GetZ() - bounds.GetWidth().GetZ()/ceil(density-(axis/3)))
        points.append(point)
    return points

def dot(a,b):
    ab0 = a.GetX() * b.GetX()
    ab1 = a.GetY() * b.GetY()
    ab2 = a.GetZ() * b.GetZ()
    return ab0 + ab1 + ab2


def isInside(b1,b2):


    u = b1[0] - b1[6];
    v = b1[0] - b1[2];
    w = b1[0] - b1[4];

    toCompU1 = dot(u, b1[0]);
    toCompU2 = dot(u, b1[6]);

    toCompV1 = dot(v, b1[0]);
    toCompV2 = dot(v, b1[2]);

    toCompW1 = dot(w, b1[0]);
    toCompW2 = dot(w, b1[4]);

    for p in b2:
        resU = dot(u, p);
        resV = dot(v, p);
        resW = dot(w, p);

        isu = toCompU1 > resU and resU > toCompU2;
        isv = toCompV1 > resV and resV > toCompV2;
        isw = toCompW1 > resW and resW > toCompW2;
        if isu and isv and isw:
            return True;

    return False;

def toggleVision():
        MaxPlus.Core.EvalMAXScript("if displayColor.shaded == #material then displayColor.shaded = #object else displayColor.shaded = #material") 

def toggleBox(iNodes):
    if iNodes:
        mode = not iNodes[0].GetBoxMode()
        for iNode in iNodes:
            iNode.SetBoxMode(mode)
    MaxPlus.ViewportManager.RedrawViews(MaxPlus.Core.GetCurrentTime())

def debugBounds(bounds):
    for p in bounds:
        sph = MaxPlus.Factory.CreateGeomObject(MaxPlus.ClassIds.Sphere)
        node = MaxPlus.Factory.CreateNode(sph)
        node.Scale(MaxPlus.Point3(0.1,0.1,0.1))
        node.Position = p

class seeThrough():
    seeTID = -1
    seeTObj = None

    def __init__(self,sid,sobj):
        self.seeTID = sid
        self.seeTObj = sobj

class BoundChecker(QtGui.QWidget):

    def __init__(self,mainWindow):
        self.closeInstances(mainWindow)
        QtGui.QWidget.__init__(self,mainWindow)
        
        self.scene = exportableScene.exportableScene("ThisFile")
        self.seeThroughs = []
        self.links = {}
        self.previousMeshColor = {}
        self.createWindow()
        self.refreshLinks()

    def closeEvent(self, evnt):
        QtGui.QWidget.closeEvent(self,evnt)
        self.revertColors()
        print "CLOSED!"
        # super(MyDialog, self).closeEvent(evnt)

        
    def closeInstances(self,parentWindow):
        for obj in parentWindow.children():
            if obj.objectName() == boundsTitle: # Compare object names
                obj.setParent(None)
                obj.deleteLater()  
                obj.revertColors()      


    def refreshLinks(self):
        self.links = self.getMeshesInside()
        for link in self.links:
            self.paintDummy(link,self.links[link])

        MaxPlus.ViewportManager.RedrawViews(MaxPlus.Core.GetCurrentTime())


    def createWindow(self):
        main_layout = QtGui.QVBoxLayout()
        self.setWindowTitle(boundsTitle)
        self.setObjectName(boundsTitle)
        # self.setWindowFlags(QTCore.QtGui.Window)
        self.resize(200, 50)
        self.setLayout(main_layout)

        togShadingButton = QtGui.QPushButton("Toggle Shading")
        togBoxesButton = QtGui.QPushButton("Toggle Boxes")
        refreshVisibilityButton = QtGui.QPushButton("Refresh")


        togShadingButton.clicked.connect(lambda : toggleVision())
        togBoxesButton.clicked.connect(lambda : toggleBox([st.seeTObj.objectRepresentation for st in self.seeThroughs]))
        refreshVisibilityButton.clicked.connect(lambda : self.refreshLinks())


        main_layout.addWidget(togShadingButton)
        main_layout.addWidget(togBoxesButton)
        main_layout.addWidget(refreshVisibilityButton)

    def getExportableNodes(self,expParent):        
        seeThroughs = []
        meshes = []
        notVisited = []
        current = expParent
        
            
        if expParent.extraData:
            hideables = [expO["DAT_node"] for expO in expParent.extraData["objectLayers"] if expO["DAT_layer"] == "LAYOUT_HIDE"]
            stIds = dict([(expO["DAT_node"], expO["DAT_id"]) for expO in expParent.extraData["seeThroughBoxes"]])

            while current != None :
                seeThroughs = seeThroughs + [seeThrough(stIds[str(st)],st) for st in current.exportableContent if str(st) in stIds]
                
                if str(current) in hideables or str(current.exportableParent) in hideables: #this wont gonna work on deep level 3, Ask if... "ITS IN PARENT"
                    meshes = meshes + [mesh for mesh in current.exportableContent if mesh.contentType == EXPORTABLE_TYPE.MESH ]

                notVisited = notVisited + current.exportableChildren
                if notVisited and len(notVisited) > 0:
                    current = notVisited.pop(0)
                else:
                    current = None
            
        return seeThroughs,meshes
#{\"typ\": 3, \"value\": [{\"DAT_node\": \"ST_CT_01\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_002\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_003\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_004\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_005\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_006\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_007\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_008\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_009\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_010\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_011\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_012\", \"DAT_colType\": \"BOX\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST_CT_CURVED01\", \"DAT_colType\": \"MESH\", \"DAT_id\": \"\"}, {\"DAT_node\": \"ST
    def checkMeshes(self,meshO, seeThroughs):

        mesh = meshO.objectRepresentation
        boxTM = mesh.GetWorldTM()
        boxbound = mesh.GetObject().GetDeformBBox()
        bounds1Points = [boxTM.PointTransform(p) for p in  enumeratePoints(boxbound) ]

        linked = []

        for seeThroughO in seeThroughs:
            seeThrough = seeThroughO.seeTObj.objectRepresentation
            boundsTM = seeThrough.GetWorldTM()
            boundsToCheck = seeThrough.GetObject().GetDeformBBox()
            bounds2Points = [boundsTM.PointTransform(p) for p in  enumeratePoints(boundsToCheck) ]
            
            if isInside(bounds1Points,bounds2Points) or isInside(bounds2Points,bounds1Points):
                # print str(meshO.exportableParent), " AFFECTED BY SEETHROUGH " , str(seeThroughO)
                linked.append(seeThroughO)

        return linked

    def revertColors(self):
        if self.previousMeshColor:
            for mesh in self.previousMeshColor:
                mesh.objectRepresentation.SetWireColor(self.previousMeshColor[mesh])
            MaxPlus.ViewportManager.RedrawViews(MaxPlus.Core.GetCurrentTime())

    def saveColor(self,mesh):
        if mesh not in self.previousMeshColor:
            self.previousMeshColor[mesh] = mesh.objectRepresentation.GetWireColor()

    def paintDummy(self,expParent, seeThroughs):
        # print len(seeThroughs)
        if len(seeThroughs) == 0:
            meshes = [mesh for mesh in expParent.exportableContent if mesh.contentType == EXPORTABLE_TYPE.MESH ]
            for mesh in meshes :
                self.saveColor(mesh)
                mesh.objectRepresentation.SetWireColor(MaxPlus.Color(0.0,0.0,0.0))
        elif len(seeThroughs) == 1 or all([st.seeTID == seeThroughs[0].seeTID for st in seeThroughs]):
            meshes = [mesh for mesh in expParent.exportableContent if mesh.contentType == EXPORTABLE_TYPE.MESH ]
            for mesh in meshes :
                self.saveColor(mesh)
                mesh.objectRepresentation.SetWireColor(seeThroughs[0].seeTObj.objectRepresentation.GetWireColor())
        elif len(seeThroughs) > 1:
            meshes = [mesh for mesh in expParent.exportableContent if mesh.contentType == EXPORTABLE_TYPE.MESH ]
            for mesh in meshes :
                self.saveColor(mesh)
                mesh.objectRepresentation.SetWireColor(MaxPlus.Color(1.0,1.0,1.0))
       
    def getMeshesInside(self):
        expP = self.scene.exportableParents
        self.seeThroughs = []

        for exp in expP:
            seeThroughs,meshes = self.getExportableNodes(exp)
            
            self.seeThroughs = self.seeThroughs +   seeThroughs
            # meshes = list(set(self.getMeshes(exp)))
            links = {}
            for mesh in meshes:
                checks = self.checkMeshes(mesh,seeThroughs)
                if mesh.exportableParent not in links:
                    links[mesh.exportableParent] = []
                if checks:
                    links[mesh.exportableParent] = list(set(links[mesh.exportableParent] + checks))
                        
        return links
                  
 
        

# checker = BoundChecker(MaxPlus.GetQMaxWindow())
# checker.show()



def checkMeshes(mesh, seeThroughs):

    boxTM = mesh.GetWorldTM()
    boxbound = mesh.GetObject().GetDeformBBox()
    bounds1Points = [boxTM.PointTransform(p) for p in  enumeratePoints(boxbound,3) ]

    linked = []

    for seeThrough in seeThroughs:
        boundsTM = seeThrough.GetWorldTM()
        boundsToCheck = seeThrough.GetObject().GetDeformBBox()
        bounds2Points = [boundsTM.PointTransform(p) for p in  enumeratePoints(boundsToCheck,3) ]
        
        if isInside(bounds1Points,bounds2Points) or isInside(bounds2Points,bounds1Points):
            # print str(meshO.exportableParent), " AFFECTED BY SEETHROUGH " , str(seeThroughO)
            linked.append(seeThrough)

    return linked

def paintDummy(mesh, seeThroughs):
    if len(seeThroughs) == 0:
            mesh.SetWireColor(MaxPlus.Color(0.0,0.0,0.0))
    elif len(seeThroughs) == 1:
            mesh.SetWireColor(seeThroughs[0].GetWireColor())
    elif len(seeThroughs) > 1:
            mesh.SetWireColor(MaxPlus.Color(1.0,1.0,1.0))

def test(vieport):
    stBox = [MaxPlus.INode.GetINodeByName("ST_Box002")]
    meshesTT = [MaxPlus.INode.GetINodeByName("boxes_004_00"),MaxPlus.INode.GetINodeByName("boxes_004_01"),MaxPlus.INode.GetINodeByName("boxes_004_02")]
    links = {}
    for m in meshesTT:
        links[m] = checkMeshes(m,stBox)

    for l in links:
        paintDummy(l,links[l])
# handler = None

# if handler:
#     MaxPlus.NotificationManager.Unregister(handler)
#     handler = None
#     print "UNREGISTER"
# else:
#     handler = MaxPlus.NotificationManager.Register(MaxPlus.NotificationCodes.ViewportChange  , test)
#     print "REGISTERED"
ugh = MaxPlus.INode.GetINodeByName("ST_Box002")
boundsTM = ugh.GetWorldTM()
boundsToCheck = ugh.GetObject().GetDeformBBox()
points = enumeratePoints(boundsToCheck,2)
debugBounds(points)