import json
import datetime
import os

dataFolder = './data'

def getSampleCommitFileName(date):
    return os.path.join(dataFolder, f'sampleCommit{date}.json')

def getExtensionsUsedInCommit(commit):
    exts = set()
    for file in commit["files"]:
        name = file["filename"]
        splitStr = name.split('.')
        if len(splitStr) > 1:
            ext = splitStr[len(splitStr)-1]
            exts.add(ext)
    return exts

def getCommitsFromFile(date):
    with open(getSampleCommitFileName(date), 'r') as infile:
        fileContents = infile.read()
    commits = json.loads(fileContents)
    return commits


if __name__ == '__main__':
    commits = getCommitsFromFile(datetime.date(2017,12,1))
    extensions = getExtensionsUsedInCommit(commits[8])
    print(extensions)
    # print(getExtensionsUsedInCommit(commits[2]))
