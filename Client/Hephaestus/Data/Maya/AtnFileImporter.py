import json
import urllib2 as url
import os
import copy
from sets import Set
import sys
import maya.mel as mel
import threading
import maya.utils as utils
import maya.cmds as cmds
import pymel.core as pm
import time
import maya.mel as mel
import tempfile

version = 1

artistsPlaticPath = "C:\\Proyectos\\Artmasters"



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


def loadUnityMaterialsData():
    shadersData = json.loads(url.urlopen("http://sv-server:13370/tools/data/shaders").read().decode("utf-8") )["shaders"]
   
    return shadersData

class AteneaImporter():

    def createShader(self,shaderType='StingrayPBS', name=''):
        if name == '':
            name = shaderType
        
        print(shaderType)
        print(name)
        shader = cmds.shadingNode(shaderType, asShader=True,  name=name)
        

        return shader
    def createShaderGroup(self,shader,name=''):
        if name == '':
            name = shaderType

        sg = cmds.sets(renderable=True, noSurfaceShader=True, name='%sSG'%(name))
        cmds.connectAttr('%s.outColor' %shader ,'%s.surfaceShader' %sg)
        return sg

    def assignMaterials(self,objectsData,importedMaterials,morder):
        print("READY TO ASSIGN " + str(objectsData))
        for obj in objectsData:
            for mesh in obj["meshes"]:
                
                meshName = mesh["meshName"]
                meshesMaterials = morder[meshName]
                for matName in meshesMaterials:
                    matAssignment = meshesMaterials[matName]
                    cmds.select( clear=True )
                    for i in range(matAssignment["first"],matAssignment["last"]):
                        cmds.select(meshName+'.f['+str(i)+']',add=True)
                        #cmds.sets(e=True, forceElement="SU_hallway_meshtrim1SG")
                    #material = next((x for x in test_list if x.value == value), None)

                    print("MESH : " + meshName)
                # for mat in mesh["materialIds"]:
                #     matId = mat["materialId"]
                    print("Assigning " + importedMaterials[matName] + " TO " + meshName)
                    cmds.sets(e=True, forceElement=importedMaterials[matName])
                    #self.assignShaderToSelection(importedMaterials[matName],meshName)
        print("DONE!")




    def loadAteneaFile(self):
        basicFilter = "*.atenea"
        a = cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2,fileMode=1)
        if a and len(a) == 1:
            return a[0]
        else:
            print("ERROR OPENING THE FILE")
            return ""

    
#


    def setupMaterial(self,matData,shader):
        mel.eval("shaderfx -sfxnode \""+shader+"\" -initShaderAttributes")
        shaderName = matData["shaderName"]
        properties = matData["properties"]
        for prop in properties:
            propType = prop["propType"]
            propValue = prop["propValue"]
            propName = prop["propName"]
            if 'TexEnv' in propType:
                if equivalenceShaderTable[propName][0]: 
                    self.setMaterialProperties(shader,propName,propValue)
    
    def setMaterialProperties(self,shader,propName,propValue):
        print("ACTIVATE :" + shader+"."+equivalenceShaderTable[propName][0])
        cmds.setAttr('%s.%s' %(shader,equivalenceShaderTable[propName][0]), True)

        fileNodeName = 'file'
        file_node=cmds.shadingNode(fileNodeName,asTexture=True)
        
        texFile = (artistsPlaticPath+"/Textures/"+ propValue)
        print("ASSIGN : " +file_node + " TO " + texFile)
        cmds.setAttr( file_node +'.fileTextureName', texFile, type = "string")
        cmds.connectAttr('%s.outColor' %file_node,shader+"."+equivalenceShaderTable[propName][1])

    def importMaterials(self,matData):    
        matProps = {}
        for x in range(0,len(matData)):
            matName = x
            found = cmds.ls( matData[matName]["name"] ,typ="StingrayPBS")
            if found:
                shader = matData[matName]["name"] 
                shaderGroup = self.createShaderGroup( shader = shader, name = matData[matName]["name"])    
                
            else:
                shader = self.createShader( name = matData[matName]["name"])    
                self.setupMaterial(matData[matName],shader)
                shaderGroup = self.createShaderGroup( shader = shader, name = matData[matName]["name"])    
                
            
            
            matProps[matData[matName]["name"]] = shaderGroup     

        return matProps


    def importObj(self,objData):
        objDir = tempfile.gettempdir() + "\\tmp.obj"

        with open(objDir, "w+") as objFile:
            objFile.write(objData)

        return cmds.file(objDir.replace("\\","/"), i=True,typ="OBJ",rpr= "tmp",ignoreVersion=True,rnn=True)

    def assignLayers(self,objects):
        meshesName = "Meshes"
        cmds.createDisplayLayer( nr=True, name=meshesName, number=1 )
        cmds.editDisplayLayerMembers('Meshes', objects ,nr=True)
        cmds.setAttr('%s.displayType' %meshesName, 0)
        cmds.setAttr('%s.color' %meshesName, 13)

    def importAtenea(self,filePath):
        if os.path.exists(filePath):
            with open(filePath,'r') as obj_data_file:
                ateneaData = json.load(obj_data_file)

        objdata = ateneaData["obj"]
        materialsData = ateneaData["data"]["materials"]
        materialsOrder = ateneaData["matOrder"]
        objectsData = ateneaData["data"]["objects"]
        newNodes = self.importObj(objdata)
        self.assignLayers(newNodes)
        importedMaterials = self.importMaterials(materialsData)
        self.assignMaterials(objectsData,importedMaterials,materialsOrder)



    # def assignShaderToSelection(self,shaderSG=None, objectName=None):
    #     if objectName is None:
    #         objects = cmds.ls(sl=True, l=True)
    #     else:
    #         objects = cmds.ls(objectName)
    #     for obj in objects:
    #         print obj
    #         try:
    #             cmds.sets(obj, e=True, forceElement=shaderSG)
    #         except:
    #             pass

    # def selectNode(self,name):
    #     cmds.select(name, r=True)
    #     print("\nSELECTED " +name)


ateneaImporter = AteneaImporter()
file = ateneaImporter.loadAteneaFile()
if file:
    ateneaImporter.importAtenea(file)



