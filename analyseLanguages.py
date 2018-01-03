import json
import datetime
import os
from shared import getSampleCommitsFileName

def getExtensionsUsedInCommit(commit):
    exts = set()
    for file in commit["files"]:
        name = file["filename"]
        splitStr = name.split('.')
        if len(splitStr) > 1:
            # extension is last element
            ext = splitStr[len(splitStr)-1]
            exts.add(ext)
    return exts

def getCommitsFromFile(date):
    with open(getSampleCommitsFileName(date), 'r') as infile:
        fileContents = infile.read()
    commits = json.loads(fileContents)
    return commits

def analyseLanguagesForDates(startDate, endDateInclusive):
    #column headings for CSV file
    output = "date,"
    for ext in includeExtensions:
       output += ext + ","
    output += "\n"

    date = startDate
    while date <= endDateInclusive:
        dateExts = {}    # get total extension usages (limited to 1 per extension per commit)

        try:
            commits = getCommitsFromFile(date)
            for commit in commits:
                commitExts = getExtensionsUsedInCommit(commit)
                for ext in commitExts:
                    if not ext in dateExts:
                        dateExts[ext] = 1
                    else:
                        dateExts[ext] += 1

            output += str(date) + ","

            for ext in includeExtensions:
                if ext in dateExts:
                    output += str(dateExts[ext]) + ","
                else:
                    output += "0,"
            output += "\n"

        except FileNotFoundError:
            print(f"No file for {date}")

        date += datetime.timedelta(days=1)

    print(output)

    with open("output.csv", 'w') as outfile:
        outfile.write(output)

if __name__ == '__main__':
    commits = getCommitsFromFile(datetime.date(2017,12,1))
    extensions = getExtensionsUsedInCommit(commits[8])
    print(extensions)
    # print(getExtensionsUsedInCommit(commits[2]))
