
#Native modules
import json
import urllib2 as url
import os
import copy
import sys
import traceback
import random
import re
from sets import Set
from datetime import datetime

#Pantheon Modules
from pantheonModules.logger.ateneaLogger import AteneaLogger
from pantheonModules.exporter.overrides import BaseOverrides
from pantheonModules.pantheonUtilities import fileSystemUtilities as fsu
from pantheonModules.exceptions.exportExceptions import CriticalExportException

#3DSMax Modules
import MaxPlus
from pymxs import runtime as rt

rt.preferences.enableTMCache=False

# Maxscript helper Definitions
# MaxPlus.Core.EvalMAXScript("fn b2a b = (return b as Array)")



class ExportUtilities(BaseOverrides.ExportUtilities):

    def __init__(self):
        # AteneaLogger = ateneaLogger.AteneaLogger()
        self.meshUtilities = MeshesUtilities()

    @staticmethod
    def SetFBXParams():
        rt.pluginManager.loadClass(rt.FBXEXPORTER)
        rt.FBXExporterSetParam("Animation",False)
        rt.FBXExporterSetParam("Animation", False)
        rt.FBXExporterSetParam("ASCII", False)
        rt.FBXExporterSetParam("BakeAnimation", False)
        rt.FBXExporterSetParam("BakeFrameStart", 0)
        rt.FBXExporterSetParam("BakeFrameEnd", 0)
        rt.FBXExporterSetParam("BakeFrameStep", 0)
        rt.FBXExporterSetParam("BakeResampleAnimation", False)
        rt.FBXExporterSetParam("Cameras", False)
        rt.FBXExporterSetParam("CAT2HIK", False)
        rt.FBXExporterSetParam("ColladaTriangulate", True)
        rt.FBXExporterSetParam("ColladaSingleMatrix", False)
        rt.FBXExporterSetParam("ColladaFrameRate", 0)
        rt.FBXExporterSetParam("Convert2Tiff", False)
        rt.FBXExporterSetParam("ConvertUnit", "m")
        rt.FBXExporterSetParam("EmbedTextures", False)
        rt.FBXExporterSetParam("FileVersion", "FBX201400")
        rt.FBXExporterSetParam("FilterKeyReducer", False)
        rt.FBXExporterSetParam("GeomAsBone", False)
        rt.FBXExporterSetParam("GenerateLog", True)
        rt.FBXExporterSetParam("Lights", False)
        rt.FBXExporterSetParam("NormalsPerPoly", False)
        rt.FBXExporterSetParam("PointCache", False)
        rt.FBXExporterSetParam("Preserveinstances", True)
        rt.FBXExporterSetParam("Removesinglekeys", False)
        rt.FBXExporterSetParam("ScaleFactor", 1)
        rt.FBXExporterSetParam("Shape", False)
        rt.FBXExporterSetParam("Skin", False)
        rt.FBXExporterSetParam("ShowWarnings", True)
        rt.FBXExporterSetParam("SmoothingGroups", False)
        rt.FBXExporterSetParam("SmoothMeshExport", False)
        rt.FBXExporterSetParam("TangentSpaceExport", True)
        rt.FBXExporterSetParam("Triangulate", True)
        rt.FBXExporterSetParam("UpAxis", "Y")
        rt.FBXExporterSetParam("UseSceneName", False)

    @staticmethod
    def ExportFBX(filePath):
        ExportUtilities.SetFBXParams()
        try:
            # AteneaLogger.log("LOADED CLASSES")
            # for cl in rt.exporterPlugin.classes:
            #     AteneaLogger.log(str(cl))
            pathToSave = filePath.replace("\\","\\\\")+".fbx"
            rt.exportFile(pathToSave,rt.name("noprompt"), selectedOnly=True,using=rt.FBXEXP)
            AteneaLogger.log("Saving... {0}".format(pathToSave))
        except Exception as e:
            file = FileUtilities.GetFullFileName()
            errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',ExportUtilities.ExportFBX.__name__)).lower()
            raise CriticalExportException(file,errorSpace,"Error Exporting, the reason could not be determined, call the developer")
        

    # def getFBXData(self,filePath):
    #     ExportUtilities.SetFBXParams()
        
    #     objData = "ERROR"
    #     try:            
    #         AteneaLogger.log("exportFile \""+filePath.replace("\\","\\\\")+".fbx"+"\"  #noprompt selectedOnly:true using:FBXEXP")
    #         MaxPlus.Core.EvalMAXScript("exportFile \""+filePath.replace("\\","\\\\")+".fbx"+"\"  #noprompt selectedOnly:true using:FBXEXP")
    #         #sys.stdout.write("|OUTPUTFILE|"+filePath +".fbx\n")
    #         if os.path.exists(filePath+'.fbx'):
    #             with open(filePath+'.fbx','rb') as fbx_data_file:
    #                 objData =  fbx_data_file.read()
    #             os.remove(filePath+'.fbx')
    #     except Exception as e:
    #         file = FileUtilities.GetFullFileName()
    #         errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',ExportUtilities.ExportFBX.__name__)).lower()
    #         raise CriticalExportException(file,errorSpace,"Error Exporting, the reason could not be determined, call the developer")
        
    #     return objData.encode('base64')
    
    # def getOBJData(self,filePath,objToExport): 
    #     MeshesUtilities.SelectFullObject(objToExport)

    #     objData = "ERROR"
    #     try:              
    #         AteneaLogger.log("exportFile \""+filePath.replace("\\","\\\\")+".obj"+"\" #noprompt selectedOnly:true ")
    #         MaxPlus.Core.EvalMAXScript("exportFile \""+filePath.replace("\\","\\\\")+".obj"+"\" #noprompt selectedOnly:true ")
    #         if os.path.exists(filePath+'.obj'):
    #             with open(filePath+'.obj','r') as obj_data_file:
    #                 objData =  obj_data_file.read()
    #             os.remove(filePath+'.obj')

    #     except Exception as e:
    #         sys.stderr.write(str("ERROR EXPORTING! -> ") + str(e))
    #         try:
    #             sys.exit(-1)
    #         except SystemExit:
    #             pass 
        
    #     return objData    

