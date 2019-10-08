games = [
  {"awayTeam": "BEARS", "homeTeam": "REDSKINS",
  "preGameTotalLine": 42.5, "firstHalfTotal": 31, "secondHalfTotalLine": 19.5},

]

import csv, numpy, dateutil, time
import pandas as pd
import os
import matplotlib.pyplot as plt
from colorama import Fore, Back, Style
from utilities import fixOddsStr, nonNAdf, createPlots, purpPrint
from engine import parseDataToDF, runStrategy

print(Style.RESET_ALL)
###### SHOULD SHOW PLOTS?????
BOOL_PLOT_ON = False

###### SHOULD PRINT DEBUG?????
BOOL_DEBUG_ON = False

###### FILE TO USE?????
FILENAMES = ["nflOdds2019-20a", "nflOdds2018-19", "nflOdds2017-18"]
#FILENAME = "nflOdds2019-20"

FILE_DIR = "./../../DATA/raw/"

#READYSTR = "-READY"
#TARGETFILENAME = FILE_DIR + FILENAME + READYSTR

print Fore.GREEN + "\n====================================================="
print "------------[RUNNING RAINMAKER 2020]-----------------"
print "-----------------------------------------------------"
print(Style.RESET_ALL)

for game in games:

  awayTeam = game['awayTeam']
  homeTeam = game['homeTeam']
  preGameTotalLine = game['preGameTotalLine']
  firstHalfTotal = game['firstHalfTotal']
  secondHalfTotalLine = game['secondHalfTotalLine']
  effectiveGameTotalOfferAtHalftime = firstHalfTotal + secondHalfTotalLine

  revisionDelta = effectiveGameTotalOfferAtHalftime - preGameTotalLine

  purpPrint("========================================================")
  print "     " + awayTeam + "  VS   " + homeTeam           +   ""
  print "| Team 1st Half Total is    |     " + str(firstHalfTotal) + "              |"
  print "| Vegas Pre Game Total was  |     " + str(preGameTotalLine) + "            |"
  print "---------------------------------------------------"
  print "| Vegas 2nd Half Total Line |     " + str(secondHalfTotalLine) + "              |"
  print "------------------------------------------------------------------------"
  print "| Effective Vegas Offer is Game Total Of            |     " + str(effectiveGameTotalOfferAtHalftime) + "           |"
  print "| This is a change from the start of the game of    |     " + str(revisionDelta) + "          |"
  print "------------------------------------------------------------------------"



  for fileStr in FILENAMES:

    df = parseDataToDF(FILE_DIR + fileStr)

    createPlots(df)
    outcome = runStrategy(revisionDelta, df)

    over = 0
    under = 0
    push = 0

    if 'Over' in outcome:
      over = outcome["Over"]
    if 'Under' in outcome:
      under = outcome["Under"]
    if 'Push' in outcome:
      push = outcome["Push"]

    percOver = 0
    percUnder = 0
    print "Based on: " + Fore.WHITE + fileStr + " " + Style.RESET_ALL + "Over: [" + str(over) + "] Under: [" + str(under) + "] Push: [" + str(push) + "]"
    print '---------'
    print df['favoriteOpenResult'].value_counts()
    print df['favoriteCloseResult'].value_counts()
    print " -----"
    if (over + under + push == 0):
      print "No Data"
    else:
      percOver = float(over) / float(over + push + under)
      percUnder = float(under) / float(over + push + under)

      if (percOver > percUnder):
        print "Goes " + Fore.GREEN + "OVER: " + Style.RESET_ALL +  str(percOver*100) + " percent of the time."
      else:
        print "Goes " + Fore.RED + "UNDER: " + Style.RESET_ALL + str(percUnder*100) + " percent of the time."



    '''if (percOver > 0.56):
      purpPrint('>>>>>>>>>>  Bet the Over [conf: ' + str(percOver) + "]")

    if (percUnder > 0.56):
      purpPrint('>>>>>>>>>>  Bet the Under [conf: ' + str(percUnder) + "]")'''



  purpPrint("========================================================")
# print dataframe.
#print df

if (BOOL_PLOT_ON):
  plt.show()

print(Style.RESET_ALL)






