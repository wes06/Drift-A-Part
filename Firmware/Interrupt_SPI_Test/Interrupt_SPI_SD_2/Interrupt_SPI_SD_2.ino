/*
  Interrupt_SPI.ino
  Brian R Taylor
  brian.taylor@bolderflight.com

  Copyright (c) 2017 Bolder Flight Systems

  Permission is hereby granted, free of charge, to any person obtaining a copy of this software
  and associated documentation files (the "Software"), to deal in the Software without restriction,
  including without limitation the rights to use, copy, modify, merge, publish, distribute,
  sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is
  furnished to do so, subject to the following conditions:

  The above copyright notice and this permission notice shall be included in all copies or
  substantial portions of the Software.

  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING
  BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
  NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM,
  DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
*/


#include <SD.h>
#include <math.h>
#include <SPI.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#include <CapacitiveSensor.h>

#define OLED_RESET 0
Adafruit_SSD1306 display(OLED_RESET);

#include "MPU9250.h"


CapacitiveSensor   cs_4_2 = CapacitiveSensor(4, 2);

#define GRAVITY_COMP_CNT 1000
double accGravComp[GRAVITY_COMP_CNT];
int GravCompToChange = 0;
double accGravCompTot = 0;

const int chipSelect = BUILTIN_SDCARD;

// an MPU9250 object with the MPU-9250 sensor on SPI bus 0 and chip select pin 10
//
//
//

MPU9250 IMU(SPI, 10);
int status;
bool calibrating = false;
float accelXOffset;
float accelYOffset;
float accelZOffset;
int calSampleCount = 0;
int calSampleToCount = 100;

int sampleCount = 0;
int sampleToCount = 1000;

float accX, accY, accZ;
int timestamp;

bool dataReady = false;

String dataString = "";

void setup() {


  // ### display stuff
  // by default, we'll generate the high voltage from the 3.3v line internally! (neat!)
  display.begin(SSD1306_SWITCHCAPVCC, 0x3C);  // initialize with the I2C addr 0x3D (for the 128x64)

  // text display tests
  display.clearDisplay();
  display.setTextSize(2);
  display.setTextColor(WHITE);
  display.setCursor(0, 0);
  display.println("Setting \nIMU..");
  display.display();

  // serial to display data
  Serial.begin(1000000);
  while (!Serial) {
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("Waiting \nfor Serial\nport");
    display.display();
  }

  // see if the card is present and can be initialized:
  if (!SD.begin(chipSelect)) {
    Serial.println("SD card failed or not present");

    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("SD \nFailed..");
    display.display();
    return;
  }
  Serial.println("SD card initialized.");

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("SD \nInitialized..");
  display.display();

  // start communication with IMU
  status = IMU.begin();
  if (status < 0) {
    Serial.println("IMU initialization unsuccessful");
    Serial.println("Check IMU wiring or try cycling power");
    Serial.print("Status: ");
    Serial.println(status);
    display.clearDisplay();
    display.setCursor(0, 0);
    display.println("IMU \nInit \nfailed");
    display.display();
    while (1) {}
  }
  // setting DLPF bandwidth to 184 Hz
  IMU.setDlpfBandwidth(MPU9250::DLPF_BANDWIDTH_184HZ);
  IMU.setAccelRange(MPU9250::ACCEL_RANGE_2G);


  // setting SRD to 19 for a 50 Hz update rate
  // SAMPLE_RATE= Internal_Sample_Rate / (1 + SMPLRT_DIV)
  IMU.setSrd(49);

  // enabling the data ready interrupt
  IMU.enableDataReadyInterrupt();
  calibrating = true;
  // attaching the interrupt to microcontroller pin 1
  pinMode(9, INPUT);
  attachInterrupt(9, getIMU, RISING);
  Serial.println("IMU Setup done");
  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("IMU \nInitialized..");
  display.display();
  delay(50);

  display.clearDisplay();
  display.setCursor(0, 0);
  display.println("Calibrating \naccelerometer");
  display.display();
  Serial.println("Calibrating accel...");

}

long startWrite = 0;

long lasti2cPrint = 0;

