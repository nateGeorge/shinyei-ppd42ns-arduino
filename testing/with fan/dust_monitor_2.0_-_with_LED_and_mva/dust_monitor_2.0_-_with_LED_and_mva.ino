/* Grove - Dust Sensor v2.0
 added LED that responds to moving average
 Interface to Shinyei Model PPD42NS Particle Sensor
 
 http://www.seeedstudio.com/depot/grove-dust-sensor-p-1050.html
 http://www.sca-shinyei.com/pdf/PPD42NS.pdf
 
 JST Pin 1 (Black Wire)  => Arduino GND
 JST Pin 3 (Red wire)    => Arduino 5VDC
 JST Pin 4 (Yellow wire) => Arduino Digital Pin 8
 
Dylos Air Quality Chart - Small Count Reading (0.5 micron)+

3000 +     = VERY POOR
1050-3000  = POOR
300-1050   = FAIR
150-300    = GOOD
75-150     = VERY GOOD
0-75       = EXCELLENT

Converted to 1 micron + (or whatever shinyei reads) (/4)
750+ = VERY POOR
262.5 - 750 = POOR
75 - 262.5 = FAIR
37.5 - 75 = GOOD
18.75 - 37.5 = VERY GOOD
0 - 18.75 = TOTALLY EXCELLENT, DUDE!
 */

int redpin = 4; // select the pin for the red LED
int greenpin = 5 ;// select the pin for the green LED
int bluepin = 6; // select the pin for the blue LED

const int numReadings = 10;

int readings[numReadings];      // the readings from the analog input
int index = 0;                  // the index of the current reading
int total = 0;                  // the running total
int average = 0;                // the average
bool ledON = 0;                // turn LED on or off


int pin = 8; // yellow cable (P1 pin, second from left on board)
unsigned long duration;
unsigned long startTime_ms;
unsigned long sampleTime_ms = 1000;// sample every 1s
unsigned long lowPulseOccupancy = 0;
float ledSignal = 0;
float ratio = 0;
float concentration = 0;
float smallConcentration = 0;
bool firstTime = true;
int firstTimeCounter = 1;

void setup() {
  pinMode(redpin, OUTPUT);
  pinMode(bluepin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  Serial.begin(9600);
  pinMode(8,INPUT);
  startTime_ms = millis();//get the current time;
  
  // initialize all the readings to 0: 
  for (int thisReading = 0; thisReading < numReadings; thisReading++)
    readings[thisReading] = 0;
}

void loop() {
  duration = pulseIn(pin, LOW);
  lowPulseOccupancy = lowPulseOccupancy+duration;

  if ((millis()-startTime_ms) > sampleTime_ms)//if the sampel time == 30s
  {
    ratio = lowPulseOccupancy/(sampleTime_ms*10.0);  // Integer percentage 0=>100
    concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
    Serial.print("concentration: ");
    Serial.println(concentration);
    smallConcentration = concentration*4;
    Serial.println(smallConcentration);//roughly multiply by 4 to get particles > 0.5 micron
    lowPulseOccupancy = 0;
    startTime_ms = millis();
    
    
    // subtract the last reading:
    total = total - readings[index];         
    // read from the sensor:  
    readings[index] = smallConcentration; 
    // add the reading to the total:
    total = total + readings[index];       
    // advance to the next position in the array:  
    index = index + 1;                    
    
    // if we're at the end of the array...
    if (index >= numReadings)              
    // ...wrap around to the beginning: 
    index = 0;                           

    // calculate the average:
    average = total / numReadings;
    Serial.print("moving average: ");
    Serial.println(average);

    // wait until moving average has been completed to use it as a judgement for LED color, otherwise use current value
    if (!firstTime) {
      ledSignal = average;
    }
    else {
      ledSignal = smallConcentration;
      firstTimeCounter += 1;
      if (firstTimeCounter > numReadings) {
        firstTime = false;
      }
    } 
    if (ledON) {
      if (ledSignal > 3000.0) { // air quality is VERY POOR
        analogWrite(redpin, 255);
        analogWrite(greenpin, 0);
        analogWrite(bluepin, 0);
        Serial.println("very poor");
      }
      else if (ledSignal > 1050.0) { // air quality is POOR
        analogWrite(redpin, 255);
        analogWrite(greenpin, 255);
        analogWrite(bluepin, 0);
        Serial.println("poor");
      }
      else if (ledSignal > 300.0) { // air quality is FAIR
        analogWrite(redpin, 255);
        analogWrite(greenpin, 0);
        analogWrite(bluepin, 255);
        Serial.println("fair");
      }
      else if (ledSignal > 150.0) { // air quality is GOOD
        analogWrite(redpin, 0);
        analogWrite(greenpin, 255);
        analogWrite(bluepin, 255);
        Serial.println("good");
      }
      else if (ledSignal > 75.0) { // air quality is VERY GOOD
        analogWrite(redpin, 0);
        analogWrite(greenpin, 0);
        analogWrite(bluepin, 255);
        Serial.println("very good");
      }
      else { // air quality is EXCELLENT (<75)
        analogWrite(redpin, 0);
        analogWrite(greenpin, 255);
        analogWrite(bluepin, 0);
        Serial.println("excellent");
      }
    }
  else {
      analogWrite(redpin, 0);
      analogWrite(greenpin, 0);
      analogWrite(bluepin, 0);
    }
  }
  
}
