import winreg 
import os
import glob
from subprocess import call

singleInstancePath = os.path.dirname(os.path.abspath(__file__))+"\\singleinstance.exe";
ateneaIco = os.path.dirname(os.path.abspath(__file__))+"\\atenea.ico";
regFile = os.path.dirname(os.path.abspath(__file__))+"\\ShortcutsInstaller.reg";
BuildSystemPath = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ateneaFilePath = glob.glob(BuildSystemPath+"/**/Atenea.py",recursive=True)[0]


def set_reg(base,path,keyName, value):
    try:
        winreg.CreateKey(base, path)
        registry_key = winreg.OpenKey(base, path, 0,(winreg.KEY_WOW64_64KEY + winreg.KEY_WRITE))
        winreg.SetValueEx(registry_key, keyName, 0, winreg.REG_SZ, value)
        winreg.CloseKey(registry_key)
        return True
    except WindowsError as e:
        print(e)
        return False

def get_reg(base,path,keyName):
    try:
        registry_key = winreg.OpenKey(base, path, 0, (winreg.KEY_WOW64_64KEY +winreg.KEY_READ))
        value, regtype = winreg.QueryValueEx(registry_key, keyName)
        winreg.CloseKey(registry_key)
        return value
    except WindowsError as e:
        print(e)
        return None

call(["regedit.exe", "/S",regFile])
set_reg(winreg.HKEY_CLASSES_ROOT,r"Directory\shell\atenea","icon",ateneaIco)
set_reg(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\ateneas0","icon",ateneaIco)
set_reg(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\ateneas1","icon",ateneaIco)
set_reg(winreg.HKEY_LOCAL_MACHINE,r"SOFTWARE\Microsoft\Windows\CurrentVersion\Explorer\CommandStore\shell\ateneas2","icon",ateneaIco)
set_reg(winreg.HKEY_CURRENT_USER,r"Environment","SINGLEINSTANCE",singleInstancePath)
set_reg(winreg.HKEY_CURRENT_USER,r"Environment","ATENEAPATH",ateneaFilePath)
