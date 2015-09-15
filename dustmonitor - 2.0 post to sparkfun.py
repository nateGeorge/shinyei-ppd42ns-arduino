'''
This will locally save and post to sparkfun the data from a serially-connected arduino with a PPD42NS or DSM501 module.  The locally saved files are enumerated, with the base
file name as the variable 'saveFile'.  Make sure to update your public/private keys and datastream fields accordingly.
'''

import serial, datetime, pickle
import numpy as np
import requests
import glob


PrKEY = # private key here as string
PuKEY = # public key here as string
postADDR = 'http://data.sparkfun.com/input/%s?private_key=%s&1um_particle_concentration=' % (PuKEY, PrKEY) # modify the fields for your datastream

saveFile = 'dustdata - 93 ridgeview ' # change the base filename here


fileCount = 0
for file in glob.iglob(saveFile + '*'):
	print "already existing files:"
	print file
	fileCount += 1
	
saveFile = saveFile + str(fileCount) # saves your files as the basename + the next available number

print ""
print "saving file as:"
print saveFile

ser=serial.Serial()
ser.baudrate=9600
ser.port=2
ser.open()
firsttime=True
counter=0
while True:
    # reads the data from the serial stream, tries to post to sparkfun, and saves in a local pickle file
	tempdata=ser.readline().rstrip('\r\n')
	
	if len(tempdata)>0:
		try:
			r = requests.post(postADDR + tempdata)
			print r.status_code, r.reason
			print 'air quality: ', tempdata
		except Exception as e: # need to implement better code for storing data and sending if can't connect
			print 'coulnd\'t connect, skipping data'
			print e
			continue
		timenow=datetime.datetime.now()
		if firsttime:
			dustdata=np.array([timenow,float(tempdata)])
			firsttime=False
		else:
			try:
				float(tempdata)
				dustdata=np.append(dustdata,[timenow,tempdata])
			except ValueError:
				print 'air quality: ', tempdata
		#print dustdata
		counter+=1
		if counter==1:
			try:
				pickle.dump(dustdata,open(saveFile,'wb'))
			except Exception as msg:
				print 'whoops'
				print msg
			
			#close('dustdata')
			counter=0
		