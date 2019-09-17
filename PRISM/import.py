import requests, csv, numpy, dateutil, time
import pandas as pd
import os

from utils import getStatsForGameByID, saveDataFrame, massageCityNames

TOTALS_FILENAME = "data/nba_odds_18.csv"
GAMES_FILENAME = "data/nba_stats18.csv"

FIXED_FILENAME = "data/nba_fullSeason.csv"

totalsDataFrame = pd.read_csv(TOTALS_FILENAME)
gamesDataFrame = pd.read_csv(GAMES_FILENAME)

#print totalsDataFrame.describe()
#print gamesDataFrame.describe()

print '---------'
print gamesDataFrame.head()
gamesDataFrame=gamesDataFrame.sort_values(by='AWAY_GAME_ID', ascending=True)
gamesDataFrame=gamesDataFrame.reset_index(drop=True)
#print gamesDataFrame.head()
print '-----------------------'
print '-----------------------'
print '---------RUNNING--------------'
print '-----------------------'
print '-----------------------'

totalsDict = {}

for gameIndex in range(len(totalsDataFrame)/2):
    totalIndex = gameIndex*2
    awayLine = totalsDataFrame.ix[totalIndex]
    homeLine = totalsDataFrame.ix[totalIndex+1]

    awayTeam = awayLine['Team'].replace(" ", "")
    homeTeam = homeLine['Team'].replace(" ", "")

    awayDate = awayLine['Date']
    homeDate = awayLine['Date']

    awayFirst = int(awayLine['1st'])
    homeFirst = int(homeLine['1st'])

    awaySecond = int(awayLine['2nd'])
    homeSecond = int(homeLine['2nd'])

    awayThird = int(awayLine['3rd'])
    homeThird = int(homeLine['3rd'])

    awayForth = int(awayLine['4th'])
    homeForth = int(homeLine['4th'])

    away2HFinal = int(awayLine['Final']) - awayFirst - awaySecond
    home2HFinal = int(homeLine['Final']) - homeFirst - homeSecond

    firstHalfTotal = awayFirst + homeFirst + awaySecond + homeSecond
    secondHalfTotal = away2HFinal + home2HFinal

    sortedTeam = [massageCityNames(awayTeam), massageCityNames(homeTeam)]
    sortedTeam.sort()

    key = str(sortedTeam) + "-" + str(firstHalfTotal) + "-" + str(secondHalfTotal)

    awayCloseGame = awayLine['Close']
    homeCloseGame = homeLine['Close']

    awayClose2H = awayLine['2H']
    homeClose2H = homeLine['2H']

    if str(awayCloseGame).lower().startswith("pk"):
        awayCloseGame=0

    if str(homeCloseGame).lower().startswith("pk"):
        homeCloseGame=0

    if str(awayClose2H).lower().startswith("pk"):
        awayClose2H=0

    if str(homeClose2H).lower().startswith("pk"):
        homeClose2H=0

    #print homeCloseGame

    

    print '============CLOSE==========='
    #print awayCloseGame
    #print homeCloseGame
    closeGameFloat = max(float(awayCloseGame), float(homeCloseGame))
    #print closeGameFloat
    #print '==========================='
    close2H = max(float(awayClose2H), float(homeClose2H))
    totalsDict[key]=[closeGameFloat, close2H]


print '----------------'
print '----------------'
print '----------------'

#AWAY_TEAM_CITY
#HOME_TEAM_CITY
#1ST_HALF_TOTAL
#2ND_HALF_TOTAL

#print totalsDict

LV_TOTAL = "LV_TOTAL"
LV_2H = "LV_2H"
first = True

for gameIndex in range(len(gamesDataFrame)):
    game = gamesDataFrame.ix[gameIndex]
    #print 'processing game# ' + str(game)
    
    awayTeam = game['AWAY_TEAM_CITY'].replace(" ", "")
    homeTeam = game['HOME_TEAM_CITY'].replace(" ", "")
    firstHalfTotal = game['1ST_HALF_TOTAL']
    secondHalfTotal = game['2ND_HALF_TOTAL']
    
    gameID = str(game['AWAY_GAME_ID'])

    if gameID in ["21800417", "21800523", "21800534", "21800681", "21800699", "21800748", "21800823", "21800828"]:
        firstHalfTotal -= 1
        secondHalfTotal += 1

    if gameID in ["21801130"]:
        firstHalfTotal -= 2
        secondHalfTotal += 2


    sortedTeam = [awayTeam, homeTeam]
    sortedTeam.sort()



    key = str(sortedTeam) + "-" + str(firstHalfTotal) + "-" + str(secondHalfTotal)

    if key not in totalsDict:
        print 'GAME NOT MATCHGED!' + key + ' --> ' + str(gameID)

    print '==========Set================'
    #print key
    #print totalsDict[key][0]
    gamesDataFrame.at[gameIndex,LV_TOTAL] = totalsDict[key][0]
    print key
    print totalsDict[key]
    gamesDataFrame.at[gameIndex,LV_2H] = totalsDict[key][1]
    #game[LV_TOTAL] = totalsDict[key][0]
    #game[LV_2H] = totalsDict[key][1]
        
    
print gamesDataFrame.head()
print gamesDataFrame.describe()

print 'Saving...'
saveDataFrame(gamesDataFrame, FIXED_FILENAME)
print 'Save complete!'

