/* Grove - Dust Sensor Demo v1.0
 Interface to Shinyei Model PPD42NS Particle Sensor
 Original Program by Christopher Nafis 
 Written April 2012
 Updated by Nate G, 2014
 
 http://www.seeedstudio.com/depot/grove-dust-sensor-p-1050.html
 http://www.sca-shinyei.com/pdf/PPD42NS.pdf
 
 JST Pin 1 (far right looking at dust sensor)  => Arduino GND
 JST Pin 2 (P2) => Ard pin 9
 JST Pin 3 (Vcc)    => Arduino 5VDC
 JST Pin 4 (P1) => Ard Pin 8
 JST Pin 5 (P2 setpoint => 
 
Dylos Air Quality Chart - Small Count Reading (0.5 micron)+

3000 +     = VERY POOR
1050-3000  = POOR
300-1050   = FAIR
150-300    = GOOD
75-150     = VERY GOOD
0-75       = EXCELLENT

 */

int P1pin = 8;
int P2pin = 9;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 15000;
unsigned long lowpulseoccupancy = 0;
float P1ratio = 0;
float P2ratio = 0;
bool isP1pin = true;

void setup() {
  Serial.begin(9600);
  pinMode(P1pin,INPUT);
  pinMode(P2pin,INPUT);
  starttime = millis();
}

void loop() {
  if (isP1pin) {
    duration = pulseIn(P1pin, LOW);
    lowpulseoccupancy = lowpulseoccupancy+duration;

    if ((millis()-starttime) > sampletime_ms)
    {
      P1ratio = lowpulseoccupancy/(sampletime_ms*10.0);
      Serial.print("P1 LPO: ");
      Serial.println(lowpulseoccupancy);
      Serial.print("P1 ratio: ");
      Serial.println(P1ratio);
      lowpulseoccupancy = 0;
      starttime = millis();
      isP1pin = false;
      Serial.println("starting P2 measurement");
    }
  }
  else
  {
    duration = pulseIn(P2pin, LOW);
    lowpulseoccupancy = lowpulseoccupancy+duration;

    if ((millis()-starttime) > sampletime_ms)
    {
      P2ratio = lowpulseoccupancy/(sampletime_ms*10.0);
      Serial.print("P2 LPO: ");
      Serial.println(lowpulseoccupancy);
      Serial.print("P2 ratio: ");
      Serial.println(P2ratio);
      lowpulseoccupancy = 0;
      starttime = millis();
      isP1pin = true;
      Serial.println("startingP1 mesaurement");
    }
  }
}
