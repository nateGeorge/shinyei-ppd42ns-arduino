import pylab as plt
import pickle, csv, matplotlib
import numpy as np
import matplotlib.dates as mdates
import pandas as pd



with open('dustdata','rb') as f:
	data=pickle.load(f)

counter=0
dates=[]
dustdata=[]
for each in data:
	if counter%2==0:
		dates.append(each)
	else:
		dustdata.append(str(each).split(',')[2])
	counter+=1
	

	
fig = plt.figure()
ax = fig.add_subplot(111)
dates = matplotlib.dates.date2num(dates)
# Configure x-ticks
#ax.set_xticks(dates) # Tickmark + label at every plotted point
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M'))

dustdata=np.array(dustdata)
ax.plot_date(dates, dustdata)
ax.plot_date(dates, pd.rolling_mean(dustdata,30),'-')

plt.show()