import bpy
import bmesh

import sys
import os
import json
import re

from operator import and_
from pantheonModules.logger.ateneaLogger import AteneaLogger
from pantheonModules.exporter.overrides import BaseOverrides
from pantheonModules.pantheonUtilities import fileSystemUtilities as fsu
from pantheonModules.exceptions.exportExceptions import CriticalExportException

from mathutils import Vector

class ExportUtilities(BaseOverrides.ExportUtilities): 

    @staticmethod
    def SetFBXParams():
        pass

    @staticmethod
    def ExportFBX(filePath):
        try:
            pathToSave = filePath.replace("\\","\\\\")+".fbx"
            bpy.ops.export_scene.fbx(bake_space_transform=True , filepath=(pathToSave))
            AteneaLogger.log("Saving... {0}".format(pathToSave))
        except Exception as e:
            file = FileUtilities.GetFullFileName()
            errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',ExportUtilities.ExportFBX.__name__)).lower()
            raise CriticalExportException(file,errorSpace,"Error Exporting, the reason could not be determined, call the developer")

class MeshesUtilities(BaseOverrides.MeshesUtilities): 
    exportableMeshes = ["MESH"]
    #bpy.context.selected_objects[0].type
    @staticmethod
    def GetAllChilds(parent,filt = None, includeParent = False):
        objs = []
        # if includeParent:
        #     objs.append(parent)

        #bpy.context.selected_objects[0].parent == None
        if parent.parent != None or includeParent:
            if filt:
                if parent.type in list(filt):
                    objs.append(parent)                 
            else:
                objs.append(parent)
        for obj in  parent.children:
            objs = objs + MeshesUtilities.GetAllChilds(obj,filt)


        return objs 

    @staticmethod
    def GetSubTree(parent,filt = None, includeParent = False):
        treeNode = {} #MAYBE CHANGE IT FOR A STRUCT?
        if parent.parent != None or includeParent:
            if filt:
                if parent.type in list(filt):
                    treeNode["node"] = parent                                
            else:
                treeNode["node"] = parent
                
        children = []
        for obj in  parent.children:
            children.append(MeshesUtilities.GetSubTree(obj,filt))
        treeNode["children"] = children
            # objs.append()
        return treeNode 


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
        if parent.children:
            objs = list(parent.children)        
            return objs

    @staticmethod
    def GetParent(obj):
        if obj:
            return obj.parent
        else:
            None


    @staticmethod
    def GetObjectClass(obj):
        className = obj.type
        return className

    @staticmethod
    def ReorderMesh(node): 


        assert node.type == "MESH"
        me = node.data

        bm = bmesh.new()
        bm.from_mesh(me)
        bm.verts.sort()
        bm.to_mesh(me)
        # new_order = list(range(len(bm.verts)))
        # random.shuffle(new_order)

        # for i, v in zip(new_order, bm.verts):
        #     v.index = i

        # print("shuffled indices:")
        # for v in bm.verts:
        #     print(v.index)

        # print("update index()")    
        # bm.verts.index_update()

        # print("indices returned to original order:")
        # for v in bm.verts:
        #     print(v.index)

        # print("shuffling again, followed by a sort:")
        # for i, v in zip(new_order, bm.verts):
        #     v.index = i
        # bm.verts.sort()

        # for v in bm.verts:
        #     print(v.index)

        # bm.to_mesh(me)

        # AteneaLogger.log("Processing " + node.name)

        # #bpy.ops.object.mode_set(mode='OBJECT')
        # #bpy.ops.object.select_all(action='DESELECT')
        

        
        # try:
        #     if len(node.material_slots) > 0:
        #         node.select  = True
        #         bpy.context.scene.objects.active = node
        #         bpy.ops.object.mode_set(mode="EDIT")
        #         bpy.ops.mesh.select_all(action="SELECT")
        #         bpy.ops.mesh.sort_elements(type='MATERIAL',reverse=False,elements={'FACE'})
        #         bpy.ops.object.mode_set(mode='OBJECT')
        #         node.select  = False

        # except Exception as e:
        #     file = FileUtilities.GetFullFileName()
        #     errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.ReorderMesh.__name__)).lower()
        #     raise CriticalExportException(file,errorSpace,"Error reordering '{0}' mesh , if you cant find anything wrong try to make a snapshot of it".format(node.name))

    @staticmethod
    def GetAllMaterialsFromObjects(objects):
        objectMaterials = []
        for obj in objects:
            bpy.ops.object.mode_set(mode='OBJECT')
            if len(obj.material_slots) > 0:
                for pol in obj.data.polygons:
                    if pol.material_index >= len(obj.material_slots):
                        file = FileUtilities.GetFullFileName()
                        errorSpace = " ".join(re.findall('[A-Z][^A-Z]*',MeshesUtilities.ReorderMesh.__name__)).lower()
                        raise CriticalExportException(file,errorSpace,"Error reading materials from '{0}' mesh , if you cant find anything wrong try to make a snapshot of it".format(nativeNode.name))
                    mat = obj.material_slots[pol.material_index] 
                    if not mat.name in objectMaterials: 
                        objectMaterials.append(mat)
        return list(objectMaterials)


        # objectMaterials = []
        # for obj in objects:
        #     mat = obj.GetMaterial()
        #     if mat:
        #         if mat.GetNumSubMtls() > 0:
        #             for i in range(0,mat.GetNumSubMtls()):
        #                 subMtl = mat.GetSubMtl(i)
        #                 if subMtl:
        #                     nativeNode = MiscUtilities.GetNativeFromINode(obj) #AT ONE POINT I SHOULD USE NATIVE NODE EVERYWHERE AND STOP CASTING
        #                     rt.convertToPoly(nativeNode)
        #                     nativeNode.selectByMaterial(i+1)
        #                     selectedFaces = rt.getFaceSelection(nativeNode)
        #                     facesCount = [(index+1) for index in range(selectedFaces.count) if selectedFaces[index] == True]
        #                     if facesCount:
        #                         objectMaterials.append(subMtl)
        #                     else:
        #                         print "{0} object has no faces for id {1}".format(nativeNode.name,i+1)
        #         else:
        #             if mat.GetName() not in [m.GetName() for m in objectMaterials]:
        #                 objectMaterials.append(mat)
                    
        # return list(objectMaterials)

    
    

    @staticmethod
    def SelectFullObject(objToSelect , add = False):
        bpy.ops.object.mode_set(mode='OBJECT')

        if not add:
            bpy.ops.object.select_all(action='DESELECT')


        if objToSelect:
            objectsToSelect = MeshesUtilities.GetAllChilds(objToSelect,includeParent=True)
            for obj in objectsToSelect:
                obj.select = True

        selectedObjects = bpy.context.selected_objects
        
        return selectedObjects 


    @staticmethod
    def MergeObjects(objects):
        if len(objects) == 0: return None
        if len(objects) == 1: return objects[0]


        scene = bpy.context.scene

        obs = []
        for ob in objects:
            if ob.type == 'MESH':
                obs.append(ob)

        ctx = bpy.context.copy()
        ctx['active_object'] = obs[0]
        ctx['selected_objects'] = obs
        ctx['selected_editable_bases'] = [scene.object_bases[ob.name] for ob in obs]

        bpy.ops.object.join(ctx)

        bm = bmesh.new()
        bm.from_mesh(obs[0].data)
        bmesh.ops.remove_doubles(bm, verts=bm.verts, dist=0.001)
        bm.to_mesh(obs[0].data)
        obs[0].data.update()

        bm.clear()
        bm.free()

        return obs[0]

    @staticmethod
    def SetPivotToPoss(obj,x,y,z):
        bpy.ops.object.mode_set(mode="OBJECT")
        bpy.context.scene.cursor_location = Vector((x,y,z))
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR')
        bpy.context.scene.cursor_location = Vector((0,0,0))

      

