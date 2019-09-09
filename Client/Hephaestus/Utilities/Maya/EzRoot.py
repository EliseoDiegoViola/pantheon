import pymel.core as pm
import maya.cmds as cmds
import maya.mel as mel

actualRoot = pm.ls("|Root")[0]

                  
startTime = int(cmds.playbackOptions(query = True, minTime=True))
endTime = int(cmds.playbackOptions(query = True, maxTime=True))+1
                
for time in range(startTime,endTime):
    cmds.currentTime (time)
    cmds.select('Main')
    rootMirror = pm.ls("Root_Mirror")[0]
    imm = rootMirror.transformationMatrix().inverse()
    matrixArray = [imm.a00,imm.a01,imm.a02,imm.a03,
                    imm.a10,imm.a11,imm.a12,imm.a13,
                     imm.a20,imm.a21,imm.a22,imm.a23,
                      imm.a30,imm.a31,imm.a32,imm.a33]    
    cmds.xform(matrix=matrixArray)




