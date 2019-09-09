import bpy
import sys
import os
import json
from urllib.request import urlopen
sys.path.append('C:/Proyectos/BuildSystem')
from AteneaModules.parser import jsonStructures

exportLayers = (0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18)
garbageLayer = 19
output = bpy.path.abspath("//")+os.path.basename(bpy.data.filepath).replace(".blend","")
filename = os.path.basename(bpy.data.filepath).replace(".blend","")

version = 1

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



def getAllMaterials():

    objectMaterials = {}
    #py.context.scene.objects["Plane.004"].data.polygons[0].material_index
    scene = bpy.context.scene
    objects = scene.objects
    for obj in objects:
        if obj.type == "MESH" and len(obj.material_slots) > 0:

            
            for pol in obj.data.polygons:
                mat = obj.material_slots[pol.material_index]
                if mat.name:
                    if not mat.name in objectMaterials:
                        objectMaterials[mat.name] = []
                        objectMaterials[mat.name].append(obj)
                    else:
                        if not obj in objectMaterials[mat.name]:
                            objectMaterials[mat.name].append(obj)  
            # for mat in obj.material_slots:   
            #     if not mat.name in objectMaterials:
            #         objectMaterials[mat.name] = []
            #         objectMaterials[mat.name].append(obj)
            #     else:
            #         objectMaterials[mat.name].append(obj)
    return objectMaterials

def parseAllData():    
    #RawData
    rawMaterials = getAllMaterials()
    
    #structs for connections
    meshShaders = {}
    shaderToId = {}
    meshes = [ob for ob in bpy.data.objects if ob.type == "MESH"]
    points = [ob for ob in bpy.data.objects if ob.type == "EMPTY"]
    matProps = {}

    weapons = [[ob] + list(ob.children) for ob in bpy.data.objects if not ob.parent and ob.type == "ARMATURE"]
    
    #structs for JSON
    data = {}
    materials = []
    
    
    hasProperties = False

    if os.path.exists(output+'.jsonMats'):
        with open(output+'.jsonMats') as data_file:
            hasProperties = True    
            matProps = json.load(data_file)
    
    
    matId = 0;
    for key in rawMaterials:        
        #meshes = meshes + rawMaterials[key]
        
        if "Material" in key :
            continue
                
        if not key :
            continue
        materialData = {}
        materialData["id"] = matId
        materialData["name"] = key

        if hasProperties :
            materialData["properties"] = matProps[str(key)]["properties"]
            materialData["shaderName"] = matProps[str(key)]["shaderName"]
        else:
            materialData["properties"] = []
            materialData["shaderName"] = "Standard"


        materialObject = bpy.data.materials.get(key)

        colorProperty = {}
        colorProperty["propName"] = "_Color"
        colorProperty["propType"] = "Color"
        colorProperty["propValue"] = str(materialObject.diffuse_color[0]) + "/" + str(materialObject.diffuse_color[1]) + "/" + str(materialObject.diffuse_color[2]) + "/" + str(materialObject.alpha)
        materialData["properties"].append(colorProperty)

        materials.append(materialData)
        
        shaderToId[key] = matId

        matId = matId + 1
    
    wpnsData = []

    for wpnIndex in range(0,len(weapons)):
        wpnData = {}
        wpnData["id"] = wpnIndex
        wpnData["name"] = weapons[wpnIndex][0].name
        wpnData["meshes"] = []

        meshes = [ob for ob in weapons[wpnIndex] if ob.type == "MESH"] 
        colliders = []
        triggers = []
        holdingPoints = []

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
                    wpnData["meshes"].append(meshData)

        armatures = [ob for ob in weapons[wpnIndex] if ob.type == "ARMATURE"]   
        actions = []
        if len(armatures):
            
            animID = 0
            armature = armatures[0]

            bone_names = set([b.name for b in armature.data.bones])

            for action in bpy.data.actions:
                if set([fc.data_path.split('"')[1] for fc in action.fcurves]).issubset(bone_names):
                    animationData = {}
                    animationData["id"] = animID
                    animationData["animName"] = armature.name + "|" + action.name
                    animationData["animStart"] = action.frame_range.x
                    animationData["animEnd"] = action.frame_range.y
                    actions.append(animationData)
                    animID = animID + 1

        if points:
            for i in range(0,len(points)):
                meshData = {}
                meshData["id"] = i
                meshData["pointName"] = str(points[i].name)
                holdingPoints.append(meshData)  

        wpnData["holdPoints"] = holdingPoints  
        wpnData["actions"] = actions
        wpnData["colliders"] = colliders
        wpnData["triggers"] = triggers
        wpnsData.append(wpnData)
    
    data["materials"] = materials         
    data["objects"] = wpnsData
    data["type"] = "Weapon"

    versions = {}
    versions["Blender_EzMaterials"] = jsonStructures.getDataOrDefault(matProps,"version",0)
    versions["Blender_WpnToFbx"] = version

    data ["versions"] = versions

    if "World" in bpy.data.worlds:
        if "TYPE" in bpy.data.worlds['World']:
            data["sub-type"] = bpy.data.worlds['World']["TYPE"]
        else:
            sys.stderr.write(str("ERROR! -> ") + "TYPE IS NOT SPECIFIED")
    else:
        sys.stderr.write(str("ERROR! -> ") + "WORLD DOES NOT EXIST")
    
    

    json_data = json.dumps(data)
    return json_data

def exportMetaData(filePath):
    try:
        json_data = parseAllData()

        with open(filePath+".jsonMeta", "w+") as text_file:
            text_file.write(json_data)

        sys.stdout.write("|OUTPUTFILE|"+filePath+".jsonMeta\n")

    except Exception as e:
        sys.stderr.write(str("ERROR! -> ") + str(e))
        sys.exit(-1)
        
def exportFBX(filePath):
    try:
        
        selectLayers(garbageLayer)
        selectObjectsInLayers(garbageLayer)
        bpy.ops.object.delete() 
        selectLayers(*exportLayers)

        bpy.ops.export_scene.fbx(bake_space_transform=True , filepath=(filePath+".fbx"))
        sys.stdout.write("|OUTPUTFILE|"+filePath +".fbx\n")

    except Exception as e:
        sys.stderr.write(str("ERROR! -> ") + str(e))
        sys.exit(-1)



# print(fbxPath)
sys.stdout.write(" PATH AS " + bpy.data.filepath)
# selectLayers(garbageLayer)
# selectObjectsInLayers(garbageLayer)
# bpy.ops.object.delete() 
# selectLayers(*exportLayers)
# bpy.ops.export_scene.fbx(filepath=fbxPath)
bpy.ops.object.mode_set(mode='OBJECT')
exportFBX(output)
exportMetaData(output)