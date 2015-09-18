import pylab as plt
import pickle, csv, matplotlib, time
import numpy as np
import matplotlib.dates as mdates
import pandas as pd
import matplotlib.animation as animation


def get_data(file):
	with open(file,'rb') as f:
		data=pickle.load(f)
	f.close()

	counter=0
	dates=[]
	dustdata=[]
	for each in data:
		if counter%2==0:
			dates.append(each)
		else:
			dustdata.append(str(each).split(',')[2])
		counter+=1
	return dates, dustdata

def animate(i):
	dates,dustdata=get_data('dustdata')
	
	dates = matplotlib.dates.date2num(dates)

	
	dustdata=np.array(dustdata)
	ax.plot_date(dates, dustdata,c='grey')
	ax.plot_date(dates, pd.rolling_mean(dustdata,20),'w-',linewidth=4)
	return





		

fig = plt.figure(facecolor='k')
ax = fig.add_subplot(111,axisbg='k')
ax.xaxis.set_major_formatter(mdates.DateFormatter('%I:%M'))
ax.tick_params(color='w', labelcolor='w')
for spine in ax.spines.values():
	spine.set_edgecolor('w')


ani = animation.FuncAnimation(fig, animate, interval=10000)
plt.show()