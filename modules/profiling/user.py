import os
from Registry import Registry

def getSIDList(dest_path):
    dest_path = os.path.join(dest_path, r"SOFTWARE")
    key = Registry.Registry(dest_path).open("Microsoft\\Windows NT\\CurrentVersion\\ProfileList")
    
    return [
        (values.value().rpartition('\\')[2], sid)
        for sid in [subkey.name() for subkey in key.subkeys()] 
        for values in Registry.Registry(dest_path).open(f"Microsoft\\Windows NT\\CurrentVersion\\ProfileList\\{sid}").values() 
        if values.name() == "ProfileImagePath"
    ]

def getFVvalues(dest_path):
    list = []
    dest_path = os.path.join(dest_path, r"SAM")
    key = Registry.Registry(dest_path).open("SAM\\Domains\\Account\\Users")
    for subkey in key.subkeys():
        try:
            list.append((subkey.name(), subkey.value('F').raw_data(), subkey.value('V').raw_data()))
        except Registry.RegistryValueNotFoundException:
            continue
    return list

def getPasswordHint(dest_path):
    list = []
    dest_path = os.path.join(dest_path, r"SAM")
    key = Registry.Registry(dest_path).open("SAM\\Domains\\Account\\Users")
    for subkey in key.subkeys():
        try:
            list.append((subkey.name(), subkey.value('UserPasswordHint').raw_data()))
        except Registry.RegistryValueNotFoundException:
            continue
    return list