class LayersUtilities(BaseOverrides.LayersUtilities):

    exportableSkeleton = [""]
    exportableParents = ["EMPTY"]
    exportableMesh = ["MESH"]

    garbageLayer = [False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,False,True]

    def __init__(self):
        pass
        

    def loadAllLayerNames(self):        
        return list(bpy.context.scene.layers)

    @staticmethod
    def CleanGarbageLayer():

        garbageObjects = [o for o in bpy.data.objects if any(map(and_,o.layers,LayersUtilities.garbageLayer))]
        for go in garbageObjects:
            bpy.data.objects.remove(go)
        

class DataParser(BaseOverrides.DataParser): 
    version = 1
    exportableMeshes = ["MESH"]

    def __init__(self,output):
        # self.logger = AteneaLogger.AteneaLogger()
        # self.meshUtilities = MeshesUtilities()

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
            return True

        def __init__(self,node,attributeName):
            self.node = node
            self.attrName = attributeName


        def addCustomParameter(self,parameterName,parameterValue,parameterType = ATTR_TYPES.STRING):
            parameterValue = self.castFrom(parameterValue,parameterType)
            self.node["{0}_{1}".format(self.attrName,parameterName)] = parameterValue
            return "{0}_{1}".format(self.attrName,parameterName)


        def editCustomParameter(self,parameterName,parameterValue, parameterType = ATTR_TYPES.STRING):
            parameterValue = self.castFrom(parameterValue,parameterType)
            self.node["{0}_{1}".format(self.attrName,parameterName)] = parameterValue
            return "{0}_{1}".format(self.attrName,parameterName)


        def getCustomParameter(self,parameterName):
            if "{0}_{1}".format(self.attrName,parameterName) not in self.node:
                print ("Attribute {0}_{1} does not exists, cannot get!".format(self.attrName,parameterName))
                return None
            
            paramValue = self.node["{0}_{1}".format(self.attrName,parameterName)]

            value,typ = self.castTo(paramValue)

            attrParam = self.attributeParameter()
            attrParam.parameterName=  parameterName
            attrParam.parameterValue =  value
            attrParam.parameterType = typ


            return attrParam

        def deleteCustomParameter(self,parameterName):
            del(self.node["{0}_{1}".format(self.attrName,parameterName)])

        def listCustomParametersNames(self):
            paremetersNames = []
            for param in self.node.keys():
                if param.split("_")[0] == self.attrName:
                    paremetersNames.append(param.split("_")[1])
            
            return paremetersNames
            #return list(set(self.node.keys()) - set(('type', 'subtype')))

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
                            print("ARRAY elements should be all the same type", data)
                            return None
                    else:
                        dataToSave["typ"] = newType
                        dataToSave["value"] = data
                        return json.dumps(dataToSave)#.replace('"', '\\"')
                else:
                    print("This",data,"is not type ARRAY", data)
                    return None
                
            elif newType == self.ATTR_TYPES.BOOL: 
                dataToSave["typ"] = newType
                dataToSave["value"] = data
                return json.dumps(dataToSave)#.replace('"', '\\"')
            elif newType == self.ATTR_TYPES.NONE:
                return None
            else:
                print("ERROR , CAST FROM INVALID TYPE ", newType)
                return None

