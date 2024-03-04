#include <Servo.h>
#include <Arduino.h>

Servo LEDr;
Servo LEDg;
Servo LEDb;

void setup() {
  Serial.begin(9600);
  LEDr.attach(2);
  LEDg.attach(3);
  LEDb.attach(4);
}
void loop() {
  if (Serial.available() > 0) {
    char command = Serial.read();
    //Serial.print("Received command: ");
    //Serial.println(command);

    if (command == 'R') {
      LEDr.write(255);
      LEDg.write(0);
      LEDb.write(0);
    } else if (command == 'G') {
      LEDr.write(0);
      LEDg.write(255);
      LEDb.write(0);
    } else if (command == 'B') {
      LEDr.write(0);
      LEDg.write(0);
      LEDb.write(255);
    }
  }
}