class MeshesUtilities(BaseOverrides.MeshesUtilities):

    exportableMeshes = ["Editable Poly"]

    def __init__(self):
        pass

    @staticmethod
    def GetAllChilds(parent,filt = None, includeParent = False):
        objs = []
        # if includeParent:
        #     objs.append(parent)
        if not parent.GetIsRoot() or includeParent:
            if filt:
                if parent.GetObject().GetClassName() in list(filt):
                    objs.append(parent)                 
            else:
                objs.append(parent)
        for obj in  parent.Children:
            objs = objs + MeshesUtilities.GetAllChilds(obj,filt)


        return objs 

    @staticmethod
    def GetSubTree(parent,filt = None, includeParent = False):
        treeNode = {} #MAYBE CHANGE IT FOR A STRUCT?
        if not parent.GetIsRoot() or includeParent:
            if filt:
                filValid = False
                if parent.GetDerivedObject():
                    filValid = parent.GetDerivedObject().GetObjRef().GetClassName() in list(filt)
                else:
                    filValid = parent.GetObject().GetClassName() in list(filt)
                
                if filValid:
                    treeNode["node"] = parent
            else:
                treeNode["node"] = parent
                
        children = []
        for obj in  parent.Children:
            children.append(MeshesUtilities.GetSubTree(obj,filt))
        treeNode["children"] = children
            # objs.append()


        return treeNode 


    @staticmethod
    def GetChildren(parent):
        if parent.Children:
            objs = list(parent.Children)        
            return objs

    @staticmethod
    def GetParent(obj):
        if obj and not obj.GetIsRoot() and not obj.GetParent().GetIsRoot() :
            return obj.GetParent()
        else:
            return None


    @staticmethod
    def GetObjectClass(obj):
        className = obj.GetBaseObject().GetClassName()
        return className

    @staticmethod
    def ReorderMesh(node): # 101 seg -> 1.34 seg
        # AteneaLogger.log("Reorder Meshes New NEW")
        # MAX_FACES = 10000
        AteneaLogger.log("Processing " + node.GetName())
        # meshesMaterialsIndexes[str(node.GetName())] = {}
        
        nativeNode = MiscUtilities.GetNativeFromINode(node)
        rt.convertToPoly(nativeNode)
        # obj = node.GetObject()
        # geo = obj.AsTriObject()
        # mesh = geo.GetMesh()
        
        facesByMaterialId = {}
        facesOffsetByMaterialId = {}
        objectMaterial = nativeNode.material
        if not objectMaterial:
            AteneaLogger.log("{0} Has no material".format(nativeNode.name))
            return
            # file = FileUtilities.GetFullFileName()
            # errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.ReorderMesh.__name__)).lower()
            # raise CriticalExportException(file,errorSpace,"Error accessing '{0}' mesh material , it probably have no material assigned".format(nativeNode.name))

        try:
            rt.convertToPoly(nativeNode)
            maxIndex = rt.getNumSubMtls(objectMaterial)
            if maxIndex > 0:
                for matID in range(1,maxIndex+1):
                    nativeNode.selectByMaterial(matID)
                    selectedFaces = rt.getFaceSelection(nativeNode)
                    
                    
                    if [(index+1) for index in range(selectedFaces.count) if selectedFaces[index] == True]:
                        newName = nativeNode.name + "-DETACHED-" + str(matID)
                        rt.polyOp.detachFaces(nativeNode,selectedFaces,asNode=True,name=newName)
                        detachedFaces = rt.getnodebyname(newName)
                        facesByMaterialId[matID] = detachedFaces


                sortedMatIds = sorted(facesByMaterialId.keys())
                for matID in range(0,len(sortedMatIds)):
                    detFaces = facesByMaterialId[sortedMatIds[matID]]
                    #rt.convertToMesh(detFaces)
                    #rt.convertToPoly(detFaces)
                    rt.polyop.attach(nativeNode,detFaces)
            AteneaLogger.log("{0} is done".format(nativeNode.name))

        except Exception as e:
            file = FileUtilities.GetFullFileName()
            errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.ReorderMesh.__name__)).lower()
            raise CriticalExportException(file,errorSpace,"Error reordering '{0}' mesh , if you cant find anything wrong try to make a snapshot of it".format(nativeNode.name))


    @staticmethod
    def GetAllMaterialsFromObjects(objects):
        objectMaterials = []
        for obj in objects:
            mat = obj.GetMaterial()
            if mat:
                if mat.GetNumSubMtls() > 0:
                    for i in range(0,mat.GetNumSubMtls()):
                        subMtl = mat.GetSubMtl(i)
                        if subMtl:
                            nativeNode = MiscUtilities.GetNativeFromINode(obj) #AT ONE POINT I SHOULD USE NATIVE NODE EVERYWHERE AND STOP CASTING
                            rt.convertToPoly(nativeNode)
                            nativeNode.selectByMaterial(i+1)
                            selectedFaces = rt.getFaceSelection(nativeNode)
                            facesCount = [(index+1) for index in range(selectedFaces.count) if selectedFaces[index] == True]
                            if facesCount:
                                objectMaterials.append(subMtl)
                            else:
                                print "{0} object has no faces for id {1}".format(nativeNode.name,i+1)
                else:
                    if mat.GetName() not in [m.GetName() for m in objectMaterials]:
                        objectMaterials.append(mat)
                    
        return list(objectMaterials)

    
    

    @staticmethod
    def SelectFullObject(objToSelect , add = False):
        nodes = MaxPlus.INodeTab ()
        if objToSelect:
            objectsToSelect = MeshesUtilities.GetAllChilds(objToSelect,includeParent=True)
            for nodeToAppend in objectsToSelect:
                nodes.Append(nodeToAppend)

        if not add:
            MaxPlus.SelectionManager.ClearNodeSelection()
        else:
            nodesToAdd = MaxPlus.SelectionManager.GetNodes()
            for nodeToAdd in nodesToAdd:
                nodes.Append(nodeToAdd)

        MaxPlus.SelectionManager.SelectNodes(nodes)
        return nodes 


    @staticmethod
    def MergeObjects(objects): # 103 seg -> 7 seg
        if len(objects) == 0:
            return None

        MiscUtilities.SelectObject(*objects)    
        allNativeNodes = rt.selection



        AteneaLogger.log("Mergin Objects: " + str(len(allNativeNodes)))
        while len(allNativeNodes) > 1: 
            forNextIter = []
            selcount = len(allNativeNodes)
            if selcount % 2 != 0:
                forNextIter.append(allNativeNodes[0])
            for i in range(selcount-1,0,-2):
                try:

                    obj0 = allNativeNodes[i]
                    obj1 = allNativeNodes[i-1]

                    rt.maxOps.CollapseNode(obj0,True)
                    rt.convertToPoly(obj0)
                    rt.maxOps.CollapseNode(obj1,True)
                    rt.convertToPoly(obj1)

                    

                    rt.polyop.attach(obj0,obj1)    
                    forNextIter.append(obj0)
                except Exception as e:
                    file = FileUtilities.GetFullFileName()
                    errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.MergeObjects.__name__)).lower()
                    raise CriticalExportException(file,errorSpace,"Error merging objects '{0}' and '{1}' , probably one of those are not Editable Poly or have weird modifiers".format(obj0.name,obj1.name))

            allNativeNodes = forNextIter    
        
        

        finalObject = allNativeNodes[0]


        try:
            deadFacesBitArray = rt.polyop.getDeadFaces(finalObject)
            if not deadFacesBitArray.IsEmpty:
                fixDeadFacesCommand = rt.polyop.CollapseDeadStructs(finalObject)
                AteneaLogger.log("Found dead faces on: " + str(finalObject.name))
        except Exception as e:
            file = FileUtilities.GetFullFileName()
            errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.MergeObjects.__name__)).lower()
            raise CriticalExportException(file,errorSpace,"Error trying dead faces in '{0}' , try to make a snapshot of this poly and every other poly in the same hierarchy level ".format(finalObject.name))


        return MiscUtilities.GetINodeFromNative(finalObject)

    @staticmethod
    def SetPivotToPoss(obj,x,y,z):
        nodes = MaxPlus.INodeTab ()
        MaxPlus.SelectionManager.ClearNodeSelection()
        nodes.Append(obj)
        MaxPlus.SelectionManager.SelectNodes(nodes)
        rt.selection[0].pivot = rt.Array(*(x, y, z))        
        # MaxPlus.Core.EvalMAXScript("$.pivot = [{0},{1},{2}]".format(x,y,z))

