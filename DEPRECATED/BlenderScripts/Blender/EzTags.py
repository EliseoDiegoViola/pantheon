bl_info = {
    "name": "EzTags",
    "description": "Allow the user to set the unity's static and navmesh flags in blender.",
    "author": "Eliseo Viola (Fasox)",
    "version": (1, 2),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

import bpy, random
import json
from urllib.request import urlopen
from bpy.props import *

version = 1

def loadUnitynavmeshLayers():
    #DEPRECATED    
    layersData = {}#json.loads(urlopen("http://sv-server-3d:13370/?thing=navmeshLayers").read().decode("utf-8") )["layers"]
    return layersData

def initObjectProperties(): 

    layers = loadUnitynavmeshLayers();
    layerItems = []
    for layer in layers:
        layerItems.append( (layer["layerName"],layer["layerName"],layer["layerName"]))
 
    bpy.types.Object.NavmeshLayer = EnumProperty(
        items = layerItems,
        name="NavmeshLayer",
        description="Navmesh Layers")

    bpy.types.Object.BatchingStatic = BoolProperty(
        name = "BatchingStatic", 
        description = "True or False?")

    bpy.types.Object.LightmapStatic = BoolProperty(
        name = "LightmapStatic", 
        description = "True or False?")

    bpy.types.Object.NavigationStatic = BoolProperty(
        name = "NavigationStatic", 
        description = "True or False?")

    bpy.types.Object.OccludeeStatic = BoolProperty(
        name = "OccludeeStatic", 
        description = "True or False?")

    bpy.types.Object.OccluderStatic = BoolProperty(
        name = "OccluderStatic", 
        description = "True or False?")

    bpy.types.Object.ReflectionProbeStatic = BoolProperty(
        name = "ReflectionProbeStatic", 
        description = "True or False?")    


    return 
#
#    Menu in UI region
#
class LayersPanel(bpy.types.Panel):
    bl_label = "Object Flags"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
 
    @classmethod
    def poll(self, context):
        valid = True
        for obj in context.selected_objects:
            valid = (valid and obj.type == 'MESH')
        return valid
 
    


    def draw(self, context):
        layout = self.layout
        column = layout.column()
        row = column.row()
        row.prop(context.object, 'BatchingStatic', icon='QUESTION', toggle=True)
        row.prop(context.object, 'LightmapStatic', icon='QUESTION', toggle=True)
        row.prop(context.object, 'NavigationStatic', icon='QUESTION', toggle=True)
        row = column.row()
        row.prop(context.object, 'OccludeeStatic', icon='QUESTION', toggle=True)
        row.prop(context.object, 'OccluderStatic', icon='QUESTION', toggle=True)
        row.prop(context.object, 'ReflectionProbeStatic', icon='QUESTION', toggle=True)

        if(len(bpy.context.selected_objects) > 1):
            layout.operator("replicate.flags")

        if(all(obj.NavigationStatic for obj in bpy.context.selected_objects)) :
            layout.prop(context.object, 'NavmeshLayer' , icon='EDIT')

 
class ReplicatorButton(bpy.types.Operator):
    bl_idname = "replicate.flags"
    bl_label = "Replicate Flags"
 
    def execute(self, context):
        objectsToReplicate = bpy.context.selected_objects
        selectedObject = bpy.context.scene.objects.active
        for obj in objectsToReplicate:
            obj.BatchingStatic = selectedObject.BatchingStatic
            obj.LightmapStatic = selectedObject.LightmapStatic
            obj.NavigationStatic = selectedObject.NavigationStatic
            obj.OccludeeStatic = selectedObject.OccludeeStatic
            obj.OccluderStatic = selectedObject.OccluderStatic
            obj.ReflectionProbeStatic = selectedObject.ReflectionProbeStatic
        return{'FINISHED'}    
 

# class UpdateServerData(bpy.types.Operator):
#     bl_idname = "update.serverdata"
#     bl_label = "Update Server Data"
 
#     def execute(self, context):
#         initObjectProperties()
#         return{'FINISHED'}    

#    Registration


def register():    
    initObjectProperties()
    bpy.utils.register_module(__name__)



def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()