import os
import shutil
from  textnode import TextNode

def main():
    #textNode = TextNode("This is a text node", "bold", "https://www.google.com")
    #print(textNode)

    path = "./"
    src = "static"
    dst = "public"
    ignore = ['_', '.']

    clearDir(path, dst)
    createDir(path, dst)
    copyAll(os.path.join(path, src), os.path.join(path, src), os.path.join(path, dst), ignore)

def clearDir(path, targetDir):
    if targetDir in os.listdir(path):
        shutil.rmtree(targetDir)
        print(f"{targetDir} removed from {path}")

def createDir(path, newDir, permissions=0o777):
    try:
        os.mkdir(os.path.join(path, newDir), permissions)
        print(f"Directory created: {os.path.join(path, newDir)}")
    except FileNotFoundError:
        print(f"Path does not exist: {path}")
    except FileExistsError:
        print(f"Directory already exists: {newDir}")

def RmTreeErrorHandler(func, path, excinfo):
    print(func, path, excinfo)
   
def copyAll(path, src, dst, ignore=None):
    pathEntries = os.listdir(path)
    for entry in pathEntries:
        if ignore and any(ord(entry[0]) == ord(item) for item in ignore):
            print("Ignored:", entry)
            continue
        tempPath = os.path.join(path, entry)
        if os.path.isfile(tempPath):
            if os.path.exists(os.path.join(dst, entry)):
                print(f"Replacing {os.path.join(dst, entry)}")
            print(f"Copied: {tempPath} -> {shutil.copy(tempPath, dst)}")
        else:
            if not os.path.exists(os.path.join(dst, entry)):
                createDir(dst, entry)
            copyAll(tempPath, src, dst, ignore)

main()
