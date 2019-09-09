import maya.mel as mel
import maya.cmds as cmds
import os
import json
import sys
sys.path.append('C:/Proyectos/BuildSystem')
from AteneaModules.parser import jsonStructures

import maya.standalone as std
# std.initialize(name='python')

import maya.cmds as cmds
# cmds.loadPlugin("fbxmaya")



def selectBaseLayer():
    cmds.animLayer(baseAnimation,edit=True,lock = False, mute=False, selected=True)
    cmds.animLayer(bckpLayer,edit=True, lock = True, mute=True, selected=False)
    
def selectBckupLayer():
    cmds.animLayer(bckpLayer,edit=True,lock = False, mute=False, selected=True)
    cmds.animLayer(baseAnimation,edit=True,lock = True, mute=True,  selected=False)

def setupLayers():
    try:
        cmds.select("|Root", hi = True)
        selection = cmds.ls(selection=True)
        for r in selection:
            if cmds.objExists(r):
                print("Exist : " + r)
            if not cmds.objExists(r):
                print("NOT exist : "+ r)


        cmds.animLayer("ProxyLayer",addSelectedObjects=True)
        cmds.setAttr('ProxyLayer.rotationAccumulationMode',0)
        cmds.setAttr('ProxyLayer.scaleAccumulationMode',1)
        cmds.animLayer(bckpLayer,copy=baseAnimation)
        cmds.delete( "ProxyLayer")
        selectBaseLayer()
        print("cut")
        cmds.cutKey(selection, time = (startTime+1,endTime))
    except Exception, e:
        sys.stderr.write(str(e))
        std.uninitialize()
        os._exit(-1)
    

def copyAnimationToExportLayer(animData):
    cmds.select("|Root", hi = True)
    selection = cmds.ls(selection=True)
    try:
        cmds.playbackOptions( min=startTime,ast=startTime ,max=endTime, aet=endTime)
        selectBckupLayer()
        cmds.cutKey(selection, time = (anim["clipStart"],anim["clipEnd"]))
        
        selectBaseLayer()
        cmds.pasteKey(selection , time = (0,0))
        cmds.playbackOptions( min=0,ast=0 ,max=anim["clipLen"], aet=anim["clipLen"])
    except Exception, e:
        sys.stderr.write(str(e))
        std.uninitialize()
        os._exit(-1)
    
    

def exportAnim(anim):
    
    copyAnimationToExportLayer(anim) 

    try:
        cmds.selectKey( '|Root', time=(0,0), attribute='translateX' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '|Root', time=(0,0),  attribute='translateY' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '|Root', time=(0,0),  attribute='translateZ' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '|Root', time=(0,0), attribute='rotateX' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '|Root', time=(0,0),  attribute='rotateY' )
        cmds.keyTangent( inTangentType='linear')
        cmds.selectKey( '|Root', time=(0,0), attribute='rotateZ' )
        cmds.keyTangent( inTangentType='linear')
        
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='translateX' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='translateY' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='translateZ' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='rotateX' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='rotateY' )
        cmds.keyTangent( outTangentType='linear')
        cmds.selectKey( '|Root', time=(anim["clipLen"],anim["clipLen"]), attribute='rotateZ' )
        cmds.keyTangent( outTangentType='linear')
            
        output = mel.eval("file -q -sceneName").replace(".mb","").replace(".ma","")
        
        
        
        outPutpath = output+".fbx"

        cmds.select("|Root" ,hi = True)
            
        mel.eval('FBXResetExport') # This ensures the user's settings are ignored so that you can just set values which differ from the default
        #mel.eval('FBXExportAnimationOnly -v 1')  # DONT!
        mel.eval('FBXExportBakeComplexAnimation -v 1')
        mel.eval('FBXExportBakeComplexStart -v 0')
        mel.eval('FBXExportSkeletonDefinitions  -v 1')
        mel.eval('FBXExportBakeComplexEnd -v '+ str(anim["clipLen"]))
        mel.eval('FBXExport -f "%s" -s' % outPutpath)

        sys.stdout.write("|OUTPUTFILE|"+outPutpath+"\n")

    except Exception, e:
        sys.stderr.write(str(e))
        std.uninitialize()
        os._exit(-1)

