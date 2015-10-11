import os, re, time, math
import pandas as pd
import numpy as np
import pylab as plt
from datetime import datetime
from dateutil.parser import parse
from scipy import interp
from scipy.optimize import curve_fit as cf
from datetime import timedelta

mvaperiod = 20

#timeCutoff = datetime(2015,8,1,14)
#timeCutoff = (timeCutoff - datetime(1970,1,1)).total_seconds()

def func(x, a, b, c):
    return np.power(x,3)*a + np.power(x,2)*b + x*c
    
def deg2func(x, a, b, c):
    return np.power(x,2)*a + x*b + c
    
def expfunc(x, a, b):
    return np.exp(a*x)*b
    
def linearfunc(x, a):
    return a*x

plt.style.use('dark_background')

# data from room in 93 ridgeview
#arduinoDataFile = '2015-08-06 21-14-21 arduino data.csv'
#dylosDataFile = '2015-08-06 21-15-04 dylos data.csv'

# for loading multiple files and joining them

firstArduinoFile = False
firstdylosFile = False
day = 17
corrFiles = os.listdir('correlation data')
arduinoFiles = []
dylosFiles = []
# for joining many files from the same day
'''for file in corrFiles:
    print os.path.isfile(os.getcwd() + '\\correlation data\\' + file)
    if os.path.isfile(os.getcwd() + '\\correlation data\\' + file):
        print file
        if re.search('2015-08-' + str(day), file):
            print file
            if re.search('arduino', file):
                arduinoFiles.append(pd.read_csv(os.getcwd() + '\\correlation data\\' + file))
            if re.search('dylos', file):
                dylosFiles.append(pd.read_csv(os.getcwd() + '\\correlation data\\' + file))
                
arduinoData = pd.concat(arduinoFiles)
dylosData = pd.concat(dylosFiles)
'''
'''frames = [dylosData, pd.DataFrame(data=interpArduinoData, columns=['1um arduino']), pd.DataFrame(data=interpArduinoRatio, columns=['arduino P1 ratio'])]
result = pd.concat(frames,axis=1)
result.to_csv(path_or_buf='concatd data - 2015-08-' + day + '.csv', index=False)'''

# for loading 2 single files
arduinoDataFile = 'correlation data/2015-09-21 15-31-39 arduino data.csv'
dylosDataFile = 'correlation data/2015-09-21 15-31-37 dylos data.csv'

arduinoData = pd.read_csv(arduinoDataFile)
rawRollingArduinoP1Ratio = pd.rolling_mean(np.array(arduinoData['P1 ratio']), 2)
rawRollingArduinoP2Ratio = pd.rolling_mean(np.array(arduinoData['P2 ratio']), 2)
for each in range(len(rawRollingArduinoP1Ratio)):
    print rawRollingArduinoP1Ratio[each], arduinoData['P1 ratio'][each]
    if math.isnan(rawRollingArduinoP1Ratio[each]):
        rawRollingArduinoP1Ratio[each]=arduinoData['P1 ratio'][each]
        rawRollingArduinoP2Ratio[each]=arduinoData['P2 ratio'][each]
        print rawRollingArduinoP1Ratio[each]
dylosData = pd.read_csv(dylosDataFile)

arduinoTime = [(parse(eachTime) - datetime(1970, 1, 1)).total_seconds() for eachTime in arduinoData['time (iso)']]
dylosTime = [(parse(eachTime) - datetime(1970, 1, 1)).total_seconds() for eachTime in dylosData['time (iso)']]

interpArduinoTime = interp(dylosTime, arduinoTime, arduinoTime)#arduinoData['1um'])
interpArduinoP1Ratio = interp(dylosTime, arduinoTime, rawRollingArduinoP1Ratio)  
interpArduinoP2Ratio = interp(dylosTime, arduinoTime, rawRollingArduinoP2Ratio)
rollingArduinoP1Ratio = pd.rolling_mean(np.array(interpArduinoP1Ratio), 20)
rollingArduinoP2Ratio = pd.rolling_mean(np.array(interpArduinoP2Ratio), 20)

### fitting and plotting

xData = interpArduinoP1Ratio
yData = dylosData['1um']

# fitting data

# linear, assumes intercept is 0
fitLineX = np.linspace(min(xData), max(xData), 1000)
linearpopt, linearpcov = cf(linearfunc, xData, yData)
print 'linear: ',linearpopt
fitLineYlinear = linearfunc(fitLineX, linearpopt[0])

# 2nd degree
fitLineX = np.linspace(min(xData), max(xData), 1000)
deg2popt, deg2pcov = cf(deg2func, xData, yData)
print '2nd degree: ', deg2popt
fitLineY2nd = deg2func(fitLineX, deg2popt[0], deg2popt[1], deg2popt[2])

