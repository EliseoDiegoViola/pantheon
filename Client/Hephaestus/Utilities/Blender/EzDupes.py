bl_info = {
    "name": "EzDupes",
    "description": "Remove material ducplicated generated from imports.",
    "author": "Eliseo Viola (Fasox)",
    "version": (1, 1),
    "blender": (2, 74, 0),
    "location": "3D View > Quick Search",
    "category": "Object",
    "support": "COMMUNITY"
}

objectMaterials = {}

import bpy


class MaterialDupesDetector(bpy.types.Operator) :
    """Materials duplicator remover"""
    bl_idname = "object.ez_dupes"        # unique identifier for buttons and menu items to reference.
    bl_label = "Ez Dupes"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    

    def execute(self, context):


        scene = context.scene

        objects = scene.objects
        for obj in objects:
            for mat in obj.material_slots:   
                if not mat.name in objectMaterials:
                    objectMaterials[mat.name] = []
                    objectMaterials[mat.name].append(obj)
                else:
                    objectMaterials[mat.name].append(obj)

        # matsToClean = []
        for key in objectMaterials:
            if ".0" in key:
                #matsToClean.append(key)
                print("Duplicate! " + key)
                originalName = key.replace("."+key.split(".")[len(key.split("."))-1],"")
                print("Original " + originalName)
                if not  originalName in objectMaterials:
                    print ("Base Material doesnt exist")
                    oldMaterial = bpy.data.materials.get(key)
                    oldMaterial.name = originalName
                else:
                    for mesh in objectMaterials[key]:
                        if key in mesh.material_slots:
                            mesh.material_slots[key].material = bpy.data.materials.get(originalName)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MaterialDupesDetector)


def unregister():
    bpy.utils.unregister_class(MaterialDupesDetector)


if __name__ == '__main__':
    register()