#include <Wire.h>
#include <LIDARLite.h>

#define TICKS_PER_LAP 177
#define ANGLE_PER_TICK 360 / TICKS_PER_LAP

#define PIN_LED LED_BUILTIN
#define PIN_MOTOR_PWM 0
#define PIN_ENCODER_INPUT D3

volatile int LapCount;
volatile int lap_tick_count;
volatile bool got_tick = false;

LIDARLite LidarLite;
const int LidarMode = 1; //See example DistanceToi2c from LidarLite library to test Lidar modes.

void reset_lap() {
  LapCount = 0;
  lap_tick_count = 0;
  Serial.print("L");
  Serial.println(LapCount);
}

void new_lap() {
	LapCount++;
	lap_tick_count = 0;
  Serial.print("L");
  Serial.println(LapCount);
}

void encoder_tick() {
	lap_tick_count++;

  got_tick = true;

	if(lap_tick_count > TICKS_PER_LAP) {
		new_lap();
	}
}

void setup() {
	Serial.begin(500000);
	pinMode(PIN_LED, OUTPUT);
	pinMode(PIN_MOTOR_PWM, OUTPUT);
	pinMode(PIN_ENCODER_INPUT, INPUT);

	LidarLite.begin(LidarMode, true);
	LidarLite.configure(LidarMode);

	attachInterrupt(PIN_ENCODER_INPUT, encoder_tick, RISING);
	reset_lap();
}

void loop() {
  if(got_tick) {
    Serial.println(LidarLite.distance(false), DEC);
    got_tick = false;
  }
}
