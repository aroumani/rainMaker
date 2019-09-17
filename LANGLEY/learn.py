import xgboost as xgb
import matplotlib.pyplot as plt
from sklearn.metrics import mean_squared_error
import numpy as np
import requests, csv, dateutil, time
import pandas as pd
from sklearn.model_selection import train_test_split
#from sklearn import cross_validation
#from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.model_selection import RandomizedSearchCV,GridSearchCV

IS_DEBUG = True
FILENAME = "../data/nfl.csv"
fullDataSet = pd.read_csv(FILENAME)


def printMsg(msg):
    if (IS_DEBUG):
        print msg



fullDataSet.sort_values("AWAY_GAME_ID", axis = 0, ascending = True,  inplace = True, na_position ='last')


#print data

data = fullDataSet.drop([
                'AWAY_GAME_ID', 'AWAY_TEAM_ID', 
                'AWAY_TEAM_NAME', 'AWAY_TEAM_ABBREVIATION',
                'AWAY_TEAM_CITY', 'AWAY_MIN',
                'HOME_GAME_ID', 'HOME_TEAM_ID', 
                'HOME_TEAM_NAME', 'HOME_TEAM_ABBREVIATION',
                'HOME_TEAM_CITY', 'HOME_MIN', 
                'AWAY_2H_TOTAL','HOME_2H_TOTAL',
                'AWAY_FT_PCT', 'HOME_FT_PCT',
                'AWAY_REB', 'HOME_REB', 
                'AWAY_FGM','HOME_FGM',
                'AWAY_DREB','HOME_DREB',
                'AWAY_AST','HOME_AST',
                'AWAY_FTA','HOME_FTA',
                'AWAY_FG_PCT', 'HOME_FG_PCT',
                'AWAY_FG3_PCT', 'HOME_FG3_PCT',
                'AWAY_FG3M','HOME_FG3M',
                'AWAY_PLUS_MINUS','HOME_PLUS_MINUS',
                'AWAY_STL', 'HOME_STL',
                'AWAY_FTM','HOME_FTM',
                '1ST_HALF_TOTAL',
                'AWAY_BLK','HOME_BLK',
                'AWAY_OREB','HOME_OREB',
                'AWAY_FGM','HOME_FGM',
                'AWAY_FGA','HOME_FGA',
                'AWAY_FG3A','HOME_FG3A',
                ], axis=1)
'''
'AWAY_PTS','HOME_PTS',
'AWAY_TO','HOME_TO',
'AWAY_PF','HOME_PF',
'LV_2H',
'LV_TOTAL',
'2ND_HALF_TOTAL',
'''

'''#data['AWAY_PLUS_MINUS'] = data['AWAY_PLUS_MINUS']*data['AWAY_PLUS_MINUS']
#otherScores = data['2ND_HALF_TOTAL']
#data.insert(1, 'OTHER_SCOERS', otherScores)
#otherScores = (data['2ND_HALF_TOTAL'] * 0) * 2
#data.insert(0, 'AWAY_MIN', otherScores)
data['COMBINED_FGA'] = data['HOME_FGA'] + data['AWAY_FGA']
data = data.drop("AWAY_FGA",axis=1)
data = data.drop("HOME_FGA",axis=1)'''
'''data['COMBINED_PF'] = data['AWAY_PF'] + data['HOME_PF']
data = data.drop("AWAY_PF",axis=1)
data = data.drop("HOME_PF",axis=1)'''

printMsg('-==========================')
printMsg('-==========RUNNING LANGLEY ML SUITE================')
printMsg('-==========================')
printMsg('-==========Dataframe head()================')
printMsg(data.head())
printMsg('-==========Dataframe info()================')
#printMsg(data.info())
printMsg('-==========Dataframe describe()================')
printMsg(data.describe())
printMsg('-==========SPLIT INTO TEST + TRAINING DATA================')


TRAIN_START_POS = 0
TRAIN_END_POS = 1000
TEST_START_POS = TRAIN_END_POS
TEST_END_POS = len(data)

train = data[TRAIN_START_POS:TRAIN_END_POS]
test = data[TEST_START_POS:TEST_END_POS]

#Removing TARGET Column
y_train = train["2ND_HALF_TOTAL"].values
X_train = train.drop("2ND_HALF_TOTAL",axis=1).values

y_test = test["2ND_HALF_TOTAL"].values
X_test =test.drop("2ND_HALF_TOTAL",axis=1).values

'''printMsg('-==========Training Input Data================')
#print X_train
print ' '
print '-==========Training Target Data================'
#print y_train
print ' '
print '-==========Test Input Data================'
#print X_test
print ' '
print '-==========Test Target Data================'
#print y_test
print ' '
'''

################################
# TRAINING...
################################
################################
# Various hyper-parameters to tune
xgb1 = xgb.XGBRegressor()
parameters = {'nthread':[4], #when use hyperthread, xgboost may become slower
              'objective':['reg:linear'],
              'learning_rate': [.03, 0.05, .07], #so called `eta` value
              'max_depth': [5, 6, 7],
              'min_child_weight': [4],
              'silent': [0],
              'subsample': [0.7],
              'colsample_bytree': [0.7],
              'n_estimators': [500]}

'''xgb_grid = GridSearchCV(xgb1,
                        parameters,
                        cv = 2,
                        n_jobs = 5,
                        verbose=True)

xgb_grid.fit(X_train,
         y_train)

print(xgb_grid.best_score_)
print(xgb_grid.best_params_)'''

#############################
#############################

'''gbm = xgb.XGBRegressor()

print '-----------------------------------'
print '-------------GSEARCH--------------'
print '-----------------------------------'

reg_cv = GridSearchCV(gbm, {"colsample_bytree":[1.0],"min_child_weight":[1.0,1.2]
                            ,'max_depth': [3,4,6], 'n_estimators': [500,1000]}, verbose=1)

print '-----------------------------------'
print '-------------FITTING CV--------------'
print '-----------------------------------'
reg_cv.fit(X_train,y_train)

print '-----------------------------------'
print '-------------Best Params--------------'
print '-----------------------------------'
reg_cv.best_params_


print '-----------------------------------'
print '-------------PRITN Best Params--------------'
print '-----------------------------------'
print reg_cv.best_params_

print '-----------------------------------'
print '-------------GBM REGSSOR--------------'
print '-----------------------------------'
'''

printMsg('-==========TRAINING MODEL================')

bestParams = {'n_estimators': 1500, 'booster':'gbtree', 'colsample_bytree': 1, 'max_depth': 15, 'min_child_weight': 1.0, "eta": 0.50}
gbm = xgb.XGBRegressor(**bestParams)
#gbm = xgb.XGBRegressor(**xgb_grid.best_params_)

#FIT DATA
gbm.fit(X_train,y_train)






printMsg('-==========Predict on TEST DATA================')
predictions = gbm.predict(X_test)
#print predictions

printMsg('-------------GBM.SCORE() ob TRAIN DATA------------')
printMsg(gbm.score(X_train,y_train))
printMsg('-----------------------------------')

printMsg('-------------GBM.SCORE() ob TEST DATA------------')
printMsg(gbm.score(X_test,y_test))
printMsg('-----------------------------------')



featureDataFrame = data.drop("2ND_HALF_TOTAL",axis=1)

for col,score in zip(featureDataFrame.columns, gbm.feature_importances_):
    printMsg(str(col) + " - " + str(score))


plt.rcParams["figure.figsize"] = (8, 8)

# create the plot space upon which to plot the data
fig, ax = plt.subplots()

# add the x-axis and the y-axis to the plot

colNames = featureDataFrame.columns.values
#xn = range(len(colNames))
ind = np.arange(len(colNames)) 

#print gbm.booster
#weightDict = gbm.get_booster().get_score(importance_type='total_gain')
gainDict = gbm.get_booster().get_score(importance_type='gain')

#gainDict = gbm.get_score(importance_type='gain')

#print gainDict.values()
gainNP = np.array(gainDict.values())

width = 0.3

ax.bar(ind, gainNP, width, label='GAIN', color='green')


#ax.bar(ind+ width, weightDict.values(), width, label='TOTAL GAIN', color='black')
#ax.bar(ind+width+width, gbm.feature_importances_ * 10000, width, label='FI10K', color='blue')


plt.xticks(range(len(colNames)), colNames, rotation='vertical', fontsize='13')
plt.legend(loc='best')


'''feature_important = gbm.get_booster().get_score(importance_type='weight')
keys = list(feature_important.keys())
values = list(feature_important.values())

data = pd.DataFrame(data=values, index=keys, columns=["score"]).sort_values(by = "score", ascending=False)
data.plot(kind='barh')'''

#fig, ax = plt.subplots(1,1,figsize=(10,10))

#xgb.plot_importance(gbm.get_booster(), ax=ax)



'''fig = plt.figure(dpi=1000)
ax = plt.subplot(100,100,100)
xgb.plot_tree(gbm , ax = ax)
 
plt.tight_layout()
plt.show()'''


printMsg('---------------Langley MAE-----------------')
maeArr =[]
sumDelta = 0
for result, game in zip(y_test, X_test):
    prediction = gbm.predict([game])
    delta = abs(result - prediction)
    maeArr.append(delta)
    sumDelta += delta
    #print str(result) + "vs [" + str(prediction) + "] = " + str(delta)

mae = sumDelta / len(y_test)
printMsg('MAE = ' + str(mae))
deltaDataFrame = pd.DataFrame(maeArr, columns=['MAE'])
printMsg(deltaDataFrame.describe())

printMsg('---------------Vegas MAE-----------------')
maeArr =[]
sumDelta = 0
for result, vegas2H in zip(y_test, list(fullDataSet[TEST_START_POS:TEST_END_POS]['LV_2H'])):
    delta = abs(result - vegas2H)
    maeArr.append(delta)
    sumDelta += delta
    #print str(result) + "vs [" + str(prediction) + "] = " + str(delta)

mae = sumDelta / len(y_test)
printMsg('VEGAS MAE = ' + str(mae))
deltaDataFrame = pd.DataFrame(maeArr, columns=['MAE'])
printMsg(deltaDataFrame.describe())
printMsg(' ')


printMsg('---------------LANGLEY O/U-----------------')
maeArr =[]
sumDelta = 0
overs = 0
unders = 0
push = 0
for result, game in zip(y_test, X_test):
    prediction = gbm.predict([game])
    if (result - prediction > 0):
        delta = -1
        unders += 1
    elif (result -prediction == 0):
        delta = 0
        push += 1
    else:
        delta = 1
        overs += 1
    maeArr.append(delta)
    sumDelta += delta
    #print str(result) + "vs [" + str(prediction) + "] = " + str(delta)

numGames = len(y_test)
mae = sumDelta / numGames
printMsg('LANGLEY O/U = ' + str(mae))
printMsg(str(overs) + " - OVERS [" + str(float(overs)/numGames) + "] " + str(unders) + " - UNDERS[" + str(float(unders)/numGames) + "] " + str(push) + " - PUSHES[" + str(float(push)/numGames) + "]")
deltaDataFrame = pd.DataFrame(maeArr, columns=['O/U'])
#print deltaDataFrame.describe()
printMsg(' ')

printMsg('---------------Vegas O/U-----------------')
maeArr =[]
sumDelta = 0
overs = 0
unders = 0
push = 0
for result, vegas2H in zip(y_test, list(fullDataSet[TEST_START_POS:TEST_END_POS]['LV_2H'])):
    if (result - vegas2H > 0):
        delta = -1
        unders += 1
    elif (result -vegas2H == 0):
        delta = 0
        push += 1
    else:
        delta = 1
        overs += 1
    maeArr.append(delta)
    sumDelta += delta
    #print str(result) + "vs [" + str(prediction) + "] = " + str(delta)

numGames = len(y_test)
mae = sumDelta / numGames
printMsg('VEGAS O/U = ' + str(mae))
printMsg(str(overs) + " - OVERS [" + str(float(overs)/numGames) + "] " + str(unders) + " - UNDERS[" + str(float(unders)/numGames) + "] " + str(push) + " - PUSHES[" + str(float(push)/numGames) + "]")
deltaDataFrame = pd.DataFrame(maeArr, columns=['O/U'])
#print deltaDataFrame.describe()
printMsg(' ')


printMsg('---------------LANGLEY VS VEGAS----------------')
maeArr =[]
sumDelta = 0
right = 0
wrong = 0
push = 0
for result, game, vegas2H in zip(y_test, X_test, list(fullDataSet[TEST_START_POS:TEST_END_POS]['LV_2H'])):
    
    prediction = gbm.predict([game])

    vegasDelta = (result - vegas2H)

    langleyDelta = (result - prediction)

    #print str(prediction) + " VS " + str(vegas2H)
    delta = (langleyDelta - vegas2H)

    betOver=(prediction >= vegas2H)

    if (vegasDelta > 0): #GAME WENT OVER
        if (betOver):
            right += 1
        else:
            wrong += 1

    elif (vegasDelta < 0): #GAME WENT OVER
        if (not betOver):
            right += 1
        else:
            wrong += 1

    else: #GAME PUSHED
        push += 1

    maeArr.append(delta)
    sumDelta += delta
    #print str(result) + "vs [" + str(prediction) + "] = " + str(delta)

numGames = len(y_test)
mae = sumDelta / numGames
printMsg( 'LANGLEY vs VEGAS = ' + str(mae))
printMsg( str(right) + " - RIGHT [" + str(float(right)/numGames) + "] " + str(wrong) + " - WRONG[" + str(float(wrong)/numGames) + "] " + str(push) + " - PUSHES[" + str(float(push)/numGames) + "]")
deltaDataFrame = pd.DataFrame(maeArr, columns=['LANG vs VEGAS'])
#print deltaDataFrame.describe()
printMsg( ' ')

printMsg( '-==========COMPLETED LANGLEY ML SUITE================')
printMsg( '-==========================')
#plt.show()


