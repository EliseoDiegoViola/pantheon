import sys
import json
import os
import glob
import msvcrt
        


sys.path.append('C:/Proyectos/BuildSystem')
from pantheonModules.parser import jsonStructures
from pantheonModules.versioning import requests


exportTypes = ('/**/*.jsonAnim')

basePath = "C:\\Proyectos\\Artmasters\\Animations"
animDump = "C:\\Users\\Programming-Tools\\Desktop\\AnimDump.json"

with open(animDump) as data_file:    
    dump = json.load(data_file)

files = glob.glob(basePath+exportTypes,recursive=True)
parser = jsonStructures.MayaParser()
#my_dict.pop('key', None)

for file in files:
    try:
        with open(file) as data_file:    
            data = json.load(data_file)
            name = (os.path.splitext(os.path.basename(file))[0])
            ver = parser.getVersion(data)
            dumpData = ""
            if "Bogatyruy@IonCannonandGatlingWalking" in name:
                print(ver)

            if ver == 0:
                if str(name) in dump:



                    dumpData = dump[str(name)]
                    if 'events' in dumpData:
                        data['events'] = dumpData['events']
                    else:
                        data['events'] = []

                    if dumpData:
                        anims = data["animations"]
                        for i in range(0,len(anims)):
                            anim = anims[i]

                            dumpClipData = dumpData[str(i)]
                            if anim["clipName"] == dumpClipData["clipName"]:
                                a = b'Y'
                            else:
                                a = b'Y'

                            while(a != b'Y' and a != b'N'):
                                print("Unity animation name of "+ os.path.basename(file) + " is "+ dumpClipData["clipName"] +" but in metadata is " + anim["clipName"] + " OVERRIDE CLIPNAME in metadata? Y / N")
                                a = msvcrt.getch().upper()
                            if a == b'Y':
                                print(anim["clipName"])
                            
                            data.pop('animLoop',None)
                            anim["clipLoop"] = dumpClipData["clipLoop"]    
                            data.pop('rootMotion',None)
                            anim["clipRoot"] = dumpClipData["clipRoot"]
                    
                        data['version'] = 10
                    else:
                        print(file + " UNITY IMPORT PROCESS HAS NOT BEEN COMPLETED OR IS CORRUPTED! Version : " + str(ver))
            elif ver == 1:
                if str(name) in dump:
                    dumpData = dump[str(name)]
                    if 'events' in dumpData:
                        data['events'] = dumpData['events']
                    else:
                        data['events'] = []
                    if dumpData:
                        anims = data["animations"]
                        for i in range(0,len(anims)):
                            anim = anims[i]
                            dumpClipData = dumpData[str(i)]
                            if anim["clipName"] == dumpClipData["clipName"]:
                                a = b'Y'
                            else:
                                a = b'Y'

                            while(a != b'Y' and a != b'N'):
                                print("Unity animation name of "+ os.path.basename(file) + " is "+ dumpClipData["clipName"] +" but in metadata is " + anim["clipName"] + " OVERRIDE CLIPNAME in metadata? Y / N")
                                a = msvcrt.getch().upper()
                            if a == b'Y':
                                print(anim["clipName"])
                            
                            data.pop('animLoop',None)
                            anim["clipLoop"] = dumpClipData["clipLoop"]    
                            data.pop('rootMotion',None)
                            anim["clipRoot"] = dumpClipData["clipRoot"]
                            
                        data["version"] = 10
                    else:
                        print(file + " UNITY IMPORT PROCESS HAS NOT BEEN COMPLETED OR IS CORRUPTED! Version : " + str(ver))
            elif ver == 2:
                if str(name) in dump:
                    dumpData = dump[str(name)]
                    if 'events' in dumpData:
                        data['events'] = dumpData['events']
                    else:
                        data['events'] = []
                    if dumpData:
                        anims = data["animations"]
                        for i in range(0,len(anims)):
                            anim = anims[i]

                            dumpClipData = dumpData[str(i)]
                            if anim["clipName"] in dumpClipData["clipName"]:
                                a = b'Y'
                            else:
                                a = b'Y'

                            while(a != b'Y' and a != b'N'):
                                print("Unity animation name of "+ os.path.basename(file) + " is "+ dumpClipData["clipName"] +" but in metadata is " + anim["clipName"] + " OVERRIDE CLIPNAME in metadata? Y / N")
                                a = msvcrt.getch().upper()
                            if a == b'Y':
                                print(anim["clipName"])
                            # print(anim["clipLoop"])
                            data.pop('rootMotion',None)
                            anim["clipRoot"] = dumpClipData["clipRoot"]
                            # print(anim["clipRoot"])
                        data["version"] = 10
                    else:
                        print(file + " UNITY IMPORT PROCESS HAS NOT BEEN COMPLETED OR IS CORRUPTED! Version : " + str(ver))
            elif ver == 10:
                # if str(name) in dump:
                #     dumpData = dump[str(name)]
                #     data["version"] = 10
                    
                #     if 'events' in dumpData['0']:
                #         data['events'] = dumpData['0']['events']
                #         print("Version 10 EVENTS UPDATED! " + str(dumpData['0']['events']))
                #     else:
                #         data['events'] = []
                #         print("Version 10 NO EVENTS FOR! " + name)
                # else:
                #     print(name)
                # continue
                if str(name) in dump:
                    dumpData = dump[str(name)]
                    if 'events' in dumpData:
                        data['events'] = dumpData['events']
                    if dumpData:
                        anims = data["animations"]
                        for i in range(0,len(anims)):
                            anim = anims[i]

                            dumpClipData = dumpData[str(i)]
                            print(anim["clipName"])
                            if anim["clipName"] == dumpClipData["clipName"]:
                                print(anim["clipLoop"])
                                print(anim["clipRoot"])
                            else:
                                print("Version 10 - ERROR! I dont have data for " + anim["clipName"])
                    else:
                        print(file + " UNITY IMPORT PROCESS HAS NOT BEEN COMPLETED OR IS CORRUPTED! Version : " + str(ver))

            json_data = json.dumps(data)    
            with open(file, "w+") as text_file:
                text_file.write(json_data)
    except Exception as e:
        print(str(e) + str(file) + " -- "+ str(dumpData))
        break

                
                