class FileUtilities(BaseOverrides.FileUtilities):

    @staticmethod
    def GetFullFileName():
        fullName = bpy.path.abspath("//")+os.path.basename(bpy.data.filepath).replace(".blend","")
        return fullName

    @staticmethod
    def GetFullPath():
        fullName = os.path.dirname(bpy.path.abspath("//")+os.path.basename(bpy.data.filepath).replace(".blend",""))+"\\"
        return fullName  

    @staticmethod
    def OpenFile(filePath):
        bpy.ops.wm.open_mainfile(filePath)
        return True  

    @staticmethod
    def SaveFile(filepath):
        bpy.ops.wm.save_mainfile(filePath)
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

class MiscUtilities(BaseOverrides.MiscUtilities):

    @staticmethod
    def SelectObject(*nodes):
        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')
        for node in nodes:
            node.select = True 
# bpy.ops.wm.quit_blender()
    @staticmethod
    def Exit(exitCode):
        # pass
        try:
            os._exit(exitCode)
        except Exception as e:
            print("CANNOT EXIT")

    @staticmethod
    def GetMaterialMaps(mat):
        maps = []
        for k in mat.node_tree.nodes.keys():
            if k[0] == "_":
                if mat.node_tree.nodes[k].image != None:
                    filePath = mat.node_tree.nodes[k].image.filepath.encode('utf-8')
                    maps.append(filePath)
        return list(set(maps))

    @staticmethod
    def GetAllSceneMaterials():
        return list(bpy.data.materials)

    @staticmethod
    def GetObjectName(obj):
        return obj.name

    @staticmethod    
    def SetObjectName(obj,name):
        obj.name = name
        return obj

    @staticmethod
    def GetRootObjects():
        return [o for o in bpy.data.objects if not o.parent]

    @staticmethod
    def SetParent(obj,parent):
        obj.parent= parent
        obj.matrix_parent_inverse = parent.matrix_world.inverted()
        return  obj

    @staticmethod
    def TakeObjectToWorldRoot(obj):
        bpy.ops.object.parent_set(type='OBJECT')
        bpy.ops.object.select_all(action="DESELECT")
        obj.select = True;
        bpy.ops.object.parent_clear(type='CLEAR_KEEP_TRANSFORM')
        return  obj

    @staticmethod
    def GetLocalPosition(obj):
        valuePoss = (obj.location[0],obj.location[1],obj.location[2])
        return valuePoss

    @staticmethod
    def GetLocalRotation(obj):
        roundedPoss = (round(obj.rotation_euler[0], 3),round(obj.rotation_euler, 3),round(obj.rotation_euler, 3))
        return roundedPoss

    @staticmethod
    def GetLocalScale(obj):
        valueScale = (obj.scale[0],obj.scale[1],obj.scale[2])
        return valueScale

    @staticmethod
    def GetCurrentSelection():
        return bpy.context.selected_objects


    @staticmethod
    def CreateEmptyObject(objectName = "NewObject", objectPosition = (0,0,0), objectRotation = (0,0,0) ,objectScale = (1,1,1) ):
        bpy.ops.object.empty_add(type='CUBE')
        empty = bpy.context.object
        bpy.context.object.location = objectPosition
        bpy.context.object.rotation_euler = objectRotation
        bpy.context.object.scale = objectScale
        return empty;

    @staticmethod
    def DeleteObject(objectToDelete, childrenPositionStays =False, keepChildren = True):
        bpy.ops.object.parent_set(type='OBJECT')
        children = objectToDelete.children
        childOldPositions = {}
        for child in children:
            childOldPositions[child] = child.location

        bpy.ops.object.select_all(action="DESELECT")
        objectToDelete.select = True 
        bpy.ops.object.delete()
        if childrenPositionStays:
            for child in childOldPositions.keys():
                child.location = childOldPositions[child]

    @staticmethod
    def SelectMaterial(material):
        pass

    @staticmethod
    def CreateMaterial(matName,matData):

        print("LOADING MAT ",matData)
        bpy.context.scene.render.engine = 'CYCLES'

        if matName in bpy.data.materials:
            print(matName + " already exist ")
            return

        newMaterial = bpy.data.materials.new(matName)
        newMaterial.use_nodes = True
        node_tree = newMaterial.node_tree
        MiscUtilities.CovertToPBR(node_tree)
        # if "_MainTex" in node_tree.nodes:
        #     node_tree.nodes["_MainTex"].select = True

        maxPath = FileUtilities.GetFullPath()
        shader = matData.shaderName

        matDataProperties = [prop for prop in matData.properties if prop.propType == "TexEnv"]
        

        for i in range(len(matDataProperties)):
            
            prop = matDataProperties[i]

            textureName = prop.propValue
            propName = prop.propName

            if not textureName : continue
            if not propName in node_tree.nodes: 
                continue
            
            texturePath = fsu.findFileInParents(textureName,maxPath,"/Textures")

            if not texturePath : 
                MiscUtilities.DeleteMaterial(newMaterial)
                newMaterial = None
                break

            loadedTexture = bpy.data.images.load(texturePath, check_existing=True)

            print("SETTING TEXTURE TO ", propName)
            node_tree.nodes[propName].image = loadedTexture

        return newMaterial

    @staticmethod
    def ResetMaterial(material,matData):
        maxPath = FileUtilities.GetFullPath()

        matDataProperties = [prop for prop in matData.properties if prop.propType == "TexEnv"]

        for i in range(len(matDataProperties)):
            prop = matDataProperties[i]

            textureName = prop.propValue
            propName = prop.propName

            if not textureName : continue
            
            texturePath = fsu.findFileInParents(textureName,maxPath,"/Textures")

            if not texturePath : 
                newMaterial = None
                break

            loadedTexture = bpy.data.images.load(texturePath, check_existing=True)
            node_tree[propName].image = loadedTexture

        return material

    @staticmethod
    def DeleteMaterial(matToDelete):
        bpy.data.materials.remove(matToDelete)

    @staticmethod
    def DisableShortcuts():
        pass

    @staticmethod
    def EnableShortcuts():
        pass

    @staticmethod
    def CovertToPBR(node_tree):
        node_tree.nodes.clear()

        newOutputMaterialNode = node_tree.nodes.new('ShaderNodeOutputMaterial')
        #output
        newmixShaderNode = node_tree.nodes.new('ShaderNodeMixShader')
        node_tree.links.new(newmixShaderNode.outputs['Shader'], newOutputMaterialNode.inputs['Surface'])

        #DetailMask
        detailMaskNode = node_tree.nodes.new('ShaderNodeTexImage')
        detailMaskNode.name = "_DetailMask"
    
        node_tree.links.new(detailMaskNode.outputs['Alpha'], newmixShaderNode.inputs['Fac'])

        #OcclusionMap
        separateRGBNode = node_tree.nodes.new('ShaderNodeSeparateRGB')
        aoColorNode = node_tree.nodes.new('ShaderNodeTexImage')
        aoColorNode.name = "_OcclusionMap"
        node_tree.links.new(aoColorNode.outputs['Color'], separateRGBNode.inputs['Image'])
        AOmultiplyNode = node_tree.nodes.new('ShaderNodeMixRGB')
        AOmultiplyNode.blend_type = 'MULTIPLY'
        node_tree.links.new(separateRGBNode.outputs['G'], AOmultiplyNode.inputs['Color2'])

        #MetallicGlossMap
        separateRGBMetallicNode = node_tree.nodes.new('ShaderNodeSeparateRGB')
        metallicColorNode = node_tree.nodes.new('ShaderNodeTexImage')
        metallicColorNode.name = "_MetallicGlossMap"
        node_tree.links.new(metallicColorNode.outputs['Color'], separateRGBMetallicNode.inputs['Image'])

        #EmissionMap
        newEmissionNode = node_tree.nodes.new('ShaderNodeEmission')
        # node_tree.links.new(newEmissionNode.outputs['Emission'], addEmmissionNode.inputs[0])
        emmisionColorNode = node_tree.nodes.new('ShaderNodeTexImage')
        emmisionColorNode.name = "_EmissionMap"
        node_tree.links.new(emmisionColorNode.outputs['Color'], newEmissionNode.inputs["Color"])

        #MainTex
        #BumpMap
        newPrincipledNode = node_tree.nodes.new('ShaderNodeBsdfPrincipled')
        # node_tree.links.new(newPrincipledNode.outputs['BSDF'], addEmmissionNode.inputs[1])
        baseColorNode = node_tree.nodes.new('ShaderNodeTexImage')
        baseColorNode.name = "_MainTex"
        normalMapTexNode = node_tree.nodes.new('ShaderNodeTexImage')
        normalMapTexNode.name = "_BumpMap"
        normalMapNode = node_tree.nodes.new('ShaderNodeNormalMap')
        node_tree.links.new(normalMapTexNode.outputs['Color'], normalMapNode.inputs["Color"])
        node_tree.links.new(normalMapNode.outputs['Normal'], newPrincipledNode.inputs["Normal"])
        node_tree.links.new(separateRGBMetallicNode.outputs['R'], newPrincipledNode.inputs["Metallic"])
        node_tree.links.new(aoColorNode.outputs['Alpha'], newPrincipledNode.inputs["Roughness"])
        node_tree.links.new(baseColorNode.outputs['Color'], AOmultiplyNode.inputs["Color1"])
        node_tree.links.new(AOmultiplyNode.outputs['Color'], newPrincipledNode.inputs['Base Color'])

        #DetailAlbedoMap
        #DetailNormalMap
        newBSDFBasicNode = node_tree.nodes.new('ShaderNodeBsdfDiffuse')
        node_tree.links.new(newBSDFBasicNode.outputs['BSDF'], newmixShaderNode.inputs[2])
        detailAlbedoColorNode = node_tree.nodes.new('ShaderNodeTexImage')
        detailAlbedoColorNode.name = "_DetailAlbedoMap"
        node_tree.links.new(detailAlbedoColorNode.outputs['Color'], newBSDFBasicNode.inputs["Color"])
        detailNormalMapTexNode = node_tree.nodes.new('ShaderNodeTexImage')
        detailNormalMapTexNode.name = "_DetailNormalMap"
        detailNormalMapNode = node_tree.nodes.new('ShaderNodeNormalMap')
        node_tree.links.new(detailNormalMapTexNode.outputs['Color'], detailNormalMapNode.inputs["Color"])
        node_tree.links.new(detailNormalMapNode.outputs['Normal'], newBSDFBasicNode.inputs["Normal"])

        #ParallaxMap
        parallaxMap = node_tree.nodes.new('ShaderNodeTexImage')
        parallaxMap.name = "_ParallaxMap"
        node_tree.links.new(parallaxMap.outputs['Color'], newOutputMaterialNode.inputs["Displacement"])

        # newOutputMaterialNode.select = False
        # newmixShaderNode.select = False
        # detailMaskNode.select = False
        # separateRGBNode.select = False
        # aoColorNode.select = False
        # AOmultiplyNode.select = False
        # separateRGBMetallicNode.select = False
        # metallicColorNode.select = False
        # newEmissionNode.select = False
        # emmisionColorNode.select = False
        # newPrincipledNode.select = False
        # baseColorNode.select = False
        # normalMapTexNode.select = False
        # normalMapNode.select = False
        # newBSDFBasicNode.select = False
        # detailAlbedoColorNode.select = False
        # detailNormalMapTexNode.select = False
        # detailNormalMapNode.select = False
        # parallaxMap.select = False


class AnimationUtilities(BaseOverrides.AnimationUtilities): pass


    

    

    

    