class LayersUtilities(BaseOverrides.LayersUtilities):

    exportableSkeleton = [""]
    exportableParents = ["Dummy"]
    exportableMesh = ["Editable Poly","Editable Mesh"]

    garbageLayers = ["garbage", "blocking", "dressing"]   # MOVE TO A GLOBAL CONFIG

    def __init__(self):
        pass
        

    def loadAllLayerNames(self):
        excludes = self.garbageLayers
        layerNames = []
        layerCount = MaxPlus.LayerManager.GetNumLayers()
        for i in range(0,layerCount):
            layer = MaxPlus.LayerManager.GetLayer(i)
            if( layer.GetName() not in excludes):
                layerNames.append(str(layer.GetName()))
        return layerNames

    @staticmethod
    def CleanGarbageLayer():
        MaxPlus.SelectionManager.ClearNodeSelection()
        layerCount = MaxPlus.LayerManager.GetNumLayers()
        deleteLayers = []
        for i in range(0,layerCount):
            layer = MaxPlus.LayerManager.GetLayer(i)
            for garbageLayer in LayersUtilities.garbageLayers:
                if(layer.GetName().lower() == garbageLayer.lower()):
                    layerNodes = layer.GetNodes()
                    for j in range(0,layerNodes.GetCount()):
                        layerNodes.GetItem(j).Delete()
                    deleteLayers.append(layer.GetName())

        for deleteLayer in deleteLayers:
            MaxPlus.LayerManager.DeleteLayer(deleteLayer)
                




