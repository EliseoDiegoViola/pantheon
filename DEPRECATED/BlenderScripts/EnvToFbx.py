import bpy
import sys
import os
import json
from urllib.request import urlopen

sys.path.append('C:/Proyectos/BuildSystem')
from AteneaModules.parser import jsonStructures

bpy.ops.object.mode_set()
exportLayers = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)
setDressing = 18
garbageLayer = 19
output = bpy.path.abspath("//")+os.path.basename(bpy.data.filepath).replace(".blend","")
filename = os.path.basename(bpy.data.filepath).replace(".blend","")
version = 1;

def selectLayers(*args):
    for i in args:
        bpy.context.scene.layers[i] = True
    for i in range(len(bpy.context.scene.layers)):
        if i not in args:
            bpy.context.scene.layers[i] = False
    return (i in args for i in range(0, 20))

def getObjectsInLayers(*args):
    return [ob for ob in bpy.context.scene.objects if any(list(map(lambda x: x in list(args), [i for i in range(len(ob.layers)) if ob.layers[i]])))]

def selectObject(ob):
    ob.select=True

def selectObjectsInLayers(*args):
    bpy.ops.object.select_all(action='DESELECT')
    objectsInLayer = getObjectsInLayers(*args)
    list(map(lambda ob: selectObject(ob),objectsInLayer))
    return objectsInLayer

def loadUnitynavmeshLayers():
        
    layersData = json.loads(urlopen("http://sv-server-3d:13370/?thing=navmeshLayers").read().decode("utf-8") )["layers"]
    return layersData

def getAndApplyAllMaterials():
    objectMaterials = {}
    scene = bpy.context.scene
    objects = scene.objects
    bpy.ops.object.select_all(action='DESELECT')
    for obj in objects:
        print(obj.name)
        bpy.ops.object.mode_set(mode='OBJECT')
        if obj.type == "MESH" and len(obj.material_slots) > 0:
            obj.select  = True
            bpy.context.scene.objects.active = obj
            editReturn = str(bpy.ops.object.mode_set(mode="EDIT")) 
            print(obj.name + " to edit mode " + editReturn )
            selectReturn = str(bpy.ops.mesh.select_all(action="SELECT"))
            print(obj.name + " select all verts " +  selectReturn )        
            bpy.ops.mesh.sort_elements(type='MATERIAL',reverse=False,elements={'FACE'})
            bpy.ops.object.mode_set(mode='OBJECT')
            obj.select  = False
            for pol in obj.data.polygons:
                if pol.material_index >= len(obj.material_slots):
                    sys.stderr.write(str("ERROR READING MATERIAL POLYGONS FROM! -> ") + str(obj.name) + " : " + str(pol.index))
                    sys.exit(-1)
                mat = obj.material_slots[pol.material_index] 
                if not mat.name in objectMaterials: 
                    objectMaterials[mat.name] = []
                    objectMaterials[mat.name].append(obj)
                else:
                    if not obj in objectMaterials[mat.name]:
                        objectMaterials[mat.name].append(obj)
    return objectMaterials

def getAllChildren(obj, lst = []):
    if len(obj.children) > 0:
        for ob in obj.children:
            lst.append(ob)
            lst + getAllChildren(ob,lst)
    return lst


