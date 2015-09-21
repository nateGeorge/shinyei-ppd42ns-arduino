import serial, datetime, pickle
import numpy as np

ser=serial.Serial()
ser.baudrate=9600
ser.port=2
ser.open()
firsttime=True
counter=0
while True:
	tempdata=ser.readline().rstrip('\r\n')
	timenow=datetime.datetime.now()
	if firsttime:
		dustdata=np.array([timenow,tempdata])
		firsttime=False
	else:
		try:
			float(tempdata)
			dustdata=np.append(dustdata,[timenow,tempdata])
		except ValueError:
			print 'air quality: ', tempdata
	print dustdata
	counter+=1
	if counter==1:
		try:
			pickle.dump(dustdata,open('dustdata','wb'))
		except Exception as msg:
			print 'whoops'
			print msg
		#close('dustdata')
		counter=0
	