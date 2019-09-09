import tarfile
import boto3
import os
import sys
import subprocess
import argparse
import glob
import shutil
import filecmp
import zipfile
import re
import ntpath


from subprocess import call
from time import gmtime, strftime


splitProcessPath = "C:/workspaces/BuildSystem/Misc/split.exe"
logfilePath = os.path.expanduser('~/Documents/') + "AvatarCreation.log"

def log(message):
    print(message)
    with open(logfilePath, "a+") as myfile:
        myfile.write(strftime("%m/%d/%Y %H:%M:%S %p", gmtime()) + "++++++"+message+"\n")

def tryint(s):
    try:
        return int(s)
    except:
        return s


def key_func(s):
    return [ tryint(c) for c in re.split('([0-9]+)', s) ]


#define the function to join the chunks of files into a single file
def joinFiles(fileName):
    dirname = os.path.dirname(fileName)
    print(dirname)
    files = sorted(glob.glob(dirname+"/*.chunk*"),key=key_func)
    
    command = "copy /b " 

    fileList = ""

    fout = file(dirname+"/"+ntpath.basename(fileName).replace(".chunk0",""),'wb')
    for n in files:
        log("Reading "+n)
        fin = file(n,'rb')
        while True:
            data = fin.read(65536)
            if not data:
                break
            fout.write(data)
        log(n + " content Written")
        fin.close()
    fout.close()


# define the function to split the file into smaller chunks
def splitFile(inputFile,chunkSize):
    command = splitProcessPath +" " +reposTar + " 1024"
    program = subprocess.Popen(command,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err = program.communicate()
    exitcode = program.returncode

    if str(exitcode) != '0':
        log(err.decode("utf-8") )
        log ('error opening file:' + file)
        
    else:
        programoutput = out.decode("utf-8").split('\n')
        programoutput = list(filter(None, programoutput)) # fastest

        for outFile in programoutput:
            log ('Created:' + outFile+ ' from '+ inputFile)

        
        #log ('Step 1 sucessful for '+file)
    return programoutput


# C:\Program Files\MariaDB 10.1\data\rep_1
# C:\Program Files\MariaDB 10.1\data\rep_2
# C:\Program Files\MariaDB 10.1\data\rep_3
# C:\Program Files\MariaDB 10.1\data\rep_4
# C:\Program Files\MariaDB 10.1\data\rep_5
# C:\Program Files\MariaDB 10.1\data\rep_6
# C:\Program Files\MariaDB 10.1\data\rep_7
# C:\Program Files\MariaDB 10.1\data\repositories
# C:\Program Files\PlasticSCM5\server\db.conf
# C:\Program Files\PlasticSCM5\server\users.conf
# C:\Program Files\PlasticSCM5\server\server.conf
# C:\Users\admin\Desktop\plasticd.lic

mysqlData = [x[0] for x in os.walk("C:\\Program Files\\MariaDB 10.1\\data") if "rep_" in x[0]]
mysqlData.append("C:\\Program Files\\MariaDB 10.1\\data\\repositories")


reposTar = os.path.expanduser("~admin")+"/repos.tar.gz"



dbConf = "C:\\Program Files\\PlasticSCM5\\server\\db.conf"
userConf = "C:\\Program Files\\PlasticSCM5\\server\\users.conf"
serverConf = "C:\\Program Files\\PlasticSCM5\\server\\server.conf"
plasticLic = "C:\\Users\\admin\\Desktop\\plasticd.lic"

extraDataTar = os.path.expanduser("~admin")+"/extraData.tar.gz"



log("Starting building files")
tar = tarfile.open(reposTar, "w:gz")
for dire in mysqlData:
  tar.add(dire, arcname=ntpath.basename(dire),recursive=True)
  log(ntpath.basename(dire) + " ADDED TO TAR")
tar.close()

log("Repos tar DONE")

tar = tarfile.open(extraDataTar, "w:gz")
tar.add(dbConf)
tar.add(userConf)
tar.add(plasticLic)
tar.add(serverConf)
tar.close()
log("Config tar DONE")


log("BACKUP PROCESS")
log("Starting Split")
# call the file splitting function
splittedFiles = splitFile(reposTar,1024)
splittedFiles.append(extraDataTar)

#log("Starting Join")
# call the function to join the splitted files
#log(joinFiles("C:/Users/admin/repos.tar.gz.chunk0"))

s3 = boto3.resource('s3')
folderName = strftime("%m-%d-%Y-%H-%M-%S-%p", gmtime())
for file in splittedFiles:
    file = file.replace("\r","").replace("/","\\")
    s3.Object('plastic-sixthvowel', folderName+"/"+ntpath.basename(file)).put(Body=open(file, 'rb'))
    print("FINISHED " + file)
