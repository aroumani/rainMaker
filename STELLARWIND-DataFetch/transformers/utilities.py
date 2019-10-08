import matplotlib.pyplot as plt
import pandas as pd
from colorama import Fore, Back, Style

def fixOddsStr(odds):
  if (odds == "pk"):
    odds = 0
  return float(odds)


def nonNAdf(df, col):
  res = df[df[col] != 'NA'][col]
  #print res
  if (len(res) == 0):
    return pd.DataFrame(["NAN"])[0]
  #return df[col]
  return res



def createPlots(df):
  fig, axs = plt.subplots(nrows=3, ncols=3)



  #df['vHomeSpreadResult'].value_counts().plot(ax=axs[0, 0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  df['vGameTotalResult'].value_counts().plot(ax=axs[0, 0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  #df['v2hSpreadResult'].value_counts().plot(ax=axs[1,0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  df['v2hTotalResult'].value_counts().plot(ax=axs[1, 0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  df['vegasTotalLineHalftimeMove'].value_counts().plot(ax=axs[0, 1], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  nonNAdf(df, 'secondHalfRevisedDownResult').value_counts().plot(ax=axs[1,1], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'secondHalfRevisedUpResult').value_counts().plot(ax=axs[2, 1], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  df['vegasTotalLineHalftimeMove'].value_counts().plot(ax=axs[0,2], kind='bar')
  nonNAdf(df, 'secondHalfRevisedDownResult').value_counts().plot(ax=axs[1,2], kind='bar')
  nonNAdf(df, 'secondHalfRevisedUpResult').value_counts().plot(ax=axs[2, 2], kind='bar')

  #fig2, axs2 = plt.subplots(nrows=1, ncols=1)

  fig, axs = plt.subplots(2)
  fig.suptitle('Vertically stacked subplots')
  df['revisedAmount'].value_counts().sort_index().plot(ax=axs[0], kind='bar')
  df['revisedGroup'].value_counts().sort_index().plot(ax=axs[1], kind='bar')


  fig, axs = plt.subplots(nrows=4, ncols=5)
  #df['vHomeSpreadResult'].value_counts().plot(ax=axs[0, 0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  #nonNAdf(df, 'revisedGroupOutcomeUnchanged').value_counts().plot(ax=axs[4, 4], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)



  nonNAdf(df, 'revisedGroupOutcomeLower0to3').value_counts().plot(ax=axs[0,0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeLower3to6').value_counts().plot(ax=axs[0, 1], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeLower6to9').value_counts().plot(ax=axs[0, 2], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeLower9to13').value_counts().plot(ax=axs[0, 3], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeLower13').value_counts().plot(ax=axs[0, 4], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  #nonNAdf(df, '').value_counts().plot(ax=axs[1,0], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeLower0to3').value_counts().plot(ax=axs[1,0], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeLower3to6').value_counts().plot(ax=axs[1,1], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeLower6to9').value_counts().plot(ax=axs[1,2], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeLower9to13').value_counts().plot(ax=axs[1,3], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeLower13').value_counts().plot(ax=axs[1,4], kind='bar')




  nonNAdf(df, 'revisedGroupOutcomeHigher0to3').value_counts().plot(ax=axs[2, 0], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeHigher3to6').value_counts().plot(ax=axs[2,1], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeHigher6to9').value_counts().plot(ax=axs[2, 2], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeHigher9to13').value_counts().plot(ax=axs[2, 3], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)
  nonNAdf(df, 'revisedGroupOutcomeHigher13').value_counts().plot(ax=axs[2, 4], kind='pie', autopct='%1.0f%%', pctdistance=1.1, labeldistance=1.2)

  nonNAdf(df, 'revisedGroupOutcomeHigher0to3').value_counts().plot(ax=axs[3,0], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeHigher3to6').value_counts().plot(ax=axs[3,1], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeHigher6to9').value_counts().plot(ax=axs[3,2], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeHigher9to13').value_counts().plot(ax=axs[3,3], kind='bar')
  nonNAdf(df, 'revisedGroupOutcomeHigher13').value_counts().plot(ax=axs[3,4], kind='bar')


def purpPrint(str):
  print Fore.MAGENTA + str + Style.RESET_ALL