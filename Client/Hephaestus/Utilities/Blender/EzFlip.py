bl_info = {
    "name": "EzFlip",
    "description": "Apply scales to all objects and fixes the normals to the ones with negative values.",
    "author": "Eliseo Viola (Fasox)",
    "version": (1, 1),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

objectMaterials = {}

import bpy


class ApplyAndFlipNormals(bpy.types.Operator) :
    """Materials duplicator remover"""
    bl_idname = "object.ez_flip"        # unique identifier for buttons and menu items to reference.
    bl_label = "Ez Flip"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    

    def execute(self, context):


        scn = bpy.context.scene
        bpy.ops.object.mode_set(mode="OBJECT")
        allobjects = bpy.context.selected_objects
        meshes = [o for o in allobjects if o.type == 'MESH']

        bpy.ops.object.select_all(action='DESELECT')

        for obj in meshes:    
            
            needFlip = False
            needApply = False
            for scale in obj.scale:
                if scale < 0:
                    needFlip = not needFlip
                    needApply = True
            

            

            if needApply:
                
                obj.select  = True
                bpy.ops.object.transform_apply(scale=True)

                print(obj.name +" -> " + str(needFlip))
            
                if needFlip:
                    scn.objects.active = obj
                    bpy.ops.object.mode_set(mode="EDIT")
                    bpy.ops.mesh.select_all(action="SELECT")          
                    bpy.ops.mesh.flip_normals()
                    bpy.ops.object.mode_set()

                
                obj.select  = False

        return {'FINISHED'}


def register():
    bpy.utils.register_class(ApplyAndFlipNormals)


def unregister():
    bpy.utils.unregister_class(ApplyAndFlipNormals)


if __name__ == '__main__':
    register()