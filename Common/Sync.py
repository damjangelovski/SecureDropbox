import os, time, base64, json

rootPath = ''
dict = {}
refreshInterval = 100

def init(rootPathTmp):
    global rootPath
    rootPath = rootPathTmp


def checkChanges():
    files = getFiles(rootPath)

    for file in files:
        now = time.time()
        modifiedDate = os.path.getmtime(file)
        elapsedSeconds = now - modifiedDate

        if file in dict:
            lastModifiedDate = dict[file]
            if lastModifiedDate == modifiedDate:
                prepareFile(file, modifiedDate)
        else:
            if elapsedSeconds < refreshInterval:
                prepareFile(file, modifiedDate)


def prepareFile(filePath, modifiedDate):
    dict[filePath] = modifiedDate

    print('applying changes for file ' + filePath)

    with open(filePath, "rb") as file:
        encoded_string = base64.b64encode(file.read())

        print(encoded_string)

        data = {}
        data['path'] = filePath
        data['contents'] = encoded_string

        return data


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