import os
import re

dataFolder = './data'

def getCommitSearchFileName(date, page):
    return os.path.join(dataFolder, f'commitSearch{date}-page{page}.json')

def getSampleCommitsFileName(date):
    return os.path.join(dataFolder, f'sampleCommits{date}.json')

def getCommitSearchFilePattern(date):
    return f'commitSearch{date}-page[0-9]+\.json'

def findAllFilesMatching(path, pattern):
    results = []
    with os.scandir(path) as listOfEntries:
        for entry in listOfEntries:
            if entry.is_file():
                if re.search(pattern, entry.name) != None:
                    results.append(os.path.join(dataFolder,entry.name))
    return results

def findAllCommitSearchResultFilesForDate(date):
    pattern = getCommitSearchFilePattern(date)
    return findAllFilesMatching(dataFolder, pattern)
