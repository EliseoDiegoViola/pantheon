import os
import glob
import os
import subprocess
import sys

#print(os.path.expanduser("~"))

filePath = (os.path.dirname(os.path.abspath(__file__)))
modulesPath = next(glob.iglob("**/Pantheon/Client",recursive=True), None) # FIX THIS SHIT
pantheonModulesPath = os.path.join(filePath,"Client")



def install(package):
    subprocess.call([sys.executable, "-m", "pip", "install", package])

if __name__ == '__main__':
    print("installing ")
    install('PySide2')
    install('PyQt5')
    print("Setting environment variable...")
    print("setx PYTHONPATH "+pantheonModulesPath)
    print(os.system('setx PYTHONPATH '+pantheonModulesPath))
    #print("FINISHED - PLEASE REBOOT")
