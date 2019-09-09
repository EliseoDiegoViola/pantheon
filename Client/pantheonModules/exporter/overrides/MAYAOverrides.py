

import maya.standalone as std
try:
    std.initialize(name='python')
except Exception:
    pass
    #print("Python is already included")
import maya.cmds as cmds

# std.initialize(name='python')
try:
    cmds.loadPlugin("fbxmaya", quiet =True)
except Exception:
    print("fbxmaya is already included")




import json
import maya.mel as mel
import os
import pymel.core as pm
import sys
import re
#mel.eval('source "namedCommandSetup.mel"')


#Pantheon Modules
from pantheonModules.logger.ateneaLogger import AteneaLogger
from pantheonModules.exporter.overrides import BaseOverrides
from pantheonModules.pantheonUtilities import fileSystemUtilities as fsu
from pantheonModules.exceptions.exportExceptions import CriticalExportException

from sets import Set
from datetime import datetime

class ExportUtilities(BaseOverrides.ExportUtilities):

    def __init__(self):
        # self.logger = ateneaLogger.AteneaLogger()
        self.meshUtilities = MeshesUtilities()

    @staticmethod
    def SetFBXParams():
        mel.eval('FBXResetExport') # This ensures the user's settings are ignored so that you can just set values which differ from the default
        mel.eval('FBXExportCameras -v false;')
        mel.eval('FBXExportLights -v false;')
        mel.eval('FBXExportShapes -v true;')
        mel.eval('FBXExportSkeletonDefinitions -v true;')
        mel.eval('FBXExportScaleFactor 1;')
        mel.eval('FBXExportSkins -v true;')
        mel.eval('FBXExportSmoothMesh -v true;')
        mel.eval('FBXExportEmbeddedTextures  -v false;')
        mel.eval('FBXExportUpAxis y;')

    @staticmethod
    def SetFBXParamsForAnimation():
        mel.eval('FBXResetExport') # This ensures the user's settings are ignored so that you can just set values which differ from the default
        #mel.eval('FBXExportAnimationOnly -v 1')  # DONT!
        mel.eval('FBXExportBakeComplexAnimation -v 1')
        mel.eval('FBXExportBakeComplexStart -v 0')
        mel.eval('FBXExportSkeletonDefinitions  -v 1')
        mel.eval('FBXExportBakeComplexEnd -v '+ str(clipLen))

    @staticmethod
    def ExportFBX(filePath):
        try:
            print(filePath +".fbx")            
            # self.logger.log("-file {0}.fbx - s".format(filePath))
            cmds.FBXExport('-file', filePath +".fbx", "-s")
            #MAYA MUST delete exported object becuse duplicate Names.

        except Exception as e:
            sys.stderr.write(str("ERROR EXPORTING! -> ") + str(e))
            try:
                sys.stderr.write(str(e))
                std.uninitialize()
                os._exit(-1)
            except SystemExit:
                pass 

    # def validateSelectedObjects(self,parents):
    #     objectValidity = []
    #     if not parents:
    #         objectValidity.append( (None,[lambda objects: ("001",[])]))
    #     for parent in parents:
    #         objectValidity.append( (parent,[lambda objects: ("000",[])]))

    #     return objectValidity