class DataParser(BaseOverrides.DataParser):
    
    version = 1
    exportableMeshes = ["Editable Poly"]

    def __init__(self,output):
        # self.logger = AteneaLogger.AteneaLogger()
        self.meshUtilities = MeshesUtilities()

        self.anims =[]
        self.events =[]
        self.matProps = {}

        AteneaLogger.log(output+'.jsonMats')
        if os.path.exists(output+'.jsonMats'):
            with open(output+'.jsonMats') as data_file:
                self.matProps = json.load(data_file)
        


        AteneaLogger.log(output+'.jsonAnim')
        if os.path.exists(output+'.jsonAnim'):
            with open(output+'.jsonAnim') as data_file:
                animData = json.load(data_file)
                self.anims = animData['animations']
                self.events = animData['events']


    class nodeAttribute(BaseOverrides.DataParser.nodeAttribute):

        class ATTR_TYPES(BaseOverrides.DataParser.nodeAttribute.ATTR_TYPES):
            pass

        class attributeParameter(BaseOverrides.DataParser.nodeAttribute.attributeParameter):
            pass
        

        @staticmethod
        def IsDefined(node,attributeName):
            for i in xrange(node.NumModifiers):
                currMod = node.GetModifier(i)
                if currMod.GetName() == attributeName:
                    return True
            return False

        # ATTRIBUTE_TYPES = BaseOverrides.DataParser.nodeAttribute.ATTR_TYPES

        def __init__(self,node,attributeName):
            # print dir(BaseOverrides.DataParser.nodeAttribute)
            # print "AAAAA ", self.ATTR_TYPES.STRING
            # print "AAAAA ", ATTR_TYPES.STRING
            self.node = node
            self.attrName = attributeName
            custAttr = self.__getCustomAttribute()
            if not custAttr:
                custAttr = self.__addCustomAttribute()

            self.customAttr = custAttr
            


        def __getCustomAttribute(self):

            returnMod = None
            for i in xrange(self.node.NumModifiers):
                currMod = self.node.GetModifier(i)
                if currMod.GetName() == self.attrName:
                    returnMod =  currMod
                    break
            return returnMod

        def __addCustomAttribute(self):
            attrHolder = MaxPlus.Factory.CreateObjectModifier(MaxPlus.ClassIds.EmptyModifier)
            attrHolder.SetName(MaxPlus.WStr(self.attrName))
            self.node.AddModifier(attrHolder)
            self.__initializeCustomAttribute()

            return self.__getCustomAttribute()

        def __initializeCustomAttribute(self):
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")

            attrDef  = """
                custAttrDef = attributes dummyData
                (
                parameters main rollout:params
                (
                    -- Param Def Begin
                    -- Param Def End
                )
                rollout params "Object Parameters"
                (
                    -- Rollout Def Begin
                    -- Rollout Def End
                )
                )
                """

            attribute = getattr(rt.targetObj, self.attrName)
            rt.execute('emptyMod=$.modifiers[#'+self.attrName+']')
            count = rt.CustAttributes.count(rt.emptyMod)

            rt.execute(attrDef)
            rt.CustAttributes.add(rt.emptyMod, rt.custAttrDef)
            rt.CustAttributes.makeUnique(rt.emptyMod, count + 1)

        def addCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            
            node = self.node
            #print parameterValue
            parameterValue = self.castFrom(parameterValue,parameterType)
            #print parameterValue

            if not parameterValue:
                print "Error casting parameter value to type ",parameterType
                return None

            #print parameterValue
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")
            attribute = getattr(rt.targetObj, self.attrName)

            count = rt.CustAttributes.count(attribute)
        

            customAttr = rt.CustAttributes.get(attribute,count)

            if not customAttr: 
                print ("This node has no attributes")
                return None

            if hasattr(customAttr, parameterName) : 
                print ("Parameter '"+parameterName+"' already exist in "+self.attrName+" attribute")
                return None

            dataDef = rt.CustAttributes.getDef(customAttr)
            defSource = dataDef.source

            defLines = defSource.splitlines()

            
            endParamIndex = next( iter([defLines.index(s) for s in defLines if '-- Param Def End' in s]),None)
            if endParamIndex:
                defLines.insert(endParamIndex, '\t\t\t '+parameterName+' type: #string ui:'+parameterName+'UI default: "'+parameterValue+'"')
            else:
                print ("-- Param Def End  NOT FOUND , Wrong Param name? ")
                return None


            endRolloutIndex = next( iter([defLines.index(s) for s in defLines if '-- Rollout Def End' in s]),None)
            if endRolloutIndex:
                defLines.insert(endRolloutIndex, '\t\t\t edittext  '+parameterName+'UI \"'+parameterName+'\" type: #string')
            else:
                print ("-- Rollout Def End NOT FOUND , Wrong Param name? ")
                return None



            newDef = '\n'.join(defLines)
            #print newDef
            rt.CustAttributes.redefine(dataDef, newDef)
            # print "DONE!"
            return parameterName

        def editCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            parameterValue = self.castFrom(parameterValue,parameterType)
            attrHolder = self.customAttr
            
            if not parameterValue:
                print "Error casting parameter value to type ",parameterType
                return None
            
            if not attrHolder:
                print ("Attribute holder is NULL!")
                return None
            
            node = self.node
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")

            attribute = getattr(rt.targetObj, self.attrName)
            count = rt.CustAttributes.count(attribute)
        

            customAttr = rt.CustAttributes.get(attribute,count)

            if not hasattr(customAttr, parameterName) : 
                print ("Attribute "+self.attrName+" has not " + parameterName)
                return  None

            setattr(customAttr, parameterName, parameterValue)

        def getCustomParameter(self,parameterName):

            attrHolder = self.customAttr
            
            if not attrHolder:
                print ("Attribute holder is NULL!")
                return None
            
            node = self.node
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")

            attribute = getattr(rt.targetObj, self.attrName)
            count = rt.CustAttributes.count(attribute)
            

            customAttr = rt.CustAttributes.get(attribute,count)

            if not hasattr(customAttr, parameterName) :
                print ("Attribute "+self.attrName+" has not " + parameterName)
                return None




            paramValue = getattr(customAttr, parameterName)

            value,typ = self.castTo(paramValue)

            attrParam = self.attributeParameter()
            attrParam.parameterName=  parameterName
            attrParam.parameterValue =  value
            attrParam.parameterType = typ



            return attrParam

        def deleteCustomParameter(self,parameterName):

            attrHolder = self.customAttr
            
            if not attrHolder:
                print ("Attribute holder is NULL!")
                return

            node = self.node
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")

            attribute = getattr(rt.targetObj, self.attrName)
            count = rt.CustAttributes.count(attribute)
        

            customAttr = rt.CustAttributes.get(attribute,count)
            dataDef = rt.CustAttributes.getDef(customAttr)

            if not hasattr(customAttr, parameterName) : 
                print ("Attribute "+self.attrName+" has not " + parameterName)
                return 

            dataDef = rt.CustAttributes.getDef(customAttr)
            defSource = dataDef.source

            defLines = defSource.splitlines()
            filterDef = [line for line in defLines if parameterName+'UI' not in line]
            
            newDef = '\n'.join(filterDef)

            rt.CustAttributes.redefine(dataDef, newDef)

        def listCustomParametersNames(self):
            paremetersNames = []
            attrHolder = self.customAttr
            
            if not attrHolder:
                print ("Attribute holder is NULL!")
                return
            
            node = self.node
            MiscUtilities.SelectObject(self.node)
            rt.execute(" targetObj = $")

            attribute = getattr(rt.targetObj, self.attrName)
            count = rt.CustAttributes.count(attribute)

        
            customAttr = rt.CustAttributes.get(attribute,count)
             

            dataDef = rt.CustAttributes.getDef(customAttr)
            #print dataDef.source 
            #leave aside getmxsprop and setmxsprop
            for prop in customAttr.__dir__():
                if prop != 'getmxsprop' and prop != 'setmxsprop':
                    paremetersNames.append(prop)

            return paremetersNames


        def castTo(self, rawData): # {"typ":"","value":""}
            try:
                parsedData = json.loads(rawData.replace('\\"', '"').replace("DAT_","")) #DAT_ for retrocompatiblity
                dType = parsedData["typ"]
                if dType == self.ATTR_TYPES.STRING: 
                    value = parsedData["value"]
                    return value,dType
                elif dType == self.ATTR_TYPES.NODE: 
                    value = parsedData["value"]
                    node = value #MaxPlus.INode.GetINodeByName(value)
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
                return json.dumps(dataToSave).replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NODE:
                dataToSave["typ"] = newType
                if isinstance(data, MaxPlus.INode):
                    dataToSave["value"] = data.GetName()
                else:
                    dataToSave["value"] = data
                return json.dumps(dataToSave).replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NUMBER:
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave).replace('"', '\\"')
            elif newType == self.ATTR_TYPES.ARRAY:
                if not data:
                    data = []
                if isinstance(data, list):
                    if len(data) > 0:
                        if all(isinstance(x, type(data[0])) for x in data):
                            dataToSave["typ"] = newType
                            dataToSave["value"] = data
                            return json.dumps(dataToSave).replace('"', '\\"')
                        else:
                            print "ARRAY elements should be all the same type", data
                            return None
                    else:
                        dataToSave["typ"] = newType
                        dataToSave["value"] = data
                        return json.dumps(dataToSave).replace('"', '\\"')
                else:
                    print "This",data,"is not type ARRAY", data
                    return None
                
            elif newType == self.ATTR_TYPES.BOOL: 
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave).replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NONE:
                return None
            else:
                print "ERROR , CAST FROM INVALID TYPE ", newType
                return None


