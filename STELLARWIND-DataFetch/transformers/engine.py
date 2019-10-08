import csv, numpy, dateutil, time
import pandas as pd
from utilities import fixOddsStr, nonNAdf, createPlots


INTERVAL_SIZE = 3
NUM_INTERVALS = 4
groupNum = 0

for i in range(0, NUM_INTERVALS):
  interval = i
  start = interval * INTERVAL_SIZE
  end = start + INTERVAL_SIZE
  groupName = str(groupNum) + ": >" + str(start) + " <= " + str(end)
  print groupName + " = " + str(start) + " to " + str(end)
  groupNum = groupNum+1

#do final tails
maxNum = INTERVAL_SIZE * NUM_INTERVALS
groupName = groupName + " = " + str(maxNum) + " to " + "INF"
print groupName

def parseDataToDF(fullFilePath):
  resultList = []

  #Open file and go through every two lines
  with open(fullFilePath) as f:
      lis = [line.split() for line in f]  # create a list of lists

      for i in range(1, len(lis), 2):
        #print lis[i], " WITH ", lis[i + 1]
        awayResult = lis[i][0].split(",")
        homeResult = lis[i + 1][0].split(",")

        #Ensure we have Home & AWays
        if (awayResult[2] == "N" and homeResult[2] == "N"):
          continue
        assert (awayResult[2] == "V" and homeResult[2] == "H"), ("AWAY:\n"+str(awayResult)) + ("\nHome:\n"+str(homeResult))
        #  0   1   2  3    4   5   6   7    8    9     10  11  12
        #Date,Rot,VH,Team,1st,2nd,3rd,4th,Final,Open,Close,ML,2H
        gameDate = awayResult[0]
        awayTeam = awayResult[3]
        homeTeam = homeResult[3]

        awayOpen = fixOddsStr(awayResult[9])
        awayClose = fixOddsStr(awayResult[10])
        away2H = fixOddsStr(awayResult[12])

        homeOpen = fixOddsStr(homeResult[9])
        homeClose = fixOddsStr(homeResult[10])
        home2H = fixOddsStr(homeResult[12])

        favoriteOpen = -1 * homeOpen
        favoriteClose = -1 * homeClose
        vHomeSpread = -1 * homeClose
        vGameTotal = awayClose
        v2hSpread = -1 * home2H
        v2hTotal = away2H
        isHomeFavoriteOpen = True
        isHomeFavoriteClose = True

        if (awayOpen <= homeOpen):
          #awayIsFavorite
          favoriteOpen = -1 * awayOpen
          isHomeFavoriteOpen=False

        if (awayClose <= homeClose):
          #awayIsFavorite
          vHomeSpread = -1 * awayClose
          vGameTotal = homeClose
          favoriteClose = -1 * awayClose
          isHomeFavoriteClose=False

        if (away2H <= home2H):
          v2hSpread = -1 * away2H
          v2hTotal = home2H




        away1st = int(awayResult[4])
        away2nd = int(awayResult[5])
        away3rd = int(awayResult[6])
        away4th = int(awayResult[7])
        awayOT = int(awayResult[8]) - away1st - away2nd - away3rd - away4th

        home1st = int(homeResult[4])
        home2nd = int(homeResult[5])
        home3rd = int(homeResult[6])
        home4th = int(homeResult[7])
        homeOT = int(homeResult[8]) - home1st - home2nd - home3rd - home4th

        awayFirstHalf = away1st + away2nd
        homeFirstHalf = home1st + home2nd

        awaySecondHalf = away3rd + away4th + awayOT
        homeSecondHalf = home3rd + home4th + homeOT


        secondHalfTotal = awaySecondHalf + homeSecondHalf
        firstHalfTotal = awayFirstHalf + homeFirstHalf

        homeTotal = homeFirstHalf + homeSecondHalf
        awayTotal = awayFirstHalf + awaySecondHalf

        gameTotal = secondHalfTotal + firstHalfTotal

        if isHomeFavoriteOpen:
          if ((homeTotal + favoriteOpen - (awayTotal)) > 0):
            favoriteOpenResult = 'W'
          elif ((homeTotal + favoriteOpen - (awayTotal)) == 0):
            favoriteOpenResult = 'P'
          else:
            favoriteOpenResult = 'L'
        else:
          if ((awayTotal + favoriteOpen - (homeTotal)) > 0):
            favoriteOpenResult = 'W'
          elif ((awayTotal + favoriteOpen - (homeTotal)) == 0):
            favoriteOpenResult = 'P'
          else:
            favoriteOpenResult = 'L'


        if isHomeFavoriteClose:
          if ((homeTotal + favoriteClose - (awayTotal)) > 0):
            favoriteCloseResult = 'W'
          elif ((homeTotal + favoriteClose - (awayTotal)) == 0):
            favoriteCloseResult = 'P'
          else:
            favoriteCloseResult = 'L'
        else:
          if ((awayTotal + favoriteClose - (homeTotal)) > 0):
            favoriteCloseResult = 'W'
          elif ((awayTotal + favoriteClose - (homeTotal)) == 0):
            favoriteCloseResult = 'P'
          else:
            favoriteCloseResult = 'L'




        ####Compute Home Game Spread Result
        if ((homeTotal + vHomeSpread - (awayTotal)) > 0):
          vHomeSpreadResult = 'W'
        elif ((homeTotal + vHomeSpread - (awayTotal)) == 0):
          vHomeSpreadResult = 'P'
        else:
          vHomeSpreadResult = 'L'

        ####Compute Second Half Spread Result
        if ((homeSecondHalf + v2hSpread - awaySecondHalf) > 0):
          v2hSpreadResult = 'W'
        elif ((homeSecondHalf + v2hSpread - awaySecondHalf) == 0):
          v2hSpreadResult = 'P'
        else:
          v2hSpreadResult = 'L'

        ####Compute Second Half Total Result
        if (secondHalfTotal > v2hTotal):
          v2hTotalResult = 'Over'
        elif (secondHalfTotal == v2hTotal):
          v2hTotalResult = 'Push'
        else:
          v2hTotalResult = 'Under'

        ####Compute Game Total Result
        if ((gameTotal - (vGameTotal)) > 0):
          vGameTotalResult = 'Over'
        elif ((gameTotal - (vGameTotal)) == 0):
          vGameTotalResult = 'Push'
        else:
          vGameTotalResult = 'Under'


        secondHalfRevisedDownResult = "NA"
        secondHalfRevisedUpResult = "NA"
        #total line moved down at half
        vegasTotalLineHalftimeMove = "RevisedUp"


        if (vGameTotal > (firstHalfTotal + v2hTotal)):
          #revisedDown
          vegasTotalLineHalftimeMove = "RevisedDown"
          secondHalfRevisedDownResult = v2hTotalResult
        elif (vGameTotal == (firstHalfTotal + v2hTotal)):
          vegasTotalLineHalftimeMove = "SAME AS START"
        else:
          #revisedUp
          secondHalfRevisedUpResult=v2hTotalResult

        revisedAmount = (firstHalfTotal + v2hTotal) - vGameTotal

        revisedGroupOutcomeLower0to3 = "NA"
        revisedGroupOutcomeLower3to6 = "NA"
        revisedGroupOutcomeLower6to9 = "NA"
        revisedGroupOutcomeLower9to13 = "NA"
        revisedGroupOutcomeLower13 = "NA"

        revisedGroupOutcomeHigher0to3 = "NA"
        revisedGroupOutcomeHigher3to6 = "NA"
        revisedGroupOutcomeHigher6to9 = "NA"
        revisedGroupOutcomeHigher9to13 = "NA"
        revisedGroupOutcomeHigher13 = "NA"

        revisedGroupOutcomeUnchanged = "NA"


        strategyOutcome = "NA"

        if (revisedAmount < 0 and revisedAmount >= -3):
          revisedGroup = "e-0.5 to -3.0"
          revisedGroupOutcomeLower0to3 = v2hTotalResult

        elif (revisedAmount < -3 and revisedAmount >= -6):
          revisedGroup = "d-3.5 to -6"
          revisedGroupOutcomeLower3to6 = v2hTotalResult

        elif (revisedAmount < -6 and revisedAmount >= -9):
          revisedGroup = "c-6.5 to -9"
          revisedGroupOutcomeLower6to9 = v2hTotalResult

        elif (revisedAmount < -9 and revisedAmount >= -13):
          revisedGroup = "b-9.5 to -13"
          revisedGroupOutcomeLower9to13 = v2hTotalResult

        elif (revisedAmount < -13):
          revisedGroup = "a-13.5 - lower"
          revisedGroupOutcomeLower13 = v2hTotalResult


        if (revisedAmount > 0 and revisedAmount <= 3):
          revisedGroup = "g0.5 to 3.0"
          revisedGroupOutcomeHigher0to3 = v2hTotalResult

        elif (revisedAmount > 3 and revisedAmount <= 6):
          revisedGroup = "h3.5 to 6"
          revisedGroupOutcomeHigher3to6 = v2hTotalResult

        elif (revisedAmount > 6 and revisedAmount <= 9):
          revisedGroup = "i6.5 to 9"
          revisedGroupOutcomeHigher6to9 = v2hTotalResult

        elif (revisedAmount > 9 and revisedAmount <= 13):
          revisedGroup = "j9.5 to 13"
          revisedGroupOutcomeHigher9to13 = v2hTotalResult

        elif (revisedAmount > 13):
          revisedGroup = "k13.5 - HIGHER"
          revisedGroupOutcomeHigher13 = v2hTotalResult


        if (revisedAmount == 0):
          revisedGroup = "fUnchanged"
          revisedGroupOutcomeUnchanged = v2hTotalResult



        resultList.append([gameDate, awayTeam, homeTeam, vHomeSpread, vGameTotal,
        away1st, home1st, away2nd, home2nd, v2hSpread, v2hTotal,
        v2hSpreadResult, v2hTotalResult, vHomeSpreadResult, vGameTotalResult,
        vegasTotalLineHalftimeMove, secondHalfRevisedDownResult, secondHalfRevisedUpResult,
        revisedAmount, revisedGroup,

        revisedGroupOutcomeLower0to3, revisedGroupOutcomeLower3to6, revisedGroupOutcomeLower6to9,
        revisedGroupOutcomeLower9to13, revisedGroupOutcomeLower13,

        revisedGroupOutcomeHigher0to3, revisedGroupOutcomeHigher3to6, revisedGroupOutcomeHigher6to9,
        revisedGroupOutcomeHigher9to13, revisedGroupOutcomeHigher13,

        revisedGroupOutcomeUnchanged,

        favoriteOpen, favoriteClose,
        favoriteOpenResult, favoriteCloseResult])


  # initialize list of lists
  data = resultList

  # Create the pandas DataFrame
  df = pd.DataFrame(resultList, columns=[
  'gameDate', 'awayTeam', 'homeTeam',
  'vHomeSpread', 'vGameTotal',
  'away1st', 'home1st', 'away2nd', 'home2nd',
  'v2hSpread', 'v2hTotal',
  'v2hSpreadResult', 'v2hTotalResult', 'vHomeSpreadResult', 'vGameTotalResult',
  'vegasTotalLineHalftimeMove', 'secondHalfRevisedDownResult', 'secondHalfRevisedUpResult',
  'revisedAmount', 'revisedGroup',

  'revisedGroupOutcomeLower0to3', 'revisedGroupOutcomeLower3to6', 'revisedGroupOutcomeLower6to9',
  'revisedGroupOutcomeLower9to13', 'revisedGroupOutcomeLower13',

  'revisedGroupOutcomeHigher0to3', 'revisedGroupOutcomeHigher3to6', 'revisedGroupOutcomeHigher6to9',
  'revisedGroupOutcomeHigher9to13', 'revisedGroupOutcomeHigher13',

  'revisedGroupOutcomeUnchanged',

  'favoriteOpen', 'favoriteClose',
  'favoriteOpenResult', 'favoriteCloseResult'])

  return df