class MeshesUtilities(BaseOverrides.MeshesUtilities):

    # def __init__(self):
    #     self.logger = ateneaLogger.AteneaLogger()

    @staticmethod
    def GetAllChilds(parent,filt = None, includeParent = False):
        objs = []
        shapeList = []
        if filt:
            shapeList = cmds.listRelatives(cmds.ls(parent), ad = True, typ = filt,fullPath=True)
        else:
            shapeList = cmds.listRelatives(cmds.ls(parent), ad = True,fullPath=True)

        if not shapeList:
            shapeList = [] # Simple workaround

        transforms = []
        for shape in shapeList:
            transforms = transforms + cmds.listRelatives( shape , parent=True ,fullPath=True)

        transforms = list(set(transforms))

        return cmds.ls(transforms,uuid=True)
 

    @staticmethod
    def GetSubTree(parent,filt = None, includeParent = False):
        treeNode = {} #MAYBE CHANGE IT FOR A STRUCT?
        if cmds.listRelatives( cmds.ls(parent) , parent=True ,fullPath=True) or includeParent:
            if filt:
                if MeshesUtilities.GetObjectClass(cmds.ls(parent)) in filt:
                    treeNode["node"] = parent
            else:
                treeNode["node"] = parent
                
        children = []
        if cmds.listRelatives(cmds.ls(parent), typ=["transform"],fullPath=True):
            for obj in  cmds.listRelatives(cmds.ls(parent), typ=["transform"],fullPath=True):
                children.append(MeshesUtilities.GetSubTree(obj,filt))
        treeNode["children"] = children
            # objs.append()


        return treeNode 

    @staticmethod
    def GetChildren(parent):
        objs = cmds.ls(cmds.listRelatives(cmds.ls(parent),fullPath=True),uuid=True)
        if objs:
            return objs    
        else:
            return []

    @staticmethod
    def GetParent(obj):
        if obj:
            return cmds.ls(cmds.listRelatives( cmds.ls(obj) , parent=True),uuid=True)
        else:
            return None

    @staticmethod
    def GetObjectClass(obj):
        if cmds.listRelatives(cmds.ls(obj), s = True):
            return "shape"
        else:
            className = cmds.objectType(cmds.ls(obj)[0])
            return className

    # def getAllMaterials(self):
    #     return cmds.ls(mat =True)

    @staticmethod
    def GetAssignedMaterials(dagObject):
        mats = []
        shape = cmds.listRelatives(dagObject,s=True)
        shapeConnections = cmds.listConnections(shape, d=True, s=False , type="shadingEngine")
        if shapeConnections:
            shapeConnections = list(set(shapeConnections))
            mats = cmds.ls(cmds.listConnections(shapeConnections), mat =True)
        return mats



    @staticmethod
    def SelectFullObject(objToSelect , add = False):
        cmds.select(cmds.ls(objToSelect), hierarchy = True, add = add)
        return cmds.ls( selection=True )

    @staticmethod
    def MergeObjects(objects):
        if objects and len(objects) > 0:
            if len(objects) > 1:
                parent = MeshesUtilities.GetParent(objects[0])
                parentName = MiscUtilities.GetObjectName(parent)
                objToMerge = cmds.ls(objects,long=True)
                cmds.polyUnite(objToMerge, ch=False,name=parentName+"_mergedGeometry")
                #cmds.delete( ch=True )
                # if "deferred" in parentName : raise Exception()
                mergedGeometry = cmds.ls(parentName+"_mergedGeometry",uuid=True)
                #MiscUtilities.SetParent(mergedGeometry,parent)
                return mergedGeometry
            else:
                return objects[0]
        else:
            return None

    @staticmethod
    def GetAllMaterialsFromObjects(objects):
        # shapes = cmds.ls(objects,o=True, dag=True, s=True)
        # shadingEngines = cmds.listConnections(shapes,type="shadingEngine")
        # materials = cmds.ls(cmds.listConnections(shadingEngines),mat=True)
        # return list(set(materials))


        # mats = []
        # shape = cmds.ls(objects,o=True, dag=True, s=True)
        # shapeConnections = cmds.listConnections(shape, d=True, s=False , type="shadingEngine")
        # if shapeConnections:
        #     shapeConnections = list(set(shapeConnections))
        #     mats = cmds.ls(cmds.listConnections(shapeConnections), mat =True)
        # return list(mats)

        orderedMats = []
        for obj in objects:
            mats = []
            shape = cmds.listRelatives(cmds.ls(obj),s=True,fullPath=True)
            shapeConnections = cmds.listConnections(shape, d=True, s=False , type="shadingEngine")
            if shapeConnections:
                shapeConnections = list(set(shapeConnections))
                mats = cmds.ls(cmds.listConnections(shapeConnections), mat =True)

            if not mats:
                return []

            #Select all faces
            facesCount = cmds.polyEvaluate(cmds.ls(obj),f=True)
            cmds.select(cl=True)
            cmds.select(cmds.ls(obj)[0]+'.f[0:'+str(facesCount)+']')
            objectMats = []
            if len(mats) > 1: #There is a hidden bug  here, in tempgrps
                for mat in mats:
                    tempset = cmds.sets(facets = True,name = mat + "__" + cmds.ls(obj)[0])
                    tempgrps = cmds.listConnections(mat,type="shadingEngine")
                    filtered = cmds.sets (tempgrps,int=tempset)
                    # print mat
                    # print cmds.sets(tempset,query=True)
                    # print cmds.ls(tempgrps)
                    # print cmds.sets(tempgrps,query=True)
                    # print cmds.ls(filtered)
                    minimumFace = cmds.ls(filtered,flatten=True,head=1)[0]
                    print(minimumFace)
                    minimumIndex = re.search("(?:\[)(.*)(?=\])",minimumFace).group(1)
                    print(minimumIndex)
                    objectMats.append((minimumIndex,mat))
                    cmds.delete(tempset)
                objectMats.sort(key = lambda elem: int(elem[0])) 
                orderedMats.extend([objMat[1] for objMat in objectMats ])
            else:
                orderedMats.extend(mats)
        return orderedMats

    @staticmethod
    def SetPivotToPoss(obj,x,y,z):
        print("SETTING PIVOT!")
        print(obj)
        print(cmds.ls(obj))
        print(x,y,z)
        print("SETTING PIVOT!!!!!!!!!!!")
        cmds.xform(cmds.ls(obj), ws=True, piv=(x,y,z) )

    # @staticmethod
    # def ReorderMesh(node):
    #     print("ReorderMesh NOT IMPLEMENTED ============================================")

        # MAX_FACES = 10000
        # # meshesMaterialsIndexes = {}
        # # self.logger.log("Processing " + node.GetName())
        # # meshesMaterialsIndexes[str(node.GetName())] = {}
        # MiscUtilities.SelectObject(node)
        # obj = node.GetObject()
        # geo = obj.AsTriObject()
        # mesh = geo.GetMesh()
        # polyCount = MaxPlus.Core.EvalMAXScript("polyop.getNumFaces $").Get()

        # facesByMaterialId = {}
        # facesOffsetByMaterialId = {}