def cleanModel():
    try:
        cmds.select("|Root" ,hi = True)
        selection = cmds.ls( selection=True )
        
           
        cmds.bakeResults(selection , simulation = True , time = (startTime,endTime))

        selection = [x for x in cmds.ls( selection=True ) if x not in cmds.ls(type="constraint")] #we excludes all the constraints

        print(selection)
        
        selection.append("frontShape")
        selection.append("front")
        selection.append("perspShape")
        selection.append("persp")
        selection.append("sideShape")
        selection.append("side")
        selection.append("topShape")
        selection.append("top")
        selection.append("frontShape")
        selection.append("perspShape")
        selection.append("sideShape")
        selection.append("topShape")
        selection.append("lambert1")
        selection.append("particleCloud1")

    
# Error: Non-deletable node 'frontShape' cannot be deleted. # 
# Error: Non-deletable node 'front' cannot be deleted. # 
# Error: Non-deletable node 'perspShape' cannot be deleted. # 
# Error: Non-deletable node 'persp' cannot be deleted. # 
# Error: Non-deletable node 'sideShape' cannot be deleted. # 
# Error: Non-deletable node 'side' cannot be deleted. # 
# Error: Non-deletable node 'topShape' cannot be deleted. # 
# Error: Non-deletable node 'top' cannot be deleted. # 
# Error: Non-deletable node 'frontShape' cannot be deleted. # 
# Error: Non-deletable node 'perspShape' cannot be deleted. # 
# Error: Non-deletable node 'sideShape' cannot be deleted. # 
# Error: Non-deletable node 'topShape' cannot be deleted. # 
# Error: Non-deletable node 'lambert1' cannot be deleted. # 
# Error: Non-deletable node 'particleCloud1' cannot be deleted. # 
# Error: RuntimeError: file <maya console> line 46: Nothing to paste 
    
        garbage = [gb for gb in cmds.ls( selection=False, transforms=True,shapes=True,geometry=True,materials=True) if gb not in selection]
        for g in garbage:
            if cmds.objExists(g):
                cmds.delete(g)


        

    except Exception, e:
        sys.stderr.write(str(e))
        std.uninitialize()
        os._exit(-1)
    

    


# filename = sys.argv[1]
cmds.file("C:\\Proyectos\\Artmasters\\Animations\\NewRig@ComboDistance\\ComboDistanceTest_006.ma",o=1,f=1)

bckpLayer = "BackUpAnimationLayer"

refs = cmds.ls(type='reference')
for i in refs:
    if not cmds.listConnections(i):
        cmds.lockNode( i, lock=False )
        cmds.delete(i)
    else:     
        rFile = cmds.referenceQuery(i, f=True)
        cmds.file(rFile, importReference=True)

namespaces =  set([str(n.split(":")[0]) for n in cmds.ls( type='joint' ) if len(n.split(":")) > 1])
for ns in namespaces:
        cmds.namespace( removeNamespace = ":"+ns, mergeNamespaceWithRoot = True)

sknJnt = cmds.ls(typ="joint")
for skn in sknJnt:
    cmds.setAttr (skn+'.tx', l=False, k=True)
    cmds.setAttr (skn+'.ty', l=False, k=True)
    cmds.setAttr (skn+'.tz', l=False, k=True)
    cmds.setAttr (skn+'.rx', l=False, k=True)
    cmds.setAttr (skn+'.ry', l=False, k=True)
    cmds.setAttr (skn+'.rz', l=False, k=True)
    cmds.setAttr (skn+'.sx', l=False, k=True)
    cmds.setAttr (skn+'.sy', l=False, k=True)
    cmds.setAttr (skn+'.sz', l=False, k=True)

