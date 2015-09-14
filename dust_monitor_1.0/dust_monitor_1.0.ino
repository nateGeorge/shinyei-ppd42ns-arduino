/* Grove - Dust Sensor Demo v1.0
 Interface to Shinyei Model PPD42NS Particle Sensor
 Program by Christopher Nafis 
 Written April 2012
 
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
 */

int redpin = 9; // select the pin for the red LED
int greenpin = 10 ;// select the pin for the green LED
int bluepin = 11; // select the pin for the blue LED


int pin = 8;
unsigned long duration;
unsigned long starttime;
unsigned long sampletime_ms = 30000;//sampe 30s ;
unsigned long lowpulseoccupancy = 0;
float ratio = 0;
float concentration = 0;
float smallConcentration = 0;

void setup() {
  pinMode(redpin, OUTPUT);
  pinMode(bluepin, OUTPUT);
  pinMode(greenpin, OUTPUT);
  Serial.begin(9600);
  pinMode(8,INPUT);
  starttime = millis();//get the current time;
}

void loop() {
  duration = pulseIn(pin, LOW);
  lowpulseoccupancy = lowpulseoccupancy+duration;

  if ((millis()-starttime) > sampletime_ms)//if the sampel time == 30s
  {
    ratio = lowpulseoccupancy/(sampletime_ms*10.0);  // Integer percentage 0=>100
    concentration = 1.1*pow(ratio,3)-3.8*pow(ratio,2)+520*ratio+0.62; // using spec sheet curve
    smallConcentration = concentration*4;
    Serial.print(lowpulseoccupancy);
    Serial.print(",");
    Serial.print(ratio);
    Serial.print(",");
    Serial.print(concentration);
    Serial.print(",");
    Serial.println(smallConcentration);//roughly multiply by 4 to get particles > 0.5 micron
    lowpulseoccupancy = 0;
    starttime = millis();

    if (smallConcentration > 3000.0) { // air quality is VERY POOR
      analogWrite(redpin, 255);
      analogWrite(greenpin, 0);
      analogWrite(bluepin, 0);
      Serial.println("very poor");
    }
    else if (smallConcentration > 1050.0) { // air quality is POOR
      analogWrite(redpin, 255);
      analogWrite(greenpin, 255);
      analogWrite(bluepin, 0);
      Serial.println("poor");
    }
    else if (smallConcentration > 300.0) { // air quality is FAIR
      analogWrite(redpin, 255);
      analogWrite(greenpin, 0);
      analogWrite(bluepin, 255);
      Serial.println("fair");
    }
    else if (smallConcentration > 150.0) { // air quality is GOOD
      analogWrite(redpin, 0);
      analogWrite(greenpin, 255);
      analogWrite(bluepin, 255);
      Serial.println("good");
    }
    else if (smallConcentration > 75.0) { // air quality is VERY GOOD
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
  
   
  
}