class LayersUtilities(BaseOverrides.LayersUtilities):

    exportableParents = ["transform"]
    exportableSkeleton = ["joint"]
    exportableMesh = ["shape"]

    garbageLayer = ["Blendshapes_lay","garbage"]

    def __init__(self):
        # self.logger = ateneaLogger.AteneaLogger()
        pass

    # def selectObjectsInLayers(self,*args,**kwargs):
    #     allTrans = cmds.ls(exactType = self.exportableParents)
    #     groups = []
    #     for trnas in allTrans:
    #         childShapes = cmds.listRelatives(trnas, s = True)
    #         if not childShapes:
    #             isRoot = cmds.listRelatives( trnas, p = True) == None
    #             if isRoot:
    #                 groups.append(trnas)

    #     cmds.select(groups, add = kwargs["add"])
    #     return groups

    @staticmethod
    def CleanGarbageLayer():
        for gLayer in LayersUtilities.garbageLayer:
            if cmds.objExists(gLayer):
                garbageNodes = cmds.editDisplayLayerMembers(gLayer, query=True, fn=True )
                if garbageNodes:
                    for blendGrp in garbageNodes:
                        if cmds.objExists(blendGrp):
                            cmds.delete(blendGrp )
                cmds.delete(gLayer)



class DataParser(BaseOverrides.DataParser):
    version = 1

    def __init__(self,output):
        # self.logger = ateneaLogger.AteneaLogger()
        # self.meshUtilities = MeshesUtilities()
        self.exportableMeshes = ["shape"]

        self.anims =[]
        self.events =[]
        self.matProps = {}

        # self.logger.log(output+'.jsonMats')
        if os.path.exists(output+'.jsonMats'):
            with open(output+'.jsonMats') as data_file:
                self.matProps = json.load(data_file)
        


        # self.logger.log(output+'.jsonAnim')
        if os.path.exists(output+'.jsonAnim'):
            with open(output+'.jsonAnim') as data_file:
                animData = json.load(data_file)
                self.anims = animData['animations']
                self.events = animData['events']

    def getRigType(self):
        return "ASSEMBLY3D"

    # def parseDataObject(self,objToParse):
    #     #RawData
    #     # rawMaterials = self.meshUtilities.getAssignedMaterials(objToParse)
    #     rawMaterials = self.meshUtilities.getAllMaterials()

    #     #structs for connections

    #     #---Meshes
    #     meshShaders = {}
    #     meshes = []
    #     #---Materials
    #     shaderToId = {}
    #     #---Animations
    #     animationDatas = []
    #     eventsDatas = []

    #     allObjects = [objToParse]
        
    #     #structs for JSON
    #     data = {}
    #     materials = []
    #     exporterObjectsData = []
        

            
    #     #FILE DATAS PARSING RAWMATERIALS
    #     for x in range(0,len(rawMaterials)):
    #         matProp = {}
    #         mat = rawMaterials[x]
    #         materialData = {}
    #         materialData["id"] = x
    #         materialData["name"] = str(mat)
    #         if self.matProps and str(mat) in self.matProps : matProp = self.matProps[str(mat)]
    #         materialData["properties"] = jsonStructures.getDataOrDefault(matProp,"properties",[])
    #         materialData["shaderName"] = jsonStructures.getDataOrDefault(matProp,"shaderName","Standard")                    
    #         materials.append(materialData)
    #         shaderToId[mat] = x

    #     #FILE DATAS PARSING ANIMATIONS
    #     for x in range(0,len(self.anims)):
    #         anim = self.anims[x]
    #         animID = x+1
    #         anim["clipLen"] = anim["clipEnd"] - anim["clipStart"]
    #         animationData = {}
    #         animationData["id"] = animID
    #         animationData["animName"] = anim["clipName"]
    #         animationData["animStart"] = 0
    #         animationData["animEnd"] = anim["clipLen"]
    #         animationData["animLoop"] = jsonStructures.getDataOrDefault(anim,"clipLoop","false")  
    #         animationData["animRoot"] = jsonStructures.getDataOrDefault(anim,"clipRoot","true")    
    #         animationDatas.append(animationData)

    #     #FILE DATAS PARSING EVENTS
    #     for x in range(0,len(self.events)):
    #         event = self.events[x]
    #         eventID = x + 1 
    #         eventData = {}
    #         eventData["id"] = eventID
    #         eventData["eventName"] = event["clipKeyEvent"]
    #         eventData["eventKey"] = event["clipKeyFrame"]
    #         eventsDatas.append(eventData)



    #     #SCENE OBJECT PARSING
    #     for objIndex in range(0,len(allObjects)):
    #         obj = allObjects[objIndex]
    #         nodeAttr = self.nodeAttribute(obj,'ObjectBaseData')

    #         expObjData = {}
    #         expObjData["id"] = objIndex
    #         expObjData["name"] = obj
    #         expObjData["meshes"] = []
    #         expObjData["animations"] = animationDatas# [] SEARCH THE CORRECT EVENTS FOR THIS OBJECT
    #         expObjData["events"] = eventsDatas# [] SEARCH THE CORRECT EVENTS FOR THIS OBJECT
    #         expObjData["type"] = nodeAttr.getCustomParameter("type")
    #         expObjData["subType"] = nodeAttr.getCustomParameter("subtype")
            
            
    #         meshes = self.meshUtilities.getAllChilds(obj,self.exportableMeshes) 
    #         if meshes:
            
    #             for i in range(0,len(meshes)):
    #                 meshData = {}
    #                 meshData["id"] = i
    #                 meshData["meshName"] = str(meshes[i])
    #                 meshMaterials = self.meshUtilities.getAssignedMaterials(meshes[i])
    #                 materialsIds = [{'materialId': shaderToId[x]} for x in meshMaterials]
    #                 meshData["materialIds"] = materialsIds
    #                 expObjData["meshes"].append(meshData) 

             

    #         exporterObjectsData.append(expObjData)

    #     data["materials"] = materials         
    #     data["objects"] = exporterObjectsData
    #     data["version"] = self.version

    #     return data

