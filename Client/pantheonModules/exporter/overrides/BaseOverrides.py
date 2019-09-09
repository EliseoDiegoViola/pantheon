class ExportUtilities():

    def __init__(self):
        print("ExportUtilities NOT IMPLEMENTED ============================================")

    def setFBXParams(self):
        print("setFBXParams NOT IMPLEMENTED ============================================")

    def exportFBX(self,filePath):
        print("exportFBX NOT IMPLEMENTED ============================================")

    def getFBXData(self,filePath):
        print("getFBXData NOT IMPLEMENTED ============================================")
        return None

    def getOBJData(self,filePath,objToExport): 
        print("getOBJData NOT IMPLEMENTED ============================================")
        return None

    # def validateSelectedObjects(self,parents):
    #     print("validateSelectedObjects NOT IMPLEMENTED ============================================")
    #     objectValidity = []
    #     if not parents:
    #         return []
    #     for parent in parents:
    #         objectValidity.append( (parent,[lambda objects: ("001",[])]))

    #     return objectValidity


class MeshesUtilities(): 

    def __init__(self):
        print("MeshesUtilities NOT IMPLEMENTED ============================================")

    def getRigType(self):
        print("getRigType NOT IMPLEMENTED ============================================")
        return None

    @staticmethod
    def GetAllChilds(parent,filt = None, includeParent = False):
        print("GetAllChilds NOT IMPLEMENTED ============================================")
        if includeParent:
            return [parent]
        else:
            return []

    @staticmethod
    def GetSubTree(parent,filt = None, includeParent = False):
        print("GetFullFromParent NOT IMPLEMENTED ============================================")
        if includeParent:
            treeNode = {}
            treeNode["node"] = parent
            treeNode["children"] = []
            return treeNode
        else:
            return {"node" : None , "children" : []}
        
    # def getAllChilds(self,parent,filt = None):
    #     print("getAllChilds NOT IMPLEMENTED ============================================")
    #     return None

    @staticmethod
    def GetChildren(parent):
        print("GetChildren NOT IMPLEMENTED ============================================")
        return []

    @staticmethod
    def GetParent(obj):
        print("GetParent NOT IMPLEMENTED ============================================")
        return None

    @staticmethod
    def GetObjectClass(obj):
        print("GetObjectClass NOT IMPLEMENTED ============================================")
        return None

    @staticmethod
    def ReorderMesh(node):
        print("ReorderMesh NOT IMPLEMENTED ============================================")


    @staticmethod
    def MergeObjects(objects):
        print("MergeObjects NOT IMPLEMENTED ============================================")
        return objects[0]        

    # def checkForInstances(self,parent):
    #     print("checkForInstances NOT IMPLEMENTED ============================================")
    #     return ("001",[])

    # def filterCollidersInSelection(self, parent, nodes):
    #     print("filterCollidersInSelection NOT IMPLEMENTED ============================================")
    #     return []

    # def filterExtraDataInSelection(self, parent, nodes):
    #     print("filterExtraDataInSelection NOT IMPLEMENTED ============================================")
    #     return []

    @staticmethod
    def SetPivotToPoss(self,obj,x,y,z):
        print("SetPivotToPoss NOT IMPLEMENTED ============================================")

    @staticmethod
    def SelectFullObject(objToSelect , add = False):
        print("SelectFullObject NOT IMPLEMENTED ============================================")
        return [] 


    @staticmethod
    def GetAllMaterialsFromObjects(objects):
        print("GetAllMaterialsFromObjects NOT IMPLEMENTED ============================================")
        return []         

class LayersUtilities():

    exportableParents = []
    exportableSkeleton = []
    exportableMesh = []
    garbageLayer = []

    def __init__(self):
        print("LayersUtilities NOT IMPLEMENTED ============================================")

    # def loadAllLayerNames(self):
    #     print("loadAllLayerNames NOT IMPLEMENTED ============================================")
    #     return None
    @staticmethod
    def CleanGarbageLayer():
        print("cleanGarbageLayer NOT IMPLEMENTED ============================================")

    # def selectObjectsInLayers(self,*args,**kwargs):
    #     print("selectObjectsInLayers NOT IMPLEMENTED ============================================")



