import platform
import subprocess
import os
import shutil
from datetime import datetime

def create_shadow_copy():
    command = ["wmic", "shadowcopy", "call", "create", "volume='C:\\'"]
    result = subprocess.run(command, capture_output=True, text=True)

    if "ShadowID" in result.stdout:
        shadow_id = result.stdout.split("ShadowID = ")[1].split(";")[0].strip().replace('"', '')
        print(f"[DONE] Created shadow copy with ID: {shadow_id}")
        return shadow_id
    else:
        print("[ERROR] Failed to create shadow copy")
        return None

def get_shadow_path(shadow_id):
    command = ["vssadmin", "list", "shadows"]
    result = subprocess.run(command, capture_output=True, text=True).stdout.splitlines()

    for i, line in enumerate(result):
        if shadow_id.lower() in line.lower():
            for j in range(i, len(result)):
                if "Shadow Copy Volume" in result[j]:
                    shadow_volume_path = result[j].split("Shadow Copy Volume: ")[1].strip()
                    print(f"[DONE] Retrieved shadow volume path: {shadow_volume_path}")
                    return shadow_volume_path

def get_registry(shadow_volume_path, dest_path):
    registry_path = {
        "SAM": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SAM"),
        "SECURITY": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SECURITY"),
        "SYSTEM": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SYSTEM"),
        "SOFTWARE": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SOFTWARE"),
    }

    for file, src_path in registry_path.items():
        save_path = os.path.join(dest_path, f"{file}")
        shutil.copy(src_path, save_path)
        print(f"[DONE] {file} file saved as: {save_path}")

def delete_shadow_copy(shadow_id):
    command = ["wmic", "shadowcopy", "where", f"ID='{shadow_id}'", "delete"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[DONE] Deleted shadow copy with ID: {shadow_id}")

def main():
    dest_path = input("[USER INPUT] Enter the destination folder: ")

    if not os.path.exists(dest_path):
        print("[ERROR] Path does not exist")
        return

    timestamp = datetime.now().strftime(f"%Y%m%d%H%M%S")
    dest_path = os.path.join(dest_path, timestamp)

    os.makedirs(os.path.join(dest_path, "registry"), exist_ok=True)

    if platform.system() == "Windows":
        shadow_id = create_shadow_copy()
        
        if shadow_id:
            registry_path = os.path.join(dest_path, "registry")
            get_registry(get_shadow_path(shadow_id), registry_path)
            delete_shadow_copy(shadow_id)

if __name__ == "__main__":
    main()