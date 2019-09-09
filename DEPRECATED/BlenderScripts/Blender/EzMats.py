import bpy
import mathutils
import sys
import os
import json
from urllib.request import urlopen
import ntpath
import copy
import shutil
from bpy.props import *
from bpy.types import Menu, Panel

bl_info = {
    "name": "EzMats",
    "description": "Create group by name",
    "author": "Eliseo Viola (Fasox)",
    "version": (1, 1),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

materialData = {}
shadersData = {}
# textureFolder = "Textures"
version = 1


def updateShaderMaterial(self,context):
    global materialData
    global shadersData

    for mat in materialData:
        if mat["name"] == self.name:
            enumProp = getattr(bpy.data.materials[mat["name"]],"m"+mat["name"]+"shaders",None)
            print(enumProp)
            mat["shaderName"] = enumProp
            for shader in shadersData:
                if shader["shaderName"] == mat["shaderName"]:
                    newProp = copy.deepcopy(shader["properties"])
                    break
            mat["properties"] = newProp

# def updateShaderProperty(self,value):
#     global materialData
#     global shadersData
#     #props[j]["propertyValue"]
#     for mat in materialData:
#         if mat["name"] == self.name:
#             #enumProp = getattr(bpy.data.materials[mat["name"]],"m"+mat["name"]+"shaders",None)
#             props = mat["properties"]
#             for prop in props:
#                 if prop["propertyName"] == mat["shaderName"]:
#                     newProp = copy.deepcopy(shader["properties"])
#                     break
#             mat["properties"] = newProp


class EzMatsPopUp(bpy.types.Operator) :
    bl_idname = "object.mats_popup"        # unique identifier for buttons and menu items to reference.
    bl_label = "Ez Mats"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    

    bl_idname = "object.mats_popup"
    bl_label = "Ez Mats"
    

    output = ""
    
    jsonMats = ""
    # texturePaths = ""
    
    # shaderNames=[]
    

    def  saveData(self):
        print("SAVE!")
        global materialData
        data = {}
        data["version"] = version
        for mat in materialData:
            newShaderData = {}
            newShaderData["shaderName"] = mat["shaderName"]
            properties = []
            serverShaders = self.loadUnityMaterialsData()
            print("shader -> " + mat["shaderName"])
            for serverShader in serverShaders:
                if serverShader["shaderName"] == mat["shaderName"]:
                    for prop in serverShader["properties"]:
                        attr = getattr(bpy.data.materials[mat["name"]],"m"+mat["name"]+prop["propertyName"],None)
                        #print(attr)

                        if attr and not attr == "None":
                            propty = {}
                            propty["propName"] = prop["propertyName"]
                            propty["propType"] = prop["propertyType"]
                            textureName = attr[attr.replace("\\","/").rfind("/")+1:]

                            # if not os.path.exists(self.texturePaths+textureName):  #UPDATE TO NEW SYSTEM , AND COPY TO THE TEXTURE POOL
                            #     print("Copying -> " +self.texturePaths+textureName)
                            #     if not os.path.exists(self.texturePaths):
                            #         os.makedirs(self.texturePaths)
                            #     if os.path.exists(attr):
                            #         shutil.copy(attr, self.texturePaths+textureName)
                            #     else:
                            #         print("Texture doesnt exist!")
                            # else:
                            #     print(self.texturePaths+textureName + " already exist")
                                
                            # for texSlot in bpy.data.materials[mat["name"]].texture_slots:
                            #     if texSlot:
                            #         if bpy.data.textures[texSlot.name].image:
                            #             if attr in bpy.data.textures[texSlot.name].image.filepath:                
                            #                 bpy.data.textures[texSlot.name].image.filepath = "//"+textureFolder+"\\"+textureName
                            propty["propValue"] = textureName
                            properties.append(propty)

            newShaderData["properties"] = properties
            data[mat["name"]] = newShaderData

        json_data = json.dumps(data)
        print(self.jsonMats)    
        with open(self.jsonMats, "w+") as text_file:
            text_file.write(json_data)


    def loadUnityMaterialsData(self):
        
        shadersData = json.loads(urlopen("http://sv-server:13370/tools/data/shaders").read().decode("utf-8") )["shaders"]
        return shadersData

    def lookMaterialsProperties(self,shaderData,shadername):
        for shader in shaderData:
            if shader["shaderName"] == shadername:
                return copy.deepcopy(shader["properties"])

    def loadModelMaterials(self):
        global shadersData
        shadersData =  self.loadUnityMaterialsData()
        #RawData
        rawMaterials = bpy.data.materials;

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
        #print(self.jsonMats)
        if os.path.exists(self.jsonMats):
            with open(self.jsonMats) as data_file:
                hasProperties = True    
                matProps = json.load(data_file)



        for x in range(0,len(rawMaterials)):
            mat = rawMaterials[x]       
            
             
            
            matDatas = {}
            if hasProperties :
                if str(mat.name) not in matProps:
                    matDatas["name"] = str(mat.name)
                    matDatas["shaderName"] = "Standard"     
                    matDatas["properties"] = self.lookMaterialsProperties(shadersData,matDatas["shaderName"])
                else:           
                    matDatas["name"] = str(mat.name)
                    matDatas["shaderName"] = matProps[str(mat.name)]["shaderName"]
                    matDatas["properties"] = self.lookMaterialsProperties(shadersData,matDatas["shaderName"])
                    for prop in matProps[str(mat.name)]["properties"]:
                        for newProp in matDatas["properties"]:
                            if newProp["propertyName"] == prop["propName"]:
                                newProp["propertyValue"] = prop["propValue"]

            else:
                matDatas["name"] = str(mat.name)
                matDatas["shaderName"] = "Standard"     
                matDatas["properties"] = self.lookMaterialsProperties(shadersData,matDatas["shaderName"])



            
            for j in range(0,len(shadersData)):
                shader = shadersData[j]
                props = shader["properties"]
                for j in range(0,len(props)):
                    textureItems = []
                    textureItems.append(("None","None","None"))
                    for ts in mat.texture_slots: 
                            if ts is not None and ts.texture is not None and  hasattr(ts.texture,"image") and ts.texture.image is not None:
                                textureItems.append( (ts.texture.image.filepath,ts.texture.image.filepath,ts.texture.image.filepath))

                    if(getattr(bpy.types.Material,"m"+mat.name+props[j]["propertyName"],None)):
                        delattr(bpy.types.Material,"m"+mat.name+props[j]["propertyName"])
                    
                    setattr(bpy.types.Material,"m"+mat.name+props[j]["propertyName"],EnumProperty(items = textureItems,name="m"+mat.name+props[j]["propertyName"],description="Textures"))

                    if(getattr(bpy.types.Material,"m"+mat.name+"shaders",None)):
                        delattr(bpy.types.Material,"m"+mat.name+"shaders")

                    shaderItems = []
                    for x in range(0,len(shadersData)):
                        shaderItems.append((shadersData[x]["shaderName"],shadersData[x]["shaderName"],shadersData[x]["shaderName"]))
                    setattr(bpy.types.Material,mat.name+"active",BoolProperty(name = mat.name, description = "Show properties"))
                    setattr(bpy.types.Material,"m"+mat.name+"shaders",EnumProperty(items = shaderItems ,name="m"+mat.name+"shaders",description="ShaderList",update=updateShaderMaterial))
            
            
            shaderToId[mat] = x
            
            materials.append(matDatas)
        
        return materials


    def updateShaderProperties(self,context):
        bpy.types.Scene.aa = self.name
        bpy.types.Scene.bb = context

    def check(self, context):
        return True

    def draw(self, context):
        layout = self.layout
        global materialData
        

        layout.label("")
        row = layout.row(align=True)
        row.alignment = 'EXPAND' 
        row.label(text="Material Name")
        row.label(text="Unity Shader")
        row.label(text="Properties")
 
        for i in range (0,len(materialData)):
            row = layout.row(align=False)
            material = materialData[i]
            row.prop(bpy.data.materials[material["name"]], material["name"]+"active", icon='QUESTION', toggle=True)
            row.prop(bpy.data.materials[material["name"]],"m"+material["name"]+"shaders")

            if(getattr(bpy.data.materials[material["name"]],material["name"]+"active",None)):
                #print(getattr(bpy.data.materials[material["name"]],material["name"]+"active",None))
                column = row.box()
                props = material["properties"]
                for j in range(0,len(props)):

                    propRow = column.row(align=False)
                    propRow.label( text=props[j]["propertyName"] + " : ")
                    propRow.label( text=props[j]["propertyValue"])
                    propRow.prop(bpy.data.materials[material["name"]],"m"+material["name"]+props[j]["propertyName"] , '')

    def execute(self, context):
        self.report({'INFO'}, "FINISH")
        self.saveData()
        return {'FINISHED'}
 
    def invoke(self, context, event):
        global materialData

        self.output = bpy.data.filepath.replace(".blend","")
        if self.output:
            self.jsonMats = self.output+'.jsonMats'
            #self.texturePaths = os.path.dirname(self.output) + "/"+textureFolder+"/"
        else:
            self.jsonMats = os.path.expanduser('~/Documents/')+'test.jsonMats'
            # self.texturePaths = os.path.expanduser('~/Documents') + "/"+textureFolder+"/"

        materialData = self.loadModelMaterials()


        return context.window_manager.invoke_props_dialog(self,width=800, height=20) #Height is overrided by the layout properties


def menu_func_landscape(self, context):
    self.layout.operator(EzMatsPopUp.bl_idname, text="Landscape", icon="RNDCURVE")


def register():    
    bpy.utils.register_module(__name__)
    bpy.types.INFO_MT_mesh_add.append(menu_func_landscape)



def unregister():
    bpy.utils.unregister_module(__name__)
    bpy.types.INFO_MT_mesh_add.remove(menu_func_landscape)


if __name__ == '__main__':
    register()

