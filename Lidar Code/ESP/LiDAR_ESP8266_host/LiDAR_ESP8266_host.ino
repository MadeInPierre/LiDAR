#include <Wire.h>
#include <LIDARLite.h>

/*=======================================
=               VARIABLES               =
=======================================*/

/*----------  Global  ----------*/
#define BATCH_SIZE 15         // Number of measures before sending them
#define TICKS_PER_LAP 177     
#define FASTMODE_SPEED 255    // Motor speed when in slow scanning rate mode.
#define SLOWMODE_SPEED 80     // Motor speed when in fast scanning rate mode.

bool Running;                 // Stops and activates the sending and motor.
int LapCount;
unsigned long lap_start_time; // Let the buffers keep smaller values by substracting the lap_start_time from millis()

/*----------  Pin Definitions  ----------*/
#define PIN_LED LED_BUILTIN
#define PIN_MOTOR_PWM 0
#define PIN_ENCODER_INPUT A0

/*----------  Global buffers  ----------*/
byte output_buffer[64]; //TODO size ?

int ticks_times_buffer[TICKS_PER_LAP + 1];          // Encoder ticks buffer for the whole lap. Holds the last tick times to later on compute the measure angles
int measuredists_shortbuffer[BATCH_SIZE + 1];       // Distances for each batch. Their angles will be processed when ticks are available.
int measuretimes_shortbuffer[BATCH_SIZE + 1];       // Measure times for each batch.
int measures_last_tick_shortbuffer[BATCH_SIZE + 1]; // Keeps the index of the last tick.
int batch_index = 0;

/*----------  Lidar  ----------*/
LIDARLite LidarLite;
const int LidarMode = 1; //See example DistanceToi2c from LidarLite to test Lidar modes.

/*----------  Motor  ----------*/
int motor_speed;
volatile int lap_ticks_count;

/*----------  System  ----------*/
#define ANGLE_PER_TICK 360 / TICKS_PER_LAP

/*========  End of VARIABLES  =========*/




/*===============================
=            Helpers            =
===============================*/

int len(int inputarray[]) {
	return sizeof(inputarray) / sizeof(int);
}

/*=====  End of Helpers  ======*/




/*=======================================
=               Functions               =
=======================================*/

/*----------  Events  ----------*/
void encoder_tick_event() {
	ticks_times_buffer[lap_ticks_count] = millis() - lap_start_time;
	lap_ticks_count++;
}

/*----------  Communication  ----------*/
void serial_send() {
	int TX_free_bytes = Serial.availableForWrite();
	if(TX_free_bytes > 0) {
		digitalWrite(PIN_LED, LOW);
		
		Serial.write(1); // (TODO) Add output bytes to TX queue

	}
	else
		digitalWrite(PIN_LED, HIGH); //Set debug LED high if the output flow is too high for the ESP (can't keep up).
}

void serial_receive() {
	while(Serial.available() > 0) {
		char message = Serial.read();
		switch(message) {
			case 'H': // HALT. Turn off motor and sending
				Running = false;
				break;
			case 'R': // RUN. Start motors and scanning
				break;
			case 'F': // FAST MODE. max motor speed, less angular resolution
				break;
			case 'S': // SLOW MODE. slower motor speed, better angular precision
				break;
			case 'f': // FASTER motor speed (incremental by an arbitrary amount)
				break;
			case 's': // SLOWER motor speed(incremental by an arbitrary amount)
				break;
		}
	}
}

/*----------  Logic  ----------*/
void analyse() {
	for (int i = 0; i < len(measuredists_shortbuffer); ++i)
	{
		int t      = measuretimes_shortbuffer[i];
		int last_t = ticks_times_buffer[measures_last_tick_shortbuffer[i]];

		int d = measuredists_shortbuffer[i];
		int a = int((t - last_t) / (ticks_times_buffer[measures_last_tick_shortbuffer[i+ 1]] - last_t) 
					+ measures_last_tick_shortbuffer[i] * ANGLE_PER_TICK);
						/*
						 *                 t      - last_t
						 * Angle formula : ---------------  +  last_tick_index * ANGLE_PER_TICK
						 *                 next_t - last_t
						 */
 
		//TODO append d and a to the output buffer
	}
}

void new_lap() {
	lap_ticks_count = 0;
	LapCount++;

	//lap_ticks_count = 0, etc.
	//empty buffers
}
void update_motor() {
	analogWrite(PIN_MOTOR_SPEED, motor_speed);
}

/*========  End of Functions  =========*/




/*====================================
=            Setup & Loop            =
====================================*/

void setup() {
	Serial.begin(115200);
	pinMode(PIN_LED, OUTPUT);
	pinMode(PIN_MOTOR_SPEED, OUTPUT);
	pinMode(PIN_ENCODER_INPUT, INPUT);

	LidarLite.begin(LidarMode, true);
	LidarLite.configure(LidarMode);

	attachInterrupt(PIN_ENCODER_INPUT, encoder_tick_event, CHANGE);
}

void loop() {
	serial_receive();

	while(batch_index < BATCH_SIZE) {
		// Get a point and it's data (distance, time and last tick index to get a reference for the angle.)
		measuredists_shortbuffer      [batch_index] = LidarLite.distance(len(measuredists_shortbuffer) == 0 ? true : false);
		measuretimes_shortbuffer      [batch_index] = millis() - lap_start_time;
		measures_last_tick_shortbuffer[batch_index] = lap_ticks_count;

		if(len(measuredists_shortbuffer) == BATCH_SIZE) {
			analyse();
			batch_index = 0;
		}
		else 
			batch_index++;
	}

	if(lap_ticks_count > TICKS_PER_LAP) new_lap();


	serial_send();
	update_motor();

}

/*=====  End of Setup & Loop  ======*/