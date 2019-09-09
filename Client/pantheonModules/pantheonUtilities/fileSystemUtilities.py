import os
import filecmp
import shutil
import glob

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
            # print("Error copying " + src_file)

def findFileInParents(fileName,startDirectory,subfolder=""): # yep... it can be found in C:/
    directoryCache = startDirectory
    searchPatttern = directoryCache+subfolder
    foundFiles = glob.glob(searchPatttern+"/"+fileName)
    
    while not foundFiles and directoryCache != os.path.dirname(directoryCache):
        directoryCache = os.path.dirname(directoryCache)
        searchPatttern = directoryCache+subfolder
        foundFiles = glob.glob(searchPatttern+"/"+fileName)

    if len(foundFiles) == 1:
        return foundFiles[0].replace("\\","/")
    elif len(foundFiles) > 1:
        print("found {0} file returning first {1} ".format(len(foundFiles),foundFiles))
        return foundFiles[0].replace("\\","/")
    else:
        return ""

def isPathExists(program_path):
    import re

    arrayPartitions = re.findall(r"[A-Z]+:.*$",os.popen("mountvol /").read(),re.MULTILINE)
    arrayRelativePaths = [
                os.environ["ProgramFiles"],
                 os.environ["PROGRAMW6432"],
                 os.environ["LOCALAPPDATA"] ,
                 os.environ["APPDATA"],
                 os.environ['PROGRAMFILES(X86)']
            ]
    for dir in arrayRelativePaths:
        path =os.path.join(dir+program_path)
        if os.path.exists(path):
            return path

    for  partition in arrayPartitions:
        path =os.path.join(partition+program_path)
        if os.path.exists(path):
            return path

    return ''        

def createBuilderIni(pathIni,arrayFilesOrPrograms): #we need a fn more configurable, withs params
    import configparser

    config = configparser.ConfigParser()
    config.read(pathIni)
    config['Paths'] = {}
    objects= {}
    for program in arrayFilesOrPrograms:
        config['Paths'][program['label']]=isPathExists(program['path']) if program['needSearch'] else program['path']
       
    with open(pathIni, 'w') as configfile:   
        config.write(configfile)

def fetchFiles(path,types):
    onlyfiles = []
    dirPath = path.replace("/","\\")
    print(dirPath)
    if os.path.isdir(dirPath):
        for ftype in types:
            files = glob.glob(dirPath+ftype,recursive=True) 
            onlyfiles.extend(files)
    return onlyfiles
    


