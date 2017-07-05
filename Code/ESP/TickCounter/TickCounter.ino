/*
Pierre L. 
Simply counts the number of encoder ticks and outputs the count.
*/

#include <Wire.h>
#include <LIDARLite.h>

#define ANGLE_PER_TICK 360 / TICKS_PER_LAP

#define PIN_LED LED_BUILTIN
#define PIN_ENCODER_INPUT D3

volatile int lap_tick_count;

void encoder_tick() {
  lap_tick_count++;
  Serial.println(lap_tick_count);
}


void setup() {
  Serial.begin(500000);
  pinMode(PIN_LED, OUTPUT);
  pinMode(PIN_ENCODER_INPUT, INPUT);

  attachInterrupt(PIN_ENCODER_INPUT, encoder_tick, CHANGE);
}

void loop() {
  
}
