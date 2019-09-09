from functools import partial
import functools
import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel
import json
import os
from pantheonModules.pantheonUtilities import modulesLoader



class MAX_EzDataEditor():

    def __init__(self):
        print("MAX!")

class MAYA_EzDataEditor():

    def __init__(self):
        print ("MAYA!")
        self.version = 10
        self.clips = {}
        self.keys = {}
        self.output = mel.eval("file -q -sceneName").replace(".mb","").replace(".ma","")
        self.windowID = 'FBXExportID'

        self.animLayoutSizes = (80,80,80,60,90,20)
        self.eventsLayoutSizes = (80,100,20)

        self.layoutMargin = 50

    
    class ui(object):
        def __init__(self,input):
            self.obj=input()
        def __enter__(self):
            pass
        def __exit__(self, type, value, traceback):
            cmds.setParent("..")

    def defineClips(self, pWindowTitle, pWindowOutput ):
        output = os.path.splitext(pWindowOutput)[0]

    def deleteClipCallback(self, rowName, *pArgs ):
       del clips[rowName]
       cmds.deleteUI(rowName )

    def deleteEventCallback(self,rowName, *pArgs ):
       del keys[rowName]
       cmds.deleteUI(rowName )

    def addClipCallback( *pArgs ):
       cmds.setParent(entriesLayout)

       rowName = cmds.rowLayout(numberOfColumns=6,columnWidth6=animLayoutSizes)
       clipData = {}
       clipData["clipNameText"]= cmds.textField(width=animLayoutSizes[0], text='MyClip')
       clipData["clipStartText"]= cmds.intField( width=animLayoutSizes[1],value=0)
       clipData["clipEndText"]= cmds.intField(width=animLayoutSizes[2], value=0)
       clipData["clipLoopCheckbox"]= cmds.checkBox(width=animLayoutSizes[3], label='Loop' , value=False) 
       clipData["clipRootCheckbox"]= cmds.checkBox(width=animLayoutSizes[4], label='RootMotion' , value=False)  
       clips[rowName] = clipData
       cmds.button(width=animLayoutSizes[len(animLayoutSizes)-1], label='-', command=functools.partial( deleteClipCallback,rowName ) )
       

       cmds.setParent("..")

    def addEventCallback( *pArgs ):
       cmds.setParent(keyEventsLayout)

       eventRowName = cmds.rowLayout(numberOfColumns=3,columnWidth3=eventsLayoutSizes)
       eventData = {}
       eventData["clipKeyFrame"]= cmds.intField( width=eventsLayoutSizes[0],value=0)
       eventData["clipKeyEvent"]= cmds.textField(width=eventsLayoutSizes[1], text='NewEvent')
       keys[eventRowName] = eventData
       cmds.button(width=eventsLayoutSizes[2], label='-', command=functools.partial( deleteEventCallback,eventRowName ) )
       

       cmds.setParent("..")

    def cancelCallback( *pArgs ):
        if cmds.window( windowID, exists=True ):
          cmds.deleteUI( windowID )
     
    global windowID
    entriesLayout = ""
    keyEventsLayout = ""

     
    if cmds.window( windowID, exists=True ):
         cmds.deleteUI( windowID )
         
    cmds.window( windowID, width=max(sum(animLayoutSizes),sum(eventsLayoutSizes)), title=pWindowTitle, sizeable=True, resizeToFitChildren=True )
    scrollLayout = cmds.scrollLayout(horizontalScrollBarThickness=16,verticalScrollBarThickness=16)
    cmds.columnLayout(width= max(sum(animLayoutSizes),sum(eventsLayoutSizes))+layoutMargin)
    
    #with ui(partial(cmds.rowLayout,numberOfColumns=4,columnWidth4=(80,80,80,80))):
    #     cmds.separator( h=30, style='none' )
    #     cmds.text( label='RootMotion?' )
    #     clips[u'rootMotion'] = cmds.symbolCheckBox( image='circle.xpm',value = True )
    #     cmds.separator( h=30, style='none' )
    
    with ui(partial(cmds.rowLayout,numberOfColumns=4,columnWidth4=(80,80,80,80))):
         cmds.separator( h=30, style='none' )          
         cmds.text( label='ANIMATION' )
         cmds.text( label='LIST' )
         cmds.separator( h=30, style='none' )
     
    with ui(partial(cmds.rowLayout,numberOfColumns=4,columnWidth4=(80,80,80,80))):            
         cmds.text( label='Anim Name' )
         cmds.text( label='Start' )
         cmds.text( label='End' )
         cmds.separator( h=20, style='none' )
   
    entriesLayout = cmds.columnLayout(width= sum(animLayoutSizes)+layoutMargin)
    if os.path.exists(output+'.jsonAnim'):
       with open(output+'.jsonAnim') as data_file:
           animData = json.load(data_file)
           if('animations' in animData):
            clipDatas = animData['animations']    
            for i in range(0,len(clipDatas)):
              rowName = cmds.rowLayout(numberOfColumns=6,columnWidth6=animLayoutSizes)
              clipData = {}
              if("clipName" in clipDatas[i]):
                 clipData["clipNameText"]= cmds.textField(width=animLayoutSizes[0], text=clipDatas[i]["clipName"])
              else:
                 clipData["clipNameText"]= cmds.textField(width=animLayoutSizes[0], text="MyClip")

              if("clipStart" in clipDatas[i]):
                 clipData["clipStartText"]= cmds.intField(width=animLayoutSizes[1], value=int(clipDatas[i]["clipStart"]))
              else:
                 clipData["clipStartText"]= cmds.intField(width=animLayoutSizes[1], value=0)

              if("clipEnd" in clipDatas[i]):
                 clipData["clipEndText"]= cmds.intField(width=animLayoutSizes[2], value=int(clipDatas[i]["clipEnd"])) 
              else:
                 clipData["clipEndText"]= cmds.intField(width=animLayoutSizes[2], value=0) 

              if("clipLoop" in clipDatas[i]):
                clipData["clipLoopCheckbox"]= cmds.checkBox(width=animLayoutSizes[3], label='Loop' , value=bool(clipDatas[i]["clipLoop"])) 
              else:
                clipData["clipLoopCheckbox"]= cmds.checkBox(width=animLayoutSizes[3], label='Loop' , value=False) 

              if("clipRoot" in clipDatas[i]):
                clipData["clipRootCheckbox"]= cmds.checkBox(width=animLayoutSizes[4], label='RootMotion' , value=bool(clipDatas[i]["clipRoot"])) 
              else:
                clipData["clipRootCheckbox"]= cmds.checkBox(width=animLayoutSizes[4], label='RootMotion' , value=False) 

              clips[rowName] = clipData
                    
              cmds.button(width=animLayoutSizes[len(animLayoutSizes)-1], label='-', command=functools.partial( deleteClipCallback,rowName ) )
              cmds.setParent("..")      

    cmds.setParent("..")
    cmds.separator( h=20, style='none' )    
    with ui(partial(cmds.rowLayout,numberOfColumns=1,columnWidth1=(240))):
       cmds.button( width=240,label='Add Animation', command=functools.partial( addClipCallback ) )
    

    with ui(partial(cmds.rowLayout,numberOfColumns=3,columnWidth3=(80,100,20))):            
         cmds.text( label='Keyframe' )
         cmds.text( label='Event Name' )
         cmds.separator( h=20, style='none' )

    keyEventsLayout = cmds.columnLayout(width= sum(eventsLayoutSizes)+layoutMargin)

    if os.path.exists(output+'.jsonAnim'):
       with open(output+'.jsonAnim') as data_file:
           animData = json.load(data_file)
           if('events' in animData):
             keyDatas = animData['events']    
             for i in range(0,len(keyDatas)):
               eventRowName = cmds.rowLayout(numberOfColumns=3,columnWidth3=eventsLayoutSizes)
               keyData = {}
               keyData["clipKeyFrame"]= cmds.intField(width=eventsLayoutSizes[0], value=int(keyDatas[i]["clipKeyFrame"]))
               keyData["clipKeyEvent"]= cmds.textField(width=eventsLayoutSizes[1], text=keyDatas[i]["clipKeyEvent"])
               keys[eventRowName] = keyData
                     
               cmds.button(width=eventsLayoutSizes[2], label='-', command=functools.partial( deleteEventCallback,eventRowName ) )
               cmds.setParent("..")      

    cmds.setParent("..")
    cmds.separator( h=20, style='none' )

    with ui(partial(cmds.rowLayout,numberOfColumns=1,columnWidth1=(240))):
       cmds.button( width=240,label='Add Event', command=functools.partial( addEventCallback ) )

    with ui(partial(cmds.rowLayout,numberOfColumns=2,columnWidth2=(120,120))):
       cmds.button(width=120, label='Save', command=functools.partial( applyCallback ) )
       cmds.button( width=120,label='Cancel', command=cancelCallback )

    cmds.showWindow()    

  def applyCallback(*pArgs ):
     global output
     global windowID
     
     clipDatas = []
     keyDatas = []
     
     for clip in clips:
      cdata = {}
      cdata["clipName"] = cmds.textField(clips[clip]["clipNameText"],query = True,text = True)
      cdata["clipStart"] = cmds.intField(clips[clip]["clipStartText"],query = True,value = True)
      cdata["clipEnd"] = cmds.intField(clips[clip]["clipEndText"],query = True,value = True)
      cdata["clipLoop"] = cmds.checkBox(clips[clip]["clipLoopCheckbox"], query = True,value = True)
      cdata["clipRoot"] = cmds.checkBox(clips[clip]["clipRootCheckbox"], query = True,value = True)
      clipDatas.append(cdata)

     for key in keys:
      kdata = {}
      kdata["clipKeyEvent"] = cmds.textField(keys[key]["clipKeyEvent"],query = True,text = True)
      kdata["clipKeyFrame"] = cmds.intField(keys[key]["clipKeyFrame"],query = True,value = True)
      keyDatas.append(kdata)

     print output+".jsonAnim"
     data = {}
     data['animations'] = clipDatas
     data['events'] = keyDatas
     data['version'] = version
     #data["rootMotion"] = cmds.symbolCheckBox(clips[u'rootMotion'],query = True,value = True)
     json_data = json.dumps(data)    
     with open(output+".jsonAnim", "w+") as text_file:
         text_file.write(json_data)
     if cmds.window( windowID, exists=True ):
             cmds.deleteUI( windowID )







defineClips('Define animation name',mel.eval("file -q -sceneName").replace(".mb","").replace(".ma",""))
# defineClips('Define animation name',"C:\\Users\\Programming-Tools\\Documents\\aaa")