import os, time, base64, json

rootPath = ''
dict = {}
refreshInterval = 10

def init(rootPathTmp):
    global rootPath
    rootPath = rootPathTmp


def checkChanges():
    files = getFiles(rootPath)

    changedFiles = []

    for file in files:
        now = time.time()
        modifiedDate = os.path.getmtime(file)
        elapsedSeconds = now - modifiedDate

        if file in dict:
            lastModifiedDate = dict[file]
            if lastModifiedDate < modifiedDate:
                prepareFile(file, modifiedDate, changedFiles)
        else:
            if elapsedSeconds < refreshInterval:
                prepareFile(file, modifiedDate, changedFiles)

    return changedFiles


def prepareFile(filePath, modifiedDate, changedFiles):
    dict[filePath] = modifiedDate

    #print('applying changes for file ' + filePath)

    with open(filePath, "r") as file:
        encoded_string = file.read()

        data = {}
        data['path'] = getRelativePath(filePath)
        data['contents'] = encoded_string

        changedFiles.append(data)


def getRelativePath(path):
    return os.path.relpath(path, rootPath)


def applyChanges(filePath, encoded_string):
    absolutePath = rootPath + os.path.sep + filePath

    print('saving to ' + absolutePath)

    with open(absolutePath, "w") as file:
        file.write(encoded_string)

    dict[absolutePath]= os.path.getmtime(absolutePath)


def getFiles(directory):
    files = []
    listdir(directory, files)

    return files


def listdir(d, files):

    if not os.path.isdir(d):
        f = open(d, "r")
        start = os.path.getmtime(d)

        if d.__contains__('.DS_Store') is False:
            files.append(d)

    else:
        for item in os.listdir(d):
            listdir((d + os.path.sep + item) if d != os.path.sep else os.path.sep + item, files)