def parseAllData():    

    #RawData


    #structs for connections
    meshShaders = {}
    shaderToId = {}
    meshes = []
    matProps = {}

    environments = [[ob] + getAllChildren(ob) for ob in bpy.data.objects if not ob.parent]
    
    #structs for JSON
    data = {}
    materials = []
    avatars = []
    
    hasProperties = False

    if os.path.exists(output+'.jsonMats'):
        with open(output+'.jsonMats') as data_file:
            hasProperties = True    
            matProps = json.load(data_file)
    
    
    matId = 0;

   
    for key in rawMaterials:        
        meshes = meshes + rawMaterials[key]
        
        if "Material" is key :
            continue
        if not key :
            continue
                
        materialData = {}
        materialData["id"] = matId
        materialData["name"] = key
        try:    
            if hasProperties :
                materialData["properties"] = matProps[str(key)]["properties"]
                materialData["shaderName"] = matProps[str(key)]["shaderName"]
            else:
                materialData["properties"] = []
                materialData["shaderName"] = "Standard"

        except Exception as e:
            sys.stderr.write(str("ERROR GETTING OLD PROPERTY! -> ") + str(key) + " : " + str(e))
            sys.exit(-1)

        materialObject = bpy.data.materials.get(key)

        colorProperty = {}
        colorProperty["propName"] = "_Color"
        colorProperty["propType"] = "Color"
        colorProperty["propValue"] = str(materialObject.diffuse_color[0]) + "/" + str(materialObject.diffuse_color[1]) + "/" + str(materialObject.diffuse_color[2]) + "/" + str(materialObject.alpha)

        


        materialData["properties"].append(colorProperty)


        materials.append(materialData)
        
        shaderToId[key] = matId

        matId = matId + 1
        
    
    bpy.ops.object.select_by_layer(match='EXACT',extend=False,layers=setDressing+1) # WHY THE FUCK THE LAYERS START FROM 1 HERE!?
    dressings = bpy.context.selected_objects;

    environmentsData = []
    for environmentIndex in range(0,len(environments)):
        environmentData = {}
        environmentData["id"] = environmentIndex
        environmentData["name"] = environments[environmentIndex][0].name
        environmentData["meshes"] = []

        meshes = [ob for ob in environments[environmentIndex] if ob.type == "MESH"] 
        colliders = []
        triggers = []   
        dressingsData =  []

        if meshes:
            for i in range(0,len(meshes)):
                if "col_" in str(meshes[i].name):
                    colliderData = {}
                    colliderData["id"] = i
                    colliderData["meshName"] = str(meshes[i].name)
                    if "COL_TYPE" in meshes[i]:
                        colliderData["colliderType"] = meshes[i]["COL_TYPE"]
                    else:
                        colliderData["colliderType"] = "BOX" 
                    colliders.append(colliderData)
                elif "trigger_" in str(meshes[i].name):
                    triggerData = {}
                    triggerData["id"] = i
                    triggerData["meshName"] = str(meshes[i].name)
                    triggerData["colliderType"] = "BOX"
                    triggers.append(triggerData)
                else:
                    meshData = {}
                    meshData["id"] = i
                    meshData["meshName"] = str(meshes[i].name)
                    meshMaterials = []
                    for matSlot in meshes[i].material_slots:
                        if matSlot.name in shaderToId and meshes[i] in rawMaterials[matSlot.name]:
                            meshMaterialIds = {}
                            meshMaterialIds["materialId"] = shaderToId[matSlot.name]
                            meshMaterials.append(meshMaterialIds)
                    meshData["materialIds"] = meshMaterials
                    if meshes[i] in dressings:
                        dressingsData.append(meshes[i].name)
                    environmentData["meshes"].append(meshData)   

                
                layerProp = {}
                if "BatchingStatic" in meshes[i]:
                    layerProp["BatchingStatic"] = bool(meshes[i]["BatchingStatic"])
                else:
                    layerProp["BatchingStatic"] = False

                if "LightmapStatic" in meshes[i]:
                    layerProp["LightmapStatic"] = bool(meshes[i]["LightmapStatic"])
                else:
                    layerProp["LightmapStatic"] = False

                if "NavigationStatic" in meshes[i]:
                    layerProp["NavigationStatic"] = bool(meshes[i]["NavigationStatic"])
                else:
                    layerProp["NavigationStatic"] = False

                if "OccludeeStatic" in meshes[i]:
                    layerProp["OccludeeStatic"] = bool(meshes[i]["OccludeeStatic"])
                else:
                    layerProp["OccludeeStatic"] = False

                if "OccluderStatic" in meshes[i]:
                    layerProp["OccluderStatic"] = bool(meshes[i]["OccluderStatic"])
                else:
                    layerProp["OccluderStatic"] = False

                if "ReflectionProbeStatic" in meshes[i]:
                    layerProp["ReflectionProbeStatic"] = bool(meshes[i]["ReflectionProbeStatic"])
                else:
                    layerProp["BatchingStatic"] = False

                if "NavmeshLayer" in meshes[i]:
                    layerProp["NavmeshLayer"] = loadUnitynavmeshLayers()[meshes[i]["NavmeshLayer"]]["layerName"]
                else:
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
    versions["Blender_EzMaterials"] = jsonStructures.getDataOrDefault(matProps,"version",0)
    versions["Blender_EnvToFbx"] = version

    data ["versions"] = versions

    json_data = json.dumps(data)
    return json_data


def exportMetaData(filePath):
    try:
        json_data = parseAllData()
    except Exception as e:
        sys.stderr.write(str("ERROR PARSING! -> ") + str(e))
        sys.exit(-1)
    
    try:
        with open(filePath+".jsonMeta", "w+") as text_file:
            text_file.write(json_data)

        sys.stdout.write("|OUTPUTFILE|"+filePath+".jsonMeta\n")
    except Exception as e:
        sys.stderr.write(str("ERROR WRITING! -> ") + str(e))
        sys.exit(-1)
   
        
def exportFBX(filePath):
    try:
        
        
        selectLayers(*exportLayers)
        bpy.ops.export_scene.fbx(bake_space_transform=True ,filepath=(filePath+".fbx"))

        sys.stdout.write("|OUTPUTFILE|"+filePath +".fbx\n")
    except Exception as e:
        sys.stderr.write(str("ERROR EXPORTING! -> ") + str(e))
        sys.exit(-1)



# print(fbxPath)

# selectLayers(garbageLayer)
# selectObjectsInLayers(garbageLayer)
# bpy.ops.object.delete() 
# selectLayers(*exportLayers)
# bpy.ops.export_scene.fbx(filepath=fbxPath)
selectLayers(garbageLayer)
selectObjectsInLayers(garbageLayer)
bpy.ops.object.delete() 

bpy.ops.object.mode_set(mode='OBJECT')
selectLayers(*exportLayers)
rawMaterials = getAndApplyAllMaterials()   

exportFBX(output)
exportMetaData(output)