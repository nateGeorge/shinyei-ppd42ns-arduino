import serial, requests, re, csv, os
from datetime import datetime

ser = serial.Serial(12,timeout=3)

datafile = 'correlation data/' + datetime.strftime(datetime.now(),'%Y-%m-%d %H-%M-%S') + ' arduino data.csv'
P1ratio = None
if not os.path.isfile(datafile):
    with open(datafile,'wb') as csvfile:
        arduinocsv = csv.writer(csvfile, delimiter = ',')
        arduinocsv.writerow(['P2 ratio', 'P1 ratio', 'time (iso)'])

while True:
    line = ser.readline()
    if line!='':
        measureTime = datetime.now().isoformat()
        if re.search('.*P1 ratio: (\d+\.\d+).*', line):
            P1ratio = re.search('.*P1 ratio: (\d+\.\d+).*', line).group(1)
        if re.search('.*P2 ratio: (\d+\.\d+).*', line) and P1ratio != None:
            P2ratio = re.search('.*P2 ratio: (\d+\.\d+).*', line).group(1)
            print 'P1, P2 ratios:', P1ratio, P2ratio
            with open(datafile,'ab+') as csvfile:
                arduinocsv = csv.writer(csvfile, delimiter = ',')
                arduinocsv.writerow([P2ratio, P1ratio, measureTime])