#### FOR ARRAY TYPE!
# cmds.addAttr( longName='colliders', numberOfChildren=4, attributeType='compound' )
# cmds.addAttr( longName='col0', dt ='string', parent='colliders' )
# cmds.addAttr( longName='col1', dt ='string', parent='colliders' )
# cmds.addAttr( longName='col2', dt ='string', parent='colliders' )
# cmds.addAttr( longName='col3', dt ='string', parent='colliders' )
####

    class nodeAttribute(BaseOverrides.DataParser.nodeAttribute):

        class ATTR_TYPES(BaseOverrides.DataParser.nodeAttribute.ATTR_TYPES):
            pass
        class attributeParameter(BaseOverrides.DataParser.nodeAttribute.attributeParameter):
            pass

        @staticmethod
        def IsDefined(node,attributeName):
            return True

        def __init__(self,node,attributeName):
            self._node = node
            self.attrName = attributeName

        @property
        def node(self):
            return cmds.ls(self._node)[0]

        @node.setter
        def node(self, value):
            self._node = value


        def addCustomParameter(self,parameterName,parameterValue,parameterType = ATTR_TYPES.STRING):
            parameterValue = self.castFrom(parameterValue,parameterType)

            if not parameterValue:
                print "Error casting parameter value to type ",parameterType
                return None

            cmds.select(self.node)
            exists = cmds.attributeQuery('{0}_{1}'.format(self.attrName,parameterName), node = self.node, ex=True)

            if exists:
                print ("Attribute {0}_{1} already not exists, cannot add!".format(self.attrName,parameterName))
                return None

            cmds.addAttr( longName="{0}_{1}".format(self.attrName,parameterName), dt ='string' ) #Maybe we need support different types...?
            cmds.setAttr('{0}.{1}_{2}'.format(self.node,self.attrName,parameterName), parameterValue , type="string")
            return parameterName


        def editCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            parameterValue = self.castFrom(parameterValue,parameterType)
            cmds.select(self.node)
            exists = cmds.attributeQuery('{0}_{1}'.format(self.attrName,parameterName), node = self.node, ex=True)

            if not parameterValue:
                print "Error casting parameter value to type ",parameterType
                return None

            if not exists:
                print ("Attribute {0}_{1} does not exists, cannot edit!".format(self.attrName,parameterName))
                return None

            cmds.setAttr('{0}.{1}_{2}'.format(self.node,self.attrName,parameterName), parameterValue , type="string")


        def getCustomParameter(self,parameterName):
            cmds.select(self.node)
            exists = cmds.attributeQuery('{0}_{1}'.format(self.attrName,parameterName), node = self.node, ex=True)
            if not exists:
                print ("Attribute {0}_{1} does not exists, cannot get!".format(self.attrName,parameterName))
                return None

            paramValue = cmds.getAttr('{0}.{1}_{2}'.format(self.node,self.attrName,parameterName))

            value,typ = self.castTo(paramValue)

            attrParam = self.attributeParameter()
            attrParam.parameterName=  parameterName
            attrParam.parameterValue =  value
            attrParam.parameterType = typ


            return attrParam

        def deleteCustomParameter(self,parameterName):
            cmds.select(self.node)
            print '{0}_{1}'.format(self.attrName,parameterName)
            exists = cmds.attributeQuery('{0}_{1}'.format(self.attrName,parameterName), node = self.node, ex=True)

            if not exists:
                print ("Attribute {0}_{1} does not exists, cannot delete!".format(self.attrName,parameterName))
                return None

            cmds.deleteAttr('{0}.{1}_{2}'.format(self.node,self.attrName,parameterName))

        def listCustomParametersNames(self):
            paremetersNames = []
            cmds.select(self.node)
            nodes =  cmds.listAttr( self.node, ud=True, u =True )
            if nodes:
                for param in nodes:
                    if param.split("_")[0] == self.attrName:
                        paremetersNames.append(param.split("_")[1])
            return paremetersNames

        def castTo(self, rawData): # {"typ":"","value":""}
            try:
                parsedData = json.loads(rawData)#.replace('\\"', '"'))
                dType = parsedData["typ"]
                if dType == self.ATTR_TYPES.STRING: 
                    value = parsedData["value"]
                    return value,dType
                elif dType == self.ATTR_TYPES.NODE: 
                    value = parsedData["value"]
                    node = value ##Get Node?
                    return node,dType
                elif dType == self.ATTR_TYPES.NUMBER:
                    value = parsedData["value"]
                    return value,dType
                elif dType == self.ATTR_TYPES.ARRAY: 
                    value = parsedData["value"]
                    return value,dType
                elif dType == self.ATTR_TYPES.BOOL: 
                    value = parsedData["value"]
                    return value,dType
                elif dType == self.ATTR_TYPES.NONE:
                    return None,dType
                else:
                    return None,dType
            except:
                return rawData,self.ATTR_TYPES.STRING

        def castFrom(self, data, newType):
            dataToSave = {}
            if newType == self.ATTR_TYPES.STRING:
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave)#.replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NODE:
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave)#.replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NUMBER:
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave)#.replace('"', '\\"')
            elif newType == self.ATTR_TYPES.ARRAY:
                if not data:
                    data = []
                if isinstance(data, list):
                    if len(data) > 0:
                        if all(isinstance(x, type(data[0])) for x in data):
                            dataToSave["typ"] = newType
                            dataToSave["value"] = data
                            return json.dumps(dataToSave)#.replace('"', '\\"')
                        else:
                            print "ARRAY elements should be all the same type", data
                            return None
                    else:
                        dataToSave["typ"] = newType
                        dataToSave["value"] = data
                        return json.dumps(dataToSave)#.replace('"', '\\"')
                else:
                    print "This",data,"is not type ARRAY", data
                    return None
                
            elif newType == self.ATTR_TYPES.BOOL: 
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave)#.replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NONE:
                return None
            else:
                print "ERROR , CAST FROM INVALID TYPE ", newType
                return None


