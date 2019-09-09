# import importlib.util
# specEzMatLab = importlib.util.spec_from_file_location("EzMatLab", "C:\\Projects\\Pantheon\\Client\\Hephaestus\\Data\\EZMatLab.py")
# moduleEZMat = importlib.util.module_from_spec(specEzMatLab)
# specEzMatLab.loader.exec_module(moduleEZMat)
# moduleEZMat.MyClass()


bl_info = {
    "name": "Hephaestus",
    "author": "Eliseo Viola",
    "version": (1, 0),
    "blender": (2, 79, 0),
    "location": "View3D > Tool Shelf > Hephaestus",
    "description": "Enable the Hephaestus toolset",
    "warning": "",
    "wiki_url": "",
    "category": "Piepeline",
    }

import bpy


def runTool(filename):
    # print(globals())
    exec(compile(open(filename).read(), filename, 'exec'), globals(), locals() )

class HephaestusMatLab(bpy.types.Operator):
    bl_idname = "myops.open_matlab"
    bl_label = "Open MatLab"


    def execute(self, context):
        runTool("C:\\Projects\\Pantheon\\Client\\Hephaestus\\Data\\EZMatLab.py")
        return {'FINISHED'}

class HephaestusEzData(bpy.types.Operator):
    bl_idname = "myops.open_ezdata"
    bl_label = "Open EzData"


    def execute(self, context):
        runTool("C:\\Projects\\Pantheon\\Client\\Hephaestus\\Data\\EZDEditor.py")
        return {'FINISHED'}

class HephaestusPanel(bpy.types.Panel):
    bl_label = "Hephaestus Panel"
    bl_idname = "OBJECT_PT_hephaestus"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'TOOLS'
    bl_category = "Hephaestus"

    def draw(self, context):
        layout = self.layout

        column = layout.column()
        column.operator("myops.open_matlab")
        column.operator("myops.open_ezdata")

def register():
    bpy.utils.register_class(HephaestusMatLab)
    bpy.utils.register_class(HephaestusEzData)
    bpy.utils.register_class(HephaestusPanel)

def unregister():
    bpy.utils.unregister_class(HephaestusMatLab)
    bpy.utils.unregister_class(HephaestusEzData)
    bpy.utils.unregister_class(HephaestusPanel)

if __name__ == "__main__":
    register()