class FileUtilities(BaseOverrides.FileUtilities):

    @staticmethod
    def GetFullFileName():
        fullName = MaxPlus.FileManager.GetFileNameAndPath().replace(".3ds","").replace(".max","")
        return fullName

    @staticmethod
    def GetFullPath():
        fullName = os.path.dirname(MaxPlus.FileManager.GetFileNameAndPath().replace(".3ds","").replace(".max",""))+"\\"
        return fullName  

    @staticmethod
    def OpenFile(filePath):
        MaxPlus.FileManager.Open(filePath)
        return True  

    @staticmethod
    def SaveFile(filepath):
        MaxPlus.FileManager.Save(filePath)
        return True


    @staticmethod
    def GetFileArguments():
        # logger = ateneaLogger.AteneaLogger()
        filesToOpen = []
        rt.execute("fto") # eval the variable or create it it it doesnt exist.
        if rt.fto:
            for fto in rt.fto:
                if isinstance(fto, str):
                    fileT = fto
                    fileT = fileT.replace("\'","\\'")
                    fileT = fileT.replace("\"","\\\"")
                    fileT = fileT.replace("\a","\\a")
                    fileT = fileT.replace("\b","\\b")
                    fileT = fileT.replace("\f","\\f")
                    fileT = fileT.replace("\n","\\n")
                    fileT = fileT.replace("\r","\\r")
                    fileT = fileT.replace("\t","\\t")
                    fileT = fileT.replace("\v","\\v")
                    AteneaLogger.log("STR " + fileT)
                    filesToOpen.append(fto)
                elif isinstance(fto, unicode):
                    fileT = fto.encode('utf8')
                    fileT = fileT.replace("\'","\\")
                    fileT = fileT.replace("\"","\\\"")
                    fileT = fileT.replace("\a","\\a")
                    fileT = fileT.replace("\b","\\b")
                    fileT = fileT.replace("\f","\\f")
                    fileT = fileT.replace("\n","\\n")
                    fileT = fileT.replace("\r","\\r")
                    fileT = fileT.replace("\t","\\t")
                    fileT = fileT.replace("\v","\\v")
                    AteneaLogger.log("UTF8 " + fileT)
                    filesToOpen.append(fileT)

                
        return filesToOpen

