from .exportableContent import *
from .exportable import *
from .exportableMaterial import *
import json

class exportableObject(exportable):
    

    exportableChildren = []
    exportableContent = []

    objectType = None
    objectSubType = None
    extraData = None
    exportableName = None

    # colliderNames = []
    # pointsNames = []
    represetationMaterials = []

    def __repr__(self):
        return self.localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)      

    def __init__(self,baseNode,parent,typ):
        
        super(exportableObject,self).__init__(baseNode,parent,typ)
        self.sceneInstance = self.exportableParent.sceneInstance
        self.parseObjectData()
        self.parseChildren()
        

    def parseObjectData(self):
        if not self.localOverride.DataParser.nodeAttribute.IsDefined(self.objectRepresentation,'ObjectBaseData'): return


        baseData = self.localOverride.DataParser.nodeAttribute(self.objectRepresentation,'ObjectBaseData')

        typeAttr = baseData.getCustomParameter("type")
        sTypeAttr = baseData.getCustomParameter("subtype")

        if typeAttr and sTypeAttr:
            self.objectType = typeAttr.parameterValue
            self.objectSubType = sTypeAttr.parameterValue

            objectExtraData = self.localOverride.DataParser.nodeAttribute(self.objectRepresentation,'ObjectExtraData')
            extraParameters = objectExtraData.listCustomParametersNames()
            self.extraData = {}
            for parameter in extraParameters:
                # print("PARSING EXTRA PARAMETER: " + parameter)
                
                attrParam = objectExtraData.getCustomParameter(parameter)
                self.extraData[attrParam.parameterName] = attrParam.parameterValue
                self.searchDataNodesChildren(attrParam.parameterValue)
                # print(attrParam.parameterValue)
                
        else:
            self.objectType = None 
            self.objectSubType = None
            
    def searchDataNodesChildren(self,data):
        if isinstance(data,list):
            for element in data:
                self.searchDataNodesChildren(element)
                # print "THE KEY IS, " ,[key for key in element]
                # self.sceneInstance.dataNodes = self.sceneInstance.dataNodes + [element[key] for key in element if "node" in key.lower()] ###FIX
                # print "DATA NODES! ",self.sceneInstance.dataNodes 
        if isinstance(data,dict):
            for key in data:
                if "node" in key.lower():
                    self.sceneInstance.dataNodes.append(data[key])
                self.searchDataNodesChildren(data[key])

    def parseChildren(self):
        self.exportableChildren = []
        self.exportableContent = []
        exportableParentTypes = self.localOverride.LayersUtilities.exportableParents
        exportableSkeletonTypes = self.localOverride.LayersUtilities.exportableSkeleton
        exportableMeshes = self.localOverride.LayersUtilities.exportableMesh
        # print "ABOUT TO PARSE ", self
        childs = self.localOverride.MeshesUtilities.GetChildren(self.objectRepresentation)
        while(len(childs) > 0):
            child = childs.pop()
        # for child in childs:
            # child = childs[i]

            # childName = self.localOverride.MiscUtilities.GetObjectName(child)     
            # print("IS AAAAA" , childName)

            if self.localOverride.MiscUtilities.IsNodeGroup(child):
                ungrouped = self.localOverride.MiscUtilities.OpenGroup(child)
                # print "CHILDS ", childs
                childs = childs + ungrouped
                # print "CHILDS ", childs
                continue


            childName = self.localOverride.MiscUtilities.GetObjectName(child)     
            childClass = self.localOverride.MeshesUtilities.GetObjectClass(child)
            if childClass in exportableParentTypes:
                newExportableObject = exportableObject(child,self,EXPORTABLE_TYPE.DUMMY)
                self.exportableChildren.append(newExportableObject)
            elif childClass in exportableSkeletonTypes:
                # print "FOUND SKELETON! ", child
                newExportableContent = exportableContent(child,self,EXPORTABLE_TYPE.SKELETON)
                self.exportableContent.append(newExportableContent)
            elif childClass in exportableMeshes:
                print(child)
                print(childName)
                print(self.sceneInstance.dataNodes)
                if childName in self.sceneInstance.dataNodes:
                    newExportableContent = exportableContent(child,self,EXPORTABLE_TYPE.DATAMESH)
                else:
                    newExportableContent = exportableContent(child,self,EXPORTABLE_TYPE.MESH)

                self.exportableContent.append(newExportableContent)
            elif childName in self.sceneInstance.dataNodes:
                newExportableContent = exportableContent(child,self,EXPORTABLE_TYPE.DATA)
                self.exportableContent.append(newExportableContent)

            

                
    
                    



    def mergeChildren(self):
        mergeableObjects = [obj for obj in self.exportableContent 
            if obj.contentType == EXPORTABLE_TYPE.MESH and not self.localOverride.AnimationUtilities.IsMeshSkinned(obj.objectRepresentation)]
        notMergeableExportableObjects = [obj for obj in self.exportableContent if obj not in mergeableObjects]


        if mergeableObjects:
            parentName = localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)
            #print "AND THE OBJECT IS ",self.localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)
            
            position = self.localOverride.MiscUtilities.GetLocalPosition(self.objectRepresentation)
            #print "AND THE POSITION IS ",position
            
            self.objectRepresentation = localOverride.MiscUtilities.AddTemporalNamespace(self.objectRepresentation)

            mergedObject = self.localOverride.MeshesUtilities.MergeObjects([obj.objectRepresentation for obj in mergeableObjects])
            mergedObject = self.localOverride.MiscUtilities.SetObjectName(mergedObject,parentName)
            
            mergedExportableObject = exportableContent(mergedObject,self,EXPORTABLE_TYPE.MESH) #Idiotic....
            mergedExportableObject.getMaterials()
            #print "AND THE OBJECT IS ",self.localOverride.MiscUtilities.GetObjectName(self.objectRepresentation)

            #position = self.localOverride.MiscUtilities.GetLocalPosition(self.objectRepresentation)
            #print "AND THE POSITION IS ",position
            #raise Exception("ABOUT TO SET PIVOT!")
            self.localOverride.MeshesUtilities.SetPivotToPoss(mergedObject,position[0],position[1],position[2]) 

            
            self.exportableContent = notMergeableExportableObjects 
            self.exportableParent.adoptChild(mergedExportableObject)
            self.localOverride.MiscUtilities.DeleteObject(self.objectRepresentation, childrenPositionStays = True)

            ##HACK! You should track the  merged materials
            # print mergedExportableObject.represetationMaterials , mergedExportableObject
            # self.represetationMaterials = [scnMat for merMat in  mergedExportableObject.represetationMaterials for scnMat in self.sceneInstance.exportableMaterials if str(scnMat) == str(merMat)]
            # print self.represetationMaterials , mergedExportableObject
            self.contentType = EXPORTABLE_TYPE.MESH
            self.objectRepresentation = mergedObject
            self.represetationMaterials = mergedExportableObject.represetationMaterials
            
        if notMergeableExportableObjects:
            for notMergeable in notMergeableExportableObjects:
                notMergeable.getMaterials()
                notMergeable.represetationMaterials = [scnMat for merMat in  notMergeable.represetationMaterials for scnMat in self.sceneInstance.exportableMaterials if str(scnMat) == str(merMat)]

        for expO in self.exportableChildren:
            expO.mergeChildren()

    # def prepareAnimation(self):
    #     rootBoneName = objectExtraData.getCustomParameter("rootBoneName")
    #     if not rootBoneName: #Hackity for now
    #         rootBoneName = "Root"


    #     if self.localOverride.AnimationUtilities.HasAnimation:
            # self.localOverride.AnimationUtilities.UnlockObjectsByType(self.localOverride.AnimationUtilities.unlockDefault)
            # self.localOverride.MiscUtilities.TakeObjectToWorldRoot(rootBoneName)
            # rootH = self.localOverride.MeshUtilities.SelectFullObject(rootBoneName)
            # self.localOverride.AnimationUtilities.BakeAnimations(rootH)
            # self.localOverride.MiscUtilities.CleanModel(objsToConserve = [rootBoneName], typesToExclude = ['constraint'])
     
    def findSkeletonParent(self):
        print("SEARCHING IN ", str(self))
        skeP = None
        for expC in self.exportableContent:
            if expC.contentType == EXPORTABLE_TYPE.SKELETON:
                print("THEY FOUND ME ", str(self))
                return self
        for expO in self.exportableChildren:
             skeP = expO.findSkeletonParent()
             if skeP:
                break
        return skeP

    def isolateAnimation(self,skeletonParent):
        for expC in skeletonParent.exportableContent:
            if expC.contentType == EXPORTABLE_TYPE.SKELETON:
                print(" THE SKELETON PARENT IS ",str(expC))

                self.exportableParent.adoptChild(expC)
                self.localOverride.MiscUtilities.DeleteObject(self.objectRepresentation,keepChildren = False)
                
                newObject = self.localOverride.MiscUtilities.AddTemporalNamespace(expC.objectRepresentation)
                self.objectRepresentation = newObject
                self.exportableContent = []
                self.exportableChildren = []
                self.localOverride.MiscUtilities.CleanSkeleton(objsToConserve = [str(self)], typesToExclude = ['constraint']) ##|Root find how to track the name changes by hierarchy changes on MAX
                

    def unlockObjects(self):
        self.localOverride.AnimationUtilities.UnlockObjectsByType(self.localOverride.AnimationUtilities.unlockDefault)

    def bakeAnimations(self):
        # print "BAKE ANIMATIONS! "
        self.localOverride.MeshesUtilities.SelectFullObject([])

        content = []
        # print "CONTENT!! ",self.exportableContent
        for expC in self.exportableContent:
            # print " ABOUT TO PARSE ! ",expC
            if expC.contentType == EXPORTABLE_TYPE.SKELETON:
                # print " SKELETON TO BAKE ! ",expC
                content = self.localOverride.MeshesUtilities.SelectFullObject(expC.objectRepresentation, add =True)
                if content:
                    self.localOverride.AnimationUtilities.BakeAnimations(content)
                    self.localOverride.AnimationUtilities.PrepareAnimationsForExport(expC.objectRepresentation)

        for expO in self.exportableChildren:
            expO.bakeAnimations()

    def reparentChildren(self):
        self.exportableParent.adoptChild(self)
        for expC in self.exportableContent:
            print(expC)
            self.adoptChild(expC)             

        for expO in self.exportableChildren:
            expO.reparentChildren()

    def propagateObjectData(self):
        if not self.objectType and isinstance(self.exportableParent,exportableObject):
            self.objectType = self.exportableParent.objectType
        if not self.objectSubType and isinstance(self.exportableParent,exportableObject):
            self.objectSubType = self.exportableParent.objectSubType
        # if not self.extraData and isinstance(self.exportableParent,exportableObject):
        #     self.extraData = self.exportableParent.extraData
        for expO in self.exportableChildren:
            expO.propagateObjectData()


    def compileExtraData(self):
        # print "STARTED!",self
        cachedData = self.extraData
        for expO in self.exportableChildren:
            # print expO, cachedData
            cachedData = self.mergeData(cachedData,expO.compileExtraData())
        return cachedData 

    # def assignData(self,allData):
    #     if allData:
    #         for u in allData:
    #             print u
    #             print allData[u]

    
    def mergeData(self,data1,data2):
        newData = {}
        # print "DATA 1",data1
        # print "DATA 2",data2
        if data1 and data2:
            allKeys = list(set(list(data1.keys()) + list(data2.keys())))
            # print "DEBUG 1 ",allKeys
            for key in allKeys:
                if key in data1 and key not in data2:
                    # print "DEBUG 2.1 ",key
                    newData[key] = data1[key]
                elif key not in data1 and key in data2:
                    # print "DEBUG 2.2 ",key
                    newData[key] = data2[key]
                elif key not in data1 and key not in data2:
                    print("SEVERE ERROR KEY ",key," IS NOT IN EITHER DICT!?")
                elif key in data1 and key in data2:
                    # print "DEBUG 2.3"
                    if type(data1[key]) != type(data2[key]):
                        print("SEVERE ERROR IN MERGE ",key," IS NOT IN THE SAME TYPE IN ", data1 , data2)
                    else:
                        if type(data1[key]) is set:
                            newData[key] = data1[key]|data2[key]
                        elif type(data1[key]) is list:
                            if any([val for val in data1[key] if val in data2[key]]):
                                print("SEVERE ERROR IN MERGE DIFFERENTS ARRAYS HAVE SAME KEY ",key, data1 , data2)
                            newData[key] = list(set(data1[key]+data2[key]))
                        elif type(data1[key]) is dict:
                            newData[key] = self.mergeData(data1[key],data2[key])
                        else:
                            newData[key] = data1[key]
            # print "FINAL DATA",newData
            return newData
        elif data1 and not data2:
            return data1
        elif not data1 and data2:
            return data2
        else:
            return {}
        
                




    def reorderMeshes(self):
        if self.contentType == EXPORTABLE_TYPE.MESH or self.contentType == EXPORTABLE_TYPE.DATAMESH:
            self.localOverride.MeshesUtilities.ReorderMesh(self.objectRepresentation)
            

        if self.exportableContent:
            for expC in self.exportableContent:
                if expC.contentType == EXPORTABLE_TYPE.MESH or expC.contentType == EXPORTABLE_TYPE.DATAMESH:
                    self.localOverride.MeshesUtilities.ReorderMesh(expC.objectRepresentation)

        for expO in self.exportableChildren:
            expO.reorderMeshes()

    def getFlatternHierarchy(self):
        flatList = []
        flatList.append(self)
        flatList = flatList + [obj for obj in self.exportableContent]

        for expO in self.exportableChildren:
            flatList = flatList + expO.getFlatternHierarchy()

        return flatList
    