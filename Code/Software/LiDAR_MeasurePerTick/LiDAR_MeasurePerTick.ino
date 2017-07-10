 #include <Wire.h>
#include <LIDARLite.h>

/*
Send number 0-5 to control motor speed (0 = stop, 5 = full)
*/

/*Different scanning modes are possible :
    - 0 : SLOW.  2 degrees angular resolution, max 1.2Hz, +- 3cm
    - 1 : FAST.  1 degree  angular resolution, max 1.5Hz, +- 6cm
    - 2 : ULTRA. 2 degrees angular resolution, max 3.0Hz, +- 6cm 
*/
#define MODE 1

int TICKS_PER_LAP = 0; //176 rising ticks per lap ==> 176 ticks if slow mode (detects only rising ticks), 354 otherwise (rising + falling)

#define PIN_LED LED_BUILTIN
#define PIN_MOTOR_PWM D7
#define PIN_ENCODER_INPUT D6

volatile int LapCount;
volatile int lap_tick_count;
volatile bool bool_got_tick = false;
volatile bool bool_new_lap = false;

bool reset = false; //if the host asks for a reset.
volatile bool recalibrate_lidar = true;

LIDARLite LidarLite;
const int LidarMode = MODE; //See example DistanceToi2c from LidarLite library to test Lidar modes. 0 for SLOW (more precise), 1 for FAST (less precise, faster) 

void motor_set_speed(int speed) {
  // Give a value from 0 (full stop) to 2013 (full speed)
  // Using transistor "BC558C W0 E"
  analogWrite(PIN_MOTOR_PWM, 1023 - speed);
}

void new_lap(bool reset) {
  // Resets the counter for a new lap. Sends a new lap header (flag for the loop).
  // arg reset : sets the lap counter to zero.
  LapCount = reset ? 0 : LapCount + 1;
  lap_tick_count = 0;
  bool_new_lap = true;
  recalibrate_lidar = true;
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
    char c = (char)Serial.read();
    switch(c) {
      case 'R': //RESET
        new_lap(true);
        reset = true;
        break;
      case 'P': //GET PPL. The host asks for the angular resolution of the lidar. Reply with the result.
        Serial.print("P");
        Serial.println(TICKS_PER_LAP + 1);
        break;
      case '0':
        motor_set_speed(0);   // motor full stop
        break;
      case '1':
        motor_set_speed(250); // minimum driving speed
        break;
      case '2':
        motor_set_speed(400); // 
        break;
      case '3':
        motor_set_speed(600); // 
        break;
      case '4':
        motor_set_speed(800); // 
        break;
      case '5':
        motor_set_speed(1023);// full motor speed
        break;
    }
  }
}

void setup() {
	Serial.begin(500000);
	pinMode(PIN_LED, OUTPUT);
	pinMode(PIN_ENCODER_INPUT, INPUT);

  LidarLite.begin(LidarMode, true);
  LidarLite.configure(LidarMode);

  switch(MODE) {
    case 0:
      TICKS_PER_LAP = 176;
      attachInterrupt(PIN_ENCODER_INPUT, encoder_tick, RISING);
      break;
    case 1:
      TICKS_PER_LAP = 176 * 2;
      LidarLite.write(0x02, 0x0d);
      attachInterrupt(PIN_ENCODER_INPUT, encoder_tick, CHANGE);
      break;
    case 2: 
      TICKS_PER_LAP = 176;
      LidarLite.write(0x02, 0x0d);
      attachInterrupt(PIN_ENCODER_INPUT, encoder_tick, RISING);
      break;
  }

  delay(10);
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
    Serial.print(LidarLite.distance(recalibrate_lidar));
    Serial.print(',');
    bool_got_tick = false;
    recalibrate_lidar = false;
  }

  check_serial_read();

  if(Serial.availableForWrite() < 10) digitalWrite(PIN_LED, LOW); //DEBUG (high and low inverted with the esp)
  else digitalWrite(PIN_LED, HIGH);
}