class MiscUtilities(BaseOverrides.MiscUtilities):

    @staticmethod
    def GetINodeFromNative(native):
        handleId = native.handle
        node = MaxPlus.INode.GetINodeByHandle(handleId)
        return node

    @staticmethod
    def GetNativeFromINode(iNode):
        handleId = iNode.GetHandle()
        native = rt.maxOps.getNodeByHandle(handleId)
        return native

    @staticmethod
    def Exit(exitCode):
        # pass
        try:
            os._exit(exitCode)
        except Exception as e:
            print "CANNOT EXIT"
        

    @staticmethod
    def CheckDuplicatedMaterials():
        materialDict = {}
        duplicated = []

        for scnMat in rt.sceneMaterials:
            if rt.classof(scnMat) == rt.Multimaterial:
                for subMat in scnMat.material:
                    if subMat:
                        materialDict[rt.GetHandleByAnim(subMat)] = subMat.name
            else:
                materialDict[rt.GetHandleByAnim(scnMat)] = scnMat.name

        duplicated = [matName for matName in list(materialDict.values()) if list(materialDict.values()).count(matName) > 1]

        return duplicated
        
    @staticmethod
    def FlattenMultiMaterial(material):
        if mat.IsMultiMtl():
            for i in range(0,mat.GetNumSubMtls()):
                subMtl = mat.GetSubMtl(i)
                if subMtl:
                    oldMat = next((x for x in allMaterials if x.GetName() == subMtl.GetName()), None)
                    if not oldMat:
                        allMaterials.append(subMtl)

    @staticmethod
    def GetAllSceneMaterials():
        duplicated = MiscUtilities.CheckDuplicatedMaterials()
        if duplicated:
            file = FileUtilities.GetFullFileName()
            errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MiscUtilities.GetAllSceneMaterials.__name__)).lower()
            raise CriticalExportException(file,errorSpace,"All these materials are duplicated: \n-{0}".format("\n-".join(duplicated)))

        allMaterials = []
        mats = [MaxPlus.Mtl._CastFrom(MaxPlus.MaterialLibrary.GetSceneMaterial(i)) for i in range(MaxPlus.MaterialLibrary.GetNumSceneMaterials())]
        
        for mat in mats:
            if mat.IsMultiMtl():
                for i in range(0,mat.GetNumSubMtls()):
                    subMtl = mat.GetSubMtl(i)
                    if subMtl:
                        oldMat = next((x for x in allMaterials if x.GetName() == subMtl.GetName()), None)
                        if not oldMat:
                            allMaterials.append(subMtl)
            else:
                oldMat = next((x for x in allMaterials if x.GetName() == mat.GetName()), None)
                if not oldMat:
                    allMaterials.append(mat)    

        return allMaterials



    @staticmethod
    def GetMaterialMaps(mat):
        maps = Set()
        params = mat.ParameterBlock.Parameters
        for p in params:
            # print p.GetName()
            if "bumpMap" == p.GetName() and p.Value:
                for s in p.Value.ParameterBlock.Parameters:
                    if "normal_map" == s.Name :
                        for b in s.Value.ParameterBlock.Parameters:
                            if "fileName" == b.Name :
                                maps.add( os.path.basename(str(b.Value.encode('utf-8'))))
            if  isinstance(p.Value,MaxPlus.Texmap) and p.Value:
                
                for s in p.Value.ParameterBlock.Parameters:
                    if "fileName" == s.Name :
                        maps.add( os.path.basename(str(s.Value.encode('utf-8'))))
        return list(maps)

    @staticmethod
    def GetObjectName(obj):
        return obj.GetName()

    @staticmethod    
    def SetObjectName(obj,name):
        obj.SetName(name)
        return obj

    @staticmethod
    def GetRootObjects():
        return list(MaxPlus.Core.GetRootNode().Children)

    @staticmethod    
    def ImportReferences():
        nodes = MiscUtilities.GetRootObjects()
        xrefs = []
        for node in nodes:
            MiscUtilities.FillXRefObjects(node, xrefs)

        # mergeXRefCommandController = "objXRefMgr.MergeXRefItemsIntoScene $.controller"
        # mergeXRefCommandMaterial = "objXRefMgr.MergeXRefItemsIntoScene $.material"
        # mergeXRefCommandObject = "objXRefMgr.MergeXRefItemsIntoScene $.baseObject"

        if len(xrefs) > 0:
            AteneaLogger.log("---Found XRef Objects in Scene, importing now----")  

        for xref in xrefs:
            AteneaLogger.log("---Importing XRef Object: " + xref.GetName())
            MiscUtilities.SelectObject(xref)
            rt.objXRefMgr.MergeXRefItemsIntoScene(rt.selection[0].controller)
            rt.objXRefMgr.MergeXRefItemsIntoScene(rt.selection[0].material)
            rt.objXRefMgr.MergeXRefItemsIntoScene(rt.selection[0].baseObject)
            # MaxPlus.Core.EvalMAXScript(mergeXRefCommandController)  
            # MaxPlus.Core.EvalMAXScript(mergeXRefCommandMaterial)                      
            # MaxPlus.Core.EvalMAXScript(mergeXRefCommandObject)

    @staticmethod
    def FillXRefObjects(node, xrefs):
        if node.Children:
            children = list(node.Children)
            if len(children) > 0:
                for child in children:
                    MiscUtilities.FillXRefObjects(child, xrefs)
        if node.GetObject().GetClassName() == "XRefObject":
            xrefs.append(node)

    @staticmethod
    def SetParent(obj,parent):
        obj.SetParent(parent)   
        return  obj

    @staticmethod
    def TakeObjectToWorldRoot(obj):
        obj.SetParent(MaxPlus.Core.GetRootNode())    
        return  obj

    @staticmethod
    def GetLocalPosition(obj):
        poss = obj.GetLocalPosition()
        valuePoss = (poss.GetX(),poss.GetY(),poss.GetZ())

        return valuePoss

    @staticmethod
    def GetLocalRotation(obj):
        poss = obj.GetLocalRotation()
        roundedPoss = (round(poss.GetX(), 3),round(poss.GetY(), 3),round(poss.GetZ(), 3))

        return roundedPoss

    @staticmethod
    def GetLocalScale(obj):
        return obj.GetLocalScale()

    @staticmethod
    def SelectObject(*nodes):
        nodesInternal = MaxPlus.INodeTab ()
        for node in nodes:
            nodesInternal.Append(node)
        MaxPlus.SelectionManager.ClearNodeSelection()
        MaxPlus.SelectionManager.SelectNodes(nodesInternal)

    @staticmethod
    def CheckEZMatsFile():
        return os.path.exists(FileUtilities.GetFullFileName()+'.jsonMats')
        # if os.path.exists(FileUtilities.GetFullFileName()+'.jsonMats'):
        #     return ("000",[])
        # else:
        #     return ("200",[])

    # @staticmethod
    # def CheckModifiers(parent):
    #     for child in parent.Children:
    #         if child.GetObject().GetClassName() == "DerivedObject":
    #             print "<{0}> | Collapsing modifiers on child: {1}".format(parent.GetName(), child.GetName())
    #             child.Collapse(True)

    #             # return ("103",[parent.GetName(), child.GetName()])
    #     return True
        # return ("000",[])       

    # @staticmethod
    # def CheckAttributes(parent):
    #     allObjects = [parent]
    #     for objIndex in range(0,len(allObjects)):

    #         baseData = DataParser.nodeAttribute(allObjects[objIndex],'ObjectBaseData')
    #         objType = baseData.getCustomParameter("type")
    #         objSubType = baseData.getCustomParameter("subType")

    #         if objType == None or objSubType == None:
    #             return False
    #             # return ("201",[parent.GetName()])
    #     return True
    #     # return ("000",[])

    @staticmethod
    def GetCurrentSelection():
        return MaxPlus.SelectionManager.GetNodes()

    @staticmethod
    def IsNodeGroup(obj):
        return obj.IsGroupHead()

    @staticmethod
    def OpenGroup(obj):
        nodes = list(obj.Children)
        tabNodes = MaxPlus.INodeTab()
        tabNodes.Append(obj)
        MaxPlus.INode.UngroupNodes(tabNodes)
        return nodes
        


    @staticmethod
    def CreateEmptyObject(objectName = "NewObject", objectPosition = (0,0,0), objectRotation = (0,0,0) ,objectScale = (1,1,1) ):
        obj = MaxPlus.Factory.CreateHelperObject(MaxPlus.ClassIds.Point)
        node = MaxPlus.Factory.CreateNode(obj, objectName)
        node.SetLocalPosition(MaxPlus.Point3(objectPosition[0],objectPosition[1],objectPosition[2]))
        quat = MaxPlus.Quat()
        quat.SetEuler(objectRotation[0],objectRotation[1],objectRotation[2])
        node.SetLocalRotation(quat)
        node.SetLocalScale(MaxPlus.Point3(objectScale[0],objectScale[1],objectScale[2]))
        return node;

    @staticmethod
    def DeleteObject(objectToDelete, childrenPositionStays =False, keepChildren = True):
        children = objectToDelete.Children
        childOldPositions = {}
        for child in children:
            childOldPositions[child] = child.GetWorldPosition()
        objectToDelete.Delete()
        if childrenPositionStays:
            for child in childOldPositions.keys():
                child.SetWorldPosition(childOldPositions[child])

    @staticmethod
    def SelectMaterial(material):
        MaxPlus.MaterialEditor.OpenMtlDlg(0)

        index = -1
        for i in range(0,24):
            mtlSlot = MaxPlus.MaterialManager.GetMtlSlot(i)
            if not mtlSlot._IsValidWrapper() or "Default" in mtlSlot.GetName():
                index = i
                break
        if index == -1:
            index = random.randint(0, 24)

        MaxPlus.MaterialManager.PutMtlToMtlEditor(material,index)
        MaxPlus.MaterialEditor.SetActiveSlot(index)

    @staticmethod
    def CreateMaterial(matName,serverMat):

        returnData = []

        newMaterial = MaxPlus.Factory.CreateDefaultStdMat()
        newMaterial.SetName(MaxPlus.WStr( matName))
        matLibrary =  MaxPlus.MaterialLibrary.GetSceneMaterialLibrary()
        matLibrary.Add(newMaterial)        

        MaxPlus.MaterialEditor.OpenMtlDlg(0)

        index = -1
        for i in range(0,24):
            mtlSlot = MaxPlus.MaterialManager.GetMtlSlot(i)
            if not mtlSlot._IsValidWrapper() or "Default" in mtlSlot.GetName():
                index = i
                break
        if index == -1:
            index = random.randint(0, 24)

           
        maxPath = FileUtilities.GetFullPath()
        shader = serverMat.shaderName

       
        matDataProperties = [prop for prop in serverMat.properties if prop.propType == "TexEnv"]
        newMaterialMaps = [param for param in newMaterial.ParameterBlock.Parameters if param.Type == MaxPlus.FPTypeConstants.Texmap]

        mainTexProp = next((x for x in matDataProperties if x.propName == "_MainTex"), None)
        diffuseMapParam = next((x for x in newMaterialMaps if x.Name == "diffuseMap"), None)

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
            print "We have to left out behind so maps...."

        for i in range(min(len(matDataProperties),len(newMaterialMaps))):
            prop = matDataProperties[i]
            matMap = newMaterialMaps[i]

            textureName = prop.propValue
            propName = prop.propName

            if not textureName : continue
            
            texturePath = fsu.findFileInParents(textureName,maxPath,"/Textures")

            

            if not texturePath : 
                MiscUtilities.DeleteMaterial(newMaterial)
                newMaterial = None
                break

            bitmapTex = MaxPlus.Factory.CreateDefaultBitmapTex()
            bitmapTex.SetMapName(texturePath)
            bitmapTex.ReloadBitmapAndUpdate()
            matMap.SetValue(bitmapTex)

            
                # if shaderProp and matMapName == p.GetName():
                #     if "bumpMap" == p.GetName() and p.Value:
                #         for s in p.Value.ParameterBlock.Parameters:
                #             if "normal_map" == s.GetName() :
                #                 s.SetValue(bitmapTex) 

                #     else:
                #         p.SetValue(bitmapTex) 
                #     break

        if newMaterial:
            MaxPlus.MaterialManager.PutMtlToMtlEditor(newMaterial,index)
            MaxPlus.MaterialEditor.SetActiveSlot(index)


        return newMaterial

    @staticmethod
    def ResetMaterial(material,matData):
        maxPath = FileUtilities.GetFullPath()

        matDataProperties = [prop for prop in matData.properties if prop.propType == "TexEnv"]
        newMaterialMaps = [param for param in material.ParameterBlock.Parameters if param.Type == MaxPlus.FPTypeConstants.Texmap]

        mainTexProp = next((x for x in matDataProperties if x.propName == "_MainTex"), None)
        diffuseMapParam = next((x for x in newMaterialMaps if x.Name == "diffuseMap"), None)

        material.Reset()

        #ONLY PUT _MainTex ON diffuseMap , EVERYTHING ELSE ON RANDOM SLOTS.
        if diffuseMapParam and mainTexProp:
            matDataProperties.remove(mainTexProp)
            matDataProperties.insert(0,mainTexProp)
            newMaterialMaps.remove(diffuseMapParam)
            newMaterialMaps.insert(0,diffuseMapParam)

        if len(matDataProperties) > len(newMaterialMaps):
            print "We have to left out behind so maps...."
        
        for i in range(min(len(matDataProperties),len(newMaterialMaps))):
            prop = matDataProperties[i]
            matMap = newMaterialMaps[i]

            textureName = prop.propValue
            propName = prop.propName

            if not textureName : continue
            
            texturePath = fsu.findFileInParents(textureName,maxPath,"/Textures")

            if not texturePath : 
                material = None
                break

            bitmapTex = MaxPlus.Factory.CreateDefaultBitmapTex()
            bitmapTex.SetMapName(texturePath)
            bitmapTex.ReloadBitmapAndUpdate()
            matMap.SetValue(bitmapTex)

        return material

    @staticmethod
    def DeleteMaterial(matToDelete):
        MaxPlus.MaterialEditor.OpenMtlDlg(0)
        index = -1
        for i in range(0,24):
            mtlSlot = MaxPlus.MaterialManager.GetMtlSlot(i)
            if mtlSlot._IsValidWrapper() and matToDelete._IsValidWrapper() and mtlSlot.GetName() == matToDelete.GetName():
                index = i
                break
        if index != -1:
            print index
            defaultSlot = MaxPlus.Factory.CreateDefaultStdMat()
            defaultSlot.SetName(MaxPlus.WStr( "Default_Slot"))
            MaxPlus.MaterialManager.PutMtlToMtlEditor(defaultSlot,index)

        MaxPlus.MaterialEditor.CloseMtlDlg(0)

        #Remove the material from the library 
        matLibrary =  MaxPlus.MaterialLibrary.GetSceneMaterialLibrary()
        matLibrary.Remove(matToDelete)


        #Remove the material from the scene, and unnasign from the meshes.
        if matToDelete._IsValidWrapper():
            matToDelete.DeleteMe()
        else:
            print "Invalid material ? " + str(matToDelete)

        #Reset Node material view
        MaxPlus.MaterialEditor.OpenMtlDlg(1)
        rt.sme.DeleteView(1,False)
        rt.sme.CreateView("View1")
        MaxPlus.MaterialEditor.CloseMtlDlg(1)

        MaxPlus.MaterialEditor.UnFlushMtlDlg()
        MaxPlus.MaterialEditor.FlushMtlDlg()
        MaxPlus.MaterialEditor.UpdateMtlEditorBrackets()

    @staticmethod
    def DisableShortcuts():
        MaxPlus.CUI.DisableAccelerators()

    @staticmethod
    def EnableShortcuts():
        MaxPlus.CUI.EnableAccelerators()

