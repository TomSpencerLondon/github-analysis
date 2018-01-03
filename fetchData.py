import requests
import datetime
import json
import os
import re
import time
import random
from shared import getCommitSearchFileName
from shared import getSampleCommitsFileName
from shared import findAllCommitSearchResultFilesForDate

DEFAULT_DELAY = 2.03
SAMPLE_COMMITS_PER_PAGE = 10

def saveJSON(filename, data):
    with open (filename, 'w') as outfile:
        json.dump(data, outfile)

def fetch(url, params, custom_headers, returnFunc):
    params["client_id"] = 'ad8123c5877d0fb7ae5a'
    params["client_secret"] = '13d3a67e4c92de09ae5f7553c5acdfd0783eddc3'
    res = requests.get(url, params, headers=custom_headers)
    print(res.url)
    if (res.status_code != 200):
        try:
            res.raise_for_status()
        except requests.HTTPError as ex:
            print(ex)
            resetTime = res.headers['X-RateLimit-Reset']
            if resetTime != None:
                print(f"X-RateLimit-Remaining: {res.headers['X-RateLimit-Remaining']}")
                print(f"X-RatLimit-Reset: {datetime.datetime.fromtimestamp(int(resetTime))}")
                print(res.headers)
            raise ex
    return returnFunc(res)

def fetchJSON(url, params, custom_headers):
    return fetch(url, params, custom_headers, lambda res: res.json())

def fetchCommitSearchData(date, page, fetchFunc=fetchJSON):
    url = "https://api.github.com/search/commits"
    params = {"q": "committer-date:" + str(date), "page":str(page)}
    custom_headers = {"Accept":"application/vnd.github.cloak-preview"}
    return fetchFunc(url, params, custom_headers)

def fetchLinkHeader(url, params, custom_headers):
    return fetch(url, params, custom_headers, lambda res: res.links)

def fetchAndSaveCommitSearchData(date, pages):
    for page in pages:
        data = fetchCommitSearchData(date, page)

        filename = getCommitSearchFileName(date, page)

        with open(filename, 'w') as outfile:
            json.dump(data, outfile)

        if DEFAULT_DELAY > 0:
            time.sleep(DEFAULT_DELAY)

def fetchAndSaveCommitSearchDataSamplePages(date):
    sample_size = 34

    links = fetchCommitSearchData(date,1, fetchLinkHeader)
    lastLink = links['last']['url']
    lastPageStr = re.findall('page=[0-9]+', lastLink)[0]
    lastPage = int(re.findall('[0-9]+', lastPageStr)[0])
    print("Last page: " + str(lastPage))

    samplePages = []
    for i in range(1, min(lastPage,sample_size)+1):
        chosenPage = i
        samplePages.append(chosenPage)

    fetchAndSaveCommitSearchData(date, samplePages)


def fetchAndSaveCommitSearchDataSamplePagesForDates(startDate, endDateInclusive):
    date = startDate
    while date <= endDateInclusive:
        fetchAndSaveCommitSearchDataSamplePages(date)
        date += datetime.timedelta(days=1)

def fetchSampleCommits(date):

    print(f"fetchSampleCommits: {date}")
    sampleCommits = []
    filenames = findAllCommitSearchResultFilesForDate(date)
    for filename in filenames:
        with open(filename, 'r') as infile:
            fileContents = infile.read()
        commitSearchDataPage = json.loads(fileContents)

        #Choose several random commit per page
        allCommits = commitSearchDataPage["items"]
        numCommits = len(allCommits)
        if numCommits > 0:
            for i in range(0,SAMPLE_COMMITS_PER_PAGE):
                chosen = allCommits[ random.randint(0,numCommits-1 )]
                url = chosen["url"]
                params = {}
                custom_headers = {}
                data = fetchJSON(url, params, custom_headers)
                sampleCommits.append(data)
    return sampleCommits

def fetchAndSaveSampleCommitsForDates(startDate, endDateInclusive):
    date = startDate
    while date <= endDateInclusive:
        commits = fetchSampleCommits(date)
        with open(getSampleCommitsFileName(date), 'w') as outfile:
            json.dump(commits, outfile)
        date += datetime.timedelta(days=1)


if __name__ == '__main__':
# fetchAndSaveCommitSearchDataSamplePagesForDates(datetime.date(2017,12,8), datetime.date(2017,12,31))
fetchAndSaveSampleCommitsForDates(datetime.date(2017,12,1), datetime.date(2017,12,31))


# result = fetchCommitSearchData(datetime.date(2017,12,1), 1)

# saveJSON("test.json", result)