sknJnt = cmds.ls(typ="scaleConstraint")
for skn in sknJnt:
    cmds.setAttr (skn+'.tx', l=False, k=True)
    cmds.setAttr (skn+'.ty', l=False, k=True)
    cmds.setAttr (skn+'.tz', l=False, k=True)
    cmds.setAttr (skn+'.rx', l=False, k=True)
    cmds.setAttr (skn+'.ry', l=False, k=True)
    cmds.setAttr (skn+'.rz', l=False, k=True)
    cmds.setAttr (skn+'.sx', l=False, k=True)
    cmds.setAttr (skn+'.sy', l=False, k=True)
    cmds.setAttr (skn+'.sz', l=False, k=True)

sknJnt = cmds.ls(typ="parentConstraint")
for skn in sknJnt:
    cmds.setAttr (skn+'.tx', l=False, k=True)
    cmds.setAttr (skn+'.ty', l=False, k=True)
    cmds.setAttr (skn+'.tz', l=False, k=True)
    cmds.setAttr (skn+'.rx', l=False, k=True)
    cmds.setAttr (skn+'.ry', l=False, k=True)
    cmds.setAttr (skn+'.rz', l=False, k=True)
    cmds.setAttr (skn+'.sx', l=False, k=True)
    cmds.setAttr (skn+'.sy', l=False, k=True)
    cmds.setAttr (skn+'.sz', l=False, k=True)

sknJnt = cmds.ls(typ="pointConstraint")
for skn in sknJnt:
    cmds.setAttr (skn+'.tx', l=False, k=True)
    cmds.setAttr (skn+'.ty', l=False, k=True)
    cmds.setAttr (skn+'.tz', l=False, k=True)
    cmds.setAttr (skn+'.rx', l=False, k=True)
    cmds.setAttr (skn+'.ry', l=False, k=True)
    cmds.setAttr (skn+'.rz', l=False, k=True)
    cmds.setAttr (skn+'.sx', l=False, k=True)
    cmds.setAttr (skn+'.sy', l=False, k=True)
    cmds.setAttr (skn+'.sz', l=False, k=True)





cmds.parent('Root',world=True)


jsonPath = mel.eval("file -q -sceneName").replace(".mb",".metadata").replace(".ma",".metadata")
animMetaData = mel.eval("file -q -sceneName").replace(".mb","jsonAnim").replace(".ma",".jsonAnim")
anims = []
events = []

animData = ""
version = 1

print(animMetaData)
if os.path.exists(animMetaData):

    with open(animMetaData) as data_file:
        animData = json.load(data_file)
        try: anims = animData['animations']
        except KeyError: anims = []
        try: events = animData['events']    
        except KeyError: events = []
        
        

startTime = int(cmds.playbackOptions(query = True, minTime=True))
endTime = int(cmds.playbackOptions(query = True, maxTime=True))



cleanModel()
setupLayers()

data = {}
data["type"] = "Animation"
#data ["rootMotion"] = jsonStructures.getDataOrDefault(animData,"rootMotion","true")
animationDatas = []

animID = 0
for anim in anims:
    animID = animID + 1 
    anim["clipLen"] = anim["clipEnd"] - anim["clipStart"]
    animationData = {}
    animationData["id"] = animID
    animationData["animName"] = anim["clipName"]
    animationData["animStart"] = 0
    animationData["animEnd"] = anim["clipLen"]
    animationData["animLoop"] = jsonStructures.getDataOrDefault(anim,"clipLoop","false")  
    animationData["animRoot"] = jsonStructures.getDataOrDefault(anim,"clipRoot","true")    
    animationDatas.append(animationData)

    exportAnim(anim)

eventsDatas = []

eventID = 0

for event in events:
    eventID = eventID + 1 
    eventData = {}
    eventData["id"] = eventID
    eventData["eventName"] = event["clipKeyEvent"]
    eventData["eventKey"] = event["clipKeyFrame"]
    eventsDatas.append(eventData)

data ["animations"] = animationDatas
data ["events"] = eventsDatas

versions = {}
# versions["Maya_EzAnims"] = jsonStructures.getDataOrDefault(animData,"version",0)
versions["Maya_AnimToFbx"] = version

data ["versions"] = versions

json_data = json.dumps(data)
with open(jsonPath, "w+") as text_file:
    text_file.write(json_data)
sys.stdout.write("|OUTPUTFILE|"+jsonPath+"\n")