class FileUtilities(BaseOverrides.FileUtilities):

    @staticmethod
    def GetFullFileName():
        fullName = cmds.file(q=True,exn=True).replace(".mb","").replace(".ma","")
        return fullName

    @staticmethod
    def GetFullPath():
        fullName = os.path.dirname(cmds.file(q=True,exn=True).replace(".mb","").replace(".ma",""))+"/"
        return fullName

    @staticmethod
    def OpenFile(filePath):
        cmds.file(filePath,o=1,f=1)
        return True
        # fullName = os.path.dirname(cmds.file(q=True,exn=True).replace(".mb","").replace(".ma",""))+"/"
        # return fullName

    @staticmethod
    def SaveFile(filepath):
        cmds.file(s=1,f=1)
        return True

    @staticmethod
    def GetFileArguments():
        filesToOpen = []
        if len(sys.argv) > 1:
            if "fto" in sys.argv[1]:
                filesArg = sys.argv[1]
                filesArg = filesArg.replace("fto=","")
                filesArg = filesArg.replace("\"","")
                filesArray = filesArg.split(",")
                filesToOpen = filesArray
        return filesToOpen

    # def GetFullPath(self):
    #     fullName = os.path.dirname(MaxPlus.FileManager.GetFileNameAndPath().replace(".3ds","").replace(".max",""))+"\\"
    #     return fullName   

    @staticmethod
    def optimizeScene():
        oldValue = "0";
        if "MAYA_TESTING_CLEANUP" in os.environ:
            oldValue = os.environ["MAYA_TESTING_CLEANUP"]

        os.environ["MAYA_TESTING_CLEANUP"] = "1"


        pm.mel.source('cleanUpScene')

        pm.mel.scOpt_performOneCleanup({
            'unknownNodesOption',
            'shadingNetworksOption',
            'renderLayerOption',
            'displayLayerOption',
            'shaderOption'
            }
        )
        os.environ["MAYA_TESTING_CLEANUP"] = oldValue


