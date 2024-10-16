from modules import setup
from modules.services import shadowcopy

def live_acquisition():
    if setup.isWindows() and setup.isAdmin():
        dest_path = False

        while not dest_path:
            dest_path = setup.getPath()
        
        shadowcopy.clone_registry(dest_path)

def main():
    print("Hello World!")

if __name__ == "__main__":
    main()