import os
import sys
import shutil

class GitSetup():

    repoPath = ""
    sourcePath = ""
    name = ""
    username = ""
    password = ""
    isNewRepo = False


    hooks = {}
    hooks["source"] = "/HOOKS/"
    hooks["dest"] = "/.git/hooks/"

    config = {}
    config["source"] = "/CONFIG/"
    config["dest"] = "/.git/"

    newRepo = {}
    newRepo["source"] = "/NEW_REPO/"
    newRepo["dest"] = "/.git/"


    def __init__(self):
        print("STARTING....")

    def askForName(self):
        print("Please enter your name in the form 'Jhon Doe'")
        while not self.name:
            self.name = input('NAME: ')
            pass

    def askForUser(self):
        print("Please enter your name in the form 'Username'")
        while not self.username:
            self.username = input('USERNAME: ')
            pass

    def askForPwd(self):
        print("Please enter your Password")
        while not self.password:
            self.password = input('PASSWORD: ')
            pass


    def askForRepo(self):
        print("Please enter your repo path in the form 'C:/example/repo/path/")
        while not os.path.isdir(self.repoPath) :
            self.repoPath = input('PATH: ')
            pass
    
    def askForSource(self):
        print("DO YOU WANT TO USE THE DEFAULT SOURCE DIRECTORY? (Y/N)")
        defaultSource = ""
        while defaultSource != "Y" and defaultSource != "N" :
            defaultSource = input('CAN I USE IT (G:/Software/GIT REPO COMMON SETUP)?: ').upper()
            pass
        if defaultSource == "N":
            print("Please enter the source files location path in the form 'G:/example/for/source/")
            while not os.path.isdir(self.sourcePath) :
                self.sourcePath = input('PATH: ')
                pass
        
        elif defaultSource == "Y":
            self.sourcePath = "G:Software/GIT REPO COMMON SETUP/"

        print("Using "+self.sourcePath)


    def askIfNewRepo(self):
        print("Is this a new repository? (Y/N)")
        while self.isNewRepo != "Y" and self.isNewRepo != "N" :
            self.isNewRepo = input('IS IT?: ').upper()
            pass

    def setupProject(self):
        print("Copying (new? {2}) repository settings from {0} to {1}".format(self.sourcePath,self.repoPath,self.isNewRepo))
        self.copyFolder(self.sourcePath+self.hooks["source"],self.repoPath+self.hooks["dest"],True)
        self.copyFolder(self.sourcePath+self.config["source"],self.repoPath+self.config["dest"],True)
        if self.isNewRepo:
            self.copyFolder(self.sourcePath+self.newRepo["source"],self.repoPath+self.newRepo["dest"],True)
        self.setUsernameConfig()
        
    def setUsernameConfig(self):
        configFilePath = self.repoPath + "/.git/config"
        if os.path.exists(configFilePath):
            with open(configFilePath, 'r') as file :
                filedata = file.read()

            filedata = filedata.replace('NEEDS_TO_CHANGE_USERNAME', self.name)
            filedata = filedata.replace('[USERNAME]', self.username)
            filedata = filedata.replace('[PASSWORD]', self.password)

            with open(configFilePath, 'w') as file:
                file.write(filedata)


    def copyFolder(self,source, destination,overwrite):
        for src_dir, dirs, files in os.walk(source):
            dst_dir = src_dir.replace(source, destination, 1)
            if not os.path.exists(dst_dir):
                os.makedirs(dst_dir)
            for file_ in files:
                src_file = os.path.join(src_dir, file_)
                dst_file = os.path.join(dst_dir, file_)
                self.copyFile(src_file,dst_file,dst_dir,overwrite)


    def copyFile(self,src_file,dst_file,dst_dir,overwrite= False):
        if os.path.exists(dst_file) and not overwrite:
            if filecmp.cmp(src_file,dst_file):
                print(src_file + " AND " + dst_file + " are identical." )
            else:
                print("Removing " + dst_file)
                os.remove(dst_file)
                print("Copying " + src_file + " TO " + dst_dir )                
                shutil.copy(src_file, dst_dir)
        else:
            if os.path.exists(src_file) and os.path.exists(dst_dir):
                print("Copying " + src_file + " TO " + dst_dir )                
                shutil.copy(src_file, dst_dir)
            else:
                if not os.path.isdir(dst_dir):
                    os.makedirs(dst_dir)                   
                shutil.copy(src_file, dst_dir)
                print("Error copying " + src_file)

if __name__ == '__main__':
    gitSetup = GitSetup()
    gitSetup.askForName()
    print("---------------------------------")
    gitSetup.askForUser()
    print("---------------------------------")
    gitSetup.askForPwd()
    print("---------------------------------")
    gitSetup.askForRepo()
    print("---------------------------------")
    gitSetup.askForSource()
    print("---------------------------------")
    gitSetup.askIfNewRepo()
    print("---------------------------------")
    gitSetup.setupProject()