class MiscUtilities(BaseOverrides.MiscUtilities):

    @staticmethod
    def Exit(exitCode):
        try:
            std.uninitialize()
            os._exit(exitCode)
        except Exception:
            print "CANNOT EXIT"
        
    
    @staticmethod
    def GetAllSceneMaterials():
        sceneMaterials = []
        mats = cmds.ls(mat=True)
        for mat in mats:
            sceneMaterials.append(mat)

        return sceneMaterials

    @staticmethod
    def GetMaterialMaps(mat):
        maps = Set()
        fileNode = cmds.listConnections(mat,type='file')
        if fileNode:
            for fNode in fileNode:
                path = cmds.getAttr(fNode+".fileTextureName")
                filename, file_extension = os.path.splitext(path)
                if  file_extension == ".tga" or file_extension == ".psd" or file_extension == ".png":
                    maps.add(os.path.basename(path))
        return list(maps)



    @staticmethod
    def GetObjectName(obj):
        foundObjects = cmds.ls(obj,long=False)
        if foundObjects:
            return foundObjects[0].split('|')[-1]
        else:
            return None

    @staticmethod    
    def SetObjectName(obj,name):
        print cmds.ls(obj)
        print obj
        cmds.rename(cmds.ls(obj), name)
        return obj#name

    @staticmethod
    def GetRootObjects():
        allTrans = cmds.ls(exactType = "transform")
        parents = []
        for trnas in allTrans:
            childShapes = cmds.listRelatives(trnas, s = True)
            if not childShapes:
                isRoot = cmds.listRelatives( trnas, p = True) == None
                if isRoot:
                    parents.append(trnas)
        cmds.select(parents)
        return cmds.ls(parents,uuid=True)

    

    @staticmethod
    def SelectObject(*nodes):
        cmds.select()
        for node in nodes:
            cmds.select(node, add = True)
        
    @staticmethod    
    def ImportReferences():
        refs = cmds.ls(type='reference')
        for ref in refs:
            if not cmds.listConnections(ref):
                cmds.lockNode( ref, lock=False )
                cmds.delete(ref)
            else:     
                rFile = cmds.referenceQuery(ref, f=True)
                cmds.file(rFile, importReference=True)
        
        namespaces =  set([str(n.split(":")[0]) for n in cmds.ls( type='joint' ) if len(n.split(":")) > 1])
        # print namespaces
        for ns in namespaces:
            cmds.namespace( removeNamespace = ":"+ns, mergeNamespaceWithRoot = True)

    @staticmethod    
    def AddTemporalNamespace(obj):
        variation = 0;
        while cmds.namespace(exists = "temporalNamespace"+str(variation)):
            variation = variation + 1
        
        cmds.namespace( addNamespace = "temporalNamespace"+str(variation))
        newName = cmds.rename(cmds.ls(obj), "temporalNamespace"+str(variation)+":"+cmds.ls(obj)[0])
        return cmds.ls(newName,uuid=True)[0]
    
    @staticmethod  
    def GetNamespce(obj):
        if isinstance(obj,list) and len(obj) == 1:
            obj = obj[0]
            namespaces =  str(obj.split(":")[0])
            return namespaces
        return None

    @staticmethod    
    def RemoveNamespace(obj):
        if isinstance(obj,list) and len(obj) == 1:
            obj = cmds.ls(obj[0])[0]
            namespace = str(obj.split(":")[0])
            finalName = str(obj.split(":")[-1])
            if cmds.namespace(exists = ":"+namespace):
                cmds.namespace( removeNamespace = ":"+namespace, mergeNamespaceWithRoot = True)
            else:
                print(finalName , " HAS NO NAMESPACE")
            return finalName
        return None

    @staticmethod
    def SetParent(obj,parent):
        relatives = cmds.listRelatives( cmds.ls(obj) , parent=True,fullPath=True )
        if not relatives or cmds.ls(parent, long = True)[0] not in relatives:
            cmds.parent(cmds.ls(obj),cmds.ls(parent))
            return obj
        else:
            print "Cannot reparent"
            return obj
           
    @staticmethod        
    def TakeObjectToWorldRoot(obj):
        if cmds.listRelatives( cmds.ls(obj), p = True) != None :
            return cmds.parent(cmds.ls(obj),world=True) [0]
        else:
            print "Wont reparent, object is already in root"
            return obj


    @staticmethod
    def GetLocalPosition(obj):
        return cmds.xform( cmds.ls(obj),query=True,translation=True,objectSpace=True) #cmds.pointPosition( obj, l=True )


    @staticmethod        
    def CleanSkeleton(objsToConserve,typesToExclude):
        print "ABOUT TO CLEAN!"
        for objToConserve in objsToConserve:
            if cmds.objExists('{0}'.format(objToConserve)):
                cmds.select('{0}'.format(objToConserve) ,hi = True) #SelectFullObject
                selection = cmds.ls( selection=True )
                print "ABOUT TO CLEAN0 !",selection
                #cmds.bakeResults(selection , simulation = True , time = (startTime,endTime))
                for typeToExcl in typesToExclude:
                    selection = [x for x in selection if x in cmds.ls(type=typeToExcl)] #we excludes all the constraints
                print "ABOUT TO CLEAN1 !",selection 
                garbage = selection # [gb for gb in cmds.ls( selection=False, transforms=True,shapes=True,geometry=True,materials=True) if gb not in selection]
                for g in garbage:
                    if cmds.objExists(g):
                        cmds.delete(g)

    @staticmethod
    def CheckEZMatsFile():
        return os.path.exists(FileUtilities.GetFullFileName()+'.jsonMats')
        # if os.path.exists(FileUtilities.GetFullFileName()+'.jsonMats'):
        #     return ("000",[])
        # else:
        #     return ("200",[])

    @staticmethod
    def CheckModifiers(parent):
        print("CheckModifiers NOT IMPLEMENTED ============================================")
        return ("000",[])

    # @staticmethod
    # def CheckAttributes(parent):
    #     allObjects = [parent]
    #     for objIndex in range(0,len(allObjects)):
    #         objName = str(allObjects[objIndex])

    #         baseData = DataParser.nodeAttribute(objName,'ObjectBaseData')
    #         objType = baseData.getCustomParameter("type")
    #         objSubType = baseData.getCustomParameter("subType")

    #         if (objType == None or objSubType == None):
    #             return False
    #             # return ("201",[parent.GetName()])
    #     # return ("000",[])
    #     return True


    @staticmethod
    def GetCurrentSelection():
        return cmds.ls(sl=True,uuid=True);

    @staticmethod
    def DeleteObject(objectToDelete, childrenPositionStays = False, keepChildren = True):
        if keepChildren:
            children = cmds.listRelatives(cmds.ls(objectToDelete), fullPath=True)
            print "CHILDREN ", children
            childOldPositions = {}
            if children:
                for child in children:
                    childOldPositions[child] = cmds.xform( child,query=True,translation=True,worldSpace=True)
                    childOldPositions[MiscUtilities.TakeObjectToWorldRoot(child)] = childOldPositions.pop(child) 
        
        cmds.delete(cmds.ls(objectToDelete))
        
        if childrenPositionStays:
            for child in childOldPositions.keys():
                cmds.move(childOldPositions[child][0],childOldPositions[child][1],childOldPositions[child][2], child, worldSpace=True )

            # child.SetWorldPosition(childOldPositions[child])


    @staticmethod
    def DeleteMaterial(matToDelete):
        cmds.delete(matToDelete)

    @staticmethod
    def CreateMaterial(matName,matData,mapTable = None):
        equivalenceShaderTable = {}
        equivalenceShaderTable["_MainTex"] = ("use_color_map","TEX_color_map")
        equivalenceShaderTable["_MetallicGlossMap"] = ("use_metallic_map","TEX_metallic_map")
        equivalenceShaderTable["_BumpMap"] = ("use_normal_map","TEX_normal_map")
        equivalenceShaderTable["_ParallaxMap"] = ("use_roughness_map","TEX_roughness_map")
        equivalenceShaderTable["_OcclusionMap"] = ("use_ao_map","TEX_ao_map")
        equivalenceShaderTable["_EmissionMap"] = ("use_emissive_map","TEX_emissive_map")
        equivalenceShaderTable["_DetailMask"] = ("","")
        equivalenceShaderTable["_DetailAlbedoMap"] = ("","")
        equivalenceShaderTable["_DetailNormalMap"] = ("","")

        shader = cmds.shadingNode('StingrayPBS', asShader=True,  name=matName)

        mel.eval("shaderfx -sfxnode \""+shader+"\" -initShaderAttributes") #Probably..... not the best way


        maya = FileUtilities.GetFullPath()
        # shader = matData["shaderName"]

       
        matDataProperties = [prop for prop in serverMat.properties if prop.propType == "TexEnv"]
        newMaterialMaps = [param for param in equivalenceShaderTable]

        mainTexProp = next((x for x in matDataProperties if x.propName == "_MainTex"), None)
        diffuseMapParam = next((x for x in newMaterialMaps if x[1] == "TEX_color_map"), None)

        # for matMap in newMaterialMaps:
        #     print matMap.setValue()
        #     matMap.setValue(None)


        #ONLY PUT _MainTex ON diffuseMap , EVERYTHING ELSE ON RANDOM SLOTS.
        if diffuseMapParam and mainTexProp:
            matDataProperties.remove(mainTexProp)
            matDataProperties.insert(0,mainTexProp)
            newMaterialMaps.remove(diffuseMapParam)
            newMaterialMaps.insert(0,diffuseMapParam)

        if len(matDataProperties) > len(newMaterialMaps):
            print "We have to left out behind some maps...."

        for i in range(min(len(matDataProperties),len(newMaterialMaps))):
            prop = matDataProperties[i]
            matMap = newMaterialMaps[i]

            textureName = prop.propValue
            propName = prop.propName
            
            if not textureName : continue
            texturePath = fsu.findFileInParents(textureName,maya,"/Textures")
            # print textureName
            # print maya

            

            if not texturePath : 
                MiscUtilities.DeleteMaterial(shader)
                shader = None
                break

            if equivalenceShaderTable[propName][0]: 
                # print("ACTIVATE :" + shader+"."+equivalenceShaderTable[propName][0])
                cmds.setAttr('%s.%s' %(shader,equivalenceShaderTable[propName][0]), True)

                fileNodeName = 'file'
                file_node=cmds.shadingNode(fileNodeName,asTexture=True)
                
                # print("ASSIGN : " +file_node + " TO " + texturePath)
                cmds.setAttr( file_node +'.fileTextureName', texturePath, type = "string")
                cmds.connectAttr('%s.outColor' %file_node,shader+"."+equivalenceShaderTable[propName][1])

        if shader:
            sg = cmds.sets(renderable=True, noSurfaceShader=True, name='%sSG'%(matName))
            cmds.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %sg)

            return sg
        else:
            return None

    @staticmethod
    def SelectMaterial(material): 
        cmds.select(material)

    @staticmethod
    def ResetMaterial(material,matData,mapTable = None):
        print("ResetMaterial NOT IMPLEMENTED ============================================") 


        

