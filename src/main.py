import sys
import os
import shutil
from textnode import TextNode
from markdown import markdown_to_html_node

def main():
    root = "./"
    src = "static"
    dst = "public"
    indexMarkdownPath = "content"
    ignore = ['_', '.']

    clearDir(root, dst)
    createDir(root, dst)
    copyFilesRecursive(os.path.join(root, src), os.path.join(root, dst), ignore)

    generate_page_recursive(os.path.join(root, "content"), os.path.join(root,
        "template.html"), os.path.join(root, dst))

def generate_page_recursive(srcPath, templatePath, dstPath):
    for entry in os.listdir(srcPath):
        tempPath = os.path.join(srcPath, entry)
        if os.path.isfile(tempPath) and entry.split(".")[-1] == "md":
            newFileName = f"{''.join(entry.split('.')[:-1])}.html"
            generate_page(tempPath, templatePath, os.path.join(dstPath,
                newFileName))
        else:
            if not os.path.exists(os.path.join(dstPath, entry)):
                createDir(dstPath, entry)
            generate_page_recursive(tempPath, templatePath,
                    os.path.join(dstPath, entry))
    return

def generate_page(srcPath, templatePath, dstPath):
    print(f"Generating page from {srcPath} to {dstPath} using {templatePath}.") 

    mdFile = None
    templateHtml = None
    title = None
    contentBody = None
    htmlPage = None

    try:
        mdFile = readFile(srcPath)
        templateHtml = readFile(templatePath)
    except Exception as ex:
        print(str(ex))
        print("Exiting...")
        sys.exit(1)

    try:
        title = extract_title(mdFile)
        contentBody = mdFile.split(title, 1)[-1]
    except Exception as ex:
        print(str(ex))
        print("Exiting...")
        sys.exit(1)
    
    htmlPage = markdown_to_html_node(contentBody)
    templateHtml = templateHtml.replace("{{ Title }}", title.lstrip("#").lstrip())
    templateHtml = templateHtml.replace("{{ Content }}", repr(htmlPage))

    saveFile(dstPath, templateHtml)
    return 

def extract_title(markdown):
    if markdown == None or len(markdown) <= 0:
        return ""
    title = markdown.lstrip().split("\n", 1)[0]
    if not title.startswith("#"):
        raise Exception("Markdown title not found.")
    return title

def clearDir(path, targetDir):
    if targetDir in os.listdir(path):
        shutil.rmtree(targetDir)
        print(f"{targetDir} removed from {path}")

def createDir(path, newDir, permissions=0o777):
    try:
        os.mkdir(os.path.join(path, newDir), permissions)
        print(f"Directory created: {os.path.join(path, newDir)}")
    except FileNotFoundError as ex:
        print(str(ex))
        print(f"Path does not exist: {path}")
    except FileExistsError as ex:
        print(str(ex))
        print(f"Directory already exists: {newDir}")

def RmTreeErrorHandler(func, path, excinfo):
    print(func, path, excinfo)
   
def copyFilesRecursive(path, dst, ignore=None):
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
            copyFilesRecursive(tempPath, os.path.join(dst, entry), ignore)

def readFile(path):
    content = None
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    if not f.closed:
        f.close()
    return content

def saveFile(path, content):
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    if not f.closed:
        f.close()
    return

main()