def runStrategy(revisionDelta, df):


  if (revisionDelta < 0 and revisionDelta >= -3):
    return nonNAdf(df, 'revisedGroupOutcomeLower0to3').value_counts()

  elif (revisionDelta < -3 and revisionDelta >= -6):
    return nonNAdf(df, 'revisedGroupOutcomeLower3to6').value_counts()

  elif (revisionDelta < -6 and revisionDelta >= -9):
    return nonNAdf(df, 'revisedGroupOutcomeLower6to9').value_counts()

  elif (revisionDelta < -9 and revisionDelta >= -13):
    return nonNAdf(df, 'revisedGroupOutcomeLower9to13').value_counts()

  elif (revisionDelta < -13):
    return nonNAdf(df, 'revisedGroupOutcomeLower13').value_counts()


  if (revisionDelta > 0 and revisionDelta <= 3):
    return nonNAdf(df, 'revisedGroupOutcomeHigher0to3').value_counts()

  elif (revisionDelta > 3 and revisionDelta <= 6):
    return nonNAdf(df, 'revisedGroupOutcomeHigher3to6').value_counts()

  elif (revisionDelta > 6 and revisionDelta <= 9):
    return nonNAdf(df, 'revisedGroupOutcomeHigher6to9').value_counts()

  elif (revisionDelta > 9 and revisionDelta <= 13):
    return nonNAdf(df, 'revisedGroupOutcomeHigher9to13').value_counts()

  elif (revisionDelta > 13):
    return nonNAdf(df, 'revisedGroupOutcomeHigher13').value_counts()


  if (revisionDelta == 0):
    return nonNAdf(df, 'revisedGroupOutcomeUnchanged').value_counts()


