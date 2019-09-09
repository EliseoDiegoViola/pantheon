from .exportableObject import *
from .exportable import *
from .exportableMaterial import *
from .animationEvent import *
from .exportableAnimation import *

from pantheonModules.conn.requests import ServerRequest
from pantheonModules.conn import serverObjects
from pantheonModules.logger.ateneaLogger import AteneaLogger
from pantheonModules.pantheonUtilities.loader import LoaderObject
from pantheonModules.conn.localComm import localClient
from pantheonModules.settings import *

import json
import os
import sys
import re


class exportableScene(exportable):

    # class __exportableScene(exportable):
    #     def __init__(self, arg):
    #         self.val = arg
    #     def __str__(self):
    #         return repr(self) + self.val



    exportableParents = []
    exportableMaterials = []
    exportableAnimations = []
    dataNodes = []
    exportDirectory = ""


    def __repr__(self):
        return self.objectRepresentation

    def __init__(self,fPath):
        super(exportableScene,self).__init__(fPath,None,EXPORTABLE_TYPE.SCENE)


        self.sceneInstance = self
        self.sceneLoader = None # RODO RETHINK HOW LOADER WORKS
        self.exportDirectory = os.path.dirname(fPath)+"/"



        
        
        # print "ANIMATIONS PARSE!"
        # self.exportableAnimations = self.getAllAnimations()        
        


        # for expO in self.exportableParents:
            # print "COMPILING DATA!"
            # print "FINALLY THIS IS ALL"
            # expO.compileExtraData()

    def reportSceneProgress(self,val,msg):
        if self.sceneLoader:
            self.sceneLoader.reportProgress(val,msg)

    def parseScene(self):

        self.reportSceneProgress(0.1,"Parsing Scene")

        AteneaLogger.log( "SEARCH EXPORTABLE!")
        self.exportableParents = self.fetchExportableParents()
        self.reportSceneProgress(0.3,"Loading Data Files")

        AteneaLogger.log(  "DATA PARSE!")
        self.dataParser = localOverride.DataParser(localOverride.FileUtilities.GetFullFileName())
        self.reportSceneProgress(0.35,"Loading Materials Files")

        AteneaLogger.log(  "MATERIALS PARSE!")
        self.exportableMaterials = self.getAllMaterials()

    def fetchExportableParents(self):
        expParents = []
        exportableTypes = localOverride.LayersUtilities.exportableParents
        rootObjects = localOverride.MiscUtilities.GetRootObjects()
        for i in range(0,len(rootObjects)):
            obj = rootObjects[i]
            objClass = localOverride.MeshesUtilities.GetObjectClass(obj)
            if objClass in exportableTypes:
                # obj = localOverride.MiscUtilities.AddTemporalNamespace(obj)#localOverride.MiscUtilities.SetObjectName(obj,localOverride.MiscUtilities.GetObjectName(obj)+"_TEMPORAL_PARENT")
                exportableObj = exportableObject(obj,self,EXPORTABLE_TYPE.DUMMY)
                exportableObj.exportableName = str(exportableObj)#.replace("_TEMPORAL_PARENT","") ##Useful only for animations
                expParents.append(exportableObj)
                
        return expParents

    # def getAllAnimations(self):
    #     allExportableAnim = []
    #     # print "ANIMATTTTIOOOOONS ", self.dataParser.anims
    #     allAnimations = self.dataParser.anims
    #     allEvents = self.dataParser.events
    #     for anim in allAnimations:
    #         expAnim = exportableAnimation()
    #         expAnim.clipName = anim["clipName"]
    #         expAnim.startKey = anim["clipStart"]
    #         expAnim.endKey = anim["clipEnd"]
    #         expAnim.isLoop = anim["clipLoop"]
    #         expAnim.isRoot = anim["clipRoot"]

    #         animEvents = []
    #         for evnt in allEvents:
    #             if anim["clipStart"] <= evnt["clipKeyFrame"] <= anim["clipEnd"]:
    #                 expEvnt = animationEvent(evnt["clipKeyFrame"],evnt["clipKeyEvent"])
    #                 animEvents.append(expEvnt)

    #         expAnim.events = animEvents
    #         allExportableAnim.append(expAnim)
    #     return allExportableAnim

    def getAllMaterials(self):
        allExportableMats = []
        allMaterials = self.localOverride.MiscUtilities.GetAllSceneMaterials()

        response = ServerRequest.mongoList(serverObjects.GameMaterials)

        for mat in allMaterials:
            expMaterial = exportableMaterial(mat,None,EXPORTABLE_TYPE.MATERIAL)
            serverMat = next((sMat for sMat in response.objects if sMat.name == str(mat)),None)
            if serverMat:
                expMaterial.setServerMaterial(serverMat)
                allExportableMats.append(expMaterial)
            
        return allExportableMats

    

    def prepareExportableObjects(self):
        self.reportSceneProgress(0.4,"Unlocking Objects")
        for i in range(len(self.exportableParents)):
            # try:
            parent = self.exportableParents[i]
            parent.unlockObjects()
            self.reportSceneProgress(0.4 + ((0.05/(len(self.exportableParents))) * (i+1/len(self.exportableParents))) ,"Baking Animation")
            parent.bakeAnimations()
            if parent.objectType != "Animation": #HACKITY HACK
                self.reportSceneProgress(0.4 + ((0.1/(len(self.exportableParents)))*(i+1/len(self.exportableParents))),"Merging Children")
                parent.mergeChildren()

                self.reportSceneProgress(0.4 + ((0.2/(len(self.exportableParents)))*(i+1/len(self.exportableParents))),"Reordering Meshes")
                parent.reorderMeshes()

                self.reportSceneProgress(0.4 + ((0.4/(len(self.exportableParents)))*(i+1/len(self.exportableParents))),"Reparent Children")
                parent.reparentChildren()

                
            else:
                self.reportSceneProgress(0.4 + ((0.15/len(self.exportableParents))*(i/len(self.exportableParents))),"Lookup for skeleton Parent")
                skeletonParent = parent.findSkeletonParent()
                self.reportSceneProgress(0.4 + ((0.4/len(self.exportableParents))*(i/len(self.exportableParents))),"Isolating Animation")
                parent.isolateAnimation(skeletonParent)
            # except Exception as e:
            #     AteneaLogger.log( str(e))
            parent.propagateObjectData() #Its still necesary?
            



    def adoptChild(self,child):
        child.objectRepresentation =  self.localOverride.MiscUtilities.TakeObjectToWorldRoot(child.objectRepresentation)

    def drawTree(self, start=None, depth=0 , showType = False,showSubType =False, showExtraData= False):
        if not start:
            start = self
        print(('--' * depth) + "{0} {1} {2} {3}".format(
            str(start),
            start.objectType if showType else "",
            start.objectSubType if showSubType else "",
            start.extraData if showExtraData else ""))
        depth = depth+1
        if isinstance(start,exportableObject):
            for node in start.exportableChildren:
                self.drawTree(node,depth,showType = True,showSubType =True, showExtraData= True)
            for node in start.exportableContent:
                self.drawTree(node,depth,showType = False,showSubType =False, showExtraData= False)
        elif isinstance(start,exportableScene):
            for node in start.exportableParents:
                self.drawTree(node,depth,showType = True,showSubType =True, showExtraData= True)



    # def validateScene(self):
    #     valid = True
    #     valid = valid and self.localOverride.MiscUtilities.CheckEZMatsFile()
    #     for expO in self.exportableParents:
    #         valid = valid and self.localOverride.MiscUtilities.CheckAttributes(expO.objectRepresentation)
    #         valid = valid and self.localOverride.MiscUtilities.CheckModifiers(expO.objectRepresentation)
        # self.meshUtilities.checkForInstances,
        # self.meshUtilities.checkMaterials

    def exportObject(self,exportableObject, data):
        self.reportSceneProgress(0.9,"Exporting FBX")
        # childName =  self.miscUtilities.GetObjectName(child)# ANIMATION HACK


        # BAD EXAMPLE
        # es_door_22_metal

        # GOOD EXAMPLE
        # es_door22_metal
        # es_door_metal_22
        AteneaLogger.log("ABOUT TO EXPORT!")
        exportnameRegex = "(\\b[a-z|A-Z]{2,}(?=_))_(.(?!_\\d+_))+$"
        exportName = exportableObject.exportableName
        regMatch = re.match(exportnameRegex,exportName)
        if not regMatch:
            exportName =  os.path.splitext(os.path.basename(str(self)))[0]

        localOverride.MeshesUtilities.SelectFullObject(exportableObject.objectRepresentation, add = False)
        exportableObject.objectRepresentation = localOverride.MiscUtilities.RemoveNamespace([exportableObject.objectRepresentation])
        # print "NAMESPACE REMOVED I LEFT ", str(exportableObject.objectRepresentation)
        localOverride.ExportUtilities.SetFBXParams()    
        localOverride.ExportUtilities.ExportFBX(self.exportDirectory+str(exportName).replace("|","")) #| Maya separator.
        json_data = json.dumps(data)
        with open(self.exportDirectory+str(exportName).replace("|","")+".jsonmeta", "w+") as text_file:
                text_file.write(json_data)
        exportableObject.objectRepresentation = localOverride.MiscUtilities.AddTemporalNamespace(exportableObject.objectRepresentation)
        AteneaLogger.log("EXPORTED!")
        return ["\n|OUTPUTFILE|"+self.exportDirectory+str(exportName)+".fbx\n","\n|OUTPUTFILE|"+self.exportDirectory+str(exportName)+".jsonmeta\n"]
                
    def parseExportDataObject(self, exportableObject):
        self.reportSceneProgress(0.85,"Parsing All object data")
        allObjects = exportableObject.getFlatternHierarchy()
        
        # print("TOTAL NUMBER OF MATERIALS! " + str(len(self.exportableMaterials)) )

        matToId = {}    
        materials = []    
        # animations = []
        # events = []    

        # usedIds = [] #kind of temporal HACKITY HACK

        # BAD EXAMPLE
        # es_door_22_metal

        # GOOD EXAMPLE
        # es_door22_metal
        # es_door_metal_22
        exportnameRegex = "(\\b[a-z|A-Z]{2,}(?=_))_(.(?!_\\d+_))+$"
        exportName = str(exportableObject)
        regMatch = re.match(exportnameRegex,exportName)
        if not regMatch:
            exportName = os.path.splitext(os.path.basename(str(self)))[0]    

        #FILE DATAS PARSING RAWMATERIALS
        for mat in self.exportableMaterials:
            materialData = {}
            materialData["id"] = mat.serverMaterial.mongoId
            materialData["name"] = mat.serverMaterial.name
            materialData["shaderName"] = mat.serverMaterial.shaderName
            materialData["properties"] = [prop.toDict() for prop in mat.serverMaterial.properties]
            materials.append(materialData)
            matToId[str(mat)] = mat.serverMaterial.mongoId

        # FILE DATAS PARSING ANIMATIONS
        # for expA in self.exportableAnimations:
        #     animationData = {}
        #     animationData["id"] = id(expA)
        #     animationData["animName"] = expA.clipName
        #     animationData["animStart"] = expA.startKey
        #     animationData["animEnd"] = expA.endKey
        #     animationData["animLoop"] = expA.isLoop
        #     animationData["animRoot"] = expA.isRoot
        #     animations.append(animationData)
        #     for expE in expA.events:
        #         eventData = {}
        #         eventData["id"] = id(expE)
        #         eventData["eventName"] = expE.eventName
        #         eventData["eventKey"] = expE.eventKey
        #         events.append(eventData)

        #######RETROCOMPATIBILITY FOR .jsonAnim
        allExportableAnim = []
        for expA in self.exportableAnimations:
            animationData = {}
            animationData["id"] = id(expA)
            animationData["clipName"] = expA.clipName
            animationData["startFrame"] = expA.startKey
            animationData["endFrame"] = expA.endKey
            animationData["isLoop"] = expA.isLoop
            animationData["isRoot"] = expA.isRoot
            animationData["events"] = []
            for expE in expA.events:
                eventData = {}
                eventData["id"] = id(expE)
                eventData["eventName"] = expE.eventName
                eventData["keyFrame"] = expE.eventKey
                animationData["events"].append(eventData)
            allExportableAnim.append(animationData)
        #######RETROCOMPATIBILITY FOR .jsonAnim

        exporterObjectsData = []
        expObjData = {}
        expObjData["id"] = id(exportableObject)
        expObjData["name"] = exportName
        expObjData["meshes"] = []
        # expObjData["animations"] = animations
        # expObjData["events"] = events
        expObjData["type"] = exportableObject.objectType
        expObjData["subType"] = exportableObject.objectSubType
        expObjData["extraData"] = exportableObject.compileExtraData()
        #######RETROCOMPATIBILITY FOR .jsonAnim
        if allExportableAnim:
            expObjData["extraData"]["objectAnimations"] = allExportableAnim
        #######RETROCOMPATIBILITY FOR .jsonAnim

        for obj in allObjects:
            if obj.contentType == EXPORTABLE_TYPE.MESH or obj.contentType == EXPORTABLE_TYPE.DATAMESH:
                meshData = {}
                meshData["id"] = id(obj)
                meshData["meshName"] = str(obj)
                materialsIds = [ {'materialId': matToId[str(meshMat)]} for meshMat in obj.represetationMaterials if str(meshMat) in matToId] #id(meshMat)

                meshData["materialIds"] = materialsIds
                expObjData["meshes"].append(meshData) 
            elif obj.contentType == EXPORTABLE_TYPE.POINT:
                # Exportal los puntos que ponen los usuarios en el 3DSMax
                # print("POINT")x
                pass
            
        exporterObjectsData.append(expObjData)

        data = {}
        # print "MATERIALS CHECKS! ", [ matIds["materialId"] for mesh in expObjData["meshes"] for matIds in mesh["materialIds"]]
        # print "MATERIALS ORIGINALS! ", [mat["id"] for mat in materials]

        # parsedMaterials = []
        # for mat in materials:
        #     for mesh in expObjData["meshes"]:
        #         for matIds in mesh["materialIds"]
        #             if mat["id"] in [matIds["materialId"]:

        usedMatIds = list(set([matIds["materialId"] for mesh in expObjData["meshes"] for matIds in mesh["materialIds"]]))
        data["materials"] = [mat for mat in materials  if mat["id"] in usedMatIds]
        data["objects"] = exporterObjectsData
        return data

