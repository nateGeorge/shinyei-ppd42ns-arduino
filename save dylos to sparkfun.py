import serial, requests, re
from datetime import datetime

ser = serial.Serial(4,timeout=10)

PrKEY = 'ZaVbANqmDlfpp99PVgoy'
PuKEY = 'xRNEMxZAKXTQQzzqrmYx'
postADDR1um = 'http://data.sparkfun.com/input/%s?private_key=%s&1um=' % (PuKEY, PrKEY)
dataToSend = False
stuckData = []

while True:
	line = ser.readline()
	if dataToSend:
		for eachPoint in stuckData:
			try:
				r = requests.post(postADDR1um + eachPoint[0] + '&5um=' + eachPoint[1] + '&datetime=' + eachPoint[2])
				print r.status_code, r.reason
				if r.status_code == 200:
					stuckData.remove(eachPoint)
					if len(stuckData) == 0:
						dataToSend = False
			except Exception as e: # need to implement better code for storing data and sending if can't connect
				print 'couldn\'t connect, skipping data for now'
				print e
	if line!='':
		match = re.search('(\d+),(\d+)',line)
		smallCount = match.group(1)
		largeCount = match.group(2)
		print '1um: ', smallCount, '5um: ', largeCount
		print type(smallCount)
		measureTime = datetime.now().isoformat()
		try:
			r = requests.post(postADDR1um + smallCount + '&5um=' + largeCount + '&datetime=' + measureTime)
			print r.status_code, r.reason
			if r.status_code != 200:
				print 'not successfully sent, will try again later'
				stuckData.append([smallCount,largeCount,measureTime])
				dataToSend = True
		except Exception as e: # need to implement better code for storing data and sending if can't connect
			print 'couldn\'t connect, skipping data for now'
			print e
			stuckData.append([smallCount,largeCount,measureTime])
			dataToSend = True