class DataParser():

    def __init__(self,output):
        print("DataParser NOT IMPLEMENTED ============================================")

    # def parseDataObject(self,objToParse):    
    #     print("parseDataObject NOT IMPLEMENTED ============================================")
    #     return None


    class nodeAttribute():

        @staticmethod
        def IsDefined(node,attributeName):
            print("IsDefined NOT IMPLEMENTED ============================================")
            return False

        class ATTR_TYPES:
            NONE = -1
            STRING = 0
            NODE = 1
            NUMBER = 2
            ARRAY = 3
            BOOL = 4

        class attributeParameter():
            parameterName = None
            parameterValue = None
            parameterType = -1


        def __init__(self,node,attributeName):
            print("nodeAttribute NOT IMPLEMENTED ============================================")

        def addCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            print("addCustomParameter NOT IMPLEMENTED ============================================")
            return ""

        def editCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            print("editCustomParameter NOT IMPLEMENTED ============================================")

        def getCustomParameter(self,parameterName):
            print("getCustomParameter NOT IMPLEMENTED ============================================")
            return None

        def deleteCustomParameter(self,parameterName):
            print("deleteCustomParameter NOT IMPLEMENTED ============================================")

        def listCustomParametersNames(self):
            print("listCustomParametersNames NOT IMPLEMENTED ============================================")
            return []        


class FileUtilities():

    @staticmethod
    def GetFullFileName():
        print("GetFullFileName NOT IMPLEMENTED ============================================")
        return None

    @staticmethod
    def GetFullPath():
        print("GetFullPath NOT IMPLEMENTED ============================================")
        return None

    @staticmethod
    def OpenFile(filePath):
        print("OpenFile NOT IMPLEMENTED ============================================")
        return False

    @staticmethod
    def SaveFile(filepath):
        print("SaveFile NOT IMPLEMENTED ============================================")
        return False

    @staticmethod
    def optimizeScene():
        print("optimizeScene NOT IMPLEMENTED ============================================")

    @staticmethod
    def GetFileArguments():
        print("GetFileArguments NOT IMPLEMENTED ============================================")
        return []

class MiscUtilities():

    @staticmethod
    def Exit(exitCode):
        print("Exit NOT IMPLEMENTED ============================================")

    @staticmethod
    def CheckDuplicatedMaterials():
        print("CheckDuplicatedMaterials NOT IMPLEMENTED ============================================")
        return []

    @staticmethod
    def GetAllSceneMaterials():
        print("GetMaterialMaps NOT IMPLEMENTED ============================================")
        return []

    @staticmethod
    def GetMaterialMaps(mat):
        print("GetMaterialMaps NOT IMPLEMENTED ============================================")
        return []

    @staticmethod
    def GetRootObjects():
        print("GetRootObjects NOT IMPLEMENTED ============================================")
        return []

    @staticmethod    
    def GetObjectName(obj):
        print("GetObjectName NOT IMPLEMENTED ============================================")
        return None

    @staticmethod    
    def SetObjectName(obj,name):
        print("SetObjectName NOT IMPLEMENTED ============================================")

    @staticmethod    
    def ImportReferences():
        print("importReferences NOT IMPLEMENTED ============================================")

    @staticmethod    
    def AddTemporalNamespace(obj):
        print("AddTemporalNamespace NOT IMPLEMENTED ============================================")
        return obj

    @staticmethod  
    def GetNamespce(obj):
        print("GetNamespce NOT IMPLEMENTED ============================================")
        return None

    @staticmethod    
    def RemoveNamespace(obj):
        print("RemoveNamespace NOT IMPLEMENTED ============================================")
        return obj[0]

    @staticmethod
    def SetParent(obj,parent):
        print("SetParent NOT IMPLEMENTED ============================================")
        return obj

    @staticmethod    
    def TakeObjectToWorldRoot(obj):
        print("TakeObjectToWorldRoot NOT IMPLEMENTED ============================================")
        return obj

    @staticmethod
    def GetLocalPosition(obj):
        print("GetLocalPosition NOT IMPLEMENTED ============================================")
        return (-9999,-9999,-9999)

    @staticmethod    
    def CleanSkeleton(objsToConserve,typesToExclude):
        print("cleanModel NOT IMPLEMENTED ============================================")

    @staticmethod
    def SelectObject(*nodes):
        print("SelectObject NOT IMPLEMENTED ============================================")

    @staticmethod
    def CheckEZMatsFile():
        print("CheckEZMatsFile NOT IMPLEMENTED ============================================")
        return ("001",[])

    @staticmethod
    def CheckModifiers(parent):
        print("CheckModifiers NOT IMPLEMENTED ============================================")
        return ("001",[])

    # @staticmethod
    # def CheckAttributes(parent):
    #     print("CheckAttributes NOT IMPLEMENTED ============================================")
    #     return ("001",[])

    @staticmethod
    def GetCurrentSelection():
        print("GetCurrentSelection NOT IMPLEMENTED ============================================")
        return [];

    @staticmethod
    def CreateEmptyObject(objectName = "NewObject", objectPosition = (0,0,0), objectRotation = (0,0,0) ,objectScale = (1,1,1)):
        print("CreateEmptyObject NOT IMPLEMENTED ============================================")
        return None;

    @staticmethod
    def IsNodeGroup(obj):
        print("IsNodeGroup NOT IMPLEMENTED ============================================") 
        return False

    @staticmethod
    def OpenGroup(obj):
        print("OpenGroup NOT IMPLEMENTED ============================================") 
        return []
        

    @staticmethod
    def DeleteObject(objectToDelete, childrenPositionStays =False, keepChildren = True):
        print("DeleteObject NOT IMPLEMENTED ============================================") 

    @staticmethod
    def DeleteMaterial(matToDelete):
        print("DeleteMaterial NOT IMPLEMENTED ============================================") 

    @staticmethod
    def CreateMaterial(matName,matData,mapTable = None):
        print("CreateMaterial NOT IMPLEMENTED ============================================")

    @staticmethod
    def SelectMaterial(material): 
        print("SelectMaterial NOT IMPLEMENTED ============================================")


    @staticmethod
    def ResetMaterial(material,matData,mapTable = None):
        print("ResetMaterial NOT IMPLEMENTED ============================================") 

    @staticmethod
    def DisableShortcuts():
        print("DisableShortcuts NOT IMPLEMENTED ============================================") 

    @staticmethod
    def EnableShortcuts():
        print("EnableSDhortcuts NOT IMPLEMENTED ============================================") 


