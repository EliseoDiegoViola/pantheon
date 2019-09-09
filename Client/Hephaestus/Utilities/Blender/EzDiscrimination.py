bl_info = {
    "name": "EzDiscrimination",
    "description": "Allow the user to separate meshes by material.",
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

theString = "Name"

class EzDiscriminationDialog(bpy.types.Operator):
    bl_idname = "object.disc_popup"        # unique identifier for buttons and menu items to reference.
    bl_label = "Ez Discrimination"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    bl_idname = "object.disc_pop_up"

    matName = StringProperty(name="Material Name :")

    @classmethod
    def poll(self, context):
        valid = True
        for obj in context.selected_objects:
            valid = (valid and obj.type == 'MESH')
        return valid


    def execute(self, context):
        objectsToSeparate = bpy.context.selected_objects
        for obj in objectsToSeparate:
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.context.scene.objects.active=obj
            bpy.ops.object.mode_set(mode='EDIT')
            for i in range(len(obj.material_slots)):
                if obj.material_slots[i].name == self.matName:
                    obj.active_material_index = i
                    bpy.ops.mesh.select_all(action="DESELECT")  
                    bpy.ops.object.material_slot_select()
                    selected_verts = [v for v in obj.data.vertices if v.select]
                    if len(selected_verts) > 0:
                        bpy.ops.mesh.separate(type="SELECTED")
                    else:
                        print(obj.name + " Has " + self.matName + " Material but is not using it")
                    break    

        self.report({'INFO'}, "Objects separated by " + self.matName)
        bpy.ops.object.mode_set(mode='OBJECT')
        return{'FINISHED'}  

    def invoke(self, context, event):
        if len(bpy.context.selected_objects) > 0:
            global theString
            self.groupName = theString
            return context.window_manager.invoke_props_dialog(self)
        else:
            return {'FINISHED'}

def register():    
    bpy.utils.register_module(__name__)



def unregister():
    bpy.utils.unregister_module(__name__)


if __name__ == '__main__':
    register()