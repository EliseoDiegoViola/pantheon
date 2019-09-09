import os
import glob
import json
import shutil


texturesPath = "F:/Projects/ArtMasters/old/Textures"
artmastersPath = "F:/Projects/ArtMasters"
relativeTexturesPath = "/TEXTURES/"

MSRM_PISTOL = "F:/Projects/ArtMasters/Weapons/Single/Single_Smgs_Csac/CSAC_smgs.jsonMats"

def fetchFiles(path,types):
    onlyfiles = []
    dirPath = path.replace("/","\\")
    if os.path.isdir(dirPath):
        for ftype in types:
            files = [f for f in glob.glob(dirPath+ftype,recursive=True)]
            onlyfiles.extend(files)
    return onlyfiles

def parseJsonMats(jsonPath):
    startDir = os.path.dirname(jsonPath)
    texturesDir = startDir+relativeTexturesPath
    print(startDir)
    print(texturesDir)

    with open(jsonPath) as data_file:    
        data = json.load(data_file)
        for key in data:
            content = data[key]
            if isinstance(content, dict):
                properties = content["properties"]
                for prop in properties:
                    pty = prop["propValue"]
                    texturesFetched = fetchFiles(texturesPath,['/**/*'+pty])
                    for tex in texturesFetched:
                        copyFile(tex,texturesDir+pty)

def copyFolder(src_path,dest_path,overwrite = False):
    for src_dir, dirs, files in os.walk(src_path):
        dst_dir = src_dir.replace(src_path, dest_path, 1)
        for file_ in files:
            src_file = os.path.join(src_dir, file_)
            dst_file = os.path.join(dst_dir, file_)
            copyFile(src_file,dst_file,overwrite)

def copyFile(src_file,dst_file,overwrite= False):
    if not os.path.exists(os.path.dirname(dst_file)):
        print("Creating folder for  " + os.path.dirname(dst_file) )
        os.makedirs(os.path.dirname(dst_file))

    if os.path.exists(dst_file) and not overwrite:
        if filecmp.cmp(src_file,dst_file):
            print(src_file + " AND " + dst_file + " are identical." )
        else:
            print("Removing old" + dst_file)
            os.remove(dst_file)
            print("Copying " + src_file + " TO " + dst_file )                
            shutil.copy(src_file, dst_file)
    else:
        if os.path.exists(src_file) and os.path.exists(dst_file):
            print("overwriting " + src_file + " TO " + dst_file )                
            shutil.copy(src_file, dst_file)
        else:       
            shutil.copy(src_file, dst_file)
       


class TextureFile():
    def __init__(path):
        textureName = os.path.splitext(os.path.basename(path))[0]
        texturePath = path
        print(textureName)




# allJsonMats = fetchFiles(artmastersPath,['/**/*.jsonMats'])
# for jsonMats in allJsonMats:
#     print(jsonMats) 

parseJsonMats(MSRM_PISTOL)