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

bool reset = false; //if the host asks for a reset.

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
void check_serial_read() {
  if(Serial.available()) {
    char c = Serial.read();
    switch(c) {
      case 'R': //RESET
        new_lap(true);
        reset = true;
        break;
      case 'P': //GET PPL. The host asks for the angular resolution of the lidar. Reply with the result.
        Serial.print("P");
        Serial.println(TICKS_PER_LAP + 1);
        break;
    }
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
  if(reset) { Serial.println("RESET"); reset = false; } //Send 'RESET' and end line to start fresh (the host will receive 'xxxxxxxxxxRESET\n').
  
  if(bool_new_lap) {
    Serial.println();
    Serial.print("L");
    Serial.print(LapCount);
    Serial.print(":");

    bool_new_lap = false;
  }
  if(bool_got_tick) {
    Serial.print(LidarLite.distance(bool_new_lap));
    Serial.print(',');
    bool_got_tick = false;
    bool_new_lap = false;
  }

  check_serial_read();

  if(Serial.availableForWrite() < 5) Serial.println("TX BUFFER OVERFLOW"); //DEBUG
}