void loop() {

  long total1 =  cs_4_2.capacitiveSensor(30);

  if (millis() - lasti2cPrint > 50) {
    if (calibrating) {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("Accel Cal: \n");
      display.print(float(calSampleCount) / float(calSampleToCount) * 100, 1);
      display.print(" %");
      display.display();
    }
    else if (!(sampleCount <= sampleToCount)) {
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("DataCount: \n");
      display.print(float(sampleCount) / float(sampleToCount) * 100, 1);
      display.print(" %");
      display.display();
    }

    lasti2cPrint = millis();
  }


  accGravComp[GravCompToChange] = IMU.getAccelZ_mss();
  GravCompToChange++;
  if (GravCompToChange > GRAVITY_COMP_CNT) {
    GravCompToChange = 0;
  }
  accGravCompTot = 0;
  for (int i = 0; i < GRAVITY_COMP_CNT; i++) {
    accGravCompTot += accGravComp[i];
  }
  accelZOffset = accGravCompTot / double(GRAVITY_COMP_CNT);
  Serial.print("G-Comp: ");
  Serial.print(accelZOffset, 8);
  Serial.print("\t");
  if (dataReady) {
    if (sampleCount < sampleToCount) {
      // open the file. note that only one file can be open at a time,
      // so you have to close this one before opening another.
      startWrite = micros();
      File dataFile = SD.open("datalog4.csv", FILE_WRITE);
      // if the file is available, write to it:
      if (dataFile) {
        sampleCount++;
        dataFile.print(accX, 6);
        dataFile.write(",");
        dataFile.print(accY, 6);
        dataFile.write(",");
        dataFile.print(accZ, 6);
        dataFile.write(",");
        dataFile.println(timestamp);
        dataFile.close();
        dataReady = false;
        // print to the serial port too:
        Serial.print("SD: \t");
        Serial.print(accX, 6);
        Serial.write(",");
        Serial.print(accY, 6);
        Serial.write(",");
        Serial.print(accZ, 6);
        Serial.write(",");
        Serial.print(timestamp);
        Serial.print("\twritetime:\t");
        Serial.print(micros() - startWrite);
        Serial.println();
      }    // if the file isn't open, pop up an error:
      else {
        Serial.println("error opening datalog.csv");
      }
    }
    else {
      //sampling done
      Serial.println("DONE!");
      display.clearDisplay();
      display.setCursor(0, 0);
      display.print("DONE!");
      display.print("\n");
      display.print(sampleToCount);
      display.setTextSize(1);
      display.print("\n\nSamples taken");
      display.display();
      while (1) {}
    }


  }

}

long lastMicros = 0;

void getIMU() {
  if (dataReady && !calibrating && !(sampleCount <= sampleToCount)) {
    //  Serial.println("SD error, maybe too slow?");
    Serial.println("SD TOO SLOOOOOW");
    //  detachInterrupt(9);
    //  while (1) {}
  }
  // read the sensor
  IMU.readSensor();
  // display the data
  if (!calibrating && !dataReady) {
    accX = IMU.getAccelX_mss() - accelXOffset;
    accY = IMU.getAccelY_mss() - accelYOffset;
    accZ = IMU.getAccelZ_mss() - accelZOffset;
    timestamp = int(ceil(float(micros() - lastMicros) / 1000));
    //Serial.print(micros() - lastMicros);
    //Serial.print("\t");
    //Serial.print(IMU.getAccelX_mss() - accelXOffset, 20);
    //Serial.print("\t");
    //Serial.print(IMU.getAccelY_mss() - accelYOffset, 20);
    //Serial.print("\t");
    //Serial.print(IMU.getAccelZ_mss() - accelZOffset, 20);
    //Serial.print("\t");
    //Serial.print("\n");

    dataReady = true;
  }
  else if (calibrating) {
    accelXOffset += IMU.getAccelX_mss();
    accelYOffset += IMU.getAccelY_mss();
    accelZOffset += IMU.getAccelZ_mss();
    calSampleCount++;
    if (calSampleCount >= calSampleToCount) {
      calibrating = false;
      accelXOffset = accelXOffset / float(calSampleToCount);
      accelYOffset = accelYOffset / float(calSampleToCount);
      accelZOffset = accelZOffset / float(calSampleToCount);
    }
    for (int i = 0; i < GRAVITY_COMP_CNT; i++) {
      accGravComp[i] = accelZOffset;
    }
    Serial.print("Calibrating accel: ");
    Serial.print(calSampleCount);
    Serial.print(" of ");
    Serial.print(calSampleToCount);
    Serial.print(" done. \n");
  }
  lastMicros = micros();

}
