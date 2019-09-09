import json
import urllib2 as url
import maya.cmds as cmds

shaders = json.loads(url.urlopen("http://sv-server:13370/tools/data/shaders").read().decode("utf-8") )

enums = ""
for shader in shaders :
    enums = enums+shader+":"

enums = enums[:-1]
childs =  cmds.listRelatives("Model_mesh")

for child in childs:
    cmds.select (child)
    if not cmds.objExists(child+".MaterialName"):
        cmds.addAttr(longName = "MaterialName",shortName = "MN", attributeType= "enum", enumName=enums, hidden= False)
    
    