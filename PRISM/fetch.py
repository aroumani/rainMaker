import requests, csv, numpy, dateutil, time
import pandas as pd
import os

from utils import getStatsForGameByID, saveDataFrame

#https://github.com/seemethere/nba_py/wiki/stats.nba.com-Endpoint-Documentation

FILENAME = "data/nbaFIXED.csv"
#FILENAME2 = "data/nbaTMP2.csv"

def saveCurrent(headers, results):
    newDataFrame = pd.DataFrame(results, columns=headers)
    if (checkIfDataFileExists()):
        oldDataFrame = pd.read_csv(FILENAME)
        newDataFrame = newDataFrame.append(oldDataFrame, ignore_index = True)

    print 'saving to disk'
    saveDataFrame(newDataFrame, FILENAME)

def fetchData():
    
    first = True
    headers = []
    results = []

    chunk = 1

    #for gameNumber in range(2460/2):
    #663 MISSING!!!!!
    #for gameNumber in range(662, 663):
    for gameNumber in range(1108, 2460/2):
        gameIDInt = gameNumber+1
        gameID = "00218" + format(gameIDInt, '05d')
        print 'get stats for: '+ gameID + '[' + str(gameIDInt) + ']'
        gameHeaders, gameResults =  getStatsForGameByID(gameID)
        #pause here to ensure we dont get blocked
        print 'sleep time'
        time.sleep(0.05)
        if (first):
            first = False
            headers = gameHeaders

        results.append(gameResults)

        if (gameIDInt % chunk == 0):
            print 'time to save: ' + str(gameIDInt)
            saveCurrent(headers, results)
            first = True
            headers = []
            results = []

    saveCurrent(headers, results)


def checkIfDataFileExists():
    res = os.path.isfile(FILENAME)
    print res
    return res

print 'Starting Fetch Fetch.py.'
print 'checking if we already have data'

fetchData()

'''if (not checkIfDataFileExists()):
    fetchData()
else:
    print 'We already have saved data'
    #get data from file.'''

print 'Dataframes....'
dataFrame = pd.read_csv(FILENAME)
print dataFrame
print '...................'

    
    