class AnimationUtilities():


    unlockDefault = []

    @staticmethod
    def IsMeshSkinned(obj):
        # print("IsMeshSkinned NOT IMPLEMENTED ============================================")
        return False

    @staticmethod
    def UnlockObjectsByType(*args):
        print("unlockObjectsByType NOT IMPLEMENTED ============================================")

    @staticmethod
    def UnlockObjects(objs):
        print("unlockObjects NOT IMPLEMENTED ============================================")

    @staticmethod
    def BakeAnimations(objectsToBake):
        print("bakeAnimations NOT IMPLEMENTED ============================================")

    @staticmethod
    def PrepareAnimationsForExport():
        print("prepareAnimationsForExport NOT IMPLEMENTED ============================================")

    @staticmethod
    def HasAnimations():
        print("HasAnimations NOT IMPLEMENTED ============================================")
        return False


class CallBackUtilities():

    MOVEMENT_CALLBACK = None
    SCALE_CALLBACK = None
    ROTATION_CALLBACK = None

    
    def __init__(self):
        print("CallBackUtilities NOT IMPLEMENTED ============================================")
        self.callbackLists = {}

    def clean(self,force = False):
        print("clean NOT IMPLEMENTED ============================================")

    def addCallbackToObj(self,callbackName,callbackType,obj,bind):
        print("addNewCallback NOT IMPLEMENTED ============================================")
        self.callbackLists[callbackName] = callback(callbackType,obj,bind)
        self.callbackLists[callbackName].register()

    def removeCallback(self,callbackName):
        print("removeCallback NOT IMPLEMENTED ============================================")
        self.callbackLists[callbackName].unRegister()
        self.callbackLists[callbackName] = None



    class callback():

        def __init__(self,callbackType,obj,bind):
            print("callback NOT IMPLEMENTED ============================================")
            self.bind = bind
            self.obj = obj
            self.callbackType = callbackType
        
        def register(self):
            print("register NOT IMPLEMENTED ============================================")

        def unRegister(self):
            print("unRegister NOT IMPLEMENTED ============================================")

        def onExecuted(self):
            print("onExecuted NOT IMPLEMENTED ============================================")
            self.bind(self.obj)