class AnimationUtilities(BaseOverrides.AnimationUtilities): pass



class CallBackUtilities(BaseOverrides.CallBackUtilities):

    MOVEMENT_CALLBACK = MaxPlus.NotificationCodes.ViewportChange
    SCALE_CALLBACK = MaxPlus.NotificationCodes.ViewportChange
    ROTATION_CALLBACK = MaxPlus.NotificationCodes.ViewportChange

    
    def __init__(self):
        # print "INIT"
        self.handler =  MaxPlus.NotificationManager.Register(MaxPlus.NotificationCodes.SelectionsetChanged , self.__maintainObjectBinding)
        self.callbackLists = {}
        self.trackedObjects = []

    def clean(self,force = False):
        MaxPlus.NotificationManager.Unregister(self.handler)
        

        for callback in self.callbackLists:
            self.callbackLists[callback].unRegister()
            if force:
                self.callbackLists[callback].obj.Delete()
            

        

    def addCallbackToObj(self,callbackName,callbackType,obj,bind):
        
        if not callbackType :
            print(">callbackType Not Valid")
            return
        if not obj:
            print(">obj Not Valid")
            return
        if not bind:
            print(">bind Not Valid")
            return
        if not callbackName:
            print(">callbackName Not Valid")
            return
        trackedObject = {}
        trackedObject["callBackName"] = callbackName
        trackedObject["callbackType"] = callbackType
        trackedObject["obj"] = obj
        trackedObject["bind"] = bind
        self.trackedObjects.append(trackedObject)

        

    def removeCallback(self,callbackName):
        if callbackName in self.callbackLists:
            self.callbackLists[callbackName].unRegister()
            self.callbackLists.pop(callbackName)

        self.trackedObjects = filter(lambda x : x["callBackName"] != callbackName, self.trackedObjects)


    def __maintainObjectBinding(self,code):
        if MaxPlus.SelectionManager.GetCount() == 1:
            nodeSelected = MaxPlus.SelectionManager.GetNode(0)
            nodeName = nodeSelected.GetName()
            trackedNodes = [tObj["obj"].GetName() for tObj in self.trackedObjects]
            for trackedObject in self.trackedObjects:
                if nodeName == trackedObject["obj"].GetName() and trackedObject["callBackName"] not in self.callbackLists:
                    print "BINDING!"
                    self.callbackLists[trackedObject["callBackName"]] = self.callback(
                        trackedObject["callbackType"],
                        trackedObject["obj"],
                        trackedObject["bind"])

                    self.callbackLists[trackedObject["callBackName"]].register()


                



    class callback():

        def __init__(self,callbackType,obj,bind):
            self.bind = bind
            self.obj = obj
            self.callbackType = callbackType
            self.handler = None

        
        def register(self):
            print "REGISTERED"
            self.handler = MaxPlus.NotificationManager.Register(self.callbackType , self.onExecuted)

        def unRegister(self):
            print "UNBINDING {0}! ".format(self.obj.GetName()) 
            MaxPlus.NotificationManager.Unregister(self.handler)
            self.bind = None

        def onExecuted(self,code):
            self.bind(self.obj)


