from modules import helper
from modules.services import shadowcopy

def live_acquisition():
    if helper.isWindows() and helper.isAdmin():
        dest_path = False

        while not dest_path:
            dest_path = helper.getPath()
        
        shadowcopy.clone_registry(dest_path)

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()