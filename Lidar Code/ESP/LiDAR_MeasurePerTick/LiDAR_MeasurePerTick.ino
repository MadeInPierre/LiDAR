#include <Wire.h>
#include <LIDARLite.h>

#define TICKS_PER_LAP 176
#define ANGLE_PER_TICK 360 / TICKS_PER_LAP

#define PIN_LED LED_BUILTIN
#define PIN_MOTOR_PWM 0
#define PIN_ENCODER_INPUT D3

volatile int LapCount;
volatile int lap_tick_count;
volatile bool bool_got_tick = false;
volatile bool bool_new_lap = false;

LIDARLite LidarLite;
const int LidarMode = 1; //See example DistanceToi2c from LidarLite library to test Lidar modes.

void new_lap(bool reset) {
  // Resets the counter for a new lap. Sends a new lap header (flag for the loop).
  // arg reset : sets the lap counter to zero.
  LapCount = reset ? 0 : LapCount + 1;
  lap_tick_count = 0;
  bool_new_lap = true;
}

void encoder_tick() {
	lap_tick_count++;

  bool_got_tick = true;

	if(lap_tick_count > TICKS_PER_LAP) {
		new_lap(false);
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
	new_lap(true);
}

void loop() {
  
  if(bool_new_lap) {
    Serial.flush();
    Serial.print("L");
    Serial.print(LapCount);
    if(LapCount == 0) {
      Serial.print("-");

      Serial.print(TICKS_PER_LAP);
    }
    Serial.println(":");

    bool_new_lap = false;
  }
  if(bool_got_tick) {
    Serial.write(LidarLite.distance(bool_new_lap));
    bool_got_tick = false;
    bool_new_lap = false;
  }


  if(Serial.availableForWrite() < 5) Serial.println("TX BUFFER OVERFLOW"); //DEBUG
}