class AnimationUtilities(BaseOverrides.AnimationUtilities):

    unlockDefault = ['joint','scaleConstraint','parentConstraint','pointConstraint']

    @staticmethod
    def IsMeshSkinned(obj):
        attributes = cmds.listHistory(cmds.ls(obj))
        for attribute in attributes:
            if cmds.objectType(attribute) == "skinCluster":
                return True
        return False
        

    def __init__(self, rootName):
        self.backupLayerName = "BackUpAnimationLayer"
        self.baseAnimation = "BaseAnimation"
        self.startTime = int(cmds.playbackOptions(query = True, minTime=True))
        self.endTime = int(cmds.playbackOptions(query = True, maxTime=True))
        self.rootName = rootName
        # self.hasAnimation = self.__hasAnimations()

    def __selectBaseLayer(self):
        cmds.animLayer(self.baseAnimation,edit=True,lock = False, mute=False, selected=True)
        cmds.animLayer(self.backupLayerName,edit=True, lock = True, mute=True, selected=False)
    
    def __selectBckupLayer(self):
        cmds.animLayer(self.backupLayerName,edit=True,lock = False, mute=False, selected=True)
        cmds.animLayer(self.baseAnimation,edit=True,lock = True, mute=True,  selected=False)

    def setupLayers(self):
        cmds.select("|{0}".format(self.rootName), hi = True)
        selection = cmds.ls(selection=True)

        cmds.animLayer("ProxyLayer",addSelectedObjects=True)
        cmds.setAttr('ProxyLayer.rotationAccumulationMode',0)
        cmds.setAttr('ProxyLayer.scaleAccumulationMode',1)
        cmds.animLayer(self.backupLayerName,copy=self.baseAnimation)
        cmds.delete( "ProxyLayer")
        self.__selectBaseLayer()
        cmds.cutKey(selection, time = (self.startTime+1,self.endTime))

    def __copyAnimationToExportLayer(self,clipStart,clipEnd,clipLen):
        cmds.select("|{0}".format(self.rootName), hi = True)
        selection = cmds.ls(selection=True)

        cmds.playbackOptions( min=self.startTime,ast=self.startTime ,max=self.endTime, aet=self.endTime)

        self.__selectBckupLayer()
        cmds.cutKey(selection, time = (clipStart,clipEnd))
        
        self.__selectBaseLayer()
        cmds.pasteKey(selection , time = (0,0))
        cmds.playbackOptions( min=0,ast=0 ,max=clipLen, aet=clipLen)

    @staticmethod
    def HasAnimations():

        allObjects = cmds.ls()
        hasAnims = False
        startTime = int(cmds.playbackOptions(query = True, minTime=True))
        endTime = int(cmds.playbackOptions(query = True, maxTime=True))

        for obj in allObjects:
            startTime = int(cmds.playbackOptions(query = True, minTime=True))
            endTime = int(cmds.playbackOptions(query = True, maxTime=True))
            animKeys = cmds.keyframe( obj , time=(startTime,endTime), query=True, valueChange=True, timeChange=True)
            hasAnims = hasAnims or animKeys is not None;
            if hasAnims : break
        
        return hasAnims

    @staticmethod
    def UnlockObjectsByType(*args):
        objs = []
        for arg in args:
            objs = objs + cmds.ls(typ=arg)
        AnimationUtilities.UnlockObjects(objs)

    @staticmethod
    def UnlockObjects(objs):
        for obj in objs:
            exists = True#cmds.attributeQuery('{0}.tx'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.tx'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.ty'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.ty'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.tz'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.tz'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.rx'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.rx'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.ry'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.ry'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.rz'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.rz'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.sx'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.sx'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.sy'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.sy'.format(cmds.ls(obj)[0]), l=False,k=True)
            exists = True#cmds.attributeQuery('{0}.sz'.format(obj), node = obj, ex=True)
            if exists: cmds.setAttr ('{0}.sz'.format(cmds.ls(obj)[0]), l=False,k=True)

    @staticmethod
    def BakeAnimations(objectsToBake):
        startTime = int(cmds.playbackOptions(query = True, minTime=True))
        endTime = int(cmds.playbackOptions(query = True, maxTime=True))

        cmds.bakeResults(objectsToBake , simulation = True , time = (startTime,endTime))

    @staticmethod
    def PrepareAnimationsForExport(objectName):
        startTime = int(cmds.playbackOptions(query = True, minTime=True))
        endTime = int(cmds.playbackOptions(query = True, maxTime=True))

        clipLen = endTime - startTime

        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0), attribute='translateX' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0),  attribute='translateY' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0),  attribute='translateZ' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0), attribute='rotateX' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0),  attribute='rotateY' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(0,0), attribute='rotateZ' )
        cmds.keyTangent( inTangentType='linear')
        
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='translateX' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='translateY' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='translateZ' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='rotateX' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='rotateY' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '{0}'.format(cmds.ls(objectName)[0]), time=(clipLen,clipLen), attribute='rotateZ' )
        cmds.keyTangent( outTangentType='linear')

        # parentNode = cmds.createNode( 'transform', n=os.path.basename(cmds.file(q=True,exn=True)).replace(".ma","") )
        # cmds.parent( '|{0}'.format(objectName) ,parentNode)
        # realParent = cmds.createNode( 'transform', n="Anim_" + os.path.basename(cmds.file(q=True,exn=True)).replace(".ma","") )
        # cmds.parent( '|{0}'.format(parentNode) ,realParent)

            
class CallBackUtilities(BaseOverrides.CallBackUtilities):
    pass