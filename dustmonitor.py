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
		dustdata=np.append(dustdata,[timenow,tempdata])
	print dustdata
	counter+=1
	if counter==1:
		pickle.dump(dustdata,open('dustdata','wb'))
		#close('dustdata')
		counter=0
	