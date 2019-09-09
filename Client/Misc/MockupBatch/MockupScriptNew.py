import maya.standalone
import maya.cmds as cmds
import sys
import maya.standalone as std
import os
import math

from multiprocessing.connection import Client



# Start Maya in batch mode
try:
    #std.initialize()
    std.initialize(name='python')
except Exception as e:
    print(e)
#cmds.loadPlugin('mtoa')
cmds.loadPlugin("fbxmaya")
import pymel.core as pm

class MoCapFixer():
#sys.argv#
    def __init__(self):
        self.files = sys.argv
        
        # self.files = ['C:\Proyectos\Athenea\Client\Misc\MockupBatch\MockUpScriptNew.py',
        # 'RIG_FemaleProxy',
        # 'C:\Proyectos\Athenea\Client\Misc\MockupBatch\Mocks\F Half Cover R_v01.fbx']

        self.workDirectory = os.path.dirname(os.path.realpath(self.files[0]))
        self.reference = "{0}/Rig/{1}.ma".format(self.workDirectory, self.files[1])
        self.namespace = "RigWorkspace"
        self.cachedConstraints= []
        self.conn = None

        self.address = ('localhost', 6000)
        try:
            self.conn = Client(self.address, authkey=b'batch')
        except Exception as e:
            print(e)
            self.conn = None        

# can also send arbitrary objects:
# conn.send(['a', 2.5, None, int, sum])

    def log(self, msg):
        if self.conn:
            self.conn.send (msg)
        else:
            print(msg)

    def closeConn(self):
        if self.conn:
            self.log('FINISHED')
            self.conn.close()
            std.uninitialize()
            os._exit(0)


    def processFiles(self):
        scales = {
            '{0}/Rig/RIG_MidMaleProxy.ma'.format(self.workDirectory):{
                "csa":1.10,
                "ssa":1.12
            },
            '{0}/Rig/RIG_BigMaleProxy.ma'.format(self.workDirectory):{
                "csa":1.29,
                "ssa":1.20
            },
            '{0}/Rig/RIG_FemaleProxy.ma'.format(self.workDirectory):{
                "csa":1.12,
                "ssa":1.11
            }
        }

        self.log("Processing Files!")

        try:
            amountToSubstract = 2
            #importar el mocap fbx. DONE
            for i in range(amountToSubstract,len(self.files)):
                self.log("+++++++++++++++++++++++++++++++++ PARSING {0} OF {1} FILES".format(i,len(self.files)-amountToSubstract))

                #reset Values
                self.cachedConstraints= []
                cmds.file(new=True, force=True)
                fileName = self.files[i]


                if fileName != '':
                    self.log("-------------------------------------------")
                    self.log(fileName)
                    cmds.file(fileName, force=True, open=True)
                    self.log("+++++++++++++++++")        
                    self.log(fileName)

                    #sacarle el namespace al mocap skeleton. DONE
                    namespaces =  [item for n in cmds.ls( type='joint' )  if len(n.split(":")) > 1 for item in n.split(":")[:2]]
                    namespaces = sorted(set(namespaces), key=namespaces.index)
                    for ns in namespaces:
                        cmds.namespace( removeNamespace = ":"+ns, mergeNamespaceWithRoot = True)
                     #start and end animation time DONE
                    startTime = cmds.findKeyframe( "Hips", which="first" ) #int(cmds.playbackOptions(query = True, minTime=True))
                    endTime = cmds.findKeyframe( "Hips", which="last" ) #int(cmds.playbackOptions(query = True, maxTime=True))
                    
                    #Set the playback range to start and end
                    cmds.playbackOptions(min = startTime-10, max = math.ceil(endTime))
                    cmds.currentTime( startTime-10 )

                    cmds.select("Hips")
                    cmds.group( name='mocap_root_grp' )

                    #reference rig. DONE
                    
                    rigName = self.reference.replace("\\", "/")
                    self.log("--RIG: " + str(rigName))
                    self.log("--RIG: " + str(self.namespace))
                    cmds.file( rigName, namespace=self.namespace, reference=True,type="mayaAscii",ignoreVersion=True,groupLocator=True,mergeNamespacesOnClash=False,options="v=0;p=17;f=0" )
                    self.log("OPENED RIG: " + str(self.reference))

                    #set ctl rig T pose
                    cmds.setAttr ('{0}:l_armIk_00_ctl.t'.format(self.namespace), -19.16, 46.422, -3.293)
                    cmds.setAttr ('{0}:l_armIk_00_ctl.r'.format(self.namespace), 26.323, 35.337, 37.916)
                    cmds.setAttr ('{0}:r_armIk_00_ctl.t'.format(self.namespace), 19.16, 46.422, -3.293)
                    cmds.setAttr ('{0}:r_armIk_00_ctl.r'.format(self.namespace), 26.323, -35.337, -37.916)
                    cmds.setAttr ('{0}:l_armPvIk_00_ctl.spaceSwitch'.format(self.namespace), 6)
                    cmds.setAttr ('{0}:r_armPvIk_00_ctl.spaceSwitch'.format(self.namespace), 6)

                    cmds.setAttr ('{0}:l_upArmFk_00_ctl.r'.format(self.namespace), 0, -3.5, 45)
                    cmds.setAttr ('{0}:r_upArmFk_00_ctl.r'.format(self.namespace), 0, -3.5, 45)
                    cmds.setAttr ('{0}:l_lowArmFk_00_ctl.r'.format(self.namespace), 0, 29.652, 0)
                    cmds.setAttr ('{0}:r_lowArmFk_00_ctl.r'.format(self.namespace), 0, 29.652, 0)

                     
                    # HipLocator Fixer DONE
                    # spx = cmds.getAttr("%s.translateX" % '{0}:c_spine_00_rigJnt'.format(self.namespace))
                    # spy = cmds.getAttr("%s.translateY" % '{0}:c_spine_00_rigJnt'.format(self.namespace))
                    # spz = cmds.getAttr("%s.translateZ" % '{0}:c_spine_00_rigJnt'.format(self.namespace)) 
                    # cmds.spaceLocator (p=(0,0,0), n="HipLoc", a=True)
                    # cmds.move( spx,spy,spz, 'HipLoc', absolute=True )

                    # pc = cmds.parentConstraint ("HipLoc",  '{0}:c_main_00_ctl'.format(self.namespace) , mo=True)
                    
                    hx = cmds.getAttr("%s.translateX" % 'Hips')
                    hy = cmds.getAttr("%s.translateY" % 'Hips')
                    hz = cmds.getAttr("%s.translateZ" % 'Hips')
                    # cmds.move( hx, hy, hz, 'HipLoc', absolute=True )
                    # self.cachedConstraints.append(pc)
                    
                    #CHANGE PIVOT
                    cmds.move(hx,hy,hz, "mocap_root_grp.scalePivot", "mocap_root_grp.rotatePivot")
                    #THIS WILL MOVE ONE OBJECT TO THE OTHER, EVEN IF THEY ARE NOT IN THE SAME HIERARCHY
                    cmds.delete(cmds.pointConstraint('{0}:c_root_01_skn'.format(self.namespace), "mocap_root_grp", w=1))

                    # return

                    #SCALE MOCAP CENTER, AND FIRST SPINE
                    csa = scales[self.reference]["csa"] #Mocap Center Scale Amount
                    ssa = scales[self.reference]["ssa"] #Mocap Spine Scale Amount
                    cmds.scale(csa,csa,csa,"mocap_root_grp")
                    cmds.scale(ssa,ssa,ssa,"Spine")                  
                    
                    #match mocap skeleton to rig positions
                    positions = {
                    # '{0}:c_root_00_rigJnt'.format(self.namespace):'Hips', 
                    '{0}:c_spine_00_rigJnt'.format(self.namespace):'Spine', 
                    '{0}:c_spine_01_rigJnt'.format(self.namespace):'Spine1',
                    '{0}:c_spine_02_rigJnt'.format(self.namespace):'Spine2',
                    '{0}:c_chest_00_rigJnt'.format(self.namespace):'Spine3',
                    '{0}:c_neck_00_rigJnt'.format(self.namespace):'Neck',
                    '{0}:c_head_00_rigJnt'.format(self.namespace):'Head',
                    '{0}:c_head_01_rigJnt'.format(self.namespace):'HeadEnd',
                    '{0}:l_clavicle_00_rigJnt'.format(self.namespace):'LeftShoulder',
                    '{0}:l_upArm_00_rigJnt'.format(self.namespace):'LeftArm',
                    '{0}:l_lowArm_00_rigJnt'.format(self.namespace):'LeftForeArm',
                    '{0}:l_wrist_00_rigJnt'.format(self.namespace):'LeftHand',
                    '{0}:l_thumb_01_rigJnt'.format(self.namespace):'LeftHandThumb1',
                    '{0}:l_thumb_02_rigJnt'.format(self.namespace):'LeftHandThumb2',
                    '{0}:l_middle_01_rigJnt'.format(self.namespace):'LeftHandEnd',
                    '{0}:l_middle_03_rigJnt'.format(self.namespace):'L_FingersEnd',
                    '{0}:l_upLeg_00_rigJnt'.format(self.namespace):'LeftUpLeg',
                    '{0}:l_lowLeg_00_rigJnt'.format(self.namespace):'LeftLeg',
                    '{0}:l_foot_00_rigJnt'.format(self.namespace):'LeftFoot',
                    '{0}:l_ball_00_rigJnt'.format(self.namespace):'LeftToeBase',
                    '{0}:l_toes_00_rigJnt'.format(self.namespace):'LeftToeBaseEnd',

                    '{0}:r_clavicle_00_rigJnt'.format(self.namespace):'RightShoulder',
                    '{0}:r_upArm_00_rigJnt'.format(self.namespace):'RightArm',
                    '{0}:r_lowArm_00_rigJnt'.format(self.namespace):'RightForeArm',
                    '{0}:r_wrist_00_rigJnt'.format(self.namespace):'RightHand',
                    '{0}:r_thumb_01_rigJnt'.format(self.namespace):'RightHandThumb1',
                    '{0}:r_thumb_02_rigJnt'.format(self.namespace):'RightHandThumb2',
                    '{0}:r_middle_01_rigJnt'.format(self.namespace):'RightHandEnd',
                    '{0}:r_middle_03_rigJnt'.format(self.namespace):'R_FingersEnd',
                    '{0}:r_upLeg_00_rigJnt'.format(self.namespace):'RightUpLeg',
                    '{0}:r_lowLeg_00_rigJnt'.format(self.namespace):'RightLeg',
                    '{0}:r_foot_00_rigJnt'.format(self.namespace):'RightFoot',
                    '{0}:r_ball_00_rigJnt'.format(self.namespace):'RightToeBase',
                    '{0}:r_toes_00_rigJnt'.format(self.namespace):'RightToeBaseEnd'
                    }

                    #NO REPOSITION OF MOCAP RIG!!!!!
                    # cmds.currentTime (startTime-50, e=1)
                    # for items in positions.items():
                    #     # self.log('{0} position {1}'.format(items[0], items[1]))
                    #     #cmds.setAttr ((items[1]+'.r'), 0, 0, 0)
                    #     pc = cmds.pointConstraint (items[0], items[1])
                         
                    #SET KEYFRAME FOR TRANSFORM AND ROTATION FOR EVERY MOCAP JOINT
                    cmds.setKeyframe("mocap_root_grp", at='translate', hi='below')
                    cmds.setKeyframe("mocap_root_grp", at='rotate', hi='below')
                    # for items in positions.items():    
                    #     cmds.setKeyframe (items[1]+'.t')
                    #     cmds.setKeyframe (items[1]+'.r')  
                    #     cmds.delete (items[1]+'_pointConstraint1')    


                    
                    #apply offsets betwwen roots DONE
                    # attributes = ["translateX","translateY","translateZ"]
                    # cmds.currentTime (startTime, edit=True)
                    # for att in attributes:
                    #     rigRootOri = cmds.getAttr("RigWorkspace:c_root_00_rigJnt.{0}".format(att))
                    #     mocRootOri = cmds.getAttr("Hips.{0}".format(att))
                    #     print(rigRootOri-mocRootOri)
                    #     cmds.keyframe("Hips.{0}".format(att),relative=True,edit=True,time=(startTime,endTime),valueChange=rigRootOri - mocRootOri)   
                    
                    #create locator                  

                    
                    #generate ctlMocap from select set ctlMocap
                    mocapCtl=cmds.sets ('{0}:mocapCtl_set'.format(self.namespace), q=1)

                    for ctl in mocapCtl:
                        ctlSp=ctl.split(':')    
                        loc=cmds.spaceLocator (p=(0,0,0), n=ctlSp[1].replace('ctl', 'loc'))
                        grp=cmds.createNode ('transform', n=ctlSp[1].replace('ctl', 'locGrp')) 
                        ro=cmds.getAttr (ctl+'.rotateOrder')
                        cmds.setAttr (loc[0]+'.rotateOrder', ro)
                        cmds.setAttr (grp+'.rotateOrder', ro)    
                        cmds.parent (loc, grp)
                        pc=cmds.parentConstraint (ctl, grp)
                        cmds.delete (pc)
                    

                    #parent ctlMocap to skeleton
                    parents = {
                    'c_bodyIk_00_locGrp':'Hips',  
                    'c_spineFk_00_locGrp':'Spine',  
                    'c_spineFk_01_locGrp':'Spine2',  
                    'c_spineFk_02_locGrp':'Spine3',  
                    'c_neckFk_00_locGrp':'Neck',  
                    'c_headFk_00_locGrp':'Head',  
                    'l_clavicleIk_00_locGrp':'LeftShoulder',
                    'l_upArmFk_00_locGrp':'LeftArm', 
                    'l_lowArmFk_00_locGrp':'LeftForeArm',
                    'l_armPvIk_00_locGrp':'LeftForeArm',   
                    'l_wristFk_00_locGrp':'LeftHand',  
                    'l_armIk_00_locGrp':'LeftHand',

                    'r_clavicleIk_00_locGrp':'RightShoulder',  
                    'r_upArmFk_00_locGrp':'RightArm',
                    'r_lowArmFk_00_locGrp':'RightForeArm',
                    'r_armPvIk_00_locGrp':'RightForeArm',   
                    'r_wristFk_00_locGrp':'RightHand',  
                    'r_armIk_00_locGrp':'RightHand',

                    'l_upLegFk_00_locGrp':'LeftUpLeg',  
                    'l_lowLegFk_00_locGrp':'LeftLeg',
                    'l_legPvIk_00_locGrp':'LeftLeg',
                    'l_footFk_00_locGrp':'LeftFoot',  
                    'l_legIk_00_locGrp':'LeftFoot', 
                    'l_ballFk_00_locGrp':'LeftToeBase', 
                     
                    'r_upLegFk_00_locGrp':'RightUpLeg',  
                    'r_lowLegFk_00_locGrp':'RightLeg',
                    'r_legPvIk_00_locGrp':'RightLeg',
                    'r_footFk_00_locGrp':'RightFoot',  
                    'r_legIk_00_locGrp':'RightFoot', 
                    'r_ballFk_00_locGrp':'RightToeBase'
                    }
                    for items in parents.items():
                        # self.log('{0} parent to {1}'.format(items[0], items[1]))
                        cmds.parent (items[0], items[1])


                    #parentConstraints mocapCtl a ctl  
                    parentsPar = {
                    'c_bodyIk_00_loc':'{0}:c_bodyIk_00_ctl'.format(self.namespace),  
                    'l_clavicleIk_00_loc':'{0}:l_clavicleIk_00_ctl'.format(self.namespace),
                    'l_armPvIk_00_loc':'{0}:l_armIkPV_00_inp'.format(self.namespace),   
                    'l_armIk_00_loc':'{0}:l_armIk_00_ctl'.format(self.namespace),
                    'r_clavicleIk_00_loc':'{0}:r_clavicleIk_00_ctl'.format(self.namespace),  
                    'r_armPvIk_00_loc':'{0}:r_armIkPV_00_inp'.format(self.namespace),   
                    'r_armIk_00_loc':'{0}:r_armIk_00_ctl'.format(self.namespace),
                    'l_legPvIk_00_loc':'{0}:l_legIkPV_00_inp'.format(self.namespace),
                    'l_legIk_00_loc':'{0}:l_legIk_00_ctl'.format(self.namespace), 
                    'r_legPvIk_00_loc':'{0}:r_legIkPV_00_inp'.format(self.namespace),
                    'r_legIk_00_loc':'{0}:r_legIk_00_ctl'.format(self.namespace) 
                    }
                    for items in parentsPar.items():
                        # self.log('{0} parent to {1}'.format(items[0], items[1]))
                        pc = cmds.parentConstraint (items[0], items[1], mo=1)
                        self.cachedConstraints.append(pc)

                    #orientConstraints mocapCtl a ctl    
                    parentsOri = {    
                    'c_spineFk_00_loc':'{0}:c_spineFk_00_ctl'.format(self.namespace),  
                    'c_spineFk_01_loc':'{0}:c_spineFk_01_ctl'.format(self.namespace),  
                    'c_spineFk_02_loc':'{0}:c_spineFk_02_ctl'.format(self.namespace),  
                    'c_neckFk_00_loc':'{0}:c_neckFk_00_ctl'.format(self.namespace),  
                    'c_headFk_00_loc':'{0}:c_headFk_00_ctl'.format(self.namespace),
                    'l_upArmFk_00_loc':'{0}:l_upArmFk_00_ctl'.format(self.namespace), 
                    'l_lowArmFk_00_loc':'{0}:l_lowArmFk_00_ctl'.format(self.namespace),
                    'l_wristFk_00_loc':'{0}:l_wristFk_00_ctl'.format(self.namespace), 
                    'r_upArmFk_00_loc':'{0}:r_upArmFk_00_ctl'.format(self.namespace),
                    'r_lowArmFk_00_loc':'{0}:r_lowArmFk_00_ctl'.format(self.namespace),
                    'r_wristFk_00_loc':'{0}:r_wristFk_00_ctl'.format(self.namespace),
                    'l_upLegFk_00_loc':'{0}:l_upLegFk_00_ctl'.format(self.namespace),  
                    'l_lowLegFk_00_loc':'{0}:l_lowLegFk_00_ctl'.format(self.namespace),
                    'l_footFk_00_loc':'{0}:l_footFk_00_ctl'.format(self.namespace),
                    'l_ballFk_00_loc':'{0}:l_ballFk_00_ctl'.format(self.namespace), 
                    'r_upLegFk_00_loc':'{0}:r_upLegFk_00_ctl'.format(self.namespace),  
                    'r_lowLegFk_00_loc':'{0}:r_lowLegFk_00_ctl'.format(self.namespace),
                    'r_footFk_00_loc':'{0}:r_footFk_00_ctl'.format(self.namespace),
                    'r_ballFk_00_loc':'{0}:r_ballFk_00_ctl'.format(self.namespace)         
                    }
                    for items in parentsOri.items():
                        # self.log('{0} orient to {1}'.format(items[0], items[1]))
                        pc = cmds.orientConstraint (items[0], items[1], mo=1)
                        self.cachedConstraints.append(pc)
                    

                    #connect extra attrs
                    self.log("connect extra attrs")
                    cmds.connectAttr ('LeftToeBase.rz','{0}:l_legIk_00_ctl.toesWiggle'.format(self.namespace)  )
                    cmds.connectAttr ('RightToeBase.rz','{0}:r_legIk_00_ctl.toesWiggle'.format(self.namespace)  )
                    
                    # return

                    #bake animation DONE
                    self.log("bake animation")
                    cmds.bakeResults (mocapCtl, t=(startTime-10,endTime), simulation=1, sampleBy=1, oversamplingRate=1, disableImplicitControl=1, preserveOutsideKeys=1, sparseAnimCurveBake=0, controlPoints=0, shape=1) 

                    #reset main control DONE
                    self.log("resetting")
                    cmds.move( 0, 0, 0, '{0}:c_main_00_ctl'.format(self.namespace), absolute=True )                    

                    #delete constraints. DONE
                    self.log("delete constraints")
                    for constraint in self.cachedConstraints:
                        cmds.delete(constraint)

                    # return

                    #clean  unknown nodes and other stray nodes
                    oldValue = "0";
                    if "MAYA_TESTING_CLEANUP" in os.environ:
                        oldValue = os.environ["MAYA_TESTING_CLEANUP"]

                    os.environ["MAYA_TESTING_CLEANUP"] = "1"

                    pm.mel.source('cleanUpScene')

                    pm.mel.scOpt_performOneCleanup({
                        'unknownNodesOption',
                        'shadingNetworksOption',
                        'renderLayerOption',
                        'displayLayerOption',
                        'shaderOption'
                        }
                    )
                    os.environ["MAYA_TESTING_CLEANUP"] = oldValue

                    cmds.delete("Hips")
                    # cmds.delete("HipLoc")
                    
                    self.log("Exporting")
                    if not os.path.isdir(self.workDirectory+"\\Exports\\"):
                        os.makedirs(self.workDirectory+"\\Exports\\")

                    rigName = os.path.splitext(os.path.basename(self.reference))[0]
                    finalFileName = os.path.splitext(os.path.basename(fileName))[0]
                    self.log("{0}\\Exports\\{1}_{2}.ma".format(self.workDirectory,rigName, finalFileName))
                    cmds.file( rename="{0}\\Exports\\{1}_{2}.ma".format(self.workDirectory,rigName, finalFileName))
                    cmds.file(force=True, type='mayaAscii', save=True )
        except Exception as e:
            print(e)
            self.log('FINISHED')


        

mocapF = MoCapFixer()
mocapF.processFiles()
mocapF.closeConn()
# 






