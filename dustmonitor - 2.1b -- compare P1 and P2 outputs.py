import serial, csv

P2dutyCycle = 'retry with regulated power testing 70 longer term'

saveFile = P2dutyCycle + ' duty cycle data.csv'
with open(saveFile,'wb') as f:
	fileWriter = csv.writer(f,delimiter = ',')
	fileWriter.writerow(['P1','P2 - ' + P2dutyCycle])


ser=serial.Serial()
ser.baudrate=9600
ser.port=2
ser.open()

with open(saveFile,'a') as f:
	fileWriter = csv.writer(f,delimiter = ',')
	while True:
		tempdata=ser.readline().rstrip('\r\n')
		print tempdata
		if len(tempdata)>0:
			if tempdata[:2] == 'P1':
				P1concentration = tempdata[3:]
			elif tempdata[:2] == 'P2':
				fileWriter.writerow([P1concentration,tempdata[3:]])