# plotting
plt.scatter(xData, yData)
plt.plot(fitLineX, fitLineYlinear, linewidth=3, label='linear')
plt.plot(fitLineX, fitLineY2nd, linewidth=3, label='2nd degree')
plt.legend()
plt.xlabel('DSM501A P1 ratio')
plt.ylabel('Dylos DC1100 Pro 1um count')
#plt.plot(allData.index, rollingP1ratio, label='mva', c='orange', linewidth=3)
curFig = plt.gcf()
plt.savefig('corr',facecolor=curFig.get_facecolor())
plt.show()

plt.close()

plt.scatter(arduinoTime, arduinoData['P1 ratio'])
plt.plot(arduinoTime, pd.rolling_mean(arduinoData['P1 ratio'], 6), label='6-period moving average')
plt.xlabel('time')
plt.ylabel('DSM501A P1 ratio')
curFig = plt.gcf()
plt.savefig('ard over time',facecolor=curFig.get_facecolor())
plt.show()

plt.plot(arduinoTime, np.power(arduinoData['P1 ratio'],2)*deg2popt[0] + arduinoData['P1 ratio']*deg2popt[1] + deg2popt[2], label = 'dsm501a')
plt.plot(dylosTime, dylosData['1um'], label = 'dylos')
plt.xlabel('time')
plt.ylabel('1um counts')
plt.legend()
curFig = plt.gcf()
plt.savefig('compare',facecolor=curFig.get_facecolor())
plt.show()

'''
interpTimes = []
dylos1umData = []
arduinoP1ratio = []
arduinoP2ratio = []
for each in range(len(interpArduinoTime) - mvaperiod):
    #print dylosTime[each], timeMax
    if dylosTime[each] == interpArduinoTime[each]:# and dylosTime[each] > timeMin and dylosTime[each] < timeMax:
        interpTimes.append(datetime.fromtimestamp(dylosTime[each]) - timedelta(hours=-4)) # -6 for west coast time, -4 for central
        datetime.fromtimestamp(dylosTime[each]) - timedelta(hours=-4)
        print datetime.fromtimestamp(dylosTime[each]) - timedelta(hours=-4)
        dylos1umData.append(dylosData['1um'][each])
        arduino1umData.append(interpArduinoData[each]*2.5)
        arduinoP1ratio.append(interpArduinoRatio[each])
rollingP1ratio = pd.rolling_mean(np.array(arduinoP1ratio), 20)
for each in range(len(rollingP1ratio)):
    if np.isnan(rollingP1ratio[each]):
        rollingP1ratio[each] = arduinoP1ratio[each]
P1fit = np.polyfit(rollingP1ratio, dylos1umData, deg=4)
P1corr = np.poly1d(P1fit)
minRatio = min(rollingP1ratio)
maxRatio = max(rollingP1ratio)
fitLineX = np.linspace(minRatio, maxRatio, 1000)
fitLineY = P1corr(fitLineX)
print '4th order:', P1fit

popt, pcov = cf(func, rollingP1ratio, dylos1umData)
print '3rd order 0-intercept:', popt
fitLineY2 = func(fitLineX, popt[0], popt[1], popt[2])

popt3, pcov3 = cf(expfunc, rollingP1ratio, dylos1umData)
print 'exponential:',popt3
fitLineY3 = expfunc(fitLineX, popt3[0], popt3[1])

linearpopt, linearpcov = cf(linearfunc, rollingP1ratio, dylos1umData)
print 'linear:',linearpopt
fitLineYlinear = linearfunc(fitLineX, linearpopt[0])

allData = {}
allData['time'] = interpTimes
allData['dylos data'] = dylos1umData
allData['arduino data'] = arduino1umData
allData = pd.DataFrame(allData)
allData = allData.set_index('time')

corrData = {}
corrData['dylos 1um'] = dylos1umData
corrData['P1 ratio'] = rollingP1ratio

corrData = pd.DataFrame(corrData)
ax = corrData.plot(kind = 'scatter', x='P1 ratio', y='dylos 1um', c='white')
ax.plot(fitLineX, fitLineY, linewidth=3, label='4th degree')
ax.plot(fitLineX, fitLineY2, linewidth=3, label='3rd order, intercept=0')
ax.plot(fitLineX, fitLineY3, linewidth=3, label='exponential')
ax.plot(fitLineX, fitLineYlinear, linewidth=3, label='linear')
ax.legend(loc='best')
plt.show()

ax = allData.plot()
ax.plot(allData.index,pd.rolling_mean(allData['arduino data'],20), label='mva', color='orange', linewidth=3)
plt.show()

plt.scatter(allData.index, arduinoP1ratio, label='raw data')
plt.plot(allData.index, rollingP1ratio, label='mva', c='orange', linewidth=3)
plt.xlim(min(allData.index),max(allData.index))
plt.legend(loc='best')
plt.show()'''