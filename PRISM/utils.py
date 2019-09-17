import requests, csv, numpy, dateutil
import pandas as pd
import os

def getStatsForGameByID(gameID):
  # get cols, awayTeam, homeTeam
    awayHeaders1H, homeHeaders1H, away1H, home1H = getStatsByRange(gameID, "0", "14400")
    awayHeaders2H, homeHeaders2H, away2H, home2H = getStatsByRange(gameID, "14401", "68800")

    away1Hscore = away1H[len(away1H)-2]
    home1Hscore = home1H[len(home1H)-2]

    away2Hscore = away2H[len(away2H)-2]
    home2Hscore = home2H[len(home2H)-2]

    awayHeaders1H.append("AWAY_2H_TOTAL")
    homeHeaders1H.append("HOME_2H_TOTAL")
    away1H.append(away2Hscore)
    home1H.append(home2Hscore)

    headers = awayHeaders1H + homeHeaders1H + ["1ST_HALF_TOTAL"] + ["2ND_HALF_TOTAL"]
    results = away1H + home1H + [int(away1Hscore) + int(home1Hscore)] + [int(away2Hscore) + int(home2Hscore)]
    return headers, results

def getStatsByRange(gameID, startRange, endRange):
    headers = {
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    URLSTR = 'https://stats.nba.com/stats/boxscoretraditionalv2?EndPeriod=10&EndRange='+endRange+'&GameID='+gameID+'&RangeType=2&Season=2018-19&SeasonType=Regular+Season&StartPeriod=1&StartRange='+startRange+''
    #print URLSTR
    reqHalf = requests.get(URLSTR
    , timeout=10, verify=True, headers=headers)
    halfBoxScoreJSON = reqHalf.json()
    halfResultSets = halfBoxScoreJSON.get('resultSets')
    halfTeamStatList = []
    for stat in halfResultSets: 
        name = stat.get('name')
        #print(name)
        if name == "TeamStats" :
            rowSet = name = stat.get('rowSet')
            uniHeaders = stat.get('headers')
            homeHeaders=["HOME_"+str(i) for i in uniHeaders]
            awayHeaders=["AWAY_"+str(i) for i in uniHeaders]
            uniAwayStats = rowSet[0]
            awayStats=[str(i) for i in uniAwayStats] 
            uniHomeStats = rowSet[1]
            homeStats=[str(i) for i in uniHomeStats] 
            return awayHeaders, homeHeaders, awayStats, homeStats
  


def saveDataFrame(dataFrame, filename):
    dataFrame.to_csv(filename, encoding='utf-8', index=False)

def massageCityNames(cityName):
    if cityName == "LALakers":
        return "LosAngeles"
    elif cityName == "LAClippers":
        return "LA"
    return cityName

'''dataFrame = pd.DataFrame(halfTeamStatList, columns=headers)
print dataFrame'''

'''
mylist = ['foo', 'bar', 'baz']
with open('myfile.csv', 'w') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(['Header1', 'Header2', 'Header3'])
    csvwriter.writerow(teamStatList)
'''

    
    
