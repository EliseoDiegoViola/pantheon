import sys
import os
import json
sys.path.append('C:/Proyectos/BuildSystem')
from AteneaModules.parser import jsonStructures

import maya.standalone as std
# std.initialize(name='python')


import maya.cmds as cmds
# cmds.loadPlugin("fbxmaya")

import pymel.core as pm



#import maya.mel as mel
#mel.eval('source "namedCommandSetup.mel"')

#import pymel.core as pCore

version = 1


def exportFBX(filePath):
    try:
        #HIKCharName = pCore.melGlobals['gHIKCurrentCharacter']
        #mel.eval("deleteControlRig(\""+ HIKCharName +"\")")

        cmds.parent('Root',world=True)
        cmds.parent('c_meshes_00_grp',world=True)
        cmds.rename('c_meshes_00_grp','Model_Mesh')


        cmds.select ("|Root")
        cmds.select ("|Model_Mesh", add = True)
        cmds.FBXExport('-file', filePath +".fbx", "-s")
        # cmds.spaceLocator(name = "ExportRoot")
  

        #sys.stdout.write("|OUTPUTFILE|"+"ASAS")

        sys.stdout.write("|OUTPUTFILE|"+filePath +".fbx\n")
    except Exception, e:
        print(str(e))
        sys.stderr.write(str(e))
        std.uninitialize()
        os._exit(-1)

def getRigType():
    # attributes = cmds.listAttr("|Root",  visible=True, keyable=True, scalar=True , write=True)
    # isHumanIK = False

    # for attr in attributes:
    #     if str(attr) == "lockInfluenceWeights":
    #         isHumanIK = True

    # if isHumanIK:
    #     return "HUMAN_IK"
    # else:
    #     return "ADVANCE_SKELETON"
    return "ASSEMBLY3D"

def exportMetaData(filePath):
    # try:
#       data = {}
#       materialsArray = []
#
#       childs =  cmds.listRelatives("Model_mesh")
#
#       for child in childs:
#           childData = {}
#           materialValue = cmds.getAttr(child+".materialName", asString = True)
#           childData['meshName'] = child
#           childData['materialName'] = materialValue
#           materialsArray.append(childData)
#           
#       data['materials'] = materialsArray
        json_data = parseAllData()

        with open(filePath+".jsonMeta", "w+") as text_file:
            text_file.write(json_data)

        sys.stdout.write("|OUTPUTFILE|"+filePath+".jsonMeta")

    # except Exception, e:
    #     sys.stderr.write(str(e))
    #     std.uninitialize()
    #     os._exit(-1)
        

def parseAllData():    
    #RawData
    rawMaterials = cmds.ls(type='lambert')
    
    #structs for connections
    meshShaders = {}
    shaderToId = {}
    meshes = []
    matProps = {}
    
    #structs for JSON
    data = {}
    materials = []
    avatars = []
    
    hasProperties = False

    if os.path.exists(output+'.jsonMats'):
        with open(output+'.jsonMats') as data_file:
            hasProperties = True    
            matProps = json.load(data_file)
    
    
    
    for x in range(0,len(rawMaterials)):
        mat = rawMaterials[x]
        sys.stderr.write("\n AAAAAAAAAAAAA " + str(mat))  
        if "lambert" in mat :
            continue
        if "Default_Material" in mat :
            continue
        
        
        
        materialData = {}
        materialData["id"] = x
        materialData["name"] = str(mat)
        sys.stderr.write("\n BBBBB " + str(mat))
        #READ PROPERTIES FROM EXTRA FILE!
        if hasProperties :
            if str(mat) not in matProps:
                materialData["properties"] = []
                materialData["shaderName"] = "Standard"
            else:
                materialData["properties"] = matProps[str(mat)]["properties"]
                materialData["shaderName"] = matProps[str(mat)]["shaderName"]

        else:
            materialData["properties"] = []
            materialData["shaderName"] = "Standard"

        

        sys.stderr.write("\n CCCCCC " + str(mat))

        materials.append(materialData)
        
        shaderToId[mat] = x
        
        sys.stderr.write("\n DDDDD " + str(mat))
        con = cmds.listConnections('%s.outColor' % mat)
        meshes_temp = cmds.listConnections(con,destination=False,type="mesh")

        if not meshes_temp: # Unused material
            continue
        sys.stderr.write("\n EEEEEE " + str(mat))
        meshes = meshes + list(set(meshes_temp) - set(meshes))
    
        shapes = cmds.listConnections(con, shapes=True,destination=False,type="mesh")
        
        if shapes:
            for i in range(0,len(shapes)):
                datas = cmds.listConnections(shapes[i], source=False, type="shadingEngine")
                datas = list(set(datas))
                shaders = cmds.ls(cmds.listConnections(datas),materials=1) 
                meshShaders[meshes_temp[i]] = shaders
        sys.stderr.write("\n FFFFFFF " + str(mat))
    
    #WE ONLY HAVE ONE AVATAR PER FBX FOR NOW
    avatarData = {}
    avatarData["id"] = 1
    avatarData["name"] = os.path.splitext(filename)[0]
    avatarData["meshes"] = []
    
    if meshes:
        for i in range(0,len(meshes)):
            meshData = {}
            meshData["id"] = i
            meshData["meshName"] = str(meshes[i])
            meshMaterials = []
            for meshShader in meshShaders[meshes[i]]:
                if meshShader not in shaderToId:
                    sys.stderr.write(str(meshes[i]) +" IS USING AN INVALID MATERIAL LABELED AS " + str(meshShader))
                    std.uninitialize()
                    os._exit(-1)
                meshMaterialIds = {}
                meshMaterialIds["materialId"] = shaderToId[meshShader]
                meshMaterials.append(meshMaterialIds)
            meshData["materialIds"] = meshMaterials
            avatarData["meshes"].append(meshData)   
            
    data["materials"] = materials         
    data["objects"] = [avatarData]
    data["type"] = "Character"
    data["rigType"] = getRigType()

    versions = {}
    versions["Maya_EzMaterials"] = jsonStructures.getDataOrDefault(matProps,"version",0)
    versions["Maya_CharToFbx"] = version

    data ["versions"] = versions

    json_data = json.dumps(data)
    return json_data




filename = "C:\\Proyectos\\Artmasters\\Characters\\test\\MidMaleProxy.ma" #sys.argv[1]
cmds.file(filename,o=1,f=1)
output = filename.replace(".mb","").replace(".ma","")
print(output)

# Source cleanUpScene.mel
# to make scOpt_performOneCleanup available
optimizeScene()


exportFBX(output)
exportMetaData(output)




# std.uninitialize()
# os._exit(0);

# scOpt_performOneCleanup( { "unknownNodesOption" } );
# scOpt_performOneCleanup( { "shadingNetworksOption" } );
# scOpt_performOneCleanup( { "renderLayerOption" } );
# scOpt_performOneCleanup( { "displayLayerOption" } );