bl_info = {
    "name": "EzGroup",
    "description": "Create group by name",
    "author": "Eliseo Viola (Fasox)",
    "version": (1, 1),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

objectMaterials = {}

import bpy
import mathutils 
from bpy.props import *
 
theString = "Name"

 
class EzGroupDialog(bpy.types.Operator) :
    bl_idname = "object.group_popup"        # unique identifier for buttons and menu items to reference.
    bl_label = "Ez Group"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    

    bl_idname = "object.group_pop_up"
    bl_label = "Ez Group"
 
    groupName = StringProperty(name="Group Name :")

    def execute(self, context):
        scn = bpy.context.scene
        bpy.ops.object.mode_set(mode="OBJECT")
        allobjects = bpy.context.selected_objects
        bpy.ops.object.select_all(action='DESELECT')

        if(self.groupName not in bpy.data.objects):
            bpy.ops.object.empty_add(type="SPHERE")
            group = bpy.context.selected_objects[0];
            group.name = self.groupName
            group.location = (0.0,0.0,0.0)
            group.show_name = True
            group.empty_draw_size = 0.15
            group["childs"] = 0
        else:
            group = bpy.data.objects[self.groupName]

        childs = group["childs"]

        for obj in allobjects:
            if not obj.parent or obj.parent.name != group.name:
                oldParent = None
                if obj.parent:
                    oldParent = obj.parent

                obj.parent = group
                obj.matrix_parent_inverse = mathutils.Matrix.Identity(4)
                obj.name = self.groupName+"_"+str(childs)
                if obj.data:
                    obj.data.name = self.groupName+"_"+str(childs)

                if oldParent:
                    oldparentchilds =  [ob_child for ob_child in bpy.data.objects if ob_child.parent == oldParent]
                    if len(oldparentchilds) == 0:
                        oldParent.select = True
                        bpy.ops.object.delete() 
                childs+= 1

        group["childs"] = childs
        
        self.report({'INFO'}, "Grouped to " + self.groupName)
        return {'FINISHED'}
 
    def invoke(self, context, event):
        if len(bpy.context.selected_objects) > 0:
            global theString
            self.groupName = theString
            #return self.execute(context)
            return context.window_manager.invoke_props_dialog(self)
        else:
            return {'FINISHED'}


def register():
    bpy.utils.register_class(EzGroupDialog)


def unregister():
    bpy.utils.unregister_class(EzGroupDialog)


if __name__ == '__main__':
    register()
 # bpy.ops.object.group_pop_up('INVOKE_DEFAULT')