import MaxPlus
import json
import urllib2 as url
import os
import copy
from PySide import QtGui,QtCore
from sets import Set
import sys
import traceback
from datetime import datetime

sys.path.append('C:/Proyectos/BuildSystem')
from AteneaModules.parser import jsonStructures

objsMust = ["FLOOR","LAYOUT","LAYOUT_HIDE","REFERENCE_OBJS","REFERENCE_OBJS_HIDE"]

sys.stdout = sys.__stdout__
sys.stderr = sys.__stderr__

version = 1
debugPath = os.path.expanduser('~/Documents/') + "envExport.log"

exportLayers = ""
setDressing = "setDressing"
garbageLayer = "modules"
output = MaxPlus.FileManager.GetFileNameAndPath().replace(".3ds","").replace(".max","")
filename = os.path.basename(MaxPlus.FileManager.GetFileNameAndPath()).replace(".3ds","").replace(".max","")

exportableMeshes = ["Editable Poly"]

class EnvironmentExporter():

    def loadAllLayerNames(self):
        excludes = [garbageLayer]
        layerNames = []
        layerCount = MaxPlus.LayerManager.GetNumLayers()
        for i in range(0,layerCount):
            layer = MaxPlus.LayerManager.GetLayer(i)
            if( layer.GetName() not in excludes):
                layerNames.append(str(layer.GetName()))
        return layerNames

    def selectObjectsInLayers(self,*args):
        
        nodes = MaxPlus.INodeTab ()
        MaxPlus.SelectionManager.ClearNodeSelection()
        layerCount = MaxPlus.LayerManager.GetNumLayers()
        for i in range(0,layerCount):
            layer = MaxPlus.LayerManager.GetLayer(i)
            if( layer.GetName() in list(*args)):

                layerNodes = layer.GetNodes()
                # print(layerNodes.GetCount())
                for j in range(0,layerNodes.GetCount()):
                    nodes.Append(layerNodes.GetItem(j))
                    log("Added NODE " + str(layerNodes.GetItem(j).GetName()))


        MaxPlus.SelectionManager.SelectNodes(nodes)
        return nodes

    def getAllObjects(self,parent,filt = None):
        objs = []
        if not parent.GetIsRoot():
            if filt:
                if parent.GetObject().GetClassName() in list(filt):
                    objs.append(parent)
                    # print (parent.GetName() + " Added")
                else: 
                    print (" Not valid")
                 
            else:
                objs.append(parent)

        for obj in parent.Children:
            objs = objs + self.getAllObjects(obj,filt)

        return objs

    def getAndApplyAllMaterials(self):
        objectMaterials = {}
        MaxPlus.SelectionManager.ClearNodeSelection()
        for obj in self.getAllObjects(MaxPlus.Core.GetRootNode()):
            mat = obj.GetMaterial()
            if mat:
                if mat.GetNumSubMtls() > 0:
                    for i in range(0,mat.GetNumSubMtls()):
                        subMtl = mat.GetSubMtl(i)
                        if subMtl:
                            oldMat = next((x for x in objectMaterials if x.GetName() == subMtl.GetName()), None)
                            if not oldMat:
                                log(obj.GetName() + " SU "+subMtl.GetName()) 
                                objectMaterials[subMtl] = []
                                objectMaterials[subMtl].append(obj)
                            else:
                                if not obj in objectMaterials[oldMat]:
                                    objectMaterials[oldMat].append(obj)
                else:
                    oldMat = next((x for x in objectMaterials if x.GetName() == mat.GetName()), None)
                    if not oldMat: 
                        log(obj.GetName() +" NE " + mat.GetName()) 
                        objectMaterials[mat] = []
                        objectMaterials[mat].append(obj)
                    else:
                        if not obj in objectMaterials[oldMat]:
                            objectMaterials[oldMat].append(obj)

        return objectMaterials

    

    def parseAllData(self):    
        global exportLayers

        matDataVersion = 0

        #RawData
        rawMaterials = self.getAndApplyAllMaterials()

        #structs for connections
        meshShaders = {}
        shaderToId = {}
        meshes = []
        matProps = {}

        environments = []

        exportableObjects = self.selectObjectsInLayers(exportLayers)

        environments = [e for e in MaxPlus.Core.GetRootNode().Children if e in exportableObjects]
        
        #structs for JSON
        data = {}
        materials = []
        avatars = []
        
        hasProperties = False
        log(output+'.jsonMats')
        if os.path.exists(output+'.jsonMats'):
            with open(output+'.jsonMats') as data_file:
                hasProperties = True    
                matProps = json.load(data_file)
                matDataVersion = jsonStructures.getDataOrDefault(matProps,"version",0)
        
        
        matId = 0;

       
        for key in rawMaterials:        
            meshes = meshes + rawMaterials[key]

            materialObject = key    
            materialData = {}
            materialData["id"] = matId
            materialData["name"] = str(materialObject.GetName())
            try:    
                if hasProperties and str(materialObject.GetName()) in matProps:
                    materialData["properties"] = matProps[str(materialObject.GetName())]["properties"]
                    materialData["shaderName"] = matProps[str(materialObject.GetName())]["shaderName"]
                else:
                    materialData["properties"] = []
                    materialData["shaderName"] = "Standard"

            except Exception as e:
                sys.stderr.write(str("ERROR GETTING OLD PROPERTY! -> ") + str(key.GetName()) + " : " + str(e))
                try:
                    sys.exit(-1)
                except SystemExit:
                    pass 


            materials.append(materialData)
            shaderToId[key] = matId
            matId = matId + 1
            
        
        # bpy.ops.object.select_by_layer(match='EXACT',extend=False,layers=setDressing+1)
        dressings = self.selectObjectsInLayers(setDressing);
        
        environmentsData = []

        
        for environmentIndex in range(0,len(environments)):
            environmentData = {}
            environmentData["id"] = environmentIndex
            environmentData["name"] = str(environments[environmentIndex].GetName())
            environmentData["meshes"] = []
            allValidObjects = self.selectObjectsInLayers(exportLayers)
            meshes = [m for m in self.getAllObjects(environments[environmentIndex],exportableMeshes) if m in allValidObjects]
            colliders = []
            triggers = []   
            dressingsData =  []
            log("LEN " + str(len(meshes)))
            log(environmentData["name"])
            if meshes:
                for i in range(0,len(meshes)):

                    if "col_" in str(str(meshes[i].GetName())):
                        colliderData = {}
                        colliderData["id"] = i
                        colliderData["meshName"] = str(str(meshes[i].GetName()))
                        if "COL_TYPE" in meshes[i]:
                            colliderData["colliderType"] = meshes[i]["COL_TYPE"]
                        else:
                            colliderData["colliderType"] = "BOX" 
                        colliders.append(colliderData)
                    elif "trigger_" in str(str(meshes[i].GetName())):
                        triggerData = {}
                        triggerData["id"] = i
                        triggerData["meshName"] = str(str(meshes[i].GetName()))
                        triggerData["colliderType"] = "BOX"
                        triggers.append(triggerData)
                    else:
                        meshData = {}
                        meshData["id"] = i
                        meshData["meshName"] = str(str(meshes[i].GetName()))
                        meshMaterials = []
                        mat = meshes[i].GetMaterial()

                        if mat:
                            if mat.GetNumSubMtls() > 0:
                                for j in range(0,mat.GetNumSubMtls()):
                                    subMtl = mat.GetSubMtl(j)
                                    if subMtl:
                                        oldMat = next((x for x in shaderToId if x.GetName() == subMtl.GetName()), None)
                                        if oldMat:
                                            log("FOUND "  + oldMat.GetName())
                                            meshMaterialIds = {}
                                            meshMaterialIds["materialId"] = shaderToId[oldMat]
                                            meshMaterials.append(meshMaterialIds)

                                        else:
                                            log(meshData["meshName"]+ " NOT FOUND "  + oldMat.GetName())
                            else:
                                oldMat = next((x for x in shaderToId if x.GetName() == mat.GetName()), None)
                                if oldMat:
                                    meshMaterialIds = {}
                                    meshMaterialIds["materialId"] = shaderToId[oldMat]
                                    meshMaterials.append(meshMaterialIds)
                        meshData["materialIds"] = meshMaterials
                        
                        if meshes[i] in dressings:
                            dressingsData.append(str(meshes[i].GetName()))
                        environmentData["meshes"].append(meshData)

                    customProps = self.loadObjectCustomProperties(meshes[i])

                    layerProp = {}


                    if customProps:
                        layerProp = customProps
                    else:
                        layerProp["LightmapStatic"] = False
                        layerProp["NavigationStatic"] = False
                        layerProp["OccludeeStatic"] = False
                        layerProp["OccluderStatic"] = False
                        layerProp["BatchingStatic"] = False
                        layerProp["ReflectionProbeStatic"] = False
                        layerProp["NavmeshLayer"] = "Not Walkable"
                    
                    meshData["layerProperties"] =  layerProp

            environmentData["colliders"] = colliders
            environmentData["triggers"] = triggers
            environmentData["dressings"] = dressingsData
            environmentsData.append(environmentData)
            
        data["materials"] = materials         
        data["objects"] = environmentsData
        data["type"] = "Environment"

        versions = {}
        versions["Max_EzMaterials"] = jsonStructures.getDataOrDefault(matProps,"version",0)
        versions["Max_EnvToFbx"] = version

        data ["versions"] = versions

        json_data = json.dumps(data)
        return json_data


    def loadObjectCustomProperties(self,node):
        data = {}
        buff = MaxPlus.WStr("")
        node.GetUserPropBuffer(buff)
        if str(buff):
            try:
                data = json.loads(str(buff))
                # json_object = json.loads(myjson)
            except ValueError, e:
                return {}

            
        return data

    def exportMetaData(self,filePath):
        try:
            log("PARSE DATA!")
            json_data = self.parseAllData()
            log("DATA PARSED!")
        except Exception as e:
            log(str("ERROR PARSING! -> ") + str(e))
            exc_type, exc_value, exc_traceback = sys.exc_info()
            print "*** print_tb:"
            traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
            print "*** print_exception:"
            traceback.print_exception(exc_type, exc_value, exc_traceback,limit=2, file=sys.stdout)

            try:
                sys.exit(-1)
            except SystemExit:
                pass 
        
        try:
            with open(filePath+".jsonMeta", "w+") as text_file:
                text_file.write(json_data)

            sys.stdout.write("|OUTPUTFILE|"+filePath+".jsonMeta\n")
        except Exception as e:
            log(str("ERROR WRITING! -> ") + str(e))
            try:
                sys.exit(-1)
            except SystemExit:
                pass 
       
            
    def exportFBX(self,filePath):
        try:            
            log("exportFile \""+filePath.replace("\\","\\\\")+".fbx"+"\"  #noprompt selectedOnly:true using:FBXEXP")
            MaxPlus.Core.EvalMAXScript("exportFile \""+filePath.replace("\\","\\\\")+".fbx"+"\"  #noprompt selectedOnly:true using:FBXEXP")
            sys.stdout.write("|OUTPUTFILE|"+filePath +".fbx\n")

        except Exception as e:
            sys.stderr.write(str("ERROR EXPORTING! -> ") + str(e))
            try:
                sys.exit(-1)
            except SystemExit:
                pass 

    def setFBXParams(self):
        MaxPlus.Core.EvalMAXScript("pluginManager.loadClass FBXEXPORTER")    
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Animation\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ASCII\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"BakeAnimation\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"BakeFrameStart\" 0")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"BakeFrameEnd\" 0")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"BakeFrameStep\" 0")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"BakeResampleAnimation\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Cameras\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"CAT2HIK\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ColladaTriangulate\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ColladaSingleMatrix\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ColladaFrameRate\" 0")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Convert2Tiff\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ConvertUnit\" \"m\"")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"EmbedTextures\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"FileVersion\" \"FBX201400\"")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"FilterKeyReducer\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"GeomAsBone\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"GenerateLog\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Lights\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"NormalsPerPoly\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"PointCache\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Preserveinstances\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Removesinglekeys\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ScaleFactor\" 1")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Shape\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Skin\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"ShowWarnings\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"SmoothingGroups\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"SmoothMeshExport\" false")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"TangentSpaceExport\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"Triangulate\" true")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"UpAxis\" \"Y\"")
        MaxPlus.Core.EvalMAXScript("FBXExporterSetParam \"UseSceneName\" false")


    def getPolysByMatId(self,mesh,mid):
        polyCount = MaxPlus.Core.EvalMAXScript("polyop.getNumFaces $").Get()
        polys = []
        for i in range(1,polyCount+1):
            matId = MaxPlus.Core.EvalMAXScript("polyop.getFaceMatID $ "+str(i)).Get()
            if matId == mid:
                polys.append(i)
        return polys

    def reorderMeshes(self,*args):
        nodes = self.getAllObjects(MaxPlus.Core.GetRootNode(),exportableMeshes)
        #nodes = MaxPlus.SelectionManager.GetNodes();
        for node in nodes:
            log("Processing " + node.GetName())
            nodes = MaxPlus.INodeTab ()
            nodes.Append(node)
            MaxPlus.SelectionManager.ClearNodeSelection()
            MaxPlus.SelectionManager.SelectNodes(nodes)
            obj = node.GetObject()
            geo = obj.AsTriObject()
            mesh = geo.GetMesh()
            polyCount = MaxPlus.Core.EvalMAXScript("polyop.getNumFaces $").Get()

            matIds = set()

            facesByMaterialId = {}
            for i in range(1,polyCount+1):
                log( node.GetName() +  "ADDED POLY " + str(i))
                matId = MaxPlus.Core.EvalMAXScript("polyop.getFaceMatID $ "+str(i)).Get()
                matIds.add(matId)
            
            for mid in matIds:
                polys = self.getPolysByMatId(mesh,mid)
                if polys:
                    facesString = ','.join(map(str, polys)) 
                    name = node.GetName()+"detachTempObj"+str(mid)
                    detachCommand = "polyOp.detachFaces $ #{%s} delete:true asNode:true name:\"%s\"" %(facesString,name)
                    attachCommand = "polyop.attach $ $'%s' " %name

                    log(detachCommand)
                    log(attachCommand)

                    MaxPlus.Core.EvalMAXScript(detachCommand)
                    MaxPlus.Core.EvalMAXScript(attachCommand)

                MaxPlus.Core.EvalMAXScript("windows.processPostedMessages()")


   

def log(val):
    print(val)
    with open(debugPath, "a+") as myfile:
        myfile.write(val+"\n")

if __name__ == '__main__':

    envExporter = EnvironmentExporter()

    log("-----------------------------------------------CHECK IF ENVIRONMENT MATCH REQUISITES!")
    alloBjs = envExporter.getAllObjects(MaxPlus.Core.GetRootNode()) # BAD!
    alloBjs = set([obj.Name for obj in alloBjs])

    valid = set(objsMust).issubset(set(alloBjs)) 

    if not valid:

        log("-----------------------------------------------ENV NOT VALID!")
        log(str("ERROR EXPORTING! -> MODEL DOES NOT INCLUDE ALL THIS ELEMENTS  " + str(objsMust)))

    exportLayers = envExporter.loadAllLayerNames()
    envExporter.reorderMeshes(exportLayers)
    log("-----------------------------------------------MESHES REORDERED!")
    
    objs = envExporter.selectObjectsInLayers(exportLayers)
    log("-----------------------------------------------OBJECTS SELECTED!")
        
    envExporter.setFBXParams()
    log("-----------------------------------------------FBX PARAM SETTED!")
    envExporter.exportFBX(output)
    

    log("-----------------------------------------------FBX EXPORTED!")
    envExporter.exportMetaData(output) 
    log("-----------------------------------------------DATA PARSED!")
    #else:
        #log("-----------------------------------------------ENV NOT VALID!")
        #log(str("ERROR EXPORTING! -> MODEL DOES NOT INCLUDE ALL THIS ELEMENTS  " + str(objsMust)))
        #try:
        #    sys.exit(-1)
        #except SystemExit:
        